# Raid Lab

In this lab you'll follow the excellent guide by [DigitalOcean](https://www.digitalocean.com/) to create all of the common RAID types supported by Linux. DigitalOcean is a cloud services provider that will sell you Linux VMs by the hour. They specialize in Linux and have lots of guides. 

## The Guide 

Read over the guide at this link: 

 - [How To Configure RAID Arrays on Ubuntu 16.04 
](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-16-04)

The guide has the following sections: 

  1. Resetting RAID Devices (do this between steps)
  2. Creating a RAID 0 Array 
  3. Creating a RAID 1 Array 
  4. Creating a RAID 5 Array 
  5. Creating a RAID 6 Array 
  6. Creating a RAID 10 Array 

Use sections 2 through 6 to create each of the RAID types. Between sections save the output of the `mdadm --detail` command for the RAID number:

```bash
$ sudo mdadm --detail /dev/md0 > /vagrant/mdadm_raidN.txt 
```

> NOTE: Replace the N in the command with the RAID number

## Turn In 

When you're done you should have the following files:

  - `mdadm_raid0.txt`
  - `mdadm_raid1.txt`
  - `mdadm_raid5.txt`
  - `mdadm_raid6.txt`
  - `mdadm_raid10.txt`

Turn in your files on Canvas.
