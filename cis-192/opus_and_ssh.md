This page will show you how to be productive on Linux VMs using Opus and the SSH command.
IntroductionSecure Shell (SSH) is an important tool for any UNIX administrator. It gives you secure access to your machines, transfers files securely and acts as a VPN. This guide will show you how to use some of that power to simplify tasks that you face in my CIS classes.
Logging Into OpusLog in to Opus using SSH. SSH is built into Linux and Mac computers. On Windows you will have to use PuTTY. You can download PuTTY [here](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html). From the command line on Linux or Mac you login with this command:
ssh -p 2220 <my-username>@opus.cis.cabrillo.edu
If you are already on the CIS network you can simplify that somewhat with this command:
ssh <my-username>@opus
Simplify Opus LoginYou can simplify the process of logging in to Opus by using SSH's configuration file on your home computer. Add the following lines to ~/.ssh/config

Host opus  HostName opus.cis.cabrillo.edu  User <my-username>  Port 2220

Now you can SSH in to Opus by running the simple command:
ssh opus

Go PasswordlessSSH lets you securely login without a password. This is a tremendous time saver and everyone should set it up. You will be much more productive. On your home machine (Linux or Mac) run the following command:
ssh-keygen
This will generate a file in your home directory called ~/.ssh/id_rsa.pub. You must copy that file to Opus and rename it. The following line uses the Secure Copy (SCP) command to do that (it should be run on your home machine):
scp -P 2220 ~/.ssh/id_rsa.pub <my-username>@opus.cis.cabrillo.edu:~/.ssh/authorized_keys
If you have properly installed your key you should be able to login to Opus without a password using the command in the last session.
Repeat for your VMsLogging into opus quickly is useful but logging into your VMs is where you really want to go. To do that create a public/private key on Opus the same way you did on your home computer. Then install your public key on each of your VMs. From Opus:
ssh-keygenssh-copy-id student@<my-vm-ip-address>
If you don't want to remember your VM's IP addresses you can store them in your SSH configuration file on Opus:
Host vmrouter HostName 172.20.192.4 # replace this with your VMs IP address User student
Now you will be able to quickly login to your VMs from Opus like this:
ssh vmrouter
Nested VMsIn CIS 192 you have VMs that aren't accessible directly from Opus. You will need to create SSH tunnels that give you access to the VMs behind your router VM. In your SSH configuration file add a stanza for your router that creates tunnels to your other VMs:
Host router HostName <my-router-ip-address> User student LocalForward 22223 <switch-vm-internal-ip-address>:22 LocalForward 22224 <web-server-vm-internal-ip-address>:22 LocalForward 22225 <db-server-vm-internal-ip-address>:22
Host switch HostName localhost Port 22223 User student
Host web-server HostName localhost Port 22224 User student
Host db-server HostName localhost Port 22225 User student
NOTE: You cannot share port numbers with other students, make up random ones!With that configuration file you will be able to login to your switch and server VMs directly from Opus ONLY AFTER you've first logged into your router. To make things really fast make sure your public key is installed on all of your VMs:
# do this from opusssh-copy-id -i ~/.ssh/id_rsa.pub student@switchssh-copy-id-i ~/.ssh/id_rsa.pubstudent@server1ssh-copy-id-i ~/.ssh/id_rsa.pubstudent@server2
Now you can work like a professional.