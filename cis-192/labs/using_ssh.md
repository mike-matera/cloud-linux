# Copying Files with SSH 

## Commands 

  * ssh
  * scp

## Introduction 

In this lab you'll practice ways to login to your VM and get move files back and forth from your workstation to your VM. These are essential skills for an administrator. Console access to many Linux machines is not practical, either because the machine is locked away somewhere (e.g. a server) or because it's a VM with a clunky console interface (e.g. a cloud server) or because the console can only be accessed with special hardware (e.g. a smartphone, Raspberry Pi). Making the most of remote access also enables you to have access to your home machine from anywhere.

## Using SSH 

How you use SSH depends on your workstation's OS. Here are brief instructions for the most popular OSes. If you already have an SSH client and know how to use it you can skip this section. The CIS machines have PuTTY and FileZilla installed.

### On Mac OS X, Linux and Windows PowerShell 

Linux and MacOs have native SSH clients. You can SSH into your machine from the command line:

```
$ ssh <username>@<vm-name>
```

You can also copy files from the command line:

```
$ scp <source> <destination>
```

Copy a file to your VM:

```
$ scp /path/to/myfile student@<vm-name>:/path/to/destination
```

Copy a file file from your VM:

```
$ scp student@<vm-name>:/path/to/file /path/to/local/destination
```

On Linux you can use nautilus or your favorite file manager to browse remote files just like they were local. In your file manager enter your VM as a file URL:

```
ssh://student@<vm-name>/path
```

Now you can use drag-and-drop to transfer files.

### On Old Windows (Windows 8 and older)

Windows doesn't have a native SSH client. There are two programs you can download on Windows that will help you.

  - [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)- Gives you command line access
  - [FileZilla](https://filezilla-project.org/)- Uses SFTP to move files

WARNING: IF YOU DOWNLOAD FILEZILLA FROM SOURCEFORGE THE INSTALLER CONTAINS MALWARE.I recommend that you download the ZIP file, not the Windows installer. When you use drag-and-drop from FileZilla be sure to enter port number 22 at the top of the window. Otherwise FileZilla will attempt old-style insecure FTP.

### Capture and Download Packets 

Run the following command on your AWS VM: 

```
$ sudo tcpdump -i eth0 -w lab.cap not port ssh
```

The command captures packets (avoiding SSH packets) into a file called `lab.cap` in the current directory. It will run indefinitely so wait a minute or two and then hit Ctrl-C. When `tcpdump` finishes you should see something like this: 

```
$ sudo tcpdump -i eth0 -w lab.cap not port ssh 
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes

^C
30 packets captured
30 packets received by filter
0  packets dropped by kernel
```

Download `lab.cap` onto your computer and open it with Wireshark. 

## Turn In 

Turn in your `lab.cap` file. 