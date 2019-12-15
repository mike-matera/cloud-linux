# Partitioning with GNU parted 

In this lab you'll use the standard VM to partition extra disks. You should start with a fresh VM, instead of the one you used last week. To remove and re-provision your VM run the commands:

```bash
$ vagrant destroy
$ vagrant up
```

## Step 1: Partition a Disk With GPT 

Start `parted` on `/dev/sdc`:

```bash 
$ sudo parted /dev/sdc 
```

Follow the class walkthrough do to the following: 

 * Create a GPT disk label
 * Make a partition with the following attributes:
   * Name: data1
   * Type: ext4 
   * Start: 1MB
   * End: 1024MB 

## Step 2: Format `/dev/sdc1`

Format the disk with the `mkfs` command:

```bash
$ sudo mkfs -t ext4 -L data1 /dev/sdc1 
```

Verify the format:

```bash
$ sudo dumpe2fs /dev/sdc1 
```

## Step 3: Mount `/dev/sdc1`

Mount the new disk on `/mnt`

```bash
$ sudo mount /dev/sdc1 /mnt 
```

Verify that it is mounted:

```bash
$ df /dev/sdc1 
Filesystem     1K-blocks  Used Available Use% Mounted on
/dev/sdc1         967320  1224    899744   1% /mnt
```

## Step 4: Make the Mount Permanent 

Add the following line to `/etc/fstab`

```
LABEL=data1 /mnt ext4 defaults 0 0 
```

Reboot your VM and verify that the data partition is mounted.

## Turn In 

Run the following command to create files to turn in: 

```
$ mount > /vagrant/partition-lab-mount.txt
```

Turn in: 

  * `partition-lab-mount.txt`
  
Submit your files on Canvas.