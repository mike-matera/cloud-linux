Logical Volume Management is a system in Linux that allows administrators to use cutting-edge technology to manage disks. Unlike partitioning, which splits up storage, LVM brings multiple disks together to form flexible filesystems with advanced features.

The lecture slides are [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1I4kyMxPvxxV5tUbKZPU_rQgn5WyJIdly-E8jOd2TXpE/edit?usp=sharing).

### Commands 

  * pvcreate / pvremove / pvdisplay
  * vgcreate / vgremove / vgdisplay
  * lvcreate / lvremove / lvdisplay

### Configuration

  * None

### Further Reading

  * [LVM on the Ubuntu Wiki](https://wiki.ubuntu.com/Lvm)
  * [The Official LVM HowTo](http://tldp.org/HOWTO/LVM-HOWTO/)

## Introduction 

Modern Linux systems need flexible storage, not just disks. The Logical Volume Manager organizes the storage on individual disks into larger pools that can be allocated to filesystems. Unlike partitioning the allocation can change while the system is running. This is a huge benefit to the administrator because mistakes can be fixed after the system is in production. Here's a few things you can do using LVM:

  * Increase the size of a filesystem that needs more space.
  * Reduce the size of a filesystem to make space available.
  * Transparently migrate a filesystem from one disk to another while the system is running.
  * Make redundant filesystems using RAID.
  * Create snapshots of filesystems.

## Making a Disk Ready for LVM 

LVM can work on disk partitions or whole disks. By default when Ubuntu installs it creates a partition (on your VMs `/dev/sda5`) for LVM. This is because the boot disk needs to have other partitions in order for GRUB to work. If you have a computer with disks dedicated to file service those disks don't need to be partitioned, they can be turned into an LVM disk. When a partition or disk is used for LVM it becomes a physical volume. Managing physical volumes is done with pvcreate and pvremove. Here's how to partition a disk and create a physical volume in the first partition:

> **Warning!** This will destroy ALL DATA on /dev/sdb

```
$ sudo parted /dev/sdb mklabel gpt
$ sudo parted /dev/sdb mkpart LVMPartition 0% 100%
$ sudo parted /dev/sdb set 1 lvm on
$ sudo
pvcreate /dev/sdb1
 Physical volume "/dev/sdb1" successfully created
```

Now let's look at the volume we just created:

```
$ sudo pvdisplay /dev/sdb1
 "/dev/sdb1" is a new physical volume of "20.00 GiB"
 --- NEW Physical volume ---
 PV Name        /dev/sdb1
 VG Name       
 PV Size        20.00 GiB
 Allocatable      NO
 PE Size        0 
 Total PE       0
 Free PE        0
 Allocated PE     0
 PV UUID        ysQF8n-9ig0-Ckkc-HjY2-C4KJ-rzUM-OCoKMk
```

The volume is a "new" volume because it is not yet a part of a volume group. A physical volume can't be used until it joins a group. If a whole disk is to work with LVM it's better not to partition it. Instead, you can add the entire device as a physical volume. In order to do that we have to first delete `/dev/sdb1` from LVM:

```
$ sudo pvremove /dev/sdb1
Labels on physical volume "/dev/sdb1" successfully wiped
```

Now let's delete the existing partitions:

```
$ sudo parted /dev/sdb rm 1
Information: You may need to update /etc/fstab.
```

However, we can't yet create a physical volume on `/dev/sdb`. If you try to do so you will encounter this error message:

```
$ sudo pvcreate /dev/sdb
Device /dev/sdb not found (or ignored by filtering).
```

LVM is trying to save you from a terrible mistake. It noticed that there's a partition table on the disk and won't act because it thinks there's a good chance it will wipe out a lot of data. If this happens you can use dd to blank the partition then create a physical volume on `/dev/sdb`:

```
$ sudo dd if=/dev/zero of=/dev/sdb bs=1M count=1
1+0 records in
1+0 records out
1048576 bytes (1.0 MB) copied, 0.00359189 s, 292 MB/s
$ sudo 
pvcreate /dev/sdb
 Physical volume "/dev/sdb" successfully created
```

Now you have disk space to work with.

## Creating a Volume Group

Volume groups are pools of data that you can allocate for filesystems. Since you have /dev/sdb available you can now add it to an existing volume group or create a new volume group to use:

```
$ sudovgcreate MyNewGroup /dev/sdb
Volume group "MyNewGroup" successfully created
```

Let's look closely at what we've just done:

```
$ sudo vgdisplay -v MyNewGroup
  Using volume group(s) on command line
  Finding volume group "MyNewGroup"
 --- Volume group ---
 VG Name        MyNewGroup
 System ID      
 Format        lvm2
 Metadata Areas    1
 Metadata Sequence No 1
 VG Access       read/write
 VG Status       resizable
 MAX LV        0
 Cur LV        0
 Open LV        0
 Max PV        0
 Cur PV        1
 Act PV        1
 VG Size        20.00 GiB
 PE Size        4.00 MiB
 Total PE       5119
 Alloc PE / Size    0 / 0 
 Free PE / Size    5119 / 20.00 GiB
 VG UUID        nvZUT2-dTtQ-OyaM-Rfp9-y2Ur-hldi-lIGsUF
 
 --- Physical volumes ---
 PV Name        /dev/sdb  
 PV UUID        YSHIFK-C5DT-aY5q-qjYC-wcy3-h6GL-xKQpay
 PV Status       allocatable
 Total PE / Free PE  5119 / 5119
```

The volume group contains the physical volume `/dev/sdb`. Notice the VG Size is 20G. That's a useful number but the more important one is Total PE. PE is short for Physical Extent. In LVM space is divided into extents. The size of a physical extent is 4.00 MiB. The next step is to allocate physical extents to logical volumes.

## Creating Logical Volumes 

Filesystems can only exist inside of logical volumes. Logical volumes come into existence when we allocate space out of a volume group for that logical volume. There are different types of LVs that have interesting properties. Let's create a simple logical volume with the space we have from `/dev/sdb`.

```
$ sudo lvcreate -n MyLogVol -l 5119 MyNewGroup
Logical volume "MyLogVol" created
```

Notice that we specified the number of extents to use with the `-l 5119` argument. That was the entire number of free extents. 

Let's see what we've done:

```
$ sudo vgdisplay -v MyNewGroup
  Using volume group(s) on command line
  Finding volume group "MyNewGroup"
 --- Volume group ---
 VG Name        MyNewGroup
 System ID      
 Format        lvm2
 Metadata Areas    1
 Metadata Sequence No 2
 VG Access       read/write
 VG Status       resizable
 MAX LV        0
 Cur LV        1
 Open LV        0
 Max PV        0
 Cur PV        1
 Act PV        1
 VG Size        20.00 GiB
 PE Size        4.00 MiB
 Total PE       5119
 Alloc PE / Size    5119 / 20.00 GiB
 Free PE / Size    0 / 0 
 VG UUID        nvZUT2-dTtQ-OyaM-Rfp9-y2Ur-hldi-lIGsUF
 
 --- Logical volume ---
 LV Path        /dev/MyNewGroup/MyLogVol
 LV Name        MyLogVol
 VG Name        MyNewGroup
 LV UUID        dxTI2H-NFs3-KuCY-pztX-club-rJDz-G3FDyk
 LV Write Access    read/write
 LV Creation host, time ubuntu, 2015-10-08 11:57:05 -0700
 LV Status       available
 # open         0
 LV Size        20.00 GiB
 Current LE       5119
 Segments        1
 Allocation       inherit
 Read ahead sectors   auto
 - currently set to   256
 Block device      252:2
 
 --- Physical volumes ---
 PV Name        /dev/sdb  
 PV UUID        YSHIFK-C5DT-aY5q-qjYC-wcy3-h6GL-xKQpay
 PV Status       allocatable
 Total PE / Free PE  5119 / 0
```

One important thing to notice is that the logical volume has a path (`/dev/MyNewGroup/MyLogVol`). Let's look at that path:

```
$ ls -l /dev/MyNewGroup
total 0
lrwxrwxrwx 1 root root 7 Oct 8 11:57 MyLogVol -> ../dm-2
$ ls -l /dev/dm-2
brw-rw---- 1 root disk 252, 2 Oct 8 11:57 /dev/dm-2
```

The device `/dev/dm-2` is a block device! We can format it an place a filesystem on it:

```
$ sudo mkfs.ext4 /dev/MyNewGroup/MyLogVol
mke2fs 1.42.9 (4-Feb-2014)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
1310720 inodes, 5241856 blocks
262092 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=4294967296
160 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
4096000
Allocating group tables: done              
Writing inode tables: done              
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done 
$ sudo mount /dev/MyNewGroup/MyLogVol /mnt
$ ls /mnt/
lost+found
```

## Undoing It All 

Normally you won't need to delete things often, however in class you will try different storage arrangement. To undo what you've changed in this tutorial you must first unmount the filesystem that you made:

```
$ sudo umount /dev/MyNewGroup/MyLogVol
```

Next you delete the logical volume you created:

```
$ sudo lvremove /dev/MyNewGroup/MyLogVol
Do you really want to remove and DISCARD active logical volume MyLogVol? [y/n]: y
Logical volume "MyLogVol" successfully removed
```

Now you delete the volume group:

```
$ sudo vgremove MyNewGroup
Volume group "MyNewGroup" successfully removed
```

Finally you erase the logical volume information on your disk:

```
$ sudo pvremove /dev/sdb
Labels on physical volume "/dev/sdb" successfully wiped
```
