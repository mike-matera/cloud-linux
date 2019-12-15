# Partitions, Filesystems and Mount 

In this project you'll use the standard VM to partition extra disks. You should start with a fresh VM, instead of the one you used last week. To remove and re-provision your VM run the commands:

```bash
$ vagrant destroy
$ vagrant up
```

## Partitioning with Parted 

Check the additional disks on your VM:

```
$ ls -la /dev/sd?
brw-rw---- 1 root disk 8,  0 Feb 28 16:38 /dev/sda
brw-rw---- 1 root disk 8, 16 Feb 28 16:38 /dev/sdb
brw-rw---- 1 root disk 8, 32 Feb 28 16:38 /dev/sdc
brw-rw---- 1 root disk 8, 48 Feb 28 16:38 /dev/sdd
brw-rw---- 1 root disk 8, 64 Feb 28 16:38 /dev/sde
brw-rw---- 1 root disk 8, 80 Feb 28 16:38 /dev/sdf
```

This week you will partition `/dev/sdc` and `/dev/sdd` and use their storage. Start GNU parted to partition the disk. Be careful with parted, mistakes made here may destroy your VM.

Use the parted commands you learned in class to perform the following tasks:

 * Partition `/dev/sdc`
   * Create a GPT disk label
   * Make a partition with the following attributes:
     * Name: data1
     * Type: ext4 
     * Start: 1MB
     * End: 1024MB 
 * Partition `/dev/sdd`
   * Create a MSDOS disk label
   * Make a partition with the following attributes:
     * Type: primary
     * Type: btrfs
     * Start: 1MB
     * End: 1024MB 

Verify your partitioning by using `parted` from the command line: 

```bash 
$ sudo parted /dev/sdc print free 
Model: VBOX HARDDISK (scsi)
Disk /dev/sdc: 1074MB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name   Flags
        17.4kB  1049kB  1031kB  Free Space
 1      1049kB  1024MB  1023MB               data1
        1024MB  1074MB  49.3MB  Free Space
```

Check both disks:

```bash
vagrant@ubuntu-xenial:~$ sudo parted /dev/sdd print free 
Model: VBOX HARDDISK (scsi)
Disk /dev/sdd: 1074MB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags: 

Number  Start   End     Size    Type     File system  Flags
        32.3kB  1049kB  1016kB           Free Space
 1      1049kB  1024MB  1023MB  primary
        1024MB  1074MB  49.3MB           Free Space
```

## Create and Mount Fileystems

If you have successfully partitioned `/dev/sdc` and `/dev/sdd` you should now see partition numbers when you use ls in the /dev directory:

```
$ ls -la /dev/sdc? /dev/sdd?
brw-rw---- 1 root disk 8, 33 Feb 28 16:47 /dev/sdc1
brw-rw---- 1 root disk 8, 49 Feb 28 16:47 /dev/sdd1
```

The partitions are freshly created and contain no filesystem. The next task is to format the filesystems. Create filesystems on `/dev/sdc` and `/dev/sdd1` with the following specifications:

  * `/dev/sdc1`
    * `ext4` filesystem
    * Volume label: home-data
  * `/dev/sdd1`
    * `btrfs` filesystem
    * Volume label: web-data

Verify that you have correctly formatted your two partitions using the commands:

```
dumpe2fs
```

This command shows you ext2/3/4 parameters.

```
btrfs filesystem show
```

The commands will also show you the UUID of each filesystem. Make a note of the UUIDs, you will need them in a subsequent step.

## Mount Your New Filesystems 

Mount your new filesystems into the locations: 

  * `/dev/sdc1` (home-data) onto `/home`
  * `/dev/sdd1` (web-data) onto `/var/www` 
  
> You must move data like you did in last week's project!

## Make your Changes Permanent 

Update `/etc/fstab` to make your changes permanent, like you did last week. The easiest way to do this is using the label you created. For example, this adds the `/var/www` partition: 

```
LABEL=home-data /home ext4 defaults 0 0 
```

## Reboot and Verify 

Reboot your VM using Vagrant:

```
$ vagrant halt
$ vagrant up 
```

Verify that your mounts are in place using the `df` command.

## Turn In 

When your machine is rebooted and working run the following commands:

```
$ mount > /vagrant/mounts.txt
$ sudo parted /dev/sdc print free > /vagrant/parted-sdc.txt
$ sudo parted /dev/sdd print free > /vagrant/parted-sdd.txt
```

Turn in the files:

  * `mounts.txt`
  * `parted-sdc.txt`
  * `parted-sds.txt`
  * `/etc/fstab`

Submit your files on Canvas.
