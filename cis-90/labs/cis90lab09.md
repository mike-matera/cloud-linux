# Lab 9: Editing files with vi

In this lab you will use the vi editor to create new files and edit existing files.

## Preparation

- Find and skim Lesson 11 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)
- Check the forum for news on this lab: [http://oslab.cis.cabrillo.edu/forum/](http://oslab.cis.cabrillo.edu/forum/)
- For additional assistance come to the CIS Lab: [http://webhawks.org/~cislab/](http://webhawks.org/~cislab/)

## Procedure

Log on to Opus so that you have a command line shell at your service. Change directory to _edits_ to start this lab.

1. Create a text file called _home_ using **vi** and insert the following lines:

**cd**

**clear**

**echo This is the home directory of $LOGNAME**

**echo =======================================**

**ls -F**

1. Use the **chmod** command to set the permissions on the file, home to rwxr-xr-x.

1. Enter the command **home** and see what happens. Is it what you would expect?

1. Move this shell script you have just made to your _bin_ directory,

so that you may run it from anywhere on the system.

Congratulations: you have just written your first shell script!

1. Run the spell command on the file _small\_town_:

**spell small\_town**

Note all the misspelled words.

1. Make a permanent list of the above misspelled words by running the **spell** command again, but this time, redirect the output to a file called, _words_.

1. Use vi to edit the small\_town file and:

- correct all the misspelled words.

- move the "Reprinted from ..." line to the bottom.

- get rid of duplicate lines, repeated words and extraneous characters in the file.

- use a consistent indentation.

- fix the typo on the line: "The biggest business on town ..." (change to in)

- fix the typo on the line: "The airport runaway..." (change to runway)

TIPS:

- use the **dd** command to delete lines.

- use **yy** and **p** commands to copy and paste.

- use **/string** command to search for misspelled words.

- use **x** command to delete single characters.

- use **i** command to do normal notepad-like screen editing, and **Esc** to get back to command mode.

- use two login Putty sessions, one to edit _small\_town_, the other for _words_.

1. When you have fixed all the spelling errors, run the **spell** command again.

What should be done with words like "Ayshire", "moshpit" or "mashpit" that aren't in UNIX's dictionary?

1. Edit the file _words_ and remove all the misspelled words that you have corrected. (Only Ayshire and moshpit should remain in the file.)

1. Enter the following three commands from your shell prompt:

**date**

**echo Now is the time for all good men to come to the aid of their party**

**cal**

Use command line editing to redisplay the **echo** command, and change the word men to women. Then re-execute the command. Hint: to enter command line editing mode, press the up-arrow key.

1. Re-execute the command once more, but this time redirect the output to a file called _women_. You should now have a file named women with a single line in it.

1. Here is a little project for you to accomplish on a UNIX system:

- I have emailed a message titled, "Winter is coming" to your Opus account. Read your mail and save this message to a file called, _vocab_ in your _edits_ directory.
- **vi** the _vocab_ file and remove the numbers and spacing in front of each definition. Also remove the extraneous mail headers.
- If a line wraps around to two lines then edit it so it all fits on one line.
- Sort this list so that it is in dictionary order and save the results in a temporary file.
- Rename the above temporary file to _vocab_. Now your vocabulary list is in alphabetic order. Make any necessary adjustments to the file, e.g. making sure the title is at the top of the page and that there are no broken sentences.

## Extra Credit (optional)

Make a one-page website on Opus-II (2 points)

1. In your home directory create a directory named _cis90\_html_ and in that directory create two more directories named _css_ and _images_.
2. Make sure these new directories AND your home directory have read and execute permission for Others.
3. There are three files you will need from the _/home/cis90/depot directory_ named _index.html,_ _base_.css and _pengmovie.gif._
  1. Copy _index.html_ to your _cis90\_html/_ directory.
  2. Copy _base_.css to your _css/_ directory.
  3. Copy _pengmovie.gif_to your _images/_ directory.
4. Edit and personalize the _index.html_ file with your name and recommendations.
5. Change the SELinux context of your _cis90\_html/_ directory to allow web publishing:

**chcon -R -t httpd\_sys\_content\_t cis90\_html**

1. Browse to your new website using http://opus-ii.cis.cabrillo.edu/~_username__(replace_ _username_ _with your Opus-II username)_
2. Feel free to optionally modify the CSS styling in the _base.css_ file.
3. Post the URL for your new website on the forum and invite classmates to check it out.
4. Include your _index.html_ file in your lab09 file (see Submittal section below).

## Submittal

To get credit for this lab, you must send me all the files that you have created or edited in this lab.

1. Bundle (concatenate) the files below into a single text file in your home directory named _lab09_:

_home_

_words_

_small\_town_

_women_

_vocab_

_index.html_ (extra credit)

1. Copy your _lab09_ file to the _/home/rsimms/turnin/cis90_ directory renaming it as _lab09.$LOGNAME_. This can be done in a single command.

You can submit as many times as you like up to the deadline. After you submit you will receive an email on Opus-II. Read this email to verify whether your submission succeeded or failed. If you run out of time be sure to submit what you have for partial credit. Run **check9** to check your work and make sure you didn't forget anything.

Be sure to verify that your submittal was completed before the deadline. **Remember late work is not accepted.**

## Grading Rubric (30 points total)

5 points for correct version of _home_

8 points for correct version of _small\_town_

2 points for correct version of _words_

2 points for correct version of _women_

8 points for correct version of _vocab_

5 points for correctly submitting _lab09_ file

Less 1 point for each step or portion of a step not completed correctly

2 points extra credit for making a website

2 points extra credit for making your Arya into a webserver (see below)

## Even More Extra Credit (optional)

Make your Arya into a web server for HTML and PHP pages using XAMPP (2 points)

_username_ is your username on Opus-II

_172.20.90.1xx_is your Arya-_xx_ IP address (where _xx_ is your Arya number)

1. Log in as cis90 on your Arya.
2. Enter the following commands:

**sudo apt-get update**

**sudo apt-get upgrade** _(take defaults)_

**sudo init 6** _(log back in after the reboot)_

**wget https://www.apachefriends.org/xampp-files/7.2.11/xampp-linux-x64-7.2.11-0-installer.run**

**chmod +x xampp-linux-x64-7.2.11-0-installer.run**

**sudo ./xampp-linux-x64-7.2.11-0-installer.run** _(take defaults)_

**sudo /opt/lampp/lampp start**

**cd /opt/lampp/htdocs**

**sudo scp** _username_ **@opus-ii:/home/cis90/depot/benji.\* .**

**sudo scp** _username_ **@opus-ii:/home/cis90/depot/pumpkins.\* .**

**sudo mkdir images**

**cd images**

**sudo scp** _username_ **@opus-ii:/home/cis90/depot/\*.jpg .**

1. Test by browsing from the Arya belonging to tbd07, tbd08 or tbd09:
  - http://_172.20.90.1xx_/pumpkins.html
  - http://_172.20.90.1xx_/pumpkins.php
  - http://_172.20.90.1xx_/benji.html
  - http://_172.20.90.1xx_/benji.php

1. Email a screen shot of browsing to one or both of your PHP web pages to risimms@cabrillo.edu. Make sure it shows the URL and dynamic content.

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
