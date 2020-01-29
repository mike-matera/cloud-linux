# Installing Vagrant 

> *If you plan to use school computers or have Vagrant installed already you can skip the steps in this lab and just get a screenshot.* 

In this lab you'll install Vagrant on your own computer. Vagrant creates virtual machines from based on descriptions called vagrantfiles. It gives me a way to distribute pre-configured virtual machines to you. Your computer must be powerful enough to run Linux virtual machines. You should have:

 - At least 8 GiB of RAM 
 - A 4+ core 64bit processor 
 - Support for virtualization (most Intel/AMD processors made after 2006 support virtualization)
 - At least 64 GiB of available disk space
 
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
 
> **Note:** I don't have a mac and can't confirm this procedure! 

## Installing on Ubuntu 16.04+ 

On Ubuntu it's easy to get vagrant running. You can install old-ish versions that will be good enough for this class from the main repositories with the following commands: 

```
$ sudo apt update 
$ sudo apt install vagrant virtualbox 
```

## Other Linuxes and Newer Versions

The latest versions of both VirtualBox and Vagrant can be installed using your system's package magager. Instructions for doing that can be found on the respective download pages:

  * [Download VirtualBox for Linux](https://www.virtualbox.org/wiki/Linux_Downloads)
  * [Download Vagrant](https://www.vagrantup.com/downloads.html)

## Turn In 

Turn in a screenshot of VirtualBox running.