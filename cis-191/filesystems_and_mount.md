# Filesystems and Mount 

**Commands**

  * mount
  * umount
  * losetup
  * dd
  * mkfs

**Configuration**

  * /etc/fstab

## Introduction 

Linux's filesystem is a filesystem of filesystems. A filesystem is an entity that contains files and can be on physical disks, disk arrays or on the network. In order for filesystems to be useful they must be formatted and mounted. This page explain those relationships and show you the commands you need to manage and manipulate filesystems.

## The Logical Filesystem  

![image](../_static/images/filesystem_logical_view.png)

In Depth:[Navigating the Filesystem](navigating_the_filesystem)

As a Linux user you should be familiar with the unified filesystem and how to navigate it. A simplified diagram of the filesystem is above. The diagram shows a typical layout of directories. By following the arrows in the diagram you can build an absolute path. For example, if you wanted to find where my files are you would:

```
$ cd / 
$ cd home
$ cd mike
```

At the end of the process you will have constructed the path:

```
/home/mike/
```

This understanding is all a regular user needs. An administrator, however is concerned with where these paths are stored physically or on the network and what format the filesystems use.

## The Physical Filesystem 

![image](../_static/images/filesystem_physical_view.png)

There are invisible boundaries in the logical filesystem. Those boundaries are where different storage media have been mounted into the file tree. Examine the drawing above. In that drawing the same folders as above are shown but grouped together with the disk or network share that contains the files. The diagram shows that the logical filesystem is composed of four physical filesystems.

  - The root filesysem (`/`) mounted on ``/``
  - A network filesystem with home directories mounted on ``/home``
  - A DVD mounted on ``/media/cdrom``
  - A flash drive mounted on ``/media/flash``

One thing you should notice is that each physical filesystem has a root (``/``) directory. The location of the root directory in the logical filesystem is determined by where it is mounted.In the example the network filesystem that contains ``mike/`` and ``sarah/`` happens to be mounted on ``/home``. As an administrator you are free to mount it anywhere you like, even into another mounted filesystem.

## Filesystem Types 

The term "filesystem" can refer to two things. A bunch of files and directories organized into a tree structure or the on-disk format used to store data. The two uses make the work confusing for beginners. The table describes some filesystem formats that are supported by Linux:

| Filesystem Format | mount flag | Use | Description |
| --- | --- | --- | --- |  
| ext2, ext3, ext4 | -t ext4 | Native Linux disks | The EXT family of filesystems have been Linux's native filesystems for almost as long as there's been Linux. All machines you encounter in 2017 will use an EXT filesystem in at least one place. | 
| btrfs | -t btrfs | Native Linux disks | The B-Tree filesystem (pronounced butter-F-S) is an advanced filesystem that will replace the EXT family as Linux's primary filesystem. | 
| msdos, vfat | -t vfat | Flash and other removable drives | The DOS filesystem is very common for removable drives. It's lack of security are preferred for removable drives because user accounts don't have to be shared from machine to machine. | 
| NTFS | -t ntfs | Windows System Disks | NTFS is an advanced filesystem used by Windows | 
| HFS+ | -t hfsplus | OS X System Disks | HFS+ is an advanced filesystem used by Mac OS X | 
| ISO-9660 | -t iso9660 | CD/DVD ROM/R/RW disks | ISO-9660 is the standard filesystem for optical disks. It's used by CD and DVD drives (but not audio CDs). | 

There are many, many more formats supported by Linux. In fact, Linux supports more different formats out of the box than any other operating system. That makes Linux an excellent choice for data recovery and digital forensics.

## Block Devices 

A block device is a Linux device that is capable of holding a filesystem. Block devices get their name because they are devices where Linux is only allowed to read or write a block of data, rather than single bytes. The size of the block depends on the device but, for disks, is usually about 4k bytes of data. Block devices (like all devices) are found in the `/dev` directory. You can use `find` to find all of the block devices in /dev:

```bash
$ ls -l $(find /dev -type b)
brw-rw---- 1 root disk   7,  0 Feb 20 00:02 /dev/loop0
brw-rw---- 1 root disk   7,  1 Feb 20 00:02 /dev/loop1
brw-rw---- 1 root disk   7,  2 Feb 20 00:02 /dev/loop2
brw-rw---- 1 root disk   7,  3 Feb 20 00:02 /dev/loop3
brw-rw---- 1 root disk   7,  4 Feb 20 00:02 /dev/loop4
brw-rw---- 1 root disk   7,  5 Feb 20 00:02 /dev/loop5
brw-rw---- 1 root disk   7,  6 Feb 20 00:02 /dev/loop6
brw-rw---- 1 root disk   7,  7 Feb 20 00:02 /dev/loop7
brw-rw---- 1 root disk   8,  0 Feb 20 00:02 /dev/sda
brw-rw---- 1 root disk   8,  1 Feb 20 00:02 /dev/sda1
brw-rw---- 1 root disk   8, 16 Feb 20 00:02 /dev/sdb
brw-rw---- 1 root disk   8, 32 Feb 20 00:02 /dev/sdc
brw-rw---- 1 root disk   8, 48 Feb 20 00:02 /dev/sdd
brw-rw---- 1 root disk   8, 64 Feb 20 00:02 /dev/sde
brw-rw---- 1 root disk   8, 80 Feb 20 00:02 /dev/sdf
brw-rw---- 1 root cdrom 11,  0 Feb 20 00:02 /dev/sr0
```

Notice that each of the block devices has a "b" as the first character of ls's output. The block devices that begin with `sd` are the SCSI and SATA disks in the machine. In the case of your VM they are emulated SATA. Lettering is how you tell what disk is what:
 
  - `sda` - The first disk drive. 
  - `sdb` - The second disk drive. 
  - `sdc` - The third, etc.
  
If the disk is partitioned there will also be numbers. In the case of `/dev/sda` there's just one partition. 

  - `sda` - The first disk drive (the whole disk)
  - `sda1` - The first partition of `/dev/sda`
  - `sda2` - The second partition of `/dev/sda`

The loop devices work a bit differently. More on that later... 

## Formatting Block Devices 

Before you can mount a block device it must be formatted with a particular *filesystem*. Different filesystems have different uses and properties. The `ext4` filesystem is Linux's native filesystem type. In this step we'll format `/dev/sdc`. 

```
$ sudo mkfs -t ext4 /dev/sdc
mke2fs 1.42.13 (17-May-2015)
Creating filesystem with 262144 4k blocks and 65536 inodes
Filesystem UUID: a82c3899-de96-4bae-872b-1fdd983f4b4a
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```

The format process is quick, it only writes the data structures needed to access the disk. The first few blocks of the disk contains a data structure called the superblock. The superblock tells Linux what kind of filesystem is in the block device. Use the hexdump command to look at the contents of the superblock:

```
$ sudo hexdump -n 2048 -C /dev/sdc 
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000400  00 00 01 00 00 00 04 00  33 33 00 00 a5 ce 03 00  |........33......|
00000410  f5 ff 00 00 00 00 00 00  02 00 00 00 02 00 00 00  |................|
00000420  00 80 00 00 00 80 00 00  00 20 00 00 00 00 00 00  |......... ......|
00000430  1f 9d 6c 5c 00 00 ff ff  53 ef 01 00 01 00 00 00  |..l\....S.......|
00000440  1f 9d 6c 5c 00 00 00 00  00 00 00 00 01 00 00 00  |..l\............|
00000450  00 00 00 00 0b 00 00 00  00 01 00 00 3c 00 00 00  |............<...|
00000460  42 02 00 00 7b 00 00 00  a8 2c 38 99 de 96 4b ae  |B...{....,8...K.|
00000470  87 2b 1f dd 98 3f 4b 4a  00 00 00 00 00 00 00 00  |.+...?KJ........|
00000480  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
000004c0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 3f 00  |..............?.|
000004d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000004e0  08 00 00 00 00 00 00 00  00 00 00 00 ba fe 41 f8  |..............A.|
000004f0  8a 4d 40 c6 bb 6e e5 01  df 42 d5 a4 01 01 00 00  |.M@..n...B......|
00000500  0c 00 00 00 00 00 00 00  1f 9d 6c 5c 0a f3 01 00  |..........l\....|
00000510  04 00 00 00 00 00 00 00  00 00 00 00 00 20 00 00  |............. ..|
00000520  00 00 02 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000530  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000540  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 02  |................|
00000550  00 00 00 00 00 00 00 00  00 00 00 00 1c 00 1c 00  |................|
00000560  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000570  00 00 00 00 04 00 00 00  81 81 00 00 00 00 00 00  |................|
00000580  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000800
```

Hexdump can look at files too. You may need to install software to format your disk. To see what mkfs commands you have installed run this command:

```
$ ls /sbin/mkfs* 
/sbin/mkfs         /sbin/mkfs.ext3     /sbin/mkfs.minix  /sbin/mkfs.xfs
/sbin/mkfs.bfs     /sbin/mkfs.ext4     /sbin/mkfs.msdos
/sbin/mkfs.cramfs  /sbin/mkfs.ext4dev  /sbin/mkfs.ntfs
/sbin/mkfs.ext2    /sbin/mkfs.fat      /sbin/mkfs.vfat
```

If you are missing some formats you can install them with the following commands:

```
$ sudo apt-get install btrfs-tools
$ sudo apt-get install ntfs-3g
$ sudo apt-get install hfsutils hfsplus
```

Try creating a different format (like `vfat`, `btrfs` or `ntfs`), then look at the superblock.

## Mounting Filesystems with mount 

Formatting a block device places an empty filesystem on the device. An empty filesystem contains only a root directory (if it's an `ext` filesystem it also contains a directory called lost+found/). In order to access the storage on the block device you must mount it into the logical file tree. That's the job of the mount command. The mount command takes at least two arguments:

```
$ mount <what-to-mount:block-device> <where-to-mount-it:directory>
```

What to mount is a block device. The block device must contain a valid format. Usually mount is able to guess the format from looking at the superblock. In come cases it can't so you'll have to tell mount what format to use:

```
$ mount -t <filesystem-type> <what> <where>
```

Where to mount is where you want to place the block device into the logical file tree. The files and directories inside of the block device become accessible starting in the directory where you mount them. Mount the loopback device from the previous steps with the command:

```
$ sudo mount /dev/sdc /mnt
```

The `/mnt` directory is not special. It's a useful place to mount temporary filesystems. You can mount your filesystem anywhere. However, if you mount your filesystem "over" a directory that's already in use you may cause the system to become unstable. Consider this:

```
# don't do this!!!
$ sudo mount /dev/loop0 /bin
```

That command places the contents of your empty loop device in the place of `/bin`. The original contents of `/bin` are not lost but you can no longer access them. That's a big problem because you won't be able to run `mount` (or `umount`) anymore. The only way out of the hole you just made is to reboot.

### Making Mounts Permanent 

The mount command only affects the in-memory state of Linux. If you reboot any changes you've made will be lost unless you save them into `/etc/fstab` file. The `/etc/fstab` (filesystem table) file is read at system boot time. Every line in the file tells Linux what to mount. The format of the file is:

```
<file system> <mount point> <type> <options> <dump> <pass>
```

The first four fields become options to mount. If your `/etc/fstab` file contained the following line:

```
/dev/sdc /mnt ext4 ro 0 0
```

The mount command that runs at startup would be:

```
$ mount -t ext4 -o ro /dev/loop0 /mnt
```

The `-o` argument is for adding options to the mount. Different filesystems use different options. The `ro` option specified here means Read-Only. The `<dump>` and `<pass>` fields control backups and filesystem checks respectively. They are mostly there for historical reasons. It's safe to leave them both 0. Here's what Ubuntu's default `/etc/fstab` looks like:

```
LABEL=cloudimg-rootfs	/	 ext4	defaults	0 0
```

Notice the `LABEL=cloudimg-rootfs` field? That tells mount to use the `blkid` command to identify which physical device to use. Run the `blkid` command and take a look at the output: 

```
$ sudo blkid
/dev/sda1: LABEL="cloudimg-rootfs" UUID="fda3418f-b78f-47d3-aef8-ab2b203a09c3" TYPE="ext4" PARTUUID="bb816946-01"
/dev/sdb: UUID="2019-01-15-08-28-59-00" LABEL="cidata" TYPE="iso9660"
/dev/sdc: UUID="a82c3899-de96-4bae-872b-1fdd983f4b4a" TYPE="ext4"
```

The `mount` command is able to deduce /dev/sda1 based on the label from `blkid`. It's also possible to add a `UUID=XXX` option in `/etc/fstab`. Every filesystem gets a unique ID when it's formatted. That line specifies a filesystem by it's ID rather than the device it's on. Linux can find that filesystem even after you've moved disks around. It prevents a common cause of an unbootable system.

### Knowing What's Mounted 

The `mount` command will tell you what filesystems are currently mounted:

```
$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=498868k,nr_inodes=124717,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=101584k,mode=755)
/dev/sda1 on / type ext4 (rw,relatime,data=ordered)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
cgroup on /sys/fs/cgroup/net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls,net_prio)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,pids)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpu,cpuacct)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=27,pgrp=1,timeout=0,minproto=5,maxproto=5,direct)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime)
mqueue on /dev/mqueue type mqueue (rw,relatime)
debugfs on /sys/kernel/debug type debugfs (rw,relatime)
fusectl on /sys/fs/fuse/connections type fusectl (rw,relatime)
lxcfs on /var/lib/lxcfs type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
vagrant on /vagrant type vboxsf (rw,nodev,relatime)
tmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,size=101584k,mode=700,uid=1000,gid=1000)
/dev/sdc on /mnt type ext4 (rw,relatime,data=ordered)
```

That's a lot more than what's in `/etc/fstab`! I'll explain the results in groups. Most of the mounts you see are not physical devices. They're virtual devices that contain files.

### Physical Devices

These are the devices that correspond to the ones in `/etc/fstab`

```
$ mount | grep /dev/sd
/dev/sda1 on / type ext4 (rw,relatime,data=ordered)
/dev/sdc on /mnt type ext4 (rw,relatime,data=ordered)
```

### Special filesystems 

Special filesystems provide a method for communication with the kernel. These filesystems contain files that are a way for user programs to change and view operating system settings and status. Each type has one has it's own use.

```
proc on /proc type proc (rw,noexec,nosuid,nodev)
sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
udev on /dev type devtmpfs (rw,mode=0755)
devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=0620)
```

Using files and directories as a mechanism to work with the Linux kernel has gained in popularity, causing a large increase in the number of mounted virtual filesystems. When kernel controls and information are available as files it gives programmers a very simple and understandable way to read and alter them. The most complicated configuration tasks can easily be done with a BASH script.

### Temporary Filesystems

The tempfs filesystem is an in-memory filesystem or ramdisk.

```
none on /sys/fs/cgroup type tmpfs (rw)
tmpfs on /run type tmpfs (rw,noexec,nosuid,size=10%,mode=0755)
none on /run/lock type tmpfs (rw,noexec,nosuid,nodev,size=5242880)
none on /run/shm type tmpfs (rw,nosuid,nodev)
none on /run/user type tmpfs (rw,noexec,nosuid,nodev,size=104857600,mode=0755)
```

## Unmount 

The `umount` command unmounts a filesystem. Filesystems can only be unmounted when no program is using any of the files in the filesystem. This includes having the filesystem as a working directory. The ``umount`` command takes either a device or a path as its argument.

```
umount <device>
umount <mountpoint>
```

Therefore you can say either:

```
$ sudo umount /dev/sdc
$ sudo umount /mnt
```

Not both! Linux will refuse to unmount a filesystem that is in use because doing so would cause programs to crash. If your working directory is in your device mount will fail because cd-ing into the device counts as use. 

## Creating a Block Device with losetup 

If you want to practice formatting, mounting and unmounting disks on a physical machine and you don't have hard drives to spare you can create virtual block devices using the ``losetup``command. The ``losetup`` command creates a block device inside of a file. The file can be located anywhere. If you plan on using virtualization ``losetup`` is an extremely handy utility. In order to use it you must first have a file. The ``dd`` command is like the ``cp`` command but it gives you precise control over how data is copied. The following ``dd`` command creates a 10M byte file called ``disk.img``

```
$ dd if=/dev/zero of=disk.img bs=1M count=10
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0113908 s, 921 MB/s
$ ls -la disk.img
-rw-rw-r-- 1 vagrant vagrant 10485760 Feb 20 00:38 disk.img
```

Here's a quick explanation of what dd just did:
  * ``if=/dev/zero``: The ``if`` argument is "input file" this reads data from the file /dev/zero, a special device that's always reads zeros.
  * ``of=disk.img``: The ``of`` argument is "output file" this writes to our file disk.img
  * ``bs=1M``: The bs argument is "block size". Block size is the number of bytes copied in each copy operation.
  * ``count=10``: The count argument is how many copy operations to perform. The amount of data copied will be (``bs * count``)

Now you use losetup to bind that file to the block device ``/dev/loop0``:

```
$ sudo losetup /dev/loop0 disk.img 
$ sudo losetup 
NAME       SIZELIMIT OFFSET AUTOCLEAR RO BACK-FILE
/dev/loop0         0      0         0  0 /home/vagrant/disk.img
```

If you've done the `losetup` correctly running it with no arguments shows you what file is bound to the loop device. Otherwise the output will be empty. The loopback devices are special devices that can only be used with losetup. If you look at the contents of the ``/dev`` directory above you can see the loopback devices in there. They are ``/dev/loop*``.

```
$ ls -l /dev/loop*
total 0
brw-rw---- 1 root disk 7, 0 Sep 10 09:22 loop0
brw-rw---- 1 root disk 7, 1 Sep 10 09:22 loop1
brw-rw---- 1 root disk 7, 2 Sep 10 09:22 loop2
brw-rw---- 1 root disk 7, 3 Sep 10 09:22 loop3
brw-rw---- 1 root disk 7, 4 Sep 10 09:22 loop4
brw-rw---- 1 root disk 7, 5 Sep 10 09:22 loop5
brw-rw---- 1 root disk 7, 6 Sep 10 09:22 loop6
brw-rw---- 1 root disk 7, 7 Sep 10 09:22 loop7
```

Once bound to a file `/dev/loop0` works just like a disk! You can format it an mount it. 