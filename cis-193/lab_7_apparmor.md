The purpose of this lab is to create your first AppArmor profile.
IntroductionHigh security systems are secured against known threats (by installing a firewall and software updates) and secured against unknown threats. Mandatory Access Control (MAC) is a way to secure your system against unknown threats by restricting what programs and users can do to only what is "normal" for them. Thus, if a program becomes infected or a user account gets hacked the attacker will be fenced in by rules defined by the system's administrator. In this lab you will discover what is normal for the frodo program and create an AppArmor profile that restricts frodo to game play.
Learn a Program's Normal BehaviorFor this part you will begin to build a profile for the frodo program. One way to build a new profile is to run the program in "complain" mode and have Ubuntu automatically turn the complaints into rules. In frodo's case this will generate very lenient rules. For this lab you should build the rules one at a time by watching for "Permission Denied" messages from frodo and adding rules that fix the problem.
Download a copy of the CIS 98 "frodo" program using wget:
wget http://opus.cis.cabrillo.edu/cis193/frodo-lab7.tar.gz
Extract the executable using tar. The archive contains two files, "frodo" and "map". You can install frodo anywhere but make a note of Frodo's absolute path. That will be needed in the next step.
Create a Profile for FrodoNow that frodo is installed you should create a basic profile for him. In /etc/apparmor.d create a file and give it this basic contents:
#include <tunables/global>
/the/path/to/frodo { #include <abstractions/base>
 # Allow frodo to run BASH /bin/bash ix,
 # Allow frodo to read himself and his map/the/path/to/frodor, /the/path/to/map r,}
Be sure you replace /the/path/to with the path you noted in the previous step. Anytime you change rules you must run the following command for them to take effect:
service apparmor reload
Profile FrodoWith your AppArmor profile installed and activated you can now run frodo. When you run frodo for the first time you will see a error messages like this:
frodo: line 357: /usr/bin/dirname: Permission deniedfrodo: line 16: /usr/bin/clear: Permission deniedfrodo: line 313: /bin/grep: Permission deniedfrodo: line 313: /bin/sed: Permission denied
These are executable programs that Frodo depends on. Add these to the allowable programs in your profile.
Be a HackerNow that frodo has been armored you can test if the protection works. When frodo is running the '7' command allows you to execute an arbitrary shell script. This is sometimes known as a shell escape and it's a goldmine for hackers because it allows them to do anything with the privilege of the program. Create a shell script that uses the ping command and call it. If your profile is correct you will get a permission denied error.
Turn In
  - Your AppArmor profile

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 20 points for a correct profile

