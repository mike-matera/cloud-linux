# Project: Managing Users 

In this project, you will create and manage user accounts, and practice common services required to administer users on a shared Linux host. These activities include:

  - Creating Groups
  - Creating User Accounts
  - Resetting a forgotten password
  - Modifying a user's uid or gid
  - Locking an account
  - Customizing a login environment
  - Deleting a user Account

## Grade Script

This project comes with a grading script written by my predecessor Jim Griffin. You can fetch it using this link: 

> [user_accounts_and_groups.sh](../../_static/cis-191/user_accounts_and_groups.sh)


## Creating Groups

Create four new groups for your computer with the following names and group IDs:

  * `cis191`: 1201
  * `hobbits`: 1600
  * `elves`: 1700
  * `dwarves`: 1800
  * `wizards`: 1900

## Creating User Accounts

Create five new user accounts using the following names and information:

  * User: `cis191`
    * UID: 1201 
    * GID: 1201 
    * Full name: CIS191
    * Add this account to the wizards group
  * User: `frodo`
    * UID: 1601
    * GID: 1600
    * Full name: Frodo Baggins
  * User `gollum`
     * UID: 1602 
     * GID: 1600   
     * Full name: Smeagol
  * User: `legolas`
     * UID: 1701 
     * GID: 1700 
     * Full name: Legolas of Mirkwood
  * User: `gimli`
     * UID: 1801
     * GID: 1800
     * Full name: Gimli son of Gloin

The password for all of the above accounts should be `Cabri11o`. Do not create private groups for users other than `cis191`, but do take in the following considerations:

  - Gollum wants his home directory to be named `/home/smeagol`
  - All home directories should be created in the `/home` directory.
  - Legolas wants his shell to be [zsh](https://en.wikipedia.org/wiki/Z_shell)
  - Gimli doesn't want to have a password. (If you can grant his wish, do so.)

Be sure you can login to each account.

## Resetting a forgotten password 

Frodo forgot his password. You must reset it to Baggins and force him to change it the next time he logs in.

## Modifying a user's name/identity

  - Change Frodo's GID to be the users group, but make sure he retains his membership in the hobbit group.
  - Legolas wants his username changed to glorfindel
  - Gimli needs his UID changed to 1800. (Make certain that Gimli can still log in and access and create files after this change has been made.

## Locking an Account

Glorfindel (a.k.a. Legolas) has been engaged in suspicious activity. You must lock his account.

## Customizing a login environment

  - Edit the `/etc/issue` file so that the first line says "Middle Earth Linux 1.0.".
  - Edit the `/etc/motd` file to include an announcement that this class is CIS 191 and that all activity on this computer is closely monitored.
  - Gimli is confused by all the messages that come to the screen when he logs on. Configure his account so that no messages are displayed on the screen when he logs in. *Hint: search for hush login using Google.*

## Deleting a user Account

Gollum has passed away, and his account must be removed. However, do not remove his home directory until you archive it to the `/var/preserve` directory and name it `gollum.tar`.

## Turn In

Run the program, `user_accounts_and_groups.sh` until you are satisfied with the results. Save the results by redirecting to a file called `grader_output.txt` and submit the file on Canvas. 

``` 
$ sudo /vagrant/user_accounts_and_groups.sh > /vagrant/grader_output.txt
```
