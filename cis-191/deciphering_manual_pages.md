# Deciphering Manual Pages 

Manual pages are the definitive references for Linux commands. They are the best place to find out how to use a command and what you can do with it. But, they can be difficult to interpret. This guide will introduce manual page concepts and will help you understand how to decipher a command's usage.

## Commands

  * man

## Configuration

  * None

## Introduction 

UNIX manuals used to be printed. The very first edition of the [Unix Programmer's Manual](https://www.bell-labs.com/usr/dmr/www/1stEdman.html), dated November 3, 1971,is still available from Bell Labs. In the introduction the author Dennis Ritchie describes the basic layout of the UNIX manual. The same layout that is used today.

## Manual Sections 

The manual covers material that is needed by Linux programmers and Linux administrators and is divided into volumes called sections. Originally, each section would be in it's own binder. Sections are dedicated to a category of command or programming interface. The section definitions are:

| Section | Description | Audience |
| ------- | ----------- | -------- |  
| 1 | Executable programs or shell commands | All Users |
| 2 | System calls (functions provided by the kernel) | Programmers | 
| 3 | Library calls (functions within program libraries) | Programmers | 
| 4 | Special files (usually found in /dev) | Administrators | 
| 5 | File formats and conventions eg /etc/passwd | Administrators | 
| 6 | Games | All Users |
| 7 | Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7) | All Users | 
| 8 | System administration commands (usually only for root) | Administrator | 
| 9 | Kernel routines [Non standard] | Programmers | 

When you invoke the man command it searches all sections for a page with the given title and displays the first page it finds. In some cases there may be more than one match. For example, chroot is both a command and a system call. When you execute the following command:

```
$ man chroot
```

You see the manual for the command (section 8). If you wanted to see the manual for a specific section you have to tell man what one you want:

```
man 8 chroot  # the command's manual
man 2 chroot  # the system call's manual
```

Here's how you can see if there are multiple sections of a manual page:

```
$ man -k . | grep chroot
chroot (2)      - change root directory
chroot (8)      - run command or interactive shell with special root directory
ischroot (1)     - detect if running in a chroot
```

## Reading a Manual 

Manuals have a formal layout, that is designed to be used on a text-only display. They are divided into chapters. Common chapters are:
  - NAME: The name of the command or function call.
  - SYNOPSYS: For commands a description of all uses and forms of the command.
  - DESCRIPTION: A description of the command in English, including a brief description of each parameter and flag.
  - EXAMPLES: Complex commands often have usage examples, which are very helpful.
  - SEE ALSO: Related commands and manual pages.
  - BUGS: Known problems and where to report bugs you find.
  - AUTHORS: Who wrote the manual page (and possibly the command).

The remainder of this article will focus on how to interpret the synopsys to know exactly how to call a command.

## The Command Synopsys 

The command synopsys uses an informal syntax to show you what forms and what arguments a command takes. Here's the manual for the mount command:

```
MOUNT(8)          System Administration          MOUNT(8)
NAME
   mount - mount a filesystem
SYNOPSIS
   mount [-lhV]
   mount -a [-fFnrsvw] [-t vfstype] [-O optlist]
   mount [-fnrsvw] [-o option[,option]...] device|dir
   mount [-fnrsvw] [-t vfstype] [-o options] device dir
```

First, notice we're looking at the section eight manual for mount: mount(8). The synopsys shows the four different forms of mount, these forms are mutually exclusive, which is why they are listed separately. The first, and simplest form, displays the currently mounted systems:

```
mount [-lhV]
```

Items listed inside of square brackets are optional. In this form the mount command takes the ''-l'', ''-h'' or ''-V'' flag, none of the flags or any combination of the three. The second form of the command mounts all filesystems listed in ''/etc/fstab'':

```
mount -a [-fFnrsvw] [-t vfstype] [-O optlist]
```

In this form the ''-a'' flag is required. That's made clear by the fact that it is not in square brackets. The other arguments are optional. Here are some examples of how to use this form:

```
mount -a         # mount all filesystems in /etc/fstab
mount -a -t ext4     # mount all ext4 filesystems listed in /etc/fstab
mount -a -t ext4 -O ro  # mount all ext4 filesystems listed in /etc/fstab as read-only filesystems
```

The third form of mount gives us a choice:
 
```
mount [-fnrsvw] [-o option[,option]...]  device|dir
```

Normally mount needs to know what you're mounting and where to mount it. On filesystems listed in /etc/fstab you can figure out one piece of information given the other, therefore you can only use this form of mount on filesystems listed in /etc/fstab. The choice is specified by the bar (''|'') character. It's telling us that we must choose one of device or directory. For example:

```
mount /dev/sda      # mount a device (it must be listed in /etc/fstab)
mount /home       # mount the /home directory (it must be listed in /etc/fstab)
```

The final form of mount requires us to specify both a device and a directory:

```
mount [-fnrsvw] [-t vfstype] [-o options] device dir
```

Examples of this form of mount are:

```
mount /dev/sda6 /home
mount -t btrfs /dev/sda6 /home
```

Next we'll look at a more complicated example.

```
ADDUSER(8)         System Manager's Manual         ADDUSER(8)
NAME
   adduser, addgroup - add a user or group to the system
SYNOPSIS
   adduser [options] [--home DIR] [--shell SHELL] [--no-create-home]
   [--uid ID] [--firstuid ID] [--lastuid ID] [--ingroup GROUP | --gid ID]
   [--disabled-password]   [--disabled-login]   [--gecos   GECOS]
   [--add_extra_groups] [--encrypt-home] user
   adduser --system [options] [--home DIR] [--shell SHELL] [--no-create-
   home] [--uid ID] [--group | --ingroup GROUP | --gid ID] [--disabled-
   password] [--disabled-login] [--gecos GECOS] user
   addgroup [options] [--gid ID] group
   addgroup --system [options] [--gid ID] group
   adduser [options] user group

 COMMON OPTIONS   [--quiet] [--debug] [--force-badname] [--help|-h] [--version] [--conf   FILE]
```

The adduser command lists among its forms the closely related command addgroup. These two commands share a manual page. There are two forms of the adduser command:

```
adduser ...
adduser --system ...
```

Which form you use determines what options are valid. Notice that in this usage that there's a generic 
```
[options]
```

 parameter listed:

```
adduser [options] ...
```

That's a shorthand when there are options common to all forms of the command. Those are listed right below. Some options are mutually exclusive:

```
[ --ingroup GROUP | --gid ID ]
```

This tells you that you can only specify one of the optional arguments 
```
--ingroup
```

 or 
```
--gid
```

never both. Next, let's look at a very complicated example:

```
VGCREATE(8)         System Manager's Manual        VGCREATE(8)
NAME
   vgcreate - create a volume group
SYNOPSIS
   vgcreate [--addtag Tag] [--alloc AllocationPolicy] [-A|--autobackup
   {y|n}] [-c|--clustered {y|n}] [-d|--debug] [-h|--help] [-l|--maxlogiâ
   calvolumes MaxLogicalVolumes] [-M|--metadatatype type] [-p|--maxphysiâ
   calvolumes  MaxPhysicalVolumes]  [--[vg]metadatacopies  NumberOfâ
   Copies|unmanaged|all]   [-s|--physicalextentsize   PhysicalExtentâ
   Size[bBsSkKmMgGtTpPeE]] [-t|--test] [-v|--verbose] [--version] [PHYSIâ
   CAL DEVICE OPTIONS] VolumeGroupName PhysicalDevicePath [PhysicalDeviâ
   cePath...]
```

The vgcreate command has a number of complicated arguments. Some are specified as both their short form and their long form:

```
[-d|--debug]
```

Some flags take arguments and have a short and long form:

```
[-l|--maxlogicalvolumes  MaxLogicalVolumes]
```

Both of these examples would work:

```
-l 5            # maximum five logical volumes
--maxlogicalvolumes 5    # the same thing
```

Some optional flags have optional parts. When that happens you see nested square brackets:

```
[-s|--physicalextentsize     PhysicalExtentâSize[bBsSkKmMgGtTpPeE]]
```

In this example the physical extent size argument is a number that can have a magnitude modifier:

```
--physicalextentsize 1024    # physical extent of 1024 bytes (1k)
-s 1024             # same thing
-s 1k              # same again
-s 1M              # physical extent of 1 megabyte
```

Some flags only take particular values. Those values will be listed with the flag inside of curly braces:

```
[-c|--clustered {y|n}]
```

This option could be:

```
-c y
-c n
--clustered y
--clustered n
```

Though sometimes the curly braces are omitted:

```
[--[vg]metadatacopies    NumberOfâ
Copies|unmanaged|all]
```

This flag can be: 

```
--metadatacopies 5
--metadatacopies unmanaged
--metadatacopies all
```

Notice that there's an optional "vg" at the beginning of the flag so it can also be:

```
--vgmetadatacopies 5
--vgmetadatacopies unmanaged
--vgmetadatacopies all
```

Some arguments can be given more than once, these are called variadic arguments:

```
VolumeGroupName PhysicalDevicePath [PhysicalDevi
cePath...]
```

When you create a volume group you must give the volume group a name and a path to at least one physical volume, but you can give more physical volumes if you like. That's what the ellipsys tells you. The following examples all work:

```
vgcreate MyGroupName /dev/sda           # minimum required
vgcreate MyGroupName /dev/sda /dev/sdb       # one additional argument given
vgcreate MyGroupName /dev/sda /dev/sdb /dev/sdc  # two additional arguments given
```

Many commands have variadic arguments. See the manual for the "cat" command.

## Quick Reference 

| Syntax | Example | Meaning | 
| ------ | ------- | ------- | 
| literal | vgcreate | The word just as shown (e.g. the command) |
| <item> | <PhysicalDevicePath> | Describes what to put in this place. |
| [argument] | [-g] | An optional agrument |
| [choice1&vert;choice2] <br>{choice1&vert;choice2} | [ -l &vert; -L ] <br> { y &vert; n } | A choice of one of the possibilities |
| [item]... | [file]... | Zero or more items |
| item [item...] | volume [volume...] |One or more items |
