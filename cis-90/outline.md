# Outline 

## Week 1 commands 

cal			- show calendar
date		- show current time and date
clear		- clear the terminal screen

hostname		- show the host name of the computer being accessed
ps			- show processes, including the name of the shell being run
uname		- show the kernel name
cat /etc/issue 	- usually shows distro (distribution) name
cat /etc/*-release 	- usually shows distro (distribution) name

who		- shows current login sessions
who am i		- identifies which login session you are using
tty			- shows your terminal device
id			- show user info including username/UID and group/GID

history		- show previous commands

ssh			- Connect and login to remote system
exit			- terminate your shell and log off

## Week 2 Commands

echo  		- Prints text and variables
banner  	- Make a banner

ls  		- List directory contents
cat  		- View file (name comes from concatenate) 
file  		- Show additional information about a file
type  		- Shows where a command resides on the path
apropos  	- Searches the whatis database for strings
whatis  		- Searches the whatis database for commands
man  		- Show the manual page for a command
info 		- Alternate online documentation tool

bc		- Binary calculator
passwd		- Change password

set		- List all shell variables
env		- List all environment variables

## Week 3 commands 

write		- “chat” with another user by writing to their terminal
mesg		- enable/disable writes to your terminal
irssi		- Chat using IRC protocol
mail		- send and read email

## Week 4 commands 

cat 		- view a text file
more		- view a large text file by scrolling down 
less		- view a large text file by scrolling down and up
head		- view the beginning lines of a text file
tail		- view the last lines of a text file
wc		- count the lines, words and characters in a text file
xxd 		- view a binary data file as a hex dump

cd 		- change to a different directory
ls 		- list files 
pwd 		- show name of current/working directory

file 		- show additional file information
type 		- show location of a command on path

## Week 5 -- No new commands 

## Week 6 commands 

touch		- make a file (or update the timestamp)
mkdir 		- make a directory
cp		- copy a file
mv		- move or rename a file
rmdir		- remove a directory
rm		- remove a file
ln		- create a link
tree		- visual list a directory


Redirecting stdout:

> filename	- redirecting stdout to create/empty a file

## Week 7 commands 

groups 	shows group membership for a user.

id 	shows user ID (uid), primary group ID (gid), membership in secondary groups, and SELinux context.

chown - Changes the ownership of a file. (Only the superuser has this privilege) 

chgrp   - Changes the group of a file. (Only groups that you belong to) 

chmod - Changes the file mode “permission” bits of a file. 
Numeric:  chmod 640 letter  (sets the permissions) 
Mnemonic:  chmod ug+rw letter (changes the permissions)
 		u=user(owner), g=group, o=other		  
 	r=read, w=write, x=execute

umask – Allows you to fully control the permissions new files and directories are created with

## Week 8 commands 

find - Find file or content of a file
 
grep - "Global Regular Expression Print"
 
sort - sort
 
spell - spelling correction
 
wc - word count

tee - split output

cut - cut fields from a line

## Week 9 commands 

Review and more pipelines. 

## Week 10 commands 

set –x		Enable shell debugging

set +x		Disable shell debugging
ps 
job control 
sleep 
kill 
killall 
stty 
at - schedule a job to run in the future

at -c <jobnum> - view a scheduled job

atq - list queue of pending jobs

atrm - remove a pending job

## Week 11 commands 

(Repeat at)

vi

## Week 12 commands 

Environment variables and aliases 
.bashrc 

New commands:
.				- source the commands
alias			- create or show an alias
unalias			- remove an alias
set				- show all variables
env				- show environment variables
export			- export variable so child can use
exec			- replace with new code
source			- same as .

New Files and Directories:
.bash_profile			- executed at login
.bashrc			- executed at login and new shells	


## Week 13 

Scripting??? 

## Week 14 

ssh keys
ssh command - for login and running remote commands
scp command - for copying files between systems

tar 
if 

## Week 15 command 

tar				Backup and restore files
gzip				Zip and compress files
gunzip			Unzip files

