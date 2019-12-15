In this lab you will configure PAM.
IntroductionIn this lab you will alter PAM's configuration files to perform a special task for you upon login. Usually when PAM is required to do a setup task that task must happen before the user's own environment is ready. One example is mounting the user's home directory. In this lab we'll do something a bit simpler. 
The Login TaskEvery time you login you must ping opus once and record the result to the file:
/var/log/opus-ping.log
Be sure you don't ping forever (use the -c argument to ping)
Modify PAM's ConfigurationIn order to make PAM perform the ping on login you must modify one of the files in /etc/pam.d to include your instruction. You must determine what file to modify and what instruction to place in it. HINT: Look at the pam_exec.so module. Once you are satisfied with your change you will submit the file you changed and a copy of /var/log/opus-ping.log on blackboard.
If You're StuckPAM logs its activities in the file:
/var/log/auth.log
If you don't know what's wrong try looking there. You will get more information if you give the "debug" argument to the pam_exec.so module. Always use absolute paths to executables that you run with PAM, you don't know what the $PATH environment variable is set to (it may be empty).
Turn In
  - The PAM configuration file you changed.
  - The file /var/log/opus-ping.log

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 20 points for a correct change

