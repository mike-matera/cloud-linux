# (XXX: OLD) Lab: Using a Vagrant Configuration Script 

In this lab you'll create a new Vagrant box based on the standard box for the class. You will edit the `Vagrantfile` to include setup instructions. The setup will automatically install the latest version of Docker. 

## Step 0: Create a New Box Directory 

How you do this step will depend on what OS is on your computer. Start by creating a new directory for your customized Vagrant box:

``` 
$ mkdir docker-box
$ cd docker-box
```

Now download the `Vagrantfile` linked below into the new directory:

```eval_rst
- :download:`Vagrantfile <../../boxes/xenial64-disks/Vagrantfile>` - The "standard" VM for this class.
```

## Step 1: Create a Customization Script 

Vagrant can use complex configuration management software such as [Puppet](https://puppet.com/), [Chef](https://www.chef.io/) and [Ansible](https://www.ansible.com/) to manage boxes. It can also run a simple shell script when the box starts. Copy and paste this code into a script called `setup-docker.sh` in the same directory as your `Vagrantfile`. 

```bash
#! /bin/bash 

sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker vagrant

# Install docker-compose 
sudo curl -s -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
``` 

The steps in this file are the steps from last week's class. 

## Step 2: Update Vagrantfile 

Add the following configuration parameter to the Vagrantfile:

```ruby
  config.vm.provision "shell", path: "setup-docker.sh"
```

The configuration parameter must be inside the `config` clause. Here's the parameter in context: 

```ruby
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.provision "shell", path: "setup-docker.sh"

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"
```

## Step 3: Check the Docker Install 

Bring up your new box with `vagrant up` then login to your Docker box with `vagrant ssh`. Verify that Docker is installed:

```bash
docker run docker/whalesay cowsay "Linux FTW"
```

## Turn In 

Turn in a screenshot of the output of whalesay. 

