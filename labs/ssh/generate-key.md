# Generate an SSH Key 

In this lab you'll locate your SSH configuration directory and generate an SSH key. SSH keys allow you to login to a remote machine without a password. Using SSH keys are preferred over using a password because they are more secure. 

## Step 1: Locate your SSH Configuration 

The location of your SSH configuration depends on your platform. Consult the table below: 

| OS | Location | 
| --- | --- | 
| Windows 10 | $HOME/.ssh | 
| Mac OSX | ~/.ssh | 
| Linux | ~/.ssh | 

Using the command prompt on your computer change into the SSH configuration directory and view the contents. 

```
$ cd ~/.ssh
$ ls
```

## Step 2: Generate a Key 

An SSH key is really two keys: A public and a private key. The private key should never leave the machine it was generated on. The public key will be placed on other machines and will grant you the ability to login with no password. Run the following command and press "Enter" to accept the defaults:

```
$ ssh-keygen -t rsa -b 4096 
```

Now verify you have an SSH key: 

```
$ ls 
```

> Do you see `id_rsa` and `id_rsa.pub`? If not check your work. 

## Step 3: Place your Key on Opus

Now let's place the key on Opus and test to make sure it works. If you're on Linux or a Mac you can use the `ssh-copy-id` command. The argument to `ssh-copy-id` is the same as `ssh`:

```
$ ssh-copy-id yourname@opus.cis.cabrillo.edu 
```

> Replace `yourname` with your login name. 

There is no `ssh-copy-id` on Windows so you'll have to do it manually with this command: 

```
$ cat $HOME/.ssh/id_rsa.pub | ssh yourname@opus.cis.cabrillo.edu "umask 0077; mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys;"
```

> Replace `yourname` with your login name. 

## Step 4: Test Your Key 

You should now be able to login to Opus with no password:

```
$ ssh yourname@opus.cis.cabrillo.edu 
```

If you setup vscode it will no longer require you to type your password when you connect. 

## Turn In 

Turn in your public key on Canvas

