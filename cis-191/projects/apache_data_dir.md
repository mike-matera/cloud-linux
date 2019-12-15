# Project: A Data Directory for Apache

Apache is a popular web server. Web servers serve web pages and are the cornerstone of the world wide web. In this project you will install and Apache and move its data to an advanced filesystem.

## Configure Vagrant 

The Vagrantfile I gave you needs to be updated in order to allow access to Apache. You can download the latest copy using the URL below: 

> [Vagrantfile-Xenial64-Disks](http://www.lifealgorithmic.com/_static/boxes/Vagrantfile-Xenial64-Disks)

You can also edit your old Vagrant file to uncomment the following line: 

```
config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
```

If you succeed the `vagrant up` command will have this output: 

```
==> default: Forwarding ports...
    default: 80 (guest) => 8080 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
```

Notice that port 80 and 22 are forwarded. 

## Install Apache 

To install Apache run the commands: 

```bash
$ sudo apt update 
$ sudo apt install apache2
```

If you have done the setup correctly you should see the "Apache2 Ubuntu Default Page" on this URL: 

> [http://localhost:8080/](http://localhost:8080/)

Do not proceed until you can see the page. 

## Procedure 

This is the procedure for moving Apache's file to a separate data disk. The commands are not shown and you will have to figure them out. 

  1. Shutdown Apache using the `systemctl` command. 
  2. Create a `btrfs` filesystem on `/dev/sdd` 
  3. Temporarily mount `/dev/sdd` on `/mnt` 
  4. Copy the files from `/var/www` to `/mnt`. **Use the flag in cp that preserves file ownerhsip and attributes.** 
  5. Unmount `/mnt`
  6. Remount `/dev/sdd` onto `/var/www`
  7. Add `/var/www` to `/etc/fstab`
  8. Reboot your VM
  
Check your work. You should see `/dev/sdd` in the output of `df` and `lsblk`. Also verify that you can still connect to the URL from the previous step. 

## Turn In 

Gather information using the following commands:

```bash 
$ mount > ~/apache_project.txt 
$ sudo blkid >> ~/apache_project.txt
$ cat /etc/fstab >> ~/apache_project.txt
```

Submit the `apache_project.txt` file for credit. 