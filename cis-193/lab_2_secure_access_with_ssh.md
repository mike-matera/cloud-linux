In this lab you will customize SSH for secure and convenient access to class computers.
IntroductionIn this lab you will create a public/private key pair for use with SSH. The key will allow you to login to Opus and your VMs without using a password. Using keys this way is more secure than passwords because keys are much harder to guess and when you use keys you can disable password logins. This is especially useful for the root account which is a very high value target.
Part 1: Complete Your Network SetupLast week you setup the network on Ubuntu. In this lab you'll get Fedora connected too. The first step is to bring up the internal interface (eth1) on Ubuntu. Add the following lines to your /etc/network/interfaces file.
auto eth1iface eth1 inet static  address 10.193.0.1
  netmask 255.255.0.0

This will give your internal network interface the address 10.193.0.1. Because this is an internal interface all of your VMs can share it. Now you will need to configure Ubuntu to act as a router for Fedora. Do that by editing the file /etc/rc.local file. Add the following lines (above the exit line):
sysctl -w net.ipv4.ip_forward=1iptables -t nat -A POSTROUTING -s 10.193.0.0/16 -o eth0 -j MASQUERADE
Now use the GUI on Fedora to set the following network settings: IPv4 address: 10.193.0.2 Netmask: 255.255.0.0 Gateway: 10.193.0.1 Nameserver: 172.30.5.101
See the picture below:

![image](../images/fedorasettingsc31a.png)



Part 2: Create an SSH Key PairIt's simple to create an SSH key. You run the command on Opus:
ssh-keygen
That command will (by default) place your keys in the following files:
~/.ssh/id_rsa~/.ssh/id_rsa.pub
The *.pub key is your public key. You can do what you want with that, make it your email signature or post it on the Internet. The other one must be kept secret in order to stay secure. If your private key is on a shared computer (like Opus) you must encrypt it with a password. Be sure to encrypt the key you create with a password.
Part 3: Install Your Public KeyNow that you have a public key you must install it on any machine you want to be able to login to. To do this simply copy the contents of your id_dsa.pub into the file:
~/.ssh/authorized_keys
The authorized_keys file MUST be on the host you intend to login to. In other words if you want to login to your VM from Opus the private key must be on Opus and the public key must be in the authorized_keys file on your VM. You can have as many keys in your authorized_keys as you like. Once you have completed this step test that you can login as student without supplying student's password.
Part 4: Start SSH AgentAfter the last part of the lab you were able to login to your VM without typing in the user's password. Yet, you still had to type in the password for your private key. If you login again you'll have to type the password in again. That's because, by default, SSH agent is not started for you on Opus.
Turn In
  - Submit your public key with the IP address of your Ubuntu VM.

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 20 points for a public key that is installed on your VM

