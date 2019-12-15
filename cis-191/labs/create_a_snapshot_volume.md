# Lab: Create a Snapshot Logical Volume 

In this lab you'll use the volume group you created in the lab [Create a Volume Group](create_volume_group.md). You will create a simple volume and an additional volume to make a snapshot of your simple volume. A snapshot is a picture of your simple volume taken at a moment in time. 

> If you have a LV from a previous lab you must delete it. 

## Step 0: Delete Existing Logical Volumes 

Before you start this lab either reset your Vagrant VM and redo the Create a Volume Group lab or delete existing logical volumes using the command: 

```bash
$ sudo lvremove <path_to_volume>
```

> NOTE: You cannot remove a volume if it's mounted. 

## Step 1: Create the Logical Volume 

Check the existing logical volumes: 

```bash
$ sudo lvdisplay 
```

There shhould be no output. Create the logical volume called `simple_volume`:

```bash
$ sudo lvcreate -n simple_volume -l 80%FREE my_vg
  Logical volume "simple_volume" created.
```

> Notice we only used 80% of free space in the volume group. The rest will be used for the snapshot. 

Now verify that the volume exists: 

```bash
$ sudo lvdisplay 
  --- Logical volume ---
  LV Path                /dev/my_vg/simple_volume
  LV Name                simple_volume
  VG Name                my_vg
  LV UUID                McI97f-qXB8-mK8h-ZDAC-PLOV-svAx-lRlFwe
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 15:14:27 +0000
  LV Status              available
  # open                 0
  LV Size                3.19 GiB
  Current LE             816
  Segments               4
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:0
```

Notice that you have the `/dev/my_vg/simple_volume` block device available. 

## Step 2: Format the New Device 

Create a new `ext4` filesystem on the new device:

```bash
$ sudo mkfs -t ext4 /dev/my_vg/simple_volume 
mke2fs 1.42.13 (17-May-2015)
Creating filesystem with 835584 4k blocks and 209248 inodes
Filesystem UUID: c8607072-2af9-4d56-b065-48523db1c99d
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 
```

## Step 3: Mount the new Volume 

Mount the new filesystem on `/mnt`:

```bash
$ sudo mkdir -p /mnt/source
$ sudo mount /dev/my_vg/simple_volume /mnt/source
```

Check the available space on the device:

```sql
$ df /mnt/source
Filesystem                      1K-blocks  Used Available Use% Mounted on
/dev/mapper/my_vg-simple_volume   3224224  5708   3035016   1% /mnt/source
```

## Step 4: Use the New Space 

In order for the snapshot to make sense you need to use some of the space in your simple volume. These commands download the source code for the Python programming language. 

```bash
$ sudo chown vagrant:vagrant /mnt/source
$ cd /mnt/source
$ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
$ tar -xvf Python-3.7.2.tar.xz 
```

The source code should be extracted into your `/mnt/source` directory. Check that it's there: 

```bash
$ ls -la /mnt/source/
total 16672
drwxr-xr-x  4 vagrant vagrant     4096 Mar 14 15:21 .
drwxr-xr-x  3 root    root        4096 Mar 14 15:16 ..
drwx------  2 root    root       16384 Mar 14 15:15 lost+found
drwxr-xr-x 18 vagrant vagrant     4096 Dec 24 03:41 Python-3.7.2
-rw-rw-r--  1 vagrant vagrant 17042320 Dec 24 03:42 Python-3.7.2.tar.xz
```

## Step 5: Create a Snapshot 

Use the following command to create your snapshot:

```bash
$ sudo lvcreate --snapshot -n snap -l 100%FREE /dev/my_vg/simple_volume 
  Logical volume "snap" created.
```

Now check your logical volumes:

```bash
$ sudo lvdisplay 
  --- Logical volume ---
  LV Path                /dev/my_vg/simple_volume
  LV Name                simple_volume
  VG Name                my_vg
  LV UUID                McI97f-qXB8-mK8h-ZDAC-PLOV-svAx-lRlFwe
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 15:14:27 +0000
  LV snapshot status     source of
                         snap [active]
  LV Status              available
  # open                 1
  LV Size                3.19 GiB
  Current LE             816
  Segments               4
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:0
   
  --- Logical volume ---
  LV Path                /dev/my_vg/snap
  LV Name                snap
  VG Name                my_vg
  LV UUID                Qz2Emf-Iwka-wnmO-LNYl-UHql-p1sA-9Ei63Q
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 15:24:54 +0000
  LV snapshot status     active destination for simple_volume
  LV Status              available
  # open                 0
  LV Size                3.19 GiB
  Current LE             816
  COW-table size         816.00 MiB
  COW-table LE           204
  Allocated to snapshot  0.00%
  Snapshot chunk size    4.00 KiB
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:3   
```

Now you have the device `/dev/my_vg/snap`. The device is a perfect snapshot of the `/dev/my_vg/simple_volume`. The snapshot doesn't need to be formatted, you can simply mount it. Snapshots are writable, but we'll mount it read-only. 

```bash
$ sudo mkdir -p /mnt/snapshot 
$ sudo mount -o ro /dev/my_vg/snap /mnt/snapshot 
```

Let's check the mounted volumes:

```bash
$ df 
Filesystem                      1K-blocks     Used Available Use% Mounted on
udev                               498880        0    498880   0% /dev
tmpfs                              101580     3148     98432   4% /run
/dev/sda1                        10098468   901496   9180588   9% /
tmpfs                              507880        0    507880   0% /dev/shm
tmpfs                                5120        0      5120   0% /run/lock
tmpfs                              507880        0    507880   0% /sys/fs/cgroup
vagrant                         489445384 91887040 397558344  19% /vagrant
tmpfs                              101580        0    101580   0% /run/user/1000
/dev/mapper/my_vg-simple_volume   3224224   109532   2931192   4% /mnt/source
/dev/mapper/my_vg-snap            3224224   109532   2931192   4% /mnt/snapshot
```

Notice the snapshot is the same as the source. Let's look inside the snapshot: 

```bash
$ ls -la /mnt/snapshot/
total 16672
drwxr-xr-x  4 vagrant vagrant     4096 Mar 14 15:21 .
drwxr-xr-x  4 root    root        4096 Mar 14 15:26 ..
drwx------  2 root    root       16384 Mar 14 15:15 lost+found
drwxr-xr-x 18 vagrant vagrant     4096 Dec 24 03:41 Python-3.7.2
-rw-rw-r--  1 vagrant vagrant 17042320 Dec 24 03:42 Python-3.7.2.tar.xz
```

It's magic! No, it's science! 

## Step 6: Change the Source Volume 

Suppose you accidentally delete files in the source volume. Oops!

```bash 
$ rm -rf /mnt/source/*
```

Now all your files are gone: 

```bash
$ ls -la /mnt/source/
total 8
drwxr-xr-x 2 vagrant vagrant 4096 Mar 14 15:29 .
drwxr-xr-x 4 root    root    4096 Mar 14 15:26 ..
```

Don't worry they're safe in the snapshot: 

```bash
$ ls -la /mnt/snapshot/
total 16672
drwxr-xr-x  4 vagrant vagrant     4096 Mar 14 15:21 .
drwxr-xr-x  4 root    root        4096 Mar 14 15:26 ..
drwx------  2 root    root       16384 Mar 14 15:15 lost+found
drwxr-xr-x 18 vagrant vagrant     4096 Dec 24 03:41 Python-3.7.2
-rw-rw-r--  1 vagrant vagrant 17042320 Dec 24 03:42 Python-3.7.2.tar.xz
```

Periodic snapshots are a way that you can give users access to "instant" backups when they accidentally remove files. 

## Turn In 

Run the following commands to create output files: 

```bash
$ sudo lvdisplay > /vagrant/snapshots.txt 
```

Turn in the following files:

  1. `snapshots.txt`
