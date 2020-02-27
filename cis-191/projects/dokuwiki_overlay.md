# Dokuwiki and OverlayFS 

In this project you will use OverlayFS to separate the code and the data used by Dokuwiki. You should know how to install Dokuwiki using the instructions in the [Install Dokuwiki](../labs/dokuwiki_install.md) lab, however you will reinstall it during this project.   

## Background

OverlayFS lets you separate filesystems into layers. The lower layers are read-only. Only the uppermost layer is written. When combined together the layers form what looks like a normal filesystem. In this you will install Dokuwiki into a directory and make that directory the lower layer. This will keep the installation in in its pristine state with no changes to any of the files. The upper layer will start empty and, as Dokuwiki accesses files, will start populating with changes. This makes it trivial to backup just changed files. 

In oder to user OverlayFS you have to create several directories. Directories are described in the table below: 

| Directory | Function | Description | 
| --- | --- | --- | 
| `/var/www/html_lower` | Read-Only | The lower directory contains the "base" filesystem. Install Dokuwiki into this directory and it will be held in its pristine state. | 
| `/var/www/html_upper` | Read-Write | Any changes made to the union filesystem will appear in the upper directory which must be read-write. | 
| `/var/www/html_work` | Read-Write | This is a work directory for OverlayFS it must be on the same filesystem as the upper directory | 
| `/var/www/html` | Read-Write | The resulting UnionFS will be mounted here. | 

## Create the UnionFS 

OverlayFS uses mount options to tell it where the lower, upper and work directories are located. Here's how to use it. Here's the usage of mount:

```
mount -t overlay overlay -o lowerdir=<lower>,upperdir=<upper>,workdir=<work> <mount_dir>
```

You can verify your mount has worked by using `df`: 

```
$ df /var/www/html
Filesystem     1K-blocks    Used Available Use% Mounted on
overlay         10098432 1508600   8573448  15% /var/www/html
```

Make sure you see your filesystem before you proceed. 

## Make it Permanent 

When you're sure you have your OverlayFS mounted add it to `/etc/fstab` so that it's remounted after you reboot. Reboot your VM and verify that the mount is made. 

## Setup Dokuwiki

Use the setup URL to initialize your Wiki 

> [http://localhost:8080/dokuwiki/install.php](http://localhost:8080/dokuwiki/install.php)

Also, create a page like you did in the lab.

## Create a Backup 

Use `tar` to backup the contents of `/var/www/html_lower`. That directory should contain some files after you initialize Dokuwiki. Save the files into `dokuwiki_backup.tar`

## Submit 

Submit the following files with this project:

  1. `dokuwiki_backup.tar` 
  2. `/etc/fstab`

Turn in your files on Canvas.



