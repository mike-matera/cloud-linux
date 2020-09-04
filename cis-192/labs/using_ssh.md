# Using SSH 

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
$ ssh student@<vm-name>
```

You can also copy files from the command line:

```
$ scp <source> <destination>
```

Examples:

```
Copy a file to your VM:

$ scp /path/to/myfile student@<vm-name>:/path/to/destination
Copy a file file from your VM:

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
you@yourmachine# ssh student@<vm-name>
 
<enter funny Cabrillo>

student@ubuntu#
```

If you are not directly connected you must login via Opus:

```
you@yourmachine# ssh -p 2220 <my-unix-username>@opus.cis.cabrillo.edu
 
<enter your UNIX password>

you192@opus# ssh student@<vm-name>
 
<enter funny Cabrillo>

student@ubuntu#
```

Use one of the above procedures to login to your VM.

## Transferring Files 

Transferring files will be important for this class. You should know this procedure by heart. Unfortunately if you're using IPv4 like me there's extra steps. For this lab you'll bring the /etc/issue.net file onto your local computer, edit it and put it back. Be careful to follow these steps exactly.

## Lab Questions 

  - What is the IP address and hostname of your VM?
  - List, in order, the machine and directory locations that your issue.net file traveled through in order for you to edit it. Use absolute paths, including for Mac and Windows if that's what you used.

Turn in the answers to your lab questions on Canvas.