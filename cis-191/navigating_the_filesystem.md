Every task you will perform as an administrator requires that you understand how to get around the UNIX filesystem. In this lesson you will learn the commands essential for navigation and manipulation of the filesystem.

### Commands 

  * ls, tree
  * pwd
  * cd
  * df
  * pushd, popd, dirs

### Configuration 

  * /etc/fstab

### Further Reading 

  * [http://www.tldp.org/LDP/intro-linux/html/chap_03.html](http://www.tldp.org/LDP/intro-linux/html/chap_03.html)

What are the things you will do in this lab? What knowledge does will those things draw on? How does it relate to the course?

## A Unified Filesystem 

![image](images/filesystem_logical_view.png)

UNIX and Linux use a Unified Filesystem. That is a system where all the disk drives in the system (as well as partitions and network drives) are all located in the same file hierarchy. For users used to Microsoft Windows it can be a bit confusing at first. However, Linux users quickly discover how convenient it is for every file path to look the same regardless of where the data is actually located. From an administrator's standpoint this makes it possible to make your users experience the same on all UNIX machines regardless of whether the user is logged into a machine in the home office or a satellite office.

The text below shows a diagram of the Linux filesystem generated with the ``tree`` command:

```
maximus@phoenix:/$ cd / && tree -d -L 2
.
├── bin
├── boot
│   ├── efi
│   ├── grub
│   └── lost+found
├── cdrom
├── dev
│   ├── block
│   ├── bsg
│   ├── bus
│   ├── char
│   ├── cpu
│   ├── disk
│   ├── dri
│   ├── fast_group
│   ├── fd -> /proc/self/fd
│   ├── hugepages
│   ├── input
│   ├── lightnvm
│   ├── mapper
│   ├── mqueue
│   ├── net
│   ├── pts
│   ├── serial
│   ├── shm
│   ├── snd
│   ├── ubuntu-vg
│   └── vfio
├── etc
├── home
│   ├── student
├── lib
├── lib32
├── lib64
├── libx32
├── mnt
├── proc
├── root 
├── run
├── sbin
├── sys
│   ├── block
│   ├── bus
│   ├── class
│   ├── dev
│   ├── devices
│   ├── firmware
│   ├── fs
│   ├── hypervisor
│   ├── kernel
│   ├── module
│   └── power
├── tmp
├── usr
│   ├── bin
│   ├── games
│   ├── include
│   ├── lib
│   ├── lib32
│   ├── libx32
│   ├── libx86_64-linux-gnu
│   ├── local
│   ├── locale
│   ├── sbin
│   ├── share
│   └── src
└── var
    ├── backups
    ├── cache
    ├── crash
    ├── lib
    ├── local
    ├── lock -> /run/lock
    ├── log
    ├── mail
    ├── metrics
    ├── opt
    ├── run -> /run
    ├── snap
    ├── spool
    └── tmp
```

The output has been shortened for clarity. You can generate the complete directory hierarchy with this command:

```
$ cd /
$ tree -d
```

The top level directories are organized by function. Different distributions (e.g. Ubuntu and Fedora) have slightly different rules on where files go inside the hierarchy but, for the most part, the organization at the top level is as follows:

| Directory | Examples | Purpose |
| ------ | ------ | ------ |
| /bin | /bin/ls <br> /bin/pwd <br> /bin/cp <br> /bin/mv | Contains many (but not most) of the system's executable programs. The programs here tend to do the most low-level system tasks. | 
| /boot | /boot/vmlinuz <br> /boot/initrd.img <br> /boot/grub | Contains the files needed to boot Linux, including the Linux Kernel, which is the core of the operating system, the Initial Ramdisk (initramfs) and the boot loader. On x86-based systems the boot loader is GRUB which is discussed in a different lecture. |
| /dev | /dev/sda <br> /dev/null <br> /dev/random | Contains entries for hardware devices. Most peripherals in the system have an entry in this directory. There are some useful virtual devices located here too, such as a random number generator. |
| /etc | /etc/hostname <br> /etc/passwd <br> /etc/fstab | The etcetera directory (/etc) is where system configuration is stored, such as the system's name, it's IP address, what programs get started at boot time and much more. There are many things you can change about Linux using commands. Making those changes permanent usually means editing a file in the /etc directory | 
| /home | /home/student | The home directory is typically where user's private data is stored. By default most Linuxes will create a new directory in /home for each user on the system. | 
| /lib, /lib32, /lib64 | /lib/ld-linux.so.2 <br> /lib/modules | The lib family of directories is where program fragments, called Shared Objects are stored. Shared objects (*.so) files serve the same purpose as DLLs in Windows. They contain program code that many different programs use. The lib directory also holds loadable modules which extend the Linux Kernel's functionality. |
| /media | ./media/cdrom | Removable drives often get placed here | 
| /opt | /opt/google/chrome | Optional or miscellaneous software gets installed here. Most often the /opt directory gets used for commercial software. | 
| /proc, /sys | /proc/cmdline <br> /proc/cpuinfo | The /proc and /sys directories are very special. The files here are not on any disk, they are a window into the brains of Linux. By reading files /proc and /sys you can answer interesting questions (e.g. What files are open? How hot is my processor?). Writing files in /proc and /sys can alter your system's behavior (e.g. Change the processor clock speed. Hibernate the system.). | 
| /root | | The home directory of the "root" user. | 
| /run | /rsyslogd.pid/run | Temporary files used by running programs, usually daemons. Daemons are programs that perform system services. The /run directory stores files in RAM, not the disk so the contents of this directory are lost with every reboot. |
| /sbin | /sbin/init <br> /sbin/shutdown <br> /sbin/mount | Binary directory for the system and system administrator. The programs in this directory, like the /bin directory, are usually executable. | 
| /tmp | /tmp/foo | Temporary data. Unlike /run the data here is stored on disk but Linux periodically cleans out this directory to keep it from becoming full. This is a good place to store files that you don't want to keep. Be careful: Everyone can see the files so don't store private things here. | 
| /usr, /usr/local | /usr/bin/vi <br> /usr/sbin/useradd | The /usr directory contains repeats of some of the top level directories explained here (e.g. /usr/bin, /usr/lib, /usr/sbin). Most software on the system is installed under the /usr directory. |
| /var | /var/log <br> /var/www <br> /var/mail | The var directory holds persistent runtime data (e.g. the system logs). Many system services store data here. | 

## Navigating the Filesystem 

There are two kinds of paths in UNIX, absolute and relative paths. An absolute paths begin with a foreslash (`/`) and point to exactly one location on the filesystem. Here are some examples of absolute paths:

```
/usr/bin/perl
/dev/sda1
/home/mike/home/mike/assignment1.txt
```

Paths are read left to right. The last path above reads:

Start at the root directory (``/``), change into ``home``, then change into ``mike``, then look at the file ``assignment1.txt``. 

Relative paths do not start in the root directory therefore do not start with a slash. Here are examples of relative paths:

```
perl
mike/assignment1.txt
```

So what are relative paths relative to? They're relative to the current working directory. The current working directory is controlled by the ``cd`` command and displayed by the ``pwd`` command. Look at the following commands and be sure you understand them:

```
$ pwd
/home/student
$ mkdir paths
$ echo Hello > paths/greeting.txt
$ cat paths/greeting.txt
Hello
$ cat /home/student/paths/greeting.txt
Hello
```

### Using the cd Command 

The ``cd`` command changes the working directory. Like any command that takes a file or directory argument ``cd`` can accept a relative or absolute path.

```
cd /proc/self 
cd labs/lab1
cd
```

The ``cd`` command does something special when you give it no arguments. Try it and use the ``pwd`` command to determine where you are.

### Pro Tip: Using pushd and popd 

When you're working on something complicated you often edit files in more than one directory. It can become a pain to be constantly changing between two or more directories, especially when those directories are deep in the file tree. That's where the ``pushd`` and ``popd`` command come in handy. Those commands maintain a stack of directories that you can jump between quickly. Check out this example:

```
$ cd /etc/init
$ pwd
/etc/init
$ dirs
/etc/init
$ pushd /var/log
/var/log /etc/init
$ pwd
/var/log /etc/init
$ dirs
/var/log /etc/init
$ pushd
/etc/init /var/log
$ pwd
/etc/init
```

Notice that `pushd` with no arguments switches between the two directories on the stack. You can add more directories.

```
$ pushd /proc/self
/proc/self /etc/init /var/log
```

The verbose version of the dirs command will show you the stack with the directories numbered:

```
$ dirs -v
0 /proc/self
1 /etc/init
2 /var/log
```

By itself `pushd` only switches between directories zero and one. You can go to a specific directory like this:

```
$ pushd +2
/var/log /proc/self /etc/init
```

### Listing Files with ls and tree 

You can list the files, subdirectories and devices in a directory using the ``ls`` command. The ``ls`` command has arguments that give you a different level of detail about the contents of the directory. The most basic usage is:

```
$ ls
file1 file2 file3
```

If you want a long listing of the files, which provides more detail, use the ``-l`` switch:

```
$ cd /tmp/example
$ ls -l
total 1248
-rw-rw-r-- 1 mike mike 523776 Aug 4 14:36 file1
-rw-rw-r-- 1 mike mike 114176 Aug 4 14:36 file2
-rw-rw-r-- 1 mike mike 637440 Aug 4 14:36 file3
```

To see hidden files (files that begin with a period) use the ``-a`` switch:

```
$ ls -la
total 1280
drwxrwxr-x 2 mike mike  4096 Aug 4 14:35 .
drwxrwxrwt 11 root root 24576 Aug 4 14:35 ..
-rw-rw-r-- 1 mike mike 523776 Aug 4 14:36 file1
-rw-rw-r-- 1 mike mike 114176 Aug 4 14:36 file2
-rw-rw-r-- 1 mike mike 637440 Aug 4 14:36 file3
-rw-rw-r-- 1 mike mike   0 Aug 4 14:38 .hidden
```

The ``tree`` command provides a prettier way to see your files and directory. This can be handy when you're exploring, but is less informative than ``ls``.

```
$ tree example/
example/
├── file1
├── file2
├── file3

0 directories, 3 files
```

The ``tree`` command will also show you hidden files:

```
$ tree -a example/
example/
├── file1
├── file2
├── file3
└── .hidden

0 directories, 4 files
```

Remember the ``tree`` command. It will come in handy in future assignments.