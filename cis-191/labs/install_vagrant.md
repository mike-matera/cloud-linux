# Install Vagrant 

Vagrant is software that automates management of Linux virtual machines. It's really helpful for Linux classes because you can create VMs on your own system (even if you already use Linux) that you can mess with, break, throw away and start over. Having a Linux VM that you control is required for course work in my Linux classes. Vagrant is installed on class and STEM Center computers. Vagrant creates virtual machines from a description called a `Vagrantfile`. 

> If you plan to use school computers you can skip to the end of this lab.

## System Requirements 

Your computer must be powerful enough to run Linux virtual machines. You should have:

| | | 
| --- | --- |
| Operating System | Windows, Mac, Linux <br>*See thee section about ChromeOS* | 
| Processor | 4 Cores <br> Support for virtualization <br> *Most Intel/AMD processors made after 2006 support virtualization* | 
| Memory | 8 GiB of RAM | 
| Disk | 64 GiB of available space | 

## VirtualBox 

Vagrant relies on VirtualBox to run VMs. [VirtualBox](https://www.virtualbox.org/) is open source virtualization software distributed by Oracle. VirtualBox is available for Mac, Windows and Linux. 

## Windows 

  - Download and install VirtualBox 
     - [VirtualBox Download Page](https://www.virtualbox.org/wiki/Downloads)
  - Download and install Vagrant
     - [Vagrant Download Page](https://www.vagrantup.com/downloads.html)

## Mac OSX

  - Install [Homebrew](https://brew.sh/)
  - Install VirtualBox using Homebrew

```
$ brew cask install virtualbox
``` 

  - Install Vagrant using Homebrew 
  
```
$ brew cask install vagrant
$ brew cask install vagrant-manager
``` 

## Ubuntu 16.04+ 

On Ubuntu it's easy to get vagrant running. You can install old-ish versions that will be good enough for this class from the main repositories with the following commands: 

```
$ sudo apt update 
$ sudo apt install vagrant virtualbox 
```

## ChromeOS 

> **CromeOS support has not been tested.**

You cannot install Vagrant on ChromeOS. However, "Linux Mode" in ChromeOS is a virtual machine running on the Chrome Book that is in many ways very similar to how Vagrant works. If you're using a Chrome Book enable Linux mode and use Linux mode instead of a Vagrant VM. Skip to the end of the lab. 

## Other Linuxes and Newer Versions

The latest versions of both VirtualBox and Vagrant can be installed using your system's package magager. Instructions for doing that can be found on the respective download pages:

  * [Download VirtualBox for Linux](https://www.virtualbox.org/wiki/Linux_Downloads)
  * [Download Vagrant](https://www.vagrantup.com/downloads.html)

## Turn In 

Turn in a screenshot of VirtualBox (or Linux Mode in ChromeOS) running.