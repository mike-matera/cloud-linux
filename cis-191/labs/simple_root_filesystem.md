The purpose of this lab is to create a minimal but functional root filesystem. You will package your filesystem in the initramfs ramdisk format. This process is a very common task for those customizing Linux on embedded hardware like [Raspberry Pi](http://www.raspberrypi.org/) and [Beagle Bone](http://www.raspberrypi.org/) or even a rooted Android phone. 
 
 Related: [Filesystems and Mount](filesystems_and_mount)

## Step One 

You will have to do almost every step of this lab as root. You should begin by running the command

```
$ sudo -s
```

Make a work area in your /home/student directory.

```
# mkdir /home/student/proj4
# cd /home/student/proj4
```

  - In your proj4 directory create a 20MB file using dd called proj4.img.
  - Bind a loopback device (e.g. /dev/loop0) to your file

Use the losetup command to verify that you have successfully setup your loopback device. If you haven't be sure you fix what's wrong. The next part depends on this.

## Step Two 

Your block device from step one needs to be formatted. Format it with an ext2 filesystem like this:

```
mkfs -t ext2 <loopback-device>
```

Record the following information about your file system:
  * Block Size
  * Number of inodes
  * Number of blocks
  * Number of blocks reserved for super user

Remake the file system using the following additional options:

```
mkfs -t ext2 -m 0 -N 500 -L /linux <loopback-device>
```

  * What does the -m 0 option do?
  * The -N 500?
  * The -L /linux?

Submit the answers to the above questions and the stats from your first format with this assignment on Blackboard.

## Step Three 

Now that you have a filesystem you can create files and directories in it. Mount your loopback device. Create following directories in your new filesystem:
  - bin
  - dev
  - etc
  - lib
  - proc
  - sbin
  - sys
  - tmp

Change the permissions of the tmp directory to 1777.

## Step Four 

Populate the directories with the required files. In order to create a device file for the console, let's look at a long listing of the console device file from your system's dev directory:

```
# ls -l /dev/console
```

Now, use mknod to create the same device inside the dev directory of your new filesystem. The syntax of mknod is: 

```
mknod <name> <c|b> <major-number> <minor-number>
```

Here's how you would make a character device called charchar with major number 5 and minor number 1:

```
# mknod charchar c 5 1
```

Be sure to set the correct permissions, ownership and group the file you just created.

## Step Five 

Your root filesystem has it's first (and only) device. Now you need to copy programs into it.Copy the bash shell (/bin/bash) into your new filesystem's bin directory. Make a symbolic link from the bash file to /sbin/init on your new filesystem.

When Linux boots it looks for a program called /sbin/init. That's the program with PID #1. It's init's job to get the system ready. By making a symbolic link to BASH when Linux starts into our initial RAM disk it will run BASH for us. But BASH needs some additional files to run. It needs *.so library files. You can find out what *.so files are needed by an executable on Linux using the ldd command. Here's how to find out what *.so files are used by BASH:

```
$ ldd /bin/bash
linux-vdso.so.1 => (0x00007fffb7791000)
libtinfo.so.5 => /lib/x86_64-linux-gnu/libtinfo.so.5 (0x00007f1689b5e000)
libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f168995a000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1689595000)
/lib64/ld-linux-x86-64.so.2 (0x00007f1689d87000)
```

If these files are missing in your new filesystem BASH cannot run. Copy each of them into the corresponding location in your new filesystem. You can ignore linux-vdso.so.1 that is a virtual library (i.e. there's no real file to copy anywhere).

> **IMORTANT** Be sure to copy the paths exactlyas they appear in the ldd listing. This may require you to make additional directories. For example (this will NOT match your VM but is correct on my laptop) if you see the following line from ldd:

```
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7e45d96000)
```

You would have to make the /mnt/lib/x86_64-linux-gnu directory then copy libc.so.6 into it. Like this:

```
# mkdir /mnt/lib/x86_64-linux-gnu
# cp /lib/x86_64-linux-gnu/libc.so.6 /mnt/lib/x86_64-linux-gnu/libc.so.6
```

If you've copied everything over you should have a working root filesystem.

## Testing Your Work

How do you know you did it right? If you copied bash and its libraries correctly then you should be able to successfully chroot into your new filesystem.

```
# chroot /mnt /bin/bash
```

If there is an error you have not copied bash or the libraries correctly and you should check your work. I will be testing your submission using chroot. Notice that the 'ls' command doesn't work after chroot. That's because you never copied the ls command to the new filesystem. The only commands that will work are the ones built into the shell (like echo and exit).

## Turn In 

Unmount and de-loop your image file and turn it in with the answers to the questions in this lab. Compress your image file with GZIP. This will dramatically reduce its size:

```
# gzip proj4.img
```

Your image file will be graded by robot so please be sure you named your image file proj4.img.gz. Submit your file on Canvas.
