# Lab: Create a Simple Logical Volume 

In this lab you'll use the volume group you created in the lab [Create a Volume Group](create_volume_group.md). You will create a simple logical volume using the volume group. 

## Step 1: Create the Logical Volume 

Check the existing logical volumes: 

```bash
$ sudo lvdisplay 
```

There shhould be no output. Create the logical volume called `simple_volume`:

```bash
$ sudo lvcreate -n simple_volume -l 100%FREE my_vg 
  Logical volume "simple_volume" created.
```

Now verify that the volume exists: 

```bash
$ sudo lvdisplay 
  --- Logical volume ---
  LV Path                /dev/my_vg/simple_volume
  LV Name                simple_volume
  VG Name                my_vg
  LV UUID                TZd16o-q0Be-JaRr-g0ER-F6EP-PZAu-N0Sjty
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 14:42:35 +0000
  LV Status              available
  # open                 0
  LV Size                3.98 GiB
  Current LE             1020
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
Creating filesystem with 1044480 4k blocks and 261120 inodes
Filesystem UUID: 6b368763-9844-4043-bf81-0676b2936eb7
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 
```

## Step 3: Mount the new Volume 

Mount the new filesystem on `/mnt`:

```bash
$ sudo mount /dev/my_vg/simple_volume /mnt 
```

Check the available space on the device:

```
$ df /mnt/
Filesystem                      1K-blocks  Used Available Use% Mounted on
/dev/mapper/my_vg-simple_volume   4046784  8152   3813352   1% /mnt
```

Check the block devices:

```bash
$ sudo blkid
/dev/sda1: LABEL="cloudimg-rootfs" UUID="6c93f311-22e6-4c56-835f-64f7e6ecf75f" TYPE="ext4" PARTUUID="b9390537-01"
/dev/sdb: UUID="2019-02-04-14-26-04-00" LABEL="cidata" TYPE="iso9660"
/dev/sdc: UUID="JdwVUW-dnmv-YWKj-hdA8-Uhro-AyVY-m7j552" TYPE="LVM2_member"
/dev/sdd: UUID="6wh271-0heU-J92n-yKot-TR0q-IBGU-9Yyshs" TYPE="LVM2_member"
/dev/sde: UUID="aK5O9m-g6g5-KwXG-1kju-bEAY-gisb-TLe2Bz" TYPE="LVM2_member"
/dev/mapper/my_vg-simple_volume: UUID="6b368763-9844-4043-bf81-0676b2936eb7" TYPE="ext4"
/dev/sdf: UUID="n1731Z-VbIM-hYbm-6lui-bzsv-u91a-aUf2WX" TYPE="LVM2_member"
```

## Turn In 

Run the following commands to create output files: 

```bash
$ sudo lvdisplay > /vagrant/simple_volume.txt 
```

Turn in the following files:

  1. `simple_volume.txt`
 