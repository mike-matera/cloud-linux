# Lab 11: Editing files with vi

In this lab you will use the vi editor to create new files and edit existing files.

## Procedure

Log on to opus3 so that you have a command line shell at your service. Change directory to `edits` to start this lab.

1. Create a text file called `home` using `vi` and insert the following lines:

    ```
    cd
    clear
    echo This is the home directory of $LOGNAME
    echo =======================================
    ls -F
    ```

1. Use the `chmod` command to set the permissions on the file, home to `rwxr-xr-x`.

1. Enter the command `home` and see what happens. Is it what you would expect?

1. Move this shell script you have just made to your `bin` directory, so that you may run it from anywhere on the system.

    **Congratulations: you have just written your first shell script!**

1. Run the spell command on the file `small_town`:

    `spell small_town`

    Note all the misspelled words.

1. Make a permanent list of the above misspelled words by running the `spell` command again, but this time, redirect the output to a file called `words`.

1. Use vi to edit the `small_town` file and:

    1. correct all the misspelled words.
    1. move the "Reprinted from ..." line to the bottom.
    1. get rid of duplicate lines, repeated words and extraneous characters in the file.
    1. use a consistent indentation.
    1. fix the typo on the line: "The biggest business on town ..." (change to in)
    1. fix the typo on the line: "The airport runaway..." (change to runway)


    <br>Tips: 

    - use the `dd` command to delete lines.
    - use `yy` and `p` commands to copy and paste.
    - use `/string` command to search for misspelled words.
    - use `x` command to delete single characters.
    - use `i` command to do normal notepad-like screen editing, and `Esc` to get back to command mode.
    - use two login terminal sessions, one to edit `small_town`, the other for `words`.

1. When you have fixed all the spelling errors, run the `spell` command again.

1. Edit the file `words` and remove all the misspelled words that you have corrected. (Only Ayshire and moshpit should remain in the file.)

1. Enter the following three commands from your shell prompt:

    ```
    date
    echo Now is the time for all good men to come to the aid of their party
    cal
    ```

    Use command line editing to redisplay the `echo` command, and change the word men to women. Then re-execute the command. Hint: to enter command line editing mode, press the up-arrow key.

1. Re-execute the command once more, but this time redirect the output to a file called `women`. You should now have a file named `women` with a single line in it.

## Submittal

To get credit for this lab, you must send me all the files that you have created or edited in this lab.

1. Bundle (concatenate) the files below into a single text file in your home directory named `lab09`:

    1. `home`
    1. `words`
    1. `small_town`
    1. `women`

1. Copy your `lab09` file to the `/home/mmatera/turnin` directory renaming it as `lab09.$LOGNAME`. This can be done in a single command.

You can submit as many times as you like up to the deadline. Run `check9` to check your work and make sure you didn't forget anything.
