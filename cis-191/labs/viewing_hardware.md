# Viewing Hardware 

In this lab you will examine the hardware on your Linux machine. You can perform this lab on your VM or your own computer. Modern computers have  many devices, it can be difficult to know exactly what's inside the box. Even when you can look into the box, most of the devices that Linux uses aren't visible. The `lshw` command shows you what devices are connected to your computer.

## Step 1: Create the Standard VM 

I've created a Vagrantfile for this class. The Vagrantfile is a standard Ubuntu 16.04 Server VM with additional disks added. The disks will come in handy later. You can create the standard VM by downloading the Vagrant file and using `vagrant up`.

```bash 
$ wget http://www.lifealgorithmic.com/_static/boxes/Vagrantfile-Xenial64-Disks
$ mv Vagrantfile-Xenial64-Disks Vagrantfile 
$ vagrant up
```

> Note: Create a new directory for your Vagrantfile. The name of the directory is up to you.

## Step 2: SSH Into your Vagrant VM

Vagrant gives you an easy way to SSH into a VM. Once you have used `vagrant up` you can simply run the `vagrant ssh` command to connect. 

```bash
$ vagrant ssh 
```

That will connect you. To get your host prompt back simply exit. 

```bash
exit 
```

## Step 3: Gather the Information 

`lshw` must be run as root in order to see the full set of hardware available. Be sure to execute it using the `sudo` command. The output of `lshw` can be very long, redirect it to a file and view the file with your favorite editor.

```bash
$ lshw 
```

Save the output of `lshw` to a file: 

```bash 
$ lshw > hardware_list.txt
```

## Step 4: What's Inside? 

Now that you have the raw information you should be able to answer the following questions:

  - What is the `product` information on the CPU?
  - What is the `product` information on the Ethernet device?
  - How much memory is in the VM?
  - List all of the disks and their sizes. 

## Turn In 

  - Submit the output of lshw as a text file called `hardware_list.txt` (no screenshots!)
  - The answers to the lab questions in a document called `viewing_hardware.txt`

Submit your answers on Canvas.
