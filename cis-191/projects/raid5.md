# RAID Project 

In this project you'll create a RAID array with two disks on your Vagrant VM. The you'll partition, format and mount it. You'll move the `/var/www` mount point onto a RAID disk. With your web content on RAID storage your webserver can suffer a disk failure without going down.

## Create The RAID5 Array 

In class you created a RAID array in the lab. Start with a fresh Vagrant VM. 

```
$ vagrant destroy 
$ vagrant up 
```

Create a RAID5 array on the `/dev/md0` device. The array should have the following properties: 

  - RAID Level: 5
  - Disks (3)
    - `/dev/sdc`
    - `/dev/sdd`
    - `/dev/sde`
  - Spares (1) 
    - `/dev/sdf`
  - Filesystem: `ext4`
    - Label: `www-raid`
  - Mount point: `/var/www`

Format and mount the RAID device. If you do it correctly you should be able to verify that your RAID is working using the command:

```
$ sudo mdadm --detail /dev/md0 
/dev/md0:
        Version : 1.2
  Creation Time : Thu Mar  7 16:09:07 2019
     Raid Level : raid5
     Array Size : 2095104 (2046.34 MiB 2145.39 MB)
  Used Dev Size : 1047552 (1023.17 MiB 1072.69 MB)
   Raid Devices : 3
  Total Devices : 4
    Persistence : Superblock is persistent

    Update Time : Thu Mar  7 16:09:12 2019
          State : clean 
 Active Devices : 3
Working Devices : 4
 Failed Devices : 0
  Spare Devices : 1

         Layout : left-symmetric
     Chunk Size : 512K

           Name : ubuntu-xenial:0  (local to host ubuntu-xenial)
           UUID : 773813cf:e8d83d92:a510ac37:cb96dc60
         Events : 18

    Number   Major   Minor   RaidDevice State
       0       8       32        0      active sync   /dev/sdc
       1       8       48        1      active sync   /dev/sdd
       4       8       64        2      active sync   /dev/sde

       3       8       80        -      spare   /dev/sdf
```

> Verify that you have three disks and a spare!


## Verify Mount and Space

You should have your RAID volume mounted on `/var/www`. Check the available space in the volume using the `df` command. Answer the following questions: 

  1. How much space is available in `/var/www`
  
## Degrade Your Array 

Use the `mdadm` command to mark `/dev/sdd` as failed. This causes Linux to use the spare so that you don't lose data. Check the manual page for how to mark a disk as failed. If you do it correctly the output of `mdadm` should look like this:

```
$ sudo mdadm --detail /dev/md0 
/dev/md0:
        Version : 1.2
  Creation Time : Thu Mar  7 16:09:07 2019
     Raid Level : raid5
     Array Size : 2095104 (2046.34 MiB 2145.39 MB)
  Used Dev Size : 1047552 (1023.17 MiB 1072.69 MB)
   Raid Devices : 3
  Total Devices : 4
    Persistence : Superblock is persistent

    Update Time : Thu Mar  7 16:20:13 2019
          State : clean 
 Active Devices : 3
Working Devices : 3
 Failed Devices : 1
  Spare Devices : 0

         Layout : left-symmetric
     Chunk Size : 512K

           Name : ubuntu-xenial:0  (local to host ubuntu-xenial)
           UUID : 773813cf:e8d83d92:a510ac37:cb96dc60
         Events : 37

    Number   Major   Minor   RaidDevice State
       0       8       32        0      active sync   /dev/sdc
       3       8       80        1      active sync   /dev/sdf
       4       8       64        2      active sync   /dev/sde

       1       8       48        -      faulty   /dev/sdd
```

Save your "failed" output with the command:

```
$ sudo mdadm --detail /dev/md0 > /vagrant/failed_array.txt
```

Check `/var/www`. The files should still be there and accessible. RAID really works! Now fix your broken array by:

  1. Removing the device you marked as faulty (`/dev/sdd`)
  2. Re-adding the device back into the array

Once you re-add the device the array will start rebuilding. This will take some time. During the rebuilding time the output of `mdadm` should look like this:

```
$ sudo mdadm --detail /dev/md0 
/dev/md0:
        Version : 1.2
  Creation Time : Thu Mar  7 16:09:07 2019
     Raid Level : raid5
     Array Size : 2095104 (2046.34 MiB 2145.39 MB)
  Used Dev Size : 1047552 (1023.17 MiB 1072.69 MB)
   Raid Devices : 3
  Total Devices : 4
    Persistence : Superblock is persistent

    Update Time : Thu Mar  7 16:22:55 2019
          State : clean 
 Active Devices : 3
Working Devices : 4
 Failed Devices : 0
  Spare Devices : 1

         Layout : left-symmetric
     Chunk Size : 512K

           Name : ubuntu-xenial:0  (local to host ubuntu-xenial)
           UUID : 773813cf:e8d83d92:a510ac37:cb96dc60
         Events : 39

    Number   Major   Minor   RaidDevice State
       0       8       32        0      active sync   /dev/sdc
       3       8       80        1      active sync   /dev/sdf
       4       8       64        2      active sync   /dev/sde

       5       8       48        -      spare   /dev/sdd
```

Save the output of this command:

```
$ sudo mdadm --detail /dev/md0 > /vagrant/rebuilding_array.txt
```

Submit your outputs for the project.

## Turn In 

Run the commands: 

```
$ sudo blkid > /vagrant/blkid.txt
```

Turn in the following files: 

  - `/vagrant/failed_array.txt`
  - `/vagrant/rebuilding_array.txt`
  - `/vagrant/blkid.txt`
  - `/etc/fstab`

Submit your files on Canvas.