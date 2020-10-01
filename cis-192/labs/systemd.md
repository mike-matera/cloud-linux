# Work with `systemd` 

In this lab you'll practice some of the things you can do with `systemd` and the `systemctl` command. 

## Step 1: List the Loaded Targets

The configuration that `systemd` know about are called *units*. There are a few types of units. To list the loaded targets run the command:

```
$ systemctl list-units --type=target 
```

Are there any failed units? 


## Step 2: Look For Available Targets

Units are created with text configuration files. The available unit files can be seen in `/usr/lib/systemd/system` and `/etc/systemd/system` (the latter takes precedence). List installed unit files with:

```
$ systemctl list-unit-files
```

Look in the two directories for a file called `multi-user.target`. It's a text file and it describes what the target is. In the same directory there will be a subdirectory called `multi-user.target.wants/`. That subdirectory contains a list of services that should be running in order for the multi-user target to be achieved. 

1. What targets does the multi-user target require? 
1. What services does the multi-user target want? 

## Step 3: Check and Restart Services 

Services can be started and stopped or reloaded. If you installed apache in the previous lab you can use `systemctl` to see if apache is running: 

```
$ systemctl status apache2 
```

Now try stopping apache: 

```
$ sudo systemctl stop apache2 
```

What happens if you browse to your VM? 

You can start apache again by:

```
$ sudo systemctl start apache2 
```

Sometimes you want a program to reload its configuration without shutting down. You can do that with: 

```
$ sudo systemctl reload apache2 
```

## Step 4: Disable Apache 

If you don't want apache to restart when you reboot the computer you can *disable* it.

```
$ sudo systemctl disable apache2
```

You can also enable it: 

```
$ sudo systemctl disable apache2
```

## Turn In 

Answers to the questions. 
