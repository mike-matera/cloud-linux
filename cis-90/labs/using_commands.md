# Lab 2:  Using Commands

The purpose of this lab is to explore command usage with the shell and miscellaneous UNIX commands.

## Procedure

> This lab must be done on opus3 to get credit

Please log into the opus3 server at opus3.cis.cabrillo.edu You will need to use the following commands in this lab.

 * banner
 * bash 
 * bc
 * cal
 * clear
 * date
 * echo
 * exit
 * history
 * id
 * man
 * ps
 * type
 * uname
 * who   

Answer each of the questions below and be sure to issue all commands asked for. Turn these answers in on Canvas. Your command history will be scanned to verify you issued ALL the commands asked for below as well as any commands necessary to correctly answer the questions. Your answers and your command history will be graded.

## The Shell

1. There are a number of different command line shells that are available such as the Bourne shell (`sh`), the Bourne Again Shell (`bash`), the Korn shell (`ksh`), the C shell (`csh`), and many others.

    What shell are you currently using on Opus?
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    What command did you use to determine this?
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
    (Hint: We did this in Lab 1)

2. Unix commands are located in multiple directories in the Unix file tree such as `/bin`, `/usr/bin`, `/sbin`, `/usr/sbin`,  etc.  The `type` command will search to locate commands. Use the name of the command you want to search for as an argument on the `type` command. For example, to locate the `ps` command use:

    ```bash
    $ type ps  
    ps is /bin/ps
    ```

    The first occurrence of the `ps` command was found in the `/bin` directory. Now it's your turn.  Use the type   command and locate each of the following commands:

    Command Directory where command was located

    man _____________________________________
    
    uname _____________________________________
    
    tryme _____________________________________
    
    echo _____________________________________
    
    type _____________________________________
    
    bogus _____________________________________
    
    bash _____________________________________
    
    scavenge _____________________________________

    Issue this command:

    ```bash
    $ type ps tty ifconfig  
    ```

    Does the `type` command accept multiple arguments? _______ (yes or no)

3. Use the following to display your terminal type and your terminal device:

    ```bash
    $ echo $TERM  
    $ tty  
    ```

    Is your terminal type (`$TERM`) the same as your terminal device (`tty` output)?

    __________ (yes or no)

    Set the TERM variable to `dumb`, show the new value, and execute the   `clear` command.

    ```bash
    $ TERM="dumb"  
    $ echo $TERM  
    $ clear  
    ```

    What happens?  \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    Change the terminal type to `vt100` or `ansi`.

    ```bash
    $ TERM="ansi"  
    $ echo $TERM  
    $ clear  
    ```

    What happens?  \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    Set the `TERM` environment variable back to what it was when you logged in.

    ```bash
    $ TERM="xterm"  
    ```

4. What happens when you enter the following commands?

    DATE                \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

	Date                \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

    date                \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

    Why? \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

5. What results do you get from the command:

    ```bash
    $ who -g
    ```

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    What program outputs the `invalid option` error message?  \_\_\_\_\_\_\_\_\_\_\_\_\_\_

6. Enter each command below (exactly) and observe the results.

    ```bash
    echo one  two         threefour  
    ```
    > Be sure to include the extra spaces in the command above.

    Number of arguments in the command above is: \_\_\_\_\_\_

    ```bash
    echo "My TERM type is" $TERM  
    ```

    Number of arguments in the command above is: \_\_\_\_\_\_

    ```bash
    echo one.two.three  
    ```

    Number of arguments in the command above is: \_\_\_\_\_\_

7. Issue the following command:

    ```bash
    echo red 'white  
    and blue'
    ```

    What does the shell do when the closing quote mark is missing?

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    Issue the following command (press Enter immediately after the backslash):

    ```bash
    echo red white \  
    and blue  
    ```

    What does the shell do when you escape the invisible newline character at the end of the command line?

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

8. Use the shell metacharacter `;` to write out a one line command that will clear the screen, print out the date and the current month's calendar:

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

9. What `uname` command including options would output ONLY the network node hostname, the kernel release number and the operating system?

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    Your command should produce output similar to:

    ```
    opus3 3.10.0-862.9.1.el7.x86_64 GNU/Linux
    ```

    > Hint:  Use the `man uname` command, scroll up/down and use `q` to quit.

10. What is the difference in output between the following two commands?

    ```bash
    banner I am fine  
    banner "I am fine"  
    ```

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

11. What is the UID (User ID) number for your own account?

    \_\_\_\_\_\_\_\_\_  (Hint:  we did this in Lab 1)

## Using online documentation

12. Issue a `man bc` command to read the `bc` manual page. Scroll up and down then use `q` to quit.

13. Is `tryme` a UNIX command?  \_\_\_\_\_\_ (yes or no)
Hint: Use the documentation commands you know to find out.

14. What `who` command including options will output a count of the number of users logged on?

    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

    Hint: Read the man (manual) page for the   who   command and experiment.

15. Run the command: `man -k boot` Use the manual pages to find out what the `-k` option does. What command is `man -k`   equivalent to \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
Run the equivalent command and verify.

16. Here's a challenging task: Use the `man` command to discover how you can use the `bc` command to obtain the square root of 361. The `bc` command is an example of an interactive command, because you must enter the numbers to calculate from the keyboard while the program is running.

## Submit your work

Submit a document with your answers on Canvas. Your command history on opus3 will be graded in addition to the document you submit. 
