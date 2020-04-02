# Lab: Create a User Step-by-Step 

In this lab you will create a user and their home directory step-by-step the way the `adduser` command does. You'll create the following user:

  - Username: `galadriel`
  - Group: `maiar`
  - Home directory: `/home/galadriel`

## Step 0: Install Python 

The best way to generate a UNIX password from the command line is with Python. Install it with `apt`:

``` 
$ sudo apt install python-minimal
```

## Step 1: Create a User 

Users are added to *both* the `/etc/passwd` and `/etc/shadow` files. Add this line to `/etc/passwd`: 

```
galadriel:x:2000:2000:Lady of Light:/home/galadriel:/bin/bash
```

The fields are:

  1. `galadriel`: User name
  2. `x`: Always `x` 
  3. `2000`: User ID
  4. `2000`: Primary Group ID
  5. `Lady of Light`: Full name
  6. `/etc/galadriel`: Home directory
  7. `/bin/bash`: Login shell

## Step 2: Generate a Password 

The shadow file contains the hash of the users's password and a salt for the hash. Python's `crypt` library can generate the hash and salt for us. Run this command to generate a hash for `Cabri11o`.

``` 
$ python3 -c 'import crypt; print(crypt.crypt("Cabri11o"))'
```

This will generate a random salt so every hash will be different. Here's an example: 

``` 
$6$PO8tqBryUU5aZA.r$Dy0ybcqFH6aHA/vQGixiKGzKoWX2Ryh5a1aGdRqYB9U0SWpZZyUSLyMDP0Q4BonjA1c7ywdO.wktOk13KFO3T1
```

The salt is made of fields separated by the dollar sign (`$`). The fields are:

  1. `$6`: Encryption method (`SHA-512`)
  2. `$PO8tqBryUU5aZA.r`: Salt (chosen at random)
  3. `$Dy0ybcqFH6aHA...`: The hash 
  
Copy the entire output of the command so you can paste it in the next step. 

## Step 3: Give the User a Password 

Add this line to `/etc/shadow`:

``` 
galadriel:<your-hash-here>:1:0:99999:7:::
```

The fields are: 

  1. `galadriel`: User name. 
  2. `<your-hash-here>`: The hash (paste the hash here). Empty (`::`) allows login without a password. A star (`*`) disables the account. 
  3. `1`: Last password change. Days since Jan 1, 1970 that password was last changed. A zero forces a password change. 
  4. `0`: The minimum days between password changes. 
  5. `99999`: The maximum age of a password. 
  6. `7`: Password change warning days. 
  7. `<empty>`: The number of days after password expires that account is disabled. 
  8. `<empty>`: The number of days since January 1, 1970 that an account has been disabled
  9. `<empty>`: A reserved field for possible future use


## Step 4: Create a Group 

Add the following lines to `/etc/group`

```
noldor:x:2000:
teleri:x:2001:galadriel
```

The fields are: 

  1. `noldor`: Group name. 
  2. `x`: Always `x` 
  3. `2000`: Group ID
  4. Group members separated by commas
  
## Step 5: Create a Home Directory 

The directory `/etc/skel` has the *skeleton* of a home directory. That's the bare minimum files a user gets started with. Make a copy with this command:

``` 
$ sudo cp -R /etc/skel /home/galadriel
```

The directory is owned by `root`. Use `chown` to fix it: 

``` 
$ sudo chown -R galadriel:noldor /home/galadriel/
```

## Step 6: Test Your Work

You should be able to use `su` to login as Galadriel. You'll be prompted for the password:

``` 
$ su galadriel 
Password: 
```

> Don't use sudo to do this test!

See what groups Galadriel is in: 

```
$ groups 
``` 

## Turn In 

Turn in the following files on Canavas: 

  - `/etc/passwd`
  - `/etc/shadow`
  - `/etc/group`
  