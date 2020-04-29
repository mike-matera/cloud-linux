# Writing Shell Scripts 

Shell scripts are executable files that contain shell commands. The shell exececutes the commands in order, just as if you had typed them into the command line. Shell scripts usually contain special syntax that enables them to do things conditionally and in loops. This week we'll start working with shell scripts. 

## Your First Script 

Use your favorite editor to copy-and-paste this simple shell script: 

```bash
#!/bin/bash

echo
echo "==> Entering child process <=="
ps -f
echo "==> showing variables in child <=="
echo "   roses are $roses"
echo "   violets are $violets"
echo "==> setting variables in child <=="
roses=black
violets=orange
echo "   roses are $roses"
echo "   violets are $violets"
echo "==> Leaving child process <=="
echo
```

Make the script executable and put the it into your `~/work` directory to start with. You can run it from `~/work` with the following command:

```bash 
$ ./flowers 
```

You can also run the script these ways: 

```bash 
$ source ./flowers
$ . ./flowers 
$ exec ./flowers 
```

What's the difference between them? 

Moving it into `~/bin` puts it into the `$PATH`. How does that change how you execute the file? 

## Taking Input 

Scripts are more useful if they change what they do based on input. There are two ways to get input from the user, interactively by prompting them or from the command line. Add these two lines to your `flowers` script before the first `echo` and after the `#!` or "shebang" line.

```bash
echo "What are roses?"
read roses 
echo "What are violets?"
read violets 
```

How rerun your script. What changed?

When you're happy that your script is taking inptut *comment out* those lines by placing a `#` hash mark in front of them so they look like this: 

```bash
#echo "What are roses?"
#read roses 
#echo "What are violets?"
#read violets 
```

Under those lines use the `$1` and `$2` special variables to set roses and violets equal to command line options:

```bash
roses=$1
violets=$2 
``` 

Now your `flowers` program takes command line arguments. 


