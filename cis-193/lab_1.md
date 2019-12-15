The purpose of this lab is to get you ready for subsequent assignments.
IntroductionIn this lab you will login to your Ubuntu VM and give it a static IP address. The address you use should be derived from the private network number you have been assigned.
VLab AccessYour password is derived from your name and your student ID. Here's how to figure out your username and password:
  * lll = first 3 letters of your last name (lowercase)
  * fff = first 3 letters of your first name (lowercase)
  * Ff = first 2 letters of your first name (first letter uppercase)
  * Ll = first 2 letters of your last name (first letter uppercase)
  * nnnn = last 4 digits of your student ID
  * ccc = The course number (with no letters)

Your username is:
  * cislab\lllfffccc

Your password is:
  * FfLlnnnn

Here's an example:
  * Michael Matera (student ID 12345678)
  * Class: CIS-193
  * Username: cislab\matmic193
  * Password: MiMa5678

Once you have logged in, rename one of the "Student XX" folders and give it your name. Please use a name that I will recognize. There are two servers in the folder. They are networked together according to the following diagram:CIS 193 Network Diagram
Take a screen capture of your VMs in your renamed folder.
Give Ubuntu a Static IP AddressUbuntu will act like a router and gateway to your Fedora machine. You must give it a static IP address on eth0. The static IP address is derived from your private network number. You can find your private network number in VMware. The network number will be visible in the summary tab of both the web and RDP based interface. The pictures below show the locations in both interfaces.


![image](../images/netnumber_webdb2f.png)





![image](../images/netnumber_wine619.png)



Your network number will be between 1 and 100. Set the IP information on Ubuntu's eth0 as follows:
  * IPv4

  * Address: 172.20.193.X (Where X is your network number).
  * Netmask: 255.255.0.0
  * Gateway: 172.20.0.1
  * Nameservers: 172.30.5.101 and 172.30.5.102 (you can use any valid nameserver)

  * IPv6

  * Address/Mask 2607:f380:80f:f830:193:X::1/64 (Where x is your network number)
  * Do not set the gateway!

If you have completed the setup you should be able to ping "www.google.com" successfully. You can leave the IPv6 configuration in its default state. Take a screen capture of the output of the "ifconfig" command.
Turn In
  - A screenshot of your VM folder
  - A screenshot of the output of ifconfig

Submit your homework on[blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for each screenshot

