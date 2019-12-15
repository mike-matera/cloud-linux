# Create a User and a Group 

In this lab you'll create users and add them to groups the easy way, using the `adduser` and `addgroup` commands. 

## Step 1: Add Users 

The `adduser` command makes it easy to add users. It's customary to create private groups for users and this is what `adduser` does by default. 

``` 
$ sudo adduser melkor 
Adding user `melkor' ...
Adding new group `melkor' (1002) ...
Adding new user `melkor' (1002) with group `melkor' ...
Creating home directory `/home/melkor' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for melkor
Enter the new value, or press ENTER for the default
	Full Name []: Melkor
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] 
```

Now add another user:

```
$ sudo adduser --home /home/manwe --shell /bin/bash --disabled-password --gecos Manwe,,, manwe 
Adding user `manwe' ...
Adding new group `manwe' (1003) ...
Adding new user `manwe' (1003) with group `manwe' ...
Creating home directory `/home/manwe' ...
Copying files from `/etc/skel' ...
```

## Step 2: Create a Group 

The two new users have a personal group. Let's create a new group and add them to it. 

``` 
$ sudo addgroup valar 
Adding group `valar' (GID 1004) ...
Done.
```

## Step 3: Add Users to the Group 

Now add the users to the new group. 

``` 
$ sudo usermod -a -G valar melkor 
$ sudo usermod -a -G valar manwe
```

> WARNING: Do not forget the -a flag!

# Turn In 

Please turn in the files on Canvas: 

  - `/etc/passwd`
  - `/etc/group`
  