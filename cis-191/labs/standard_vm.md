# The Standard VM

In this lab you will create the VM that you'll use for the rest of the semester. Then you'll examine the VM's hardware. Modern computers have  many devices, it can be difficult to know exactly what's inside the box. Even when you can look into the box, most of the devices that Linux uses aren't visible. The `lshw` command shows you what devices are connected to your computer.

## Step 1: Create the Standard VM 

I've created a `Vagrantfile` for this class. The `Vagrantfile` is a standard Ubuntu 18.04 Server VM with additional disks added. The disks will come in handy later. You can create the standard VM by downloading the Vagrant file and using `vagrant up`.

```eval_rst
:Download: :download:`Vagrantfile <../../boxes/bionic64-disks/Vagrantfile>`
```

Create a new directory for your `Vagrantfile` and change into it. When you are in a directory with a `Vagrantfile` you can start the Vagrant VM with the command:

```
$ vagrant up
```

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
$ lshw > /vagrant/hardware_list.txt
```

## Step 4: What's Inside? 

Now that you have the raw information you should be able to answer the following questions:

  - What is the `product` information on the CPU?
  - What is the `product` information on the Ethernet device?
  - How much memory is in the VM?
  - List all of the storage devices and their sizes. 

## Step 5: A Real Example 

The hardware file you get from your VM is quite limited because VMs only need a minimum of hardware to do their job. Below is a link to download the output of `lshw` run on a server in the CIS datacenter. 

```eval_rst 
:Download: :download:`lshw_example.txt` 
```

Look through the file to answer the following questions: 

  - How many CPUs (physical chips) does the server have? 
  - How many cores does each chip have? 
  - How much memory is in the machine? 

## Turn In 

  - Submit the output of lshw as a text file called `hardware_list.txt` (no screenshots!)
  - The answers to the lab questions in a document called `viewing_hardware.txt`

Submit your answers on Canvas.
