# Build a Custom Kernel Driver 

In this lab you'll build a custom device driver from source.

## Introduction 

Git is a source control management (SCM) tool that is popular with open source projects. Git gives you a way to download source code for a program, keep up with updates and contribute your own features and fixes to the authors. Once you have a driver's source code you must compile it to yield a loadable kernel module.Using Git to get the Source CodeIn this lab you'll use a kernel driver that is an example in the excellent book [Linux Device Drivers](https://lwn.net/Kernel/LDD3/). The book was published in 2005 so some of the example code needs a bit of fixups. I maintain a Git repository that fixes some compilation problems. You can checkout the code with the following command:

```
$ git clone https://github.com/mike-matera/ldd3.git
```

That will create an "ldd3" directory in the current directory. There are several drivers in that directory, the "scull" driver compiles and can be inserted into your kernel.

```
$ cd ldd3/scull
```

Once you're in the directory you invoke the "make" command to build the source:

```
$ make
```

This creates scull.ko. The *.ko extension is used for kernel modules. You can insert the kernel module with the insmod command:

```
$ sudo insmod scull.ko
```

Check to verify that your module is inserted:

```
$ lsmod
$ lsmod | grep scull
```

Most drivers print a banner to the kernel log when they are inserted. Look at the kernel message buffer to see what the scull driver reported:

```
$ dmesg | tail
$ tail /var/log/kern.log
```

Verify that you see the banner from the scull driver. Now remove the module from the kernel and verify that it's gone:

```
$ sudo rmmod scull
$ lsmod | grep scull
```

## Turn In 

When you're done save the bottom lines of your kernel log to a file called `custom_driver.txt` like this:

```
$ tail /var/log/kern.log > custom_driver.txt
```
