# Lesson 6 Commands 

This page has the commands for Lesson 6. They are: 

| Command | Action | 
| --- | --- | 
| `groups` | Shows what groups you a a member of. | 
| `id` | shows user ID (uid), primary group ID (gid), membership in secondary groups. | 
| `chown` | Changes the ownership of a file. (Only the superuser has this privilege) | 
| `chgrp` | Changes the group of a file. (Only groups that you belong to) 
| `chmod` | Changes the file mode "permission" bits of a file. |  
| `umask` | Allows you to control the permissions new files and directories have when they are created | 

## File and Directory Permissions 

Files and directories have permissions settings that control who can access them. The permissions in the UNIX file system are more primitive than Windows, which uses an access control list. On a UNIX system there are three subjects that are important for controlling access. 

| Subject | Description | 
| --- | --- | 
| User | The owner of the file or directory | 
| Group | The group the file or directory belongs to | 
| Others | Anyone that's not the owner or in the group | 

When you run the `ls -l` command you see **three** sets of permissions that contain a letter or a dash (`-`). The letters indicate what the subject is allowed to do. Possible accesses are: 

| Access | Description |
| --- | --- | 
| Read (`r`) | For files this allows the subject to read the file. For directories allows `ls` to read the contents of the directory. | 
| Write (`w`) | For files this allows the subject to change the contents of the file (but not delete it). For directories this allows you to create and remove files in the directory. | 
| Execute (`x`) | For files this allows them to be executed. For directories this allows `cd` to change into the directory. | 

Here's an example of `ls -l`:

```bash
simben90@opus3:~$ ls -l 
total 76
drwxr-xr-x 2 simben90 simben90  4096 Mar  1 22:27 bin
-rw-r----- 1 simben90 simben90     0 Dec  3 22:12 butt
-rw-r--r-- 1 simben90 simben90    30 Dec  3 22:07 cis90.contribution
drwxrwxr-x 4 simben90 simben90  4096 Mar  1 21:58 class
-rw------- 1 simben90 simben90   373 Feb 12 08:07 dead.letter
drwxrwxr-x 2 simben90 simben90  4096 Mar  1 22:28 docs
```

Here's how to understand the permissions on the `cis90.contribution` file: 

| User (`simben90`) | Group (`simben90`) | Other | 
| --- | --- | --- | 
| `rw-` | `r--` | `r--` | 
| Read/Write | Read Only | Read Only | 


## File Permissions and Binary 

File permissions are expressed in binary. Counting in binary is easy once you get the hang of it. It's just like counting in decimal but you use powers of two instead of powers of 10. Let's start with powers of 10. Let's consider the number 237. Each number is in a *place* that has a *place value*. 

| *Hundred's Place* <br> $10^2$ | *Ten's Place* <br> $10^1$ | *One's Place* <br> $10^0$ | 
| --- | --- | --- | 
| 2 | 3 | 7 | 

Add the value of all of the places together and you get the number. Binary works the same way, but instead of multiplying each place by 10 you multiply each place by 2. Here's the number 237 in binary: 

| *128's Place* <br> $2^7$ | *64's Place* <br> $2^6$ | *32's Place* <br> $2^5$ | *16's Place* <br> $2^4$ | *8's Place* <br> $2^3$ | *4's Place* <br> $2^2$ | *2's Place* <br> $2^1$ | *1's Place* <br> $2^0$ | 
| --- | --- | --- | -- | -- | -- | -- | -- | 
| 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |  

In each place where there is a 1 you add the pace value. When you add all the places in the number above you get: 

$128 + 64 + 32 + 8 + 4 + 1 = 237$

*Not clicking for you?* This table will help you remember the binary numbers to permissions mapping. 

| Permission Decimal | Permission Binary | Permission Flags | Description | 
| --- | --- | --- | --- | 
| 0 | 000 | `---` | No access | 
| 1 | 001 | `--x` | Execute only. **Not generally useful** | 
| 2 | 010 | `-w-` | Write only. **Not generally useful** | 
| 3 | 011 | `-wx` | Write and execute. **Not generally useful** | 
| 4 | 100 | `r--` | Read only. | 
| 5 | 101 | `r-x` | Read and execute. Common for directories. Allows the use of directories. Files can be changed but cannot be created or deleted. | 
| 6 | 110 | `rw-` | Read write. Common for files. | 
| 7 | 111 | `rwx` | Read, write and execute. For files allows the execution of a file as a program. For directories allows full access. | 

## Changing File Permissions 

There are two ways to change the file permissions. You can do it *absolutely* using a binary number that represents the file permission. For example: 

```bash 
$ chmod 640 dead.letter 
$ ls -l dead.letter 
-rw-r----- 1 simben90 simben90 373 Feb 12 08:07 dead.letter
```

You can also change permissions *relatively* by adding or subtracting access. For example to add the ability for the group to write the `dead.letter` file you would run the command: 

```bash 
$ chmod g+w dead.letter 
```

To subtract the ability for the group and everyone to read or write the `dead.letter` file you would run the command: 

```bash 
$ chmod go-rw dead.letter
``` 

## Controlling Default Permissions with `umask`

The `umask` command controls the permissions of files and directories when they are created. The "mask" in `umask` signifies that bits in the `umask` disable or mask the corresponding permission bits. That means that the `umask` shows you the **opposite** of the permissions that will be created. Run `umask` without arguments on `opus3` and you can see what the default `umask` is.

```bash
$ umask 
0002
```

This says that new files and directories will not be writable. This table will help you remember `umask` values. 

| `umask` Decimal | `umask` Binary | Default Permission Flags | 
| --- | --- | --- |  
| 0 | 000 | `rwx` |  
| 1 | 001 | `rw-` |  
| 2 | 010 | `r-x` |  
| 3 | 011 | `r--` |  
| 4 | 100 | `-wx` |  
| 5 | 101 | `-w-` |  
| 6 | 110 | `--x` |  
| 7 | 111 | `---` |  

