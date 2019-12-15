In this lab you will setup auditing.
IntroductionAuditing is an important part of hardening a Linux system. It allows administrators to keep records of what users of the machine are doing. Those records can be a key to investigating problems with the machine and are an important deterrent against hackers. You can do this lab on Ubuntu or Fedora.
Watch for Configuration ChangesFor the first part of the lab you will harden the /etc directory. This is the directory on Linux that contains most of the machine's configuration. On a high-security system administrators must be held accountable for any changes made to the /etc directory. Complete this step by:
  - Auditing all writes and attribute changes to all items in the /etc directory (including subdirectories)
  - Create a user called "hax0r"
  - Use ausearch to extract the audit reports from step 2

Hint: Setting a key that identifies your audit messages will make using ausearch easier. You should verify that your search results contain the modifications to /etc/passwd, /etc/shadow and possibly /etc/group using aureport. When you are satisfied with your result save the output of ausearch to a file called etc_audit.log and submit the file on blackboard.
Evaluate a Program using autraceFor this part you will use the autrace program to audit every system call a program makes. The autrace program works in a similar way to the strace program except that the output is stored to the audit logs instead of STDOUT. The autrace program can be very useful if you want to evaluate a third-party application to see if it's doing something that it shouldn't. Of course, if you really suspect that a program is malicious you should audit it in an isolated VM.
Download a copy of the CIS 98 "frodo" program using wget:
wget http://opus.cis.cabrillo.edu/cis193/frodo.tar.gz
Extract the executable using tar. The archive contains two files, "frodo" and "map". You should be with both files in the current directory you should be able to run it like this:
./frodo
Use autrace to trace frodo. Make a few moves and exit. Analyze what frodo did using the aureport command. Submit the log of frodo's execution on Blackboard.I have hidden (possibly) malicious code in Frodo. What is it doing? You should justify your answer using the audit logs.
Extra Credit: Every Step You Take (I'l be Watching You)You can use the audit system in concert with PAM to record every keystroke a user makes. The system lets you select particular users. For extra credit, enable this for a user of your choosing and submit an audit log showing me the keystrokes of your user.
Turn In
  - Your audit report from part 1 (etc_audit.log)
  - Your audit report from part 2 (frodo_audit.log) with the answer to my questions.
  - (Optional) Your audit report from part 3 for extra credit

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for part 1
  * 10 points for part 2
  * 10 points of extra credit.

