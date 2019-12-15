In this lab you'll construct a basic firewall then add some advanced features.
IntroductionNetfilter is among the most advanced firewall systems in the world. Industrial firewalls that use artificial intelligence to identify threats (like those from Palo Alto Networks) can be built on top of Netfilter.In this lab you'll use the ip6tables command to construct an IPv6 firewall. Your firewall will help keep out hackers by reducing the threat from password guessing attacks.
Setup Basic ProtectionFirst you will setup basic protection from the outside world. The policy on your INPUT chain must be DROP. When the INPUT policy is DROP you must explicitly allow any traffic through. This prevents problems where omissions cause holes in your firewall. Omissions in your firewall rules will instead cause a loss of connectivity. This can sometimes be challenging to debug but it's better than having a security hole that you don't notice until it's too late. The following rules ensure that basic services and connectivity will operate properly:
  - Allow all incoming packets from the loopback interface (lo)
  - Allow all incoming ICMPv6 packets

If you've done the above your VM will not have any open ports. You should verify this with a port scan. Next open a couple of ports so that your VM can host services on those ports:
  - Accept new connections on port TCP/22 for SSH
  - Accept new connections on port TCP/80 for HTTP
  - Accept new connections from the subnet 2607:f380:80f::/48 on port TCP/25

For full credit you should use the state or ctstate modules to open those ports, rather than just allowing all traffic on them. Remember to accept related and established traffic. When you're happy with your firewall, save your rules into a file with the following command:
ip6tables-save > part1.rules
Also, save the output of zenmap running against your firewall and submit that.
Slow The TrollsWhen the Internet notices you're running SSH the trolls will start knocking on your door with programs like [THC-Hydra](https://www.thc.org/thc-hydra/). Those programs guess common usernames and passwords looking for weak systems. If you created a "temporary" account for someone with a password like "1234" and forgot about it, the trolls will find you and turn you into a [spam bot](http://www.rackaid.com/blog/spam-ssh-tunnel/) (or possibly something [much worse](http://www.huffingtonpost.com/2009/11/09/internet_virus_frames_use_n_350426.html)). You cannot stop people from guessing passwords but you can slow them down. A successful attack depends on being able to guess huge a number of passwords (even to get a simple one like "1234"). Slowing down guesses protects you and it helps others by wasting a hacker's valuable time. 
For this part use the "recent" module to limit the rate at which an IP address can connect to SSH. The limit should be five connections per minute.When an IP address has more than five attempts in the last minute DROP subsequent attempts and log that the IP address was denied. If you have the recent module working it will record connections in a file located in the directory:
/proc/net/xt_recent
It's a good idea to check there for debugging. Test your rules by logging in to your machine six times quickly (the sixth should fail). Port scans with Zenmap will also count as at least one login attempt. When you're satisfied with your rules save them into a file called part2.rules.
ip6tables-save > part2.rules
Turn In
  - part1.rules
  - Zenmap output from part 1
  - part2.rules

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for part 1
  * 10 points for part 2

