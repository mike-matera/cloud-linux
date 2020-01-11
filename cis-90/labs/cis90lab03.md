# Lab 3: The Unix Mail System

The goal of this lab is to become proficient with using the Unix mail utility to send and receive mail messages.

**Preparation and getting help**

1. Find and skim Lesson 3 slides: [http://simms-teach.com/docs/cis90/cis90lesson03.pdf](http://simms-teach.com/docs/cis90/cis90lesson03.pdf)
2. Check the forum for the latest news on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)
3. Watch Benji and Homer start this lab: [https://www.youtube.com/watch?v=0pD-vbaC-GE&feature=youtu.be](https://www.youtube.com/watch?v=0pD-vbaC-GE&feature=youtu.be)
4. For additional help work the lab with a tutor. Click the "Tutors" link at the top of the my website: [https://simms-teach.com/](https://simms-teach.com/)

## Procedure

**Start early and check your Opus-II email every day!**

Log on to Opus-II so that you have a command line shell at your service. Be sure that you are in your home directory to do this lab.

You will receive a mail message from me with a Unix historical event for a particular year. Save this message to a mailbox called _uhistory_.

The objective of this lab is to use Unix mail to exchange and collect at least 15 individual events with your classmates. There are more students than events so some students will receive the same event.

Start by sending an email to your other classmates with your event and ask them to send you their events. Each time you get a Unix event that you haven't already saved, save it to your _uhistory_ mailbox.

**Rules**

- Do this lab on Opus-II using the **mail** command.
- Only the events that were originally sent to students by the instructor may be exchanged. Students should not make their own events. Use the **check3** script to identify any unofficial events. Unofficial events will not earn any credit towards the overall grading score.
- When someone asks you for the date that you received, you must send it to them with the subject being just the year of the event, e.g. 1972 with no quotes. The email message must contain the complete line of event text for that year.
- Each message saved in _uhistory_ must be for a single event/year. The message body should have the complete event line as originally sent by the instructor.
- Each message saved in _uhistory_ must have a subject that is just the year of the event e.g. "1968" and nothing else. If the subject date shows with extra quotes, e.g. ""1968"" then request a corrected version.

If you receive an email that is missing the event or does not have the year as the subject, reply to the sender and ask them to resend a corrected version.

When you get all the Unix event messages saved in your _uhistory_ mailbox you should have up to 22 messages, each with a different date for the Subject field. Delete any duplicate dates you may have.

Tip: Use the distribution list _cis90-students_ to send a message to all students in the class.

Tip: You only need to specify the username when sending email to other Opus-II users. For example, **mail simben90** is equivalent to **mail simben90@opus-ii.cis.cabrillo.edu**.

**Submit your work**

To get credit you must submit your work. You can do this by entering the **submit** command. When asked for which lab, enter 3. You can submit as many times as you like up to the deadline. If you run out of time be sure to submit what you have for partial credit.

Use **check3** to tally your events and check for duplicates. Use **verify** to verify that you submitted your work and to see what you submitted.

**Grading Rubric (30 points total)**

- Each unique official event with a correct subject and complete body is worth 2 points up to a maximum of 30 points. Each event must meet the rules above and be in the submitted _uhistory_ file.
- If duplicates are found in the submitted uhistory file 2 points will be lost.

Be sure to submit your work before the deadline. **Remember, late work is not accepted.**

**Extra Credit**

- 2 points - collect all 22 events.
- 1 point - using VLab (not SSH), login into virtualterminaltty3 as the cis90 user on your Arya VM and issue these four commands:

**sudo apt-get update**

**sudo apt-get upgrade**

_Installs latest updates_

**sudo apt-get install mailutils heirloom-mailx**

_Installs the mail utilities and mailx program_

_Take all the defaults (just hit Enter key) on any questions asked_

- _General type of mail configuration: Internet site_
- _System mail name: Arya-xx_

**echo $(tty) $(hostname)** _first__last_ **| mail -s "L3 Bonus" rsimms@opus-ii.cis.cabrillo.edu**

_Replace first and last with your first and last name._

_This sends me a message with your terminal device, hostname and name with a subject of "L3 Bonus"._

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
