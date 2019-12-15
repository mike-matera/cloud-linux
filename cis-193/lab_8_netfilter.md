This lab will get you familiar with nmap and Zenmap, nmap's GUI.
IntroductionPort scanning is an important tool for understanding the defenses of a system on the network. Hackers use ports scans to look for weak machines on the network. You should use port scans to learn what hackers can learn about your systems. Nmap is a popular, open source, tool that performs many kinds of port scans. Nmap can perform some "stealth" scans. Those are port scans that use violations of the TCP protocol to trick an operating system into revealing that a service is listening even when the firewall is blocking it.
IMPORTANT: You will be learning a key security tool this week, that has proper and improper uses. A port scan is considered a hostile act when it originates from a stranger. You must only scan systems that you own or systems where you have been authorized by the owner to scan. Nmap's site has a great article about the [legal issues around port scanning](http://nmap.org/book/legal_issues.html).
Do an Initial ScanWith your Ubuntu firewall in it's default state use Zenmap to perform an "Intense scan, all TCP ports." From the command line that will look like:
nmap -p 1-65535 -T4 -A -v <your-ip-address>
Save the output of nmap into a file called "initial-scan.txt" to be submitted for credit. How long did the scan take? What ports are open?
Do a Second ScanOn your second scan you should enable the firewall. The firewall should be set to block all ports except for SSH. It's important to allow SSH so that you can stay logged in. If you don't perform the next steps in order your SSH session will freeze and you'll have to reboot.
Firewall setup:
iptables -A INPUT -i lo -j ACCEPTiptables -A INPUT -p icmp -j ACCEPTiptables -A INPUT -m state --state NEW -p tcp --dport 22 -j ACCEPTiptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPTiptables -P INPUT DROP
Repeat the same steps for your IPv6 firewall except be sure to allow ICMPv6 instead of ICMP:
ip6tables -A INPUT -p icmpv6 -j ACCEPT
Now repeat the scan from the first part and save the output to "second-scan.txt". How long did the second scan take? What ports are open?
Turn In
  - initial-scan.txt
  - second-scan.txt
  - Answers to the questions

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 5 points for each of your scan logs.
  * 10 points for answers to the questions.

