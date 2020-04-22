# Lab 10: The Shell Environment

In this lab you will customize your login environment to suit your needs and preferences. By modifying environment variables and editing your _.bash_profile_ and _.bashrc_ files, you will customize your shell environment in a number of different ways.

## Procedure

Log on to Opus so that you have a command line shell at your service. Start this lab from your home directory.

### Environment Variables

1. Display the contents of your `PWD` environment variable. Change to your `bin` subdirectory and display the same variable. How did it change?
1. Change back to your home directory.
1. Display the contents of your `PATH` environment variable. Note the colon (`:`) separating the different directory names. What is the last directory in which the system searches for commands?
1. Make a new environment variable called `GREETING` and assign it an appropriate salutation. Don't forget to use quotes if your message has whitespace in it.
1. Use the `env` command to see if it is in your environment. Is it there? What must you do to put it in the environment?
1. Export the variable `GREETING` and use `env` to verify it's there.
1. Invoke a new bash shell process by typing:

	`bash`

	Now use the `unset` command to unset the variable `PS1`. What Happened?

1. Reset the PS1 variable by entering the following command:

	`PS1="Yes master: "`

	What happens to your primary prompt?

1. Now exit out of the child shell by typing `Ctrl-D`. What is the prompt now? What does this tell you about the effect changes made by children have on their parents?

### The `.bashrc` File

Aliasing is a mechanism provided by the bash shell that allows you to define your own commands, or to redefine UNIX commands. Alias definitions should be stored in your `.bashrc` file Normally, `.bashrc` is a file that you own and you are free to change. On Opus3 I accidentally made your `.bashrc` a symlink. You have to fix that.

1. Fix your `.bashrc` by overwriting the simlink. 

	```
	rm ~/.bashrc
	cp /etc/skel/.bashrc ~/.bashrc
	```

1. Edit the `.bashrc` file in your home directory by adding the following three lines to the bottom of the file:

	```
	alias bye="clear; exit"
	alias rm="rm -i"
	alias bill="cd /home/cis90/${LOGNAME}/poems/Shakespeare"
	```

1. Edit your `.bashrc` and make the following changes:

	1. Add a command to set your `umask` to: `umask 006`
	1. Below the `umask` command line, turn messaging off with the command:

		`mesg n`

	1. Add a shell environment variable named, `BIRTHDAY` and set it equal to the date of your birth (it doesn't have to be your real birthday) using the format `mm/dd/yy`.
	1. Export this variable, since you will want your children to know when your birthday is.
	1. Now that you have made these changes, run your `.bashrc` file using the UNIX dot source command:

		`source .bashrc`

1. Try out your new `rm` command by removing some file you don't need anymore.
2. Run your `bill` command. What happens?
3. Try out your `bye` command.

## Submittal

To turn in your lab submit your `.bashrc` file on Canvas.