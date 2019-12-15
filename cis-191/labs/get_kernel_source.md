# Get the Kernel Source Code 

In this lab you'll get kernel source code from Ubuntu's vendor tree. Ubuntu packages their kernels to make it easy to customize your Ubuntu machine or VM. 

## Step 0: 

On a normal Ubuntu installation the `dpkg-dev` package will be installed. On your Vagrant VM it is not. Install it:

```
$ sudo apt update
$ sudo apt install dpkg-dev 
```

## Step 1: Enable Source Repositories 

Start by enabling source repositories in your `/etc/apt/sources.list` file. Enable them by removing the hash mark `#` from the front of these two lines:

```
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted
deb-src http://archive.ubuntu.com/ubuntu xenial-updates main restricted
```

Afterward you need to re-run `apt update`.

## Step 2: Get the Kernel Source 

Use `apt` to get the Linux source package from Ubuntu. This command only downloads a source TAR archive, so you don't need to be root to use it. 

```
$ apt source linux
```

> Note DO NOT use sudo!

## Step 3: Check The Download

The `apt source` command downloads to the current directory. Check that the files are there:

```
$ ls -l
total 144816
drwxrwxr-x 29 vagrant vagrant      4096 Apr 30 21:43 linux-4.4.0
-rw-r--r--  1 vagrant vagrant  15409994 Apr  3 20:48 linux_4.4.0-146.172.diff.gz
-rw-r--r--  1 vagrant vagrant     11601 Apr  3 20:48 linux_4.4.0-146.172.dsc
-rw-r--r--  1 vagrant vagrant 132860730 Jan 21  2016 linux_4.4.0.orig.tar.gz
```

Take a screenshot of the `ls` output. 

## Turn In 

The screenshot of the output of `ls`
