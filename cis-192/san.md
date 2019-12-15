Class presentation slides are [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1P3UynrLeu8aB6mBxCEv8jBIj7cZpeKkkFUHxk5GyQtQ/edit?usp=sharing).
IntroductionSAN is an alternative way to use Linux to get access to disks. Instead of accessing shared disks at the file level SAN accesses disks at the block level. This has some advantages and disadvantages over traditional networked file systems. There are very good articles that will help you understand SAN:
  * [LinuxJournal's article on ATA over Ehternet (AoE), a form of SAN](http://www.linuxjournal.com/article/10780?page=0,0)
  * [ATA over Ethernet Project Home Page](http://www.linuxjournal.com/article/10780?page=0,0)
  * [Official Ubuntu Documentation](https://help.ubuntu.com/community/ATAOverEthernet)
  * [HowTo Forge's HowTo](http://www.howtoforge.com/using_ata_over_ethernet_aoe_on_ubuntu_12.04_initiator_and_target)

Setup LVMTo get the fullest benefit from SAN you want to combine it with LVM. LVM lets you create virtual disks that can be resized at will. That way your SAN can grow and shrink any time you need it to. I've added three disks to my VM. In order to do this procedure you will need to add at least one. Each of my disks are:
  * 16 GB
  * Thin Provisioned

IMPORTANT: Please Thin Provision your disks that way they will only occupy space on demand.
My disks are /dev/sdb /dev/sdc and /dev/sdd.
1. Create a Physical Volume on each disk
root@filer:~#apt-get install lvm2root@filer:~# pvcreate /dev/sdb /dev/sdc /dev/sdd Physical volume "/dev/sdb" successfully created Physical volume "/dev/sdc" successfully created Physical volume "/dev/sdd" successfully created
2. Create a new Volume Group and add your new Physical Volumes
root@filer:~# vgcreate SANGroup /dev/sdb /dev/sdc /dev/sdd Volume group "SANGroup" successfully created3. Create a new Logical Volume that takes all the storage in your newly created Volume Group
root@filer:~# lvcreate -n SANVolume -l 100%VG SANGroup Logical volume "SANVolume" created
If you have done the above procedure correctly you should now see a new disk called /dev/SANGroup/SANVolume. Question: How big is that disk?
Setup AoE ServerFirst you must have the tools installed.
root@filer:~#apt-get install vblade
Next you must take the block device you created with LVM and export it using AoE.
root@filer:~#vblade 1 1 eth0 /dev/SANGroup/SANVolume &pid 1938: e1.1, 100638720 sectors O_RDWR
Notice that I asked the vblade daemon to run in the background. If you don't do this the shell will not return to the prompt.
Mount AoE on the ClientNow you are ready to have the client mount the share. Remember ATA over Ethernet is just that: Ethernet (layer 2). It is a non-routable protocol so your client MUST be on the same Ethernet network.
root@client:~# apt-get install aoetools
Now that the tools are installed you must initialize the AoE kernel modules and discover the disks that are available on your network:
root@client:~# modprobe aoeroot@client:~# aoe-interfaces eth0root@client:~# aoe-discoverroot@client:~# aoe-stat   e1.1    51.527GB  eth0 up      
If everything worked you now have a new device called/dev/etherd/e1.1. You can use that device just like you would use any other block device. A very important difference between SAN and other forms of file sharing is that the device must be formatted before it can be mounted. It's just a blob of data.
root@client:~# mke2fs /dev/etherd/e1.1mke2fs 1.42 (29-Nov-2011)Filesystem label=OS type: LinuxBlock size=4096 (log=2)Fragment size=4096 (log=2)Stride=0 blocks, Stripe width=0 blocks3145728 inodes, 12579840 blocks628992 blocks (5.00%) reserved for the super userFirst data block=0Maximum filesystem blocks=4294967296384 block groups32768 blocks per group, 32768 fragments per group8192 inodes per groupSuperblock backups stored on blocks: 32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000, 7962624, 11239424
Allocating group tables: done              Writing inode tables: done              Writing superblocks and filesystem accounting information: done 
root@client:~# mount /dev/etherd/e1.1 /mnt
TeardownTaking your SAN down is the opposite of setup.
On the client:root@client:~#umount /dev/etherd/e1.1root@client:~#rmmod aoe
On the server:root@filer:~# killall vbladeroot@filer:~# lvremove /dev/SANGroup/SANVolumeDo you really want to remove active logical volume SANVolume? [y/n]: y Logical volume "SANVolume" successfully removedroot@filer:~# vgremove SANGroup Volume group "SANGroup" successfully removedroot@filer:~# pvremove /dev/sdb /dev/sdc /dev/sdd Labels on physical volume "/dev/sdb" successfully wiped Labels on physical volume "/dev/sdc" successfully wiped Labels on physical volume "/dev/sdd" successfully wiped
ChallengeThis how-to showed you how to use LVM to bond disks together on the server. This could also be don on the client. The general procedure for that would look like:
  - Use the vblade command to setup EACH disk with a different drive number
  - On the client create a Physical Volume for each drive (e.g. /dev/etherd/e1.1)
  - Add the PVs to a VG and create a LV
  - Format and mount the LV

Make it work!
