# Introduction to iptables

This page will help you get your Firewall and NAT up and running. The information here is a simplification of the excellent [Ubuntu IptablesHowTo](https://help.ubuntu.com/community/IptablesHowTo). 

At this point in the class your IPv6 network is fully functional because there are plenty of IPv6 addresses to go around. Your IPv4, however, only has one address to use. Your router is in charge of "sharing" that address with the rest of the hosts on your network. This process is called Network Address Translation (NAT). On Linux the firewall system also performs NAT. This guide will show you the basic steps for getting a minimal firewall configured with NAT. Also, it will show you how to make your changes permanent.

You can find the lecture slides [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1KiNvG3XcVF0n7WIhMxBRziAwRYK_QX0zMrLpUfHjYT4/edit?usp=sharing).

## Commands 

  * iptables
  * ip6tables

## Configuration 

  * /etc/sysctl.conf
  * /etc/network/if-pre-up.d/firewall

## Further Reading 

  * [Ubuntu IptablesHowTo](https://help.ubuntu.com/community/IptablesHowTo)
  * [IP Masquerade HowTo](http://tldp.org/HOWTO/IP-Masquerade-HOWTO/)

## Enabling Packet Forwarding (Routing) 

By default Linux doesn't forward packets. You should have already turned on forwarding for IPv6. Before you begin working on your firewall you should double check that you have enabled forwarding for IPv4. To turn on forwarding you use the `sysctl` command. To turn on forwarding of IPv4 packets:

```
router$ sudo sysctl -w net.ipv4.ip_forward=1
```

These only set the configuration until a reboot. If you want to make the settings permanent you should uncomment the corresponding lines from `/etc/sysctl.conf`:

```
# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.ip_forward=1
```

Be sure that you have this done before you attempt to turn on NAT.

## Network Address Translation 

You must use NAT to make your private network hosts able to use the Internet. This is as simple as assigning a firewall rule. There is a complete HowTo on IP masquerade on the [Linux Documentation Project](http://tldp.org/HOWTO/IP-Masquerade-HOWTO/). NAT is performed (unsurprisingly) in the NAT table. To enable NAT for packets that originate from your internal network (10.192.0.0/16) and are being routed out via your ens192 interface run the following command:

```
router$ sudo iptables -t nat -A POSTROUTING -s 10.192.0.0/16 -o ens192 -j MASQUERADE
```

If you have completed all of the steps so far you should now see complete connectivity from your switch and your server VMs:

```
switch:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=58 time=5.04 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=58 time=4.60 ms
```

Verify that this is the case before you go on.

## Firewall Rules for Security 

Your router has the important job of keeping your network secure. You must secure both your network and the router itself. You must setup both an IPv4 and an IPv6 firewall to be secure. It's often the case that a mistake while configuring your firewall will lock you out of SSH. Be ready to get on the VMware console if that happens.

### IPv4 Stateless Rules 

Start by adding rules to your IPv4 INPUT chain. You add a rule like this:

```
iptables -A INPUT <rule-specification> -j <TARGET>
```

Add the following stateless rules:

  - Accept all packets coming from the loobpack device (`lo`)
  - Accept all packets coming from the `ens224` device
  - Accept all ICMP packets

### IPv4 Stateful Rules 

Now add stateful firewall rules. Stateful firewall rules know the difference between a packet from a new connection and a packet from an existing connection. Stateful rules are essential for security. To add a rule that matches a new connection you use the iptalbes command like this:

```
  iptables -A INPUT -m state --state NEW <rule-specification> -j ACCEPT
```

Stateful rules only apply to protocols that support connections, that's why we did the UDP rule above. Add stateful rules for new packets to do the following:
  
  - Accept connections on TCP/22 (SSH)

You must add the following rule to accept all related traffic:

```
router$ sudo iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Related traffic are packets that belong to existing connections. Those connections are formed by staring communication on one of the ports that has a "NEW" rule that you set above. If you don't use this rule you can initiate a connection but no packets will get through after that.

### IPv4 Forwarding Rules 

Your router should route! NAT does some of the firwalling for you. But you must tell your router what traffic is allowed to pass from inside to outside. Add the following rules to your FORWARD chain:

```
router$ sudo iptables -A FORWARD -i ens224 -o ens192 -j ACCEPT
router$ sudo iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
```

The first rules allows your network to pass packets to the outside world and the second makes it okay for related traffic to come back.

### IPv6 Stateless Rules 

Some of the rules in your IPv6 firewall are essentially the same as your IPv4 rules. However, some are specific to IPv6 and are there to make sure you're able to maintain the functionality your network currently has. Add the following rules to your IPv6 firewall:

  - Accept all packets from the loopback (`lo`) device
  - Accept all packets from the `ens224` device
  - Accept all ICMPv6 packets (in IPv6 the protocol should be `-p icmpv6`)
  - Accept packets with destination UDP/546 (DHCPv6)

### IPv6 Stateful Rules 

Now add stateful rules for IPv6. Add rules for the following:

  - Accept new connections on TCP/22 (SSH)
  - Accept related and established connections (as you did with IPv4)

### IPv6 Forwarding Rules 

The forwarding rules need to be more complete in IPv6. NAT prevents hosts from the internet from contacting your VMs. There is no NAT in IPv6 so you must protect your hosts explicitly using firewall rules. Add the following rules:

  - Accept all packets from `ens224` going to `ens192`
  - Accept ICMPv6 packets (the interfaces don't matter)
  - Accept new connections destined for TCP/22 (allow SSH into your VM network)
  - Accept related and established connections

### Set the Policy to DROP 

When your policy is DROP it's very helpful while debugging to see the packets that get dropped in the system log. Logging rules record packets that cross them but do not affect the travel of the packet. Add logging rules to your INPUT and FORWARD chains.

```
router$ sudo iptables -A INPUT -j LOG 
router$ sudo iptables -A FORWARD -j LOG 
router$ sudo ip6tables -A INPUT -j LOG 
router$ sudo ip6tables -A FORWARD -j LOG 
```

Finally verify that your firewall rules are complete:

```
router$ sudo iptables -L -n -v
```

If your firewall rules match mine above (order doesn't matter) you can set the policy on the INPUT and FORWARD chains to DROP. This will make it so any packets you don't explicitly allow will be discarded.

```
router$ sudo iptables -P INPUT DROP
router$ sudo iptables -P FORWARD DROP
```

Don't forget IPv6. Verify that your IPv6 firewall is complete:

```
router$ ip6tables -L -n -v
```

Once you're convinced that your IPv6 firewall matches the above set the INPUT and FORWARD policy to DROP:

```
router$ sudo ip6tables -P INPUT DROP
router$ sudo ip6tables -P FORWARD DROP
```

If you made a mistake you'll know it as soon as you run the first command above. If that's the case you can log into your VM over the console and run the following commands. First set the policy back to ACCEPT:

```
router$ sudo iptables -P INPUT ACCEPT

```

Next you can replace broken rules using the `-R` flag to `iptables` or you can use `-F` to start over:

```
router$ sudo iptables -F INPUT
router$ sudo iptables -F FORWARD
```

Those commands delete all of your rules!

## Making Firewall Rules Permanent 

There is no built-in way to make firewall rules permanent. To do it you will need to perform some simple scripting. First you will save your firewall rules in the file `/etc/default/iptables`. IPv4 and IPv6 firewall rules are saved separately. Do that with the following commands:

```
router$ sudo iptables-save | sudo tee /etc/default/iptables
router$ sudo ip6tables-save | sudo tee /etc/default/ip6tables
```

Now you need to create a script that will load your firewall rules every time you start the network. Ubuntu provides a convenient way to do that. All scripts in the `/etc/network/if-pre-up.d` directory will be run before the network interfaces are brought up. Place this script in that directory:

```
#! /bin/sh
# This is /etc/network/if-pre-up.d/firewall
iptables-restore < /etc/default/iptables
ip6tables-restore < /etc/default/ip6tables
exit 0
```

Be sure that you make it executable:

```
router$ sudo chmod ugo+rx /etc/network/if-pre-up.d/firewall
```

> IMPORTANT: Save your firewall rules any time you change them and want them to stick!

## Better Safe Than Sorry 

I strongly recommend you reboot your router after this to make absolutely certain your rules are working. There are, many, many things that can go wrong when you enable the firewall and start strictly enforcing rules. Some problems might not be obvious right away (e.g. not allowing DHCP through). The best thing to do is reboot your router and verify that the firewall is still there:

```
router$ sudo iptables -L -n -v
```

Check IPv6 too:

```
router$ sudo ip6tables -L -n -v
```

Make sure your firewall matches what you expect. Also, check to make sure that DHCP-PD worked again:

```
$ ip addr show dev ens224
3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
  link/ether 00:50:56:af:25:d3 brd ff:ff:ff:ff:ff:ff
  inet 10.192.0.1/16 brd 10.192.255.255 scope global ens192
   valid_lft forever preferred_lft forever
 inet6 2607:f380:80f:f900::1/64 scope global
   valid_lft forever preferred_lft forever
  inet6 fe80::250:56ff:feaf:25d3/64 scope link
   valid_lft forever preferred_lft forever
```

Notice that my internal interface has gotten it's IPv6 address. Great! Make sure you can SSH into and ping your router using both IPv4 and IPv6.
