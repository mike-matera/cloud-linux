# Install Ubuntu on Your Own Computer  

In this lab you'll test your Vagrant installation by using it to create a Ubuntu VM. Vagrant makes it fast and easy to install a VM.

## Step 1: Get a Shell 

This step is OS dependent. On Mac and Linux start a Terminal. On Windows start Powershell. 

  - **MacOS:** Applications -> Utilities -> Terminal 
  - **Windows:** Click Start, type PowerShell, and then click Windows PowerShell.
  - **Linux:** Press `Ctrl-Alt-T`
  
## Step 2: Create a Directory for Your VM

These commands work in Powershell on Windows and BASH on Mac/Linux.

```
$ mkdir cis-90
$ cd cis-90
``` 

Each VM in Vagrant needs its own directory. This lab uses the `cis-90` directory. Future labs won't specify where to put VMs. That's up to you. 

## Step 3: Create your Ubuntu VM

The command below creates a `Vagrantfile` in the current directory. The argument specifies a Vagrant Box to use. There are lots of boxes available. You can [discover vagrant boxes](https://app.vagrantup.com/boxes/search) on Vagrant's website.  

```
$ vagrant init ubuntu/bionic64
``` 

The next command starts your VM based on the `Vagrantfile`:

```
$ vagrant up
``` 

The `vagrant up` command will download the image of the VM. This could take a long time on slow connections. 

## Step 4: View your VM in VirtualBox 

Vagrant drives VirtualBox. The VirtualBox application doesn't have to be open for Vagrant to work. Open VirtualBox and you'll see that your new Ubuntu VM has been added. Open the VM and login.

> Tip: The username is "vagrant" and the password is "vagrant" on all Vagrant VMs.

**Take a screenshot of you logged into your new VM**

## Step 5: (Optional) Remove the VM

You can shutdown your VM from VirtualBox. You can also shut it down using the command:

```
$ vagrant halt
```

You can also remove your VM and all of its disks with the command:

```
$ vagrant destroy -f
```

When you destroy a VM the download that was done by `vagrant up` is still cached, so the next time you do a `vagrant up` it will be much quicker. 

## Turn In 

  1. The screenshot from Step 4
  