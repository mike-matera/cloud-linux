
### Commands 

  * ip
  * hostname
  * ifup
  * ssh
  * scp

Configuration
  * /etc/network/interfaces
  * /etc/hostname
  * /etc/hosts

### Reading 

  * [Networking Basics](basic_networking.html)

Contents
  - [1 Commands](#TOC_Commands)
  - [1.1 Reading](#TOC_Reading)

  - [2 Introduction](#TOC_Introduction)
  - [3 Assign a Static IP Address](#TOC_Assign_a_Static_IP_Address)
  - [3.1 Adding an IPv6 Address](#TOC_Adding_an_IPv6_Address)
  - [3.2 Changing your IPv4 Address](#TOC_Changing_your_IPv4_Address)
  - [3.3 Verify Your Address](#TOC_Verify_Your_Address)
  - [3.4 Making your IP Address Permanent](#TOC_Making_your_IP_Address_Permanent)

  - [4 Using SSH](#TOC_Using_SSH)
  - [4.1 On Mac OS X and Linux](#TOC_On_Mac_OS_X_and_Linux)
  - [4.2 On Windows](#TOC_On_Windows)
  - [4.3 IPv4 or IPv6](#TOC_IPv4_or_IPv6)

  - [5 Logging In](#TOC_Logging_In_)
  - [6 Transferring Files](#TOC_Transferring_Files_)
  - [6.1 Direct Method](#TOC_Direct_Method)
  - [6.2 Opus Method](#TOC_Opus_Method)

  - [7 Lab Questions](#TOC_Lab_Questions)

## Introduction 

In this lab you'll practice ways to login to your VM and get move files back and forth from your workstation to your VM. These are essential skills for an administrator. Console access to many Linux machines is not practical, either because the machine is locked away somewhere (e.g. a server) or because it's a VM with a clunky console interface (e.g. a cloud server) or because the console can only be accessed with special hardware (e.g. a smartphone, Raspberry Pi). Making the most of remote access also enables you to have access to your home machine from anywhere.

## Assign a Static IP Address 

Having a static IP address is not strictly required for SSH access, but it makes things a whole lot easier. You can figure out your static IP address assignment by looking in the project milestone page for next week:
 [Get Connected](get_connected.html)

This step guides you through assigning your address to your VM.Your VM has an IPv4 address assigned by DHCP and an IPv6 address assigned by SLAAC. Those protocols are covered more extensively in[CIS-192](../cis_192.html). You can see what addresses you have assigned using the
```
ip
```

command:

```
$ ip addr
1:
lo
: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
  link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
 
inet 127.0.0.1/8 scope host lo
   valid_lft forever preferred_lft forever
 
inet6 ::1/128 scope host
   valid_lft forever preferred_lft forever
2:
eth0
: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
  link/ether 00:50:56:bd:03:e3 brd ff:ff:ff:ff:ff:ff
 
inet 172.20.4.220/16 brd 172.20.255.255 scope global eth0
   valid_lft forever preferred_lft forever
 
inet6 2607:f380:80f:f830:250:56ff:febd:3e3/64 scope global dynamic
   valid_lft 2591924sec preferred_lft 604724sec
  inet6 fe80::250:56ff:febd:3e3/64 scope link
   valid_lft forever preferred_lft forever
```

I'veboldedthe interfaces and the IP addresses in the output of
```
ip addr
```

.

### Adding an IPv6 Address 

With IPv6 every interface will have multiple assigned IP addresses. You don't have to lose your old address to assign a new one. Using the address information provided to you run the following command to add another IPv6 address:

```
$ sudo ip addr add 2607:f380:80f:f830:192::X/64 dev eth0
```

Replace "X" with your network number.

### Changing your IPv4 Address 

Execute the following command to change your IPv4 address.

```
$ sudo ip addr replace 172.20.192.X/16 dev eth0
```

Replace "X" with your network number.

### Verify Your Address 

Now you should re-run ip addr to verify that you have set your addresses correctly.

```
ip addr
```

### Making your IP Address Permanent 

The changes you just made will be lost if you reboot. In order to preserve them you must edit the configuration file on Ubuntu that is read when the machine starts. That file is
```
/etc/network/interfaces
```

. The default
```
interfaces
```

file looks like this:

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).
# The loopback network interface
auto lo
iface lo inet loopback
# The primary network interface
auto eth0
iface eth0 inet dhcp
```

Edit the file to look like this:

```
# The loopback network interface
auto lo
iface lo inet loopback
# The primary network interface
auto eth0
iface eth0 inet static
 address 172.20.192.X
 netmask 255.255.0.0
 gateway 172.20.0.1
 dns-nameservers2607:f380:80f:f425::2522607:f380:80f:f425::253
iface eth0 inet6 static
 address
2607:f380:80f:f830:192::X
 netmask 64
```

WARNING: Copy-and-paste introduces subtle errors into your interfaces file. You are better typing this information in manually. Triple check the file. Once you're convinced that you have the right information reboot the VM:

```
reboot
```

If your VM doesn't boot properly it's probably because there's an error in your interfaces file. Run the following command to help you find where your error is:

```
$ ifup eth0
/etc/network/interfaces:10: unknown method
ifup: couldn't read interfaces file "/etc/network/interfaces"
```

The error above is telling you that your problem is on or near line number 10.

## Using SSH 

How you use SSH depends on your workstation's OS. Here are brief instructions for the most popular OSes. If you already have an SSH client and know how to use it you can skip this section. The CIS machines have PuTTY and FileZilla installed.

### On Mac OS X and Linux 

Linux and MacOs have native SSH clients. You can SSH into your machine from the command line:

```
$ ssh student@<vm-ip-addr>
```

You can also copy files from the command line:

```
$ scp <source> <destination>
```

Examples:

```
Copy a file to your VM:

$ scp /path/to/myfile student@<vm-ip-addr>:/path/to/destination
Copy a file file from your VM:

$ scp student@<vm-ip-addr>:/path/to/file /path/to/local/destination
```

On Linux you can use nautilus or your favorite file manager to browse remote files just like they were local. In your file manager enter your VM as a file URL:

```
ssh://student@<vm-ip-addr>/path
```

Now you can use drag-and-drop to transfer files.

### On Windows 

Windows doesn't have a native SSH client. There are two programs you can download on Windows that will help you.
  - [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)- Gives you command line access
  - [FileZilla](https://filezilla-project.org/)- Uses SFTP to move files

WARNING: IF YOU DOWNLOAD FILEZILLA FROM SOURCEFORGE THE INSTALLER CONTAINS MALWARE.I recommend that you download the ZIP file, not the Windows installer. When you use drag-and-drop from FileZilla be sure to enter port number 22 at the top of the window. Otherwize FileZilla will attempt old-style insecure FTP.

### IPv4 or IPv6 

If you are inside of the CIS network (in rooms 828, 829 or the CIS area of the STEM center) you can access your VM directly via IPv4. If you're outside of the CIS network you may be able to access your VM directly depending on whether your Internet provider gives you an IPv6 address or not. Here's how to tell:

```
On Windows Command Prompt:

> ipconfig /all
On Mac/Linux:

$ ip addr
```

If you see an IPv6 address that begins with the number "2" then you're all good with the 21st century. Otherwise you're stuck with IPv4.

## Logging In 

If you are directly connected you can login to your VM directly with SSH:

```
you@yourmachine# ssh student@<vm-ip-addr>

 
<enter funny Cabrillo>

student@ubuntu#
```

If you are not directly connected you must login via Opus:

```
you@yourmachine# ssh -p 2220 <my-unix-username>@opus.cis.cabrillo.edu

 
<enter your UNIX password>

you192@opus# ssh student@<vm-ip-addr>

 
<enter funny Cabrillo>

student@ubuntu#
```

Use one of the above procedures to login to your VM.

## Transferring Files 

Transferring files will be important for this class. You should know this procedure by heart. Unfortunately if you're using IPv4 like me there's extra steps. For this lab you'll bring the /etc/issue.net file onto your local computer, edit it and put it back. Be careful to follow these steps exactly.

### Direct Method 

```
Step 1: Copy /etc/issue.net into your current directory:
you@yourmachine# scp student@<vm-ip-addr>:/etc/issue.net . 
Step 2: Edit the local copy
you@yourmachine# nano issue.net
Step 3: Put it back into a temporary location
you@yourmachine# scp issue.net student@<vm-ip-addr>:/tmp/
Step 4: Move it back to /etc (note this is done from your VM)
student@ubuntu# sudo cp /tmp/issue.net /etc/issue.net
```

### Opus Method 

```
Step 1: (From Opus) Copy /etc/issue to your Opus home directory
you192@opus#scp student@<vm-ip-addr>:/etc/issue.net .
Step 2: Copy issue.net to your workstation (note the capital -P)
you@yourmachine# scp -P 2220 <you192>@opus.cis.cabrillo.edu:/home/cis192/<you192>/issue.net .
Step 3: Edit the local copy
you@yourmachine# nano issue.net
Step 4: Put the local copy back on Opus
you@yourmachine# scp -P 2220 issue.net <you192>@opus.cis.cabrillo.edu:/home/cis192/<you192>/
Step 5: Put the new Opus copy into a temporary location on your VM
you192@opus# scp issue.net student@<vm-ip-addr>:/tmp/
Step 6: Move it back to /etc (note this is done from your VM)
student@ubuntu# sudo cp /tmp/issue.net /etc/issue.net
```

## Lab Questions 

  - What is the IP address and hostname of your VM?
  - List, in order, the machine and directory locations that your issue.net file traveled through in order for you to edit it. Use absolute paths, including for Mac and Windows if that's what you used.

Turn in the answers to your lab questions on Canvas.