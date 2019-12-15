# Lab: Create a RAID Logical Volume 

In this lab you'll use the volume group you created in the lab [Create a Volume Group](create_volume_group.md). You will create a RAID logical volume using the volume group. 

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
$ sudo lvcreate --type raid5 -i 3 -n raid_volume -l 100%FREE my_vg 
  Using default stripesize 64.00 KiB.
  Logical volume "raid_volume" created.
```

Now verify that the volume exists: 

```bash
$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/my_vg/raid_volume
  LV Name                raid_volume
  VG Name                my_vg
  LV UUID                Jxmj2v-S3d4-phf7-2WFD-Q8he-OkMq-NkxaB7
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 15:03:59 +0000
  LV Status              available
  # open                 0
  LV Size                2.98 GiB
  Current LE             762
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     1024
  Block device           252:8
```

Notice that you have the `/dev/my_vg/raid_volume` block device available. 

## Step 2: Format the New Device 

Create a new `ext4` filesystem on the new device:

```bash
$ sudo mkfs -t ext4 /dev/my_vg/raid_volume 
mke2fs 1.42.13 (17-May-2015)
Creating filesystem with 780288 4k blocks and 195072 inodes
Filesystem UUID: 247b81aa-9ddf-460e-90e0-abf3170ae02e
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 
```

## Step 3: Mount the new Volume 

Mount the new filesystem on `/mnt`:

```bash
$ sudo mount /dev/my_vg/raid_volume /mnt 
```

Check the available space on the device:

```sql
$ df /mnt/
Filesystem                    1K-blocks  Used Available Use% Mounted on
/dev/mapper/my_vg-raid_volume   3006608  4584   2829584   1% /mnt
```

## Turn In 

Run the following commands to create output files: 

```bash
$ sudo lvdisplay > /vagrant/raid_volume.txt 
```

Turn in the following files:

  1. `raid_volume.txt`
