# Stop and Debug! 

This week we take a break from instruction so that you can get any problems with your project figured out.

## Good Debugging Procedure 

When you have a problem the best way to find the root cause is to change one thing at a time. If the change you made doesn't fix your problem, back it off and try another change. One thing I frequently see happen to students is that by leaving failed changes in place they make their network worse. Sometimes much worse. It takes discipline to work cautiously and it feels like you're moving too slowly. But, discipline pays dividends. You will find your problems much, much more quickly if you only change one thing at a time.

## Project Checklist 

Take a week to verify that your project is fully operational. After this week the changes will become a bit more complicated, so you'll want to be sure everything is operating on a stable foundation.

### 1. Reboot Every VM 

Before you begin this checkup make sure that every VM has all configuration stored on disk. When I grade you, I'll ask to see the output of 'uptime' so that I know your VMs have recently rebooted. You can reboot them in any order. If all is well they will eventually come back online.

### 2. Check Host Names 

Each of your machines should have an assigned hostname. Verify that you have set your new hostname in two places: `/etc/hostname` and `/etc/hosts`. At this point your hosts files should not have any other than the local host in them. We'll do DNS after spring break:

```
$ cat /etc/hostname
router
```

The hostname is set to router.

```
router$ cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	router

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

The name router is bound to the loopback address. If sudo takes a loooooooooooong time it's because you don't have your name set properly in `/etc/hosts`.

### 3. Check IP Addresses 

Start with your router. It has two interfaces. Use ifconfig to verify that they have both IPv4 and IPv6 addresses set:

```
router$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:99:3c:6e brd ff:ff:ff:ff:ff:ff
    inet 172.19.192.30/16 brd 172.19.255.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 2607:f380:80f:f192::30/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:fe99:3c6e/64 scope link 
       valid_lft forever preferred_lft forever
3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:99:6d:3a brd ff:ff:ff:ff:ff:ff
    inet 10.192.0.1/16 brd 10.192.255.255 scope global ens224
       valid_lft forever preferred_lft forever
    inet6 2607:f380:80f:f900::1/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:fe99:6d3a/64 scope link 
       valid_lft forever preferred_lft forever
```

If the IP address information on ens192 is incorrect go back to the instructions in [Get Connected](../milestones/get_connected.md). If you don't see an IPv4 address on ens224 go back to [Get Connected](../milestones/get_connected.md). If you don't see an IPv6 address on ens224 go back to [SLAAC](../pages/slaac.md). Now check your switch:

```
switch$ ip addr 
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
    link/ether 00:50:56:99:0b:10 brd ff:ff:ff:ff:ff:ff
3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
    link/ether 00:50:56:99:7c:78 brd ff:ff:ff:ff:ff:ff
4: ens256: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
    link/ether 00:50:56:99:42:62 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::250:56ff:fe99:4262/64 scope link 
       valid_lft forever preferred_lft forever
5: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:50:56:99:0b:10 brd ff:ff:ff:ff:ff:ff
    inet 10.192.0.2/16 brd 10.192.255.255 scope global br0
       valid_lft forever preferred_lft forever
    inet6 2607:f380:80f:f900:242e:3bb:6c67:9bbe/64 scope global temporary dynamic 
       valid_lft 86386sec preferred_lft 14386sec
    inet6 2607:f380:80f:f900:250:56ff:fe99:b10/64 scope global mngtmpaddr dynamic 
       valid_lft 86386sec preferred_lft 14386sec
    inet6 fe80::250:56ff:fe99:b10/64 scope link 
       valid_lft forever preferred_lft forever
```

You should have a bridge interface with IPv6 addresses assigned. If you don't see IPv6 addresses go back to [SLAAC](../pages/slaac.md). If you don't have an IPv4 address verify that you've completed the steps in [DHCP](../pages/dhcp_howto.md). Verify that your bridge interface has all ports connected:

```
switch$ brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.005056990b10	no		ens192
							ens224
							ens256
```

If you don't see that make sure that your interfaces file contains the following declaration:

```
auto br0
iface br0 inet dhcp
    bridge_ports ens192 ens224 ens256

iface br0 inet6 auto
```

Finally check your servers. They should be configured for DHCP. Verify that their interfaces files look like the following:

```
auto ens192
iface ens192 inet dhcp
iface ens192 inet6 auto
```

### 4. Check Router Connectivity 

Your router must have a connection to the internet. It may or may not have nameservers configured. Start by making sure you can ping yourself:

```
router$ ping -c 3 localhost

PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.044 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.136 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.047 ms
--- localhost ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.044/0.075/0.136/0.043 ms
```

If you can't ping localhost you have a problem with your firewall. Review your firewall rules and make sure they match the ones in [Testing Your Network](../milestones/testing_your_network.md). Now check to see if you can ping your router's router. First, find the configured router:

```
router$ ip route
default via 172.19.0.1 dev ens192 onlink 
10.192.0.0/16 dev ens224  proto kernel  scope link  src 10.192.0.1 
172.19.0.0/16 dev ens192  proto kernel  scope link  src 172.19.192.30 
```

Now ping the default route:

```
router$ ping -c 3 172.19.0.1
PING 172.19.0.1 (172.19.0.1) 56(84) bytes of data.
64 bytes from 172.19.0.1: icmp_seq=1 ttl=255 time=0.561 ms
64 bytes from 172.19.0.1: icmp_seq=2 ttl=255 time=0.578 ms
64 bytes from 172.19.0.1: icmp_seq=3 ttl=255 time=0.668 ms

--- 172.19.0.1 ping statistics ---3 packets transmitted, 3 received, 0% packet loss, time 1999msrtt min/avg/max/mdev = 0.561/0.602/0.668/0.051 ms
```

If you can't ping your IPv4 router, check that it matches mine. It should. If it doesn't look in `/etc/network/interfaces` and set it there. If it does match and you can't ping it then check your firewall and be sure it matches the one in [Testing Your Network](../milestones/testing_your_network.md). Now repeat the process for IPv6:

```
router$ ip -6 route
2607:f380:80f:f192::/64 dev ens192  proto kernel  metric 256  pref medium
2607:f380:80f:f900::/64 dev ens224  proto kernel  metric 256  pref medium
fe80::/64 dev ens192  proto kernel  metric 256  pref medium
fe80::/64 dev ens224  proto kernel  metric 256  pref medium
default via fe80::26e9:b3ff:fe24:fc80 dev ens192  proto ra  metric 1024  expires 1706sec hoplimit 64 pref medium
```

Notice your IPv6 router is reachable with a link-local address. That's good! That means that RA is working. If you don't see a router check that your firewall rules match the ones in [Testing Your Network](../milestones/testing_your_network.md). If they do then confirm that you have set the following system control parameter:

```
net.ipv6.conf.ens192.accept_ra = 2
```

Instructions for how to do that are in the [SLAAC](../pages/slaac.md) lecture. Now be sure you can ping your IPv6 router. Remember, when you use a link-local address you must also specify what interface the address is behind. Here's a ping command that pings the router shown above in my IPv6 routing table:

```
router$ ping6 -c 3 fe80::26e9:b3ff:fe24:fc80%ens192
PING fe80::26e9:b3ff:fe24:fc80%ens192(fe80::26e9:b3ff:fe24:fc80) 56 data bytes
64 bytes from fe80::26e9:b3ff:fe24:fc80: icmp_seq=1 ttl=64 time=0.344 ms
64 bytes from fe80::26e9:b3ff:fe24:fc80: icmp_seq=2 ttl=64 time=0.429 ms
64 bytes from fe80::26e9:b3ff:fe24:fc80: icmp_seq=3 ttl=64 time=0.463 ms

--- fe80::26e9:b3ff:fe24:fc80%ens192 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.344/0.412/0.463/0.050 ms
```

Notice that the link local address has `%ens192` on the end. That's standard and it works in other operating systems too. Now check that your router can ping beyond the local network. Do this by pinging Google on both IPv4 and IPv6:

```
router$ ping -c 3 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=59 time=4.34 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=59 time=4.38 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=59 time=4.41 ms
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 4.349/4.382/4.411/0.080 ms
```

Now with IPv6:

```
router$ ping6 -c 3 2001:4860:4860::8888
PING 2001:4860:4860::8888(2001:4860:4860::8888) 56 data bytes
64 bytes from 2001:4860:4860::8888: icmp_seq=1 ttl=59 time=4.06 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=2 ttl=59 time=4.21 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=3 ttl=59 time=4.13 ms
--- 2001:4860:4860::8888 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 4.060/4.136/4.216/0.082 ms
```

If one of the above commands doesn't work, triple check your interfaces file. You may or may not have DNS configured correctly. It's okay if you don't but if you do the following commands should work on your router:

```
router$ ping -c 3 www.google.com
PING www.google.com (172.217.4.132) 56(84) bytes of data.
64 bytes from lax17s14-in-f4.1e100.net (172.217.4.132): icmp_seq=1 ttl=56 time=10.8 ms
64 bytes from lax17s14-in-f4.1e100.net (172.217.4.132): icmp_seq=2 ttl=56 time=10.8 ms
64 bytes from lax17s14-in-f4.1e100.net (172.217.4.132): icmp_seq=3 ttl=56 time=10.8 ms
--- www.google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 10.842/10.863/10.881/0.016 ms
```

and:

```
router$ ping6 -c 3 www.google.com
PING www.google.com(lax17s14-in-x04.1e100.net) 56 data bytes
64 bytes from lax17s14-in-x04.1e100.net: icmp_seq=1 ttl=56 time=10.9 ms
64 bytes from lax17s14-in-x04.1e100.net: icmp_seq=2 ttl=56 time=11.0 ms
64 bytes from lax17s14-in-x04.1e100.net: icmp_seq=3 ttl=56 time=11.0 ms
--- www.google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 10.934/11.021/11.092/0.137 ms
```

### 5. Check IPv4 Connectivity to Your Hosts 

On each of your host VMs be sure you can ping your router, which should have the address below:

```
$ ping -c 3 10.192.0.1
PING 10.192.0.1 (10.192.0.1) 56(84) bytes of data.
64 bytes from 10.192.0.1: icmp_seq=1 ttl=64 time=0.228 ms
64 bytes from 10.192.0.1: icmp_seq=2 ttl=64 time=0.513 ms
64 bytes from 10.192.0.1: icmp_seq=3 ttl=64 time=0.343 ms
--- 10.192.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.228/0.361/0.513/0.118 ms
```

If you can't go back to step 3 and verify that your IP address is set correctly. If it is, make sure that the firewall on your router allows all traffic from ens224. Your hosts' addresses should be set by DHCP and you should have a reservation for all of them. Verify on your router that you have DHCP server setup and reservations made for all the other hosts. They should look something like this:

```
# from /etc/dhcp/dhcpd.conf on the router
host switch {
 hardware ethernet 00:50:56:af:07:ed;
 fixed-address 10.192.0.2;
}
host infra {
 hardware ethernet 00:50:56:af:33:78;
 fixed-address 10.192.0.3;
}
host app {
 hardware ethernet 00:50:56:af:d6:1d;
 fixed-address 10.192.0.4;
}
```

If you don't have that working follow the instructions in [DHCP](../pages/dhcp_howto.md). If you can ping the router and your addresses are correct make sure your router has routing and NAT setup. On each of your VMs ensure that you can ping the Internet using an IP address:

```
$ ping -c 3 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=59 time=4.34 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=59 time=4.38 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=59 time=4.41 ms
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 4.349/4.382/4.411/0.080 ms
```

### 5. Check IPv6 Connectivity to Your Hosts 

Each of your hosts should be using an EUI-64. The exact address depends on what prefix you received and what the MAC address of the machine is. On each of your hosts verify that you can ping the router:

```
$ ip -6 route 
2607:f380:80f:f900::/64 dev ens192  proto kernel  metric 256  expires 86242sec pref medium
fe80::/64 dev ens192  proto kernel  metric 256  pref medium
default via fe80::250:56ff:fe99:6d3a dev ens192  proto ra  metric 1024  expires 1642sec hoplimit 64 pref medium
```

Now check that you can ping the router:

```
$ ping6 -c 3 fe80::250:56ff:fe99:6d3a%ens192
PING fe80::250:56ff:fe99:6d3a%ens192(fe80::250:56ff:fe99:6d3a) 56 data bytes
64 bytes from fe80::250:56ff:fe99:6d3a: icmp_seq=1 ttl=64 time=0.507 ms
64 bytes from fe80::250:56ff:fe99:6d3a: icmp_seq=2 ttl=64 time=0.513 ms
64 bytes from fe80::250:56ff:fe99:6d3a: icmp_seq=3 ttl=64 time=0.627 ms

--- fe80::250:56ff:fe99:6d3a%ens192 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.507/0.549/0.627/0.055 ms
```

If you can't ping your router, check its firewall rules. The INPUT chain should allow all traffic from `ens224`. Now verify that you can ping the Internet:

```
$ ping6 -c 3 2001:4860:4860::8888
PING 2001:4860:4860::8888(2001:4860:4860::8888) 56 data bytes
64 bytes from 2001:4860:4860::8888: icmp_seq=1 ttl=59 time=4.11 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=2 ttl=59 time=4.27 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=3 ttl=59 time=4.25 ms
--- 2001:4860:4860::8888 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 4.119/4.216/4.274/0.069 ms
```

If you can't ping the internet verify the rules in the IPv6 `FORWARD` chain. They should allow all traffic from `ens224` to `ens192`. Also check that the following system control setting has been set:

```
net.ipv6.conf.all.forwarding = 1
```

Instructions on how to set that can be found in [SLAAC](../pages/slaac.md).

### 6. Verify SSH Access 

Last, but certainly not least, you should verify that you can SSH into each of your VMs from opus. Configure SSH on opus to remember the IPv6 addresses of your VMs to save time. Your configuration file should looks something like this:

```
# ~/.ssh/config

Host router
	HostName 2607:f380:80f:f192::30
	User student

Host switch
	HostName 2607:f380:80f:f900:250:56ff:fe99:5be
	User student

Host infra
	HostName 2607:f380:80f:f900:250:56ff:fe99:dc27
	User student

Host app
	HostName 2607:f380:80f:f900:250:56ff:fe99:7002
	User student
```

From opus ssh into each of your hosts and run a simple command like this:

```
opus$ ssh router uname -a
Linux router 4.4.0-66-generic #87-Ubuntu SMP Fri Mar 3 15:29:05 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```

If you are not able to connect to your router or your hosts using SSH it's very likely at this point to be a firewall issue. If you can's SSH into your router check the INPUT chain on the router. If you can't SSH into your switch or servers check that the `FORWARD` chain in the IPv6 firewall allows `NEW` traffic on port 22. If you're like me, you hate to wast time. You can make it possible to login from opus without a password by running the command:

```
opus$ ssh-copy-id <host>
```

That's it for now. There will be another debugging session on the last day of class.

## Still Have Problems? 

Ask a question on the newsgroup or visit me in my office or lab hours.
