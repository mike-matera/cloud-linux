# Networking Basics

This how-to will acquaint you with the basic tools used to setup and establish networking on Ubuntu.

  [Lecture Slides](https://docs.google.com/presentation/d/1JZLgIRUArmoUypjQK4mRo0xqUqOoVuPsGwAejlfNLjU/edit?usp=sharing)

Do you know how to decipher a manual page? [Here's how](../../cis-191/deciphering_manual_pages.md).

## Commands 

  * ifconfig
  * hostname
  * arp
  * route
  * netstat

## Configuration 

  * /etc/network/interfaces
  * /etc/hosts
  * /etc/hostname

## Network Settings 

The ifconfig command displays and alters networking parameters on Ethernet and Ethernet-like device in Linux. To determine the current configuration of Ethernet devices on your system run the command:

```
$ ifconfig
ens192  Link encap:Ethernet HWaddr 5c:26:0a:60:57:de 
     UP BROADCAST MULTICAST MTU:1500 Metric:1
     RX packets:0 errors:0 dropped:0 overruns:0 frame:0
     TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
     collisions:0 txqueuelen:1000
     RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)
     Interrupt:20 Memory:e6700000-e6720000
lo    Link encap:Local Loopback 
     inet addr:127.0.0.1 Mask:255.0.0.0
     inet6 addr: ::1/128 Scope:Host
     UP LOOPBACK RUNNING MTU:65536 Metric:1
     RX packets:2403 errors:0 dropped:0 overruns:0 frame:0
     TX packets:2403 errors:0 dropped:0 overruns:0 carrier:0
     collisions:0 txqueuelen:0
     RX bytes:275572 (275.5 KB) TX bytes:275572 (275.5 KB)
```

That will only show you the currently enabled devices. To see devices that are in the "down" state use the -a flag:

```
$ ifconfig -a
```

You can configure an interface with the following lines:

```
 ifconfig <ethX> <ip-address> netmask <netmask>
```

For example, the command below assigns the address 192.168.1.1 and netmask 255.255.255.0 to the ens192 interface:

```
$ ifconfig ens192 192.168.1.1 netmask 255.255.255.0
```

You can deactivate a device with:

``` 
ifconfig <interface-name> down
```

For example, to bring the ens192 interface down:

```
$ ifconfig ens192 down
```

Ifconfig changes immediately take effect but do not survive a reboot. In order to have changes stick after a reboot you must alter some configuration files on the system. On Ubuntu the configuration file is [/etc/network/interfaces](http://manpages.ubuntu.com/manpages/trusty/man5/interfaces.5.html). Here's an example:

```
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto ens192
iface ens192 inet static 
    address 10.0.0.41
    netmask 255.255.255.0 
    network 10.0.0.0
    broadcast 10.0.0.255
    gateway 10.0.0.1
    dns-nameservers 10.0.0.1 8.8.8.8 
    dns-domain acme.com
    dns-search acme.com

iface ens192 inet6 static 
    address 2607:f380:80f:f192::10
    netmask 64
```

Making changes to the file does not immediately change the network interfaces. The ifup and ifdown command are similar to ifconfig, but they configure your interface according to the settings in your interfaces file. So, when you want to change your IP address settings the procedure is:

```
$ ifdown <interface-name>
# now edit /etc/network/interfaces
$ ifup <interface-name>
```

If you see an error you must correct it! If the error exists when the system starts your networking will not start and that slows down bootup.

## Setting your Hostname 

When you install Ubuntu the installer asks you to give a hostname. You can change those later if you wish. You can alter your host name using the hostname command. Hostname with no arguments prints the current hostname:

```
$ hostname
8piecebox
```

You can set the hostname too:

```
$ sudo hostname newname
```

The change isn't permanent. If you want to make the change permanent you must put your new hostname into the `/etc/hostname` file. It's very important that you also make sure your hostname is listed in `/etc/hosts`. If it's not you will see funny errors when you run the sudo command. The hosts file is discussed in the next section.

## The Hosts File 

Before there was such a thing as DNS every hostname of every computer on the entire Internet was listed in a file `/etc/hosts`. A copy of that file was placed on every computer and someone was responsible for keeping it maintained. That system has obvious problems with scale but instead of being replaced, DNS just adds a layer on top of it. Your `/etc/hosts` file is still a piece configuration. Even Microsoft Windows has a hosts file it's located in `C:\Windows\System32\drivers\etc\hosts`. Here's an example of a hosts file from your VMs:

```
127.0.0.1  localhost
127.0.1.1  ubuntu-server

# The following lines are desirable for IPv6 capable hosts
::1   ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

The hosts file is where the special name "localhost" gets its meaning. Also, by adding the name of your computer to the hosts file Linux ensures you'll be able to refer to your computer by name even if it doesn't have a DNS entry. The hosts file takes precedence over DNS so if you place a host name in there Linux will use it without question. Be careful when you do that because it can cause some very hard to find problems.

## ARP

In order to function all hosts need an ARP table and a routing table. This section introduces the commands in Linux that can view and alter those tables. You can view the ARP table with the following command.

```
arp -n
```

The `-n` argument tells the arp command not to lookup hostnames (this makes it faster, especially when you have network trouble). In rare occasions you may need to add or delete entries in the ARP table. You can do that with the following commands:

Delete an entry:
```
arp -d <hostname>
```

Create an entry:

```
arp -s <hostname> <MAC Address>
```

## Routing

You will need to be root to run the latter two commands. I strongly suggest avoiding them unless you're sure of what you're doing. Altering the routing table is often required when you want to manually establish a Linux computer on the network. You can display the routing table with either of the two commands:

```
ip route  ip -6 route
```

You can use those commands to determine what (if any) default gateway you have set. If you need to establish a default gateway use the following commands:

```
ip route add default via <ipv4-address>
ip -6 route add default via <ipv6-address> dev <device>
```

Examples:

```
ip route add default via 172.20.0.1
ip -6 route add default via fe80::f831:1 dev ens192
```

The reason that the IPv6 version needs the additional "dev" argument is that in IPv6 routers are most often reached through link-local addresses. Linux would not know which Ethernet device to send the packet to without you telling it. You can also add static routes but that's beyond the scope of this article.

## DNS

Nameservers are configured using the file [/etc/resolv.conf](http://man7.org/linux/man-pages/man5/resolv.conf.5.html). The file is almost as old as Unix and has a very simple format. Here's an example:

```
nameserver 172.30.5.101
nameserver 172.30.5.102
search cis.cabrillo.edu
```

The file tells Linux where to find nameservers and what domain to search when a user enters a hostname without a domain name (e.g. opus instead of opus.cis.cabrillo.edu). On Ubuntu the file also comes with this warning:

```
# DO NOT EDIT THIS FILE BY HAND
```

On Ubuntu this file is automatically written when you run the `ifup` and `ifdown` commands. Also, if you're using Ubuntu Desktop, there's an added level of complexity the `resolvconf` program. That program lets you control things from the desktop GUIs. Where's the fun in that?

## Network Status

When debugging it's important to know what network connections are currently being maintained by your computer. This can help you spot configuration problems quickly and painlessly. The `ss` command is a Swiss Army knife command that will tell you almost anything you want to know about Linux's network. We won't use all of its functionality in class but it's important to know these formulations of the command:

Shows the current TCP connections:

```
ss -ntp
```

Shows what servers are listening for INBOUND connections on TCP (remember this!):

```
ss -lntp
```

Shows what programs have UDP sockets open:

```
ss -nup
```

Shows what programs have listening UDP sockets open:

```
ss -lnup
```

I expect you to have these commands committed to memory! A good admin should know them by heart.
