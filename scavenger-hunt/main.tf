variable "hosts" {
  description = "The hosts to create."
  type        = map
  default     = {
    enterprise = {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      os = "ubuntu"
      zone = "us-central1-a"
    },
    reliant = {
      image = "rocky-linux-cloud/rocky-linux-9"
      os = "centos"
      zone = "us-central1-b"
    },
    excelsior = {
      image = "debian-cloud/debian-10"
      os = "debian"
      zone = "us-central1-c"
    },
    voyager = {
      image = "suse-cloud/sles-15"
      os = "suse"
      zone = "us-central1-f"
    },
  }
}

variable "project" { 
  default = "cis-90" 
}

variable "credentials_file" { 
    default = "secrets/cis-90-6531e28d6815.json" 
}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project = var.project
  region  = var.region
  zone    = var.zone 
}

resource "google_dns_managed_zone" "scavenger-zone" {
  name        = "scavenger-zone"
  dns_name    = "scavenger.cis-90.net."
  description = "DNS zone for the scavenger hunt"
  labels = {
    app = "scavenger-hunt"
  }
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_instance" "vm_instance" {
  for_each     = var.hosts
  name         = each.key
  machine_type = "e2-medium"
  zone         = each.value.zone

  allow_stopping_for_update = true

  metadata = {
    enable-oslogin = "TRUE"
  }

  boot_disk {
    initialize_params {
      image = each.value.image
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }

  labels = {
    os: each.value.os 
  }
}

resource "google_compute_firewall" "ssh-rule" {
  name = "demo-ssh"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  source_ranges = ["0.0.0.0/0"]
}

resource "google_dns_record_set" "scavenger-hosts" {
  for_each = var.hosts 

  managed_zone = google_dns_managed_zone.scavenger-zone.name

  name    = "${each.key}.${google_dns_managed_zone.scavenger-zone.dns_name}"
  type    = "A"
  rrdatas = [google_compute_instance.vm_instance[each.key].network_interface.0.access_config.0.nat_ip]
  ttl     = 300
}

#output "public_dns_names" {
#  description = "Public DNS names of the hosts."
#  value       = { for p in sort(keys(var.hosts)) : p => google_comput_instance.vm_instance.name }
#}

#output "external-ip" {
#  value = google_compute_instance.vm_instance.network_interface.each.key.access_config.0.nat_ip
#}
