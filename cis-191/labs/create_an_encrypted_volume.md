# Lab: Create an Encrypted Logical Volume 

In this lab you'll use the volume group you created in the lab [Create a Volume Group](create_volume_group.md). You will create a simple volume and an encrypted volume. The encrypted volume is a virtual devices backed by storange in the simple volume.

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
$ sudo lvcreate -n encrypted_volume -l 100%FREE my_vg
  Logical volume "encrypted_volume" created.
```

Now verify that the volume exists: 

```bash
$ sudo lvdisplay 
  --- Logical volume ---
  LV Path                /dev/my_vg/encrypted_volume
  LV Name                encrypted_volume
  VG Name                my_vg
  LV UUID                OBXXAY-vcnf-wa5T-0MBe-VkQ7-t8n9-KShhtM
  LV Write Access        read/write
  LV Creation host, time ubuntu-xenial, 2019-03-14 15:40:38 +0000
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

Notice that you have the `/dev/my_vg/encrypted_volume` block device available. 

## Step 2: Encrypt the Device 

The `cryptsetup` tool manages encrypted logical volumes. Use the command below to create an encrypted format on the `/dev/my_vg/encrypted_volume` device: 

```bash
$ sudo cryptsetup --verbose --verify-passphrase luksFormat /dev/my_vg/encrypted_volume 
```

The command you just ran formats the disk with the `luks` on-disk format. It's not a filesystem but a way to store the cryptographic keys and other encryption metadata. Use this command to look at the format: 

```bash
$ sudo cryptsetup luksDump /dev/my_vg/encrypted_volume 
LUKS header information for /dev/my_vg/encrypted_volume

Version:       	1
Cipher name:   	aes
Cipher mode:   	xts-plain64
Hash spec:     	sha1
Payload offset:	4096
MK bits:       	256
MK digest:     	ee a2 d7 85 c7 90 17 aa 98 8d 3e 15 7c a8 b4 1d 58 a0 f2 00 
MK salt:       	10 63 8e de 49 df 14 4f 8a bc 00 a9 ee 26 32 4e 
               	54 42 bd e9 c8 31 2c 05 a6 86 84 34 6b d9 07 54 
MK iterations: 	94625
UUID:          	7a2e2aff-e8af-40ed-9d92-5bee940987c5

Key Slot 0: ENABLED
	Iterations:         	378697
	Salt:               	b2 b7 be 9b c9 ad ab 31 2d 9f bb 20 34 9d cb e2 
	                      	d4 57 82 4f c0 36 77 19 a1 c3 ce 2c e8 9e ea 4d 
	Key material offset:	8
	AF stripes:            	4000
Key Slot 1: DISABLED
Key Slot 2: DISABLED
Key Slot 3: DISABLED
Key Slot 4: DISABLED
Key Slot 5: DISABLED
Key Slot 6: DISABLED
Key Slot 7: DISABLED
```

## Step 3: Open the Encrypted Device 

The encrypted device has to be opened to be used. The command below opens the device and will require the password you entered in the previous step:

```bash
$ sudo cryptsetup luksOpen /dev/my_vg/encrypted_volume decrypted_volume 
```

The command should have created a virtual logical volume called `decrypted_volume`. It doesn't show up in the output of `lvdisplay` but you can see it in the `/dev/mapper` directory: 

```bash
$ ls -la /dev/mapper
total 0
drwxr-xr-x  2 root root     100 Mar 14 15:49 .
drwxr-xr-x 17 root root    3840 Mar 14 15:49 ..
crw-------  1 root root 10, 236 Mar 14 14:21 control
lrwxrwxrwx  1 root root       7 Mar 14 15:49 decrypted_volume -> ../dm-1
lrwxrwxrwx  1 root root       7 Mar 14 15:49 my_vg-encrypted_volume -> ../dm-0
```

## Step 4: Format and Mount the Encrypted Volume 

Create a new `ext4` filesystem on the new device:

```bash
$ sudo mkfs -t ext4 /dev/mapper/decrypted_volume 
mke2fs 1.42.13 (17-May-2015)
Creating filesystem with 1043968 4k blocks and 261120 inodes
Filesystem UUID: e166ce8e-6879-49ec-a2d9-4583684ea727
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done 
```

## Step 5: Mount the new Volume 

Mount the new filesystem on `/mnt`:

```bash
$ sudo mount /dev/mapper/decrypted_volume /mnt 
```

Check the available space on the device:

```bash
$ df /mnt
Filesystem                   1K-blocks  Used Available Use% Mounted on
/dev/mapper/decrypted_volume   4044736  8152   3811408   1% /mnt
```

## Turn In 

Run the following commands to create output files: 

```bash
$ sudo lvdisplay > /vagrant/encrypted.txt 
$ sudo cryptsetup luksDump /dev/my_vg/encrypted_volume > /vagrant/luks.txt
```

Turn in the following files:

  1. `encrypted.txt`
  2. `luks.txt`
