# Lab: Format and Mount a Disk 

This lab will take you through formatting and mounting a disk in your Vagrant VM. 

## Step 1: Format the `/dev/sdc`

A disk needs to be formatted before it can be mounted. Use this command to format `/dev/sdc` with the `ext4` filesystem. 

```bash 
$ sudo mkfs -t ext4 /dev/sdc 
```

## Step 2: Inspect the Format 

The `dumpe2fs` command prints information about `ext` filesystems. Use it to display information about `/dev/sdc`

```bash
$ sudo dumpe2fs /dev/sdc 
```
Answer the following questions: 

  1. What is the UUID of the filesytem? 
  2. How many free blocks does the filesystem have? 
  3. What are the lifetime writes to the fillesystem? 
  
Submit your answers in a file called `format_and_mount.txt`.

## Step 3: Mount the Filesystem

Make a directory where you can mount the filesystem. 

```bash 
$ sudo mkdir -p /data/sdc
```

Now mount your filesystem onto that directory:

```bash 
$ sudo mount /dev/sdc /data/sdc
```

What is in the /data/sdc directory? 

## Step 4: Remember the Mount 

If you reboot your VM the mount will be forgotten. If you want Linux to ensure your disk is mounted on the next reboot add the following line to `/etc/fstab`.

```
/dev/sdc /data/sdc ext4 defaults 0 0 
```

Test your `fstab` entry using the mount command. First unmount `/data/sdc`: 

```bash
$ sudo umount /data/sdc 
```

Now verify that you can mount it with the one-argument mount command: 

```bash 
$ sudo mount /data/sdc 
```

> NOTE: If mount has an error fix `/etc/fstab` before you reboot.

## Step 5: Check Your Work

Reboot your VM and check if the filesystem is still mounted using `df`. 

```bash
$ df
Filesystem     1K-blocks     Used Available Use% Mounted on
udev              498880        0    498880   0% /dev
tmpfs             101580     3124     98456   4% /run
/dev/sda1       10098468   902784   9179300   9% /
tmpfs             507880        0    507880   0% /dev/shm
tmpfs               5120        0      5120   0% /run/lock
tmpfs             507880        0    507880   0% /sys/fs/cgroup
/dev/sdc          999320     1284    929224   1% /data/sdc
vagrant        489445384 80077756 409367628  17% /vagrant
tmpfs             101580        0    101580   0% /run/user/1000
```

> You should see `/dev/sdc` listed.

Use `blkid` to check for your filesytem: 

```bash
$ sudo blkid
/dev/sda1: LABEL="cloudimg-rootfs" UUID="6c93f311-22e6-4c56-835f-64f7e6ecf75f" TYPE="ext4" PARTUUID="b9390537-01"
/dev/sdc: UUID="af4274c2-23c4-4261-ab04-e2cae193c95d" TYPE="ext4"
/dev/sdb: UUID="2019-02-04-14-26-04-00" LABEL="cidata" TYPE="iso9660"
```

Save the output of `blkid` to submit with this lab.

```bash
$ sudo blkid > /home/vagrant/blkid.txt
```

## Ansible Play (Optional)

The steps in this lab can be performed by Ansible. Add this play to your playbook:

```yaml
- hosts: all
  become: true
  name: Partition /dev/sdc 
  tasks:
    - name: Create a partition table on /dev/sdc
      parted:
        device: /dev/sdc 
    - name: Create /dev/sdc1 
      parted:
        device: /dev/sdc 
        number: 1
        state: present 
    - name: Create a ext4 filesystem on /dev/sdc1
      filesystem:
        fstype: ext4
        dev: /dev/sdc1
    - name: Create the /data/sdc1 directory
      file:
        path: /data/sdc1
        state: directory
        mode: '0755'        
    - name: Adding mount point /dev/sdc1 on /data/sdc1
      mount:
        path: /data/sdc1
        src: /dev/sdc1
        fstype: ext4
        state: mounted
```

## Submit 

Please submit the following:

  * Answers to the lab questions in a file called `format_and_mount.txt` 
  * A copy of your `/etc/fstab`
  * The output of `blkid` in a file called `blkid.txt`
  