# Routing and Switching 

Lecture slides are [here](https://docs.google.com/presentation/d/14nQ2X1JXtPdaSWpPko1CcyQZua-aMdxfrFI8BreQ1MI/edit?usp=sharing).
In this lesson you'll learn the commands that view and alter the routing and switching functions of Linux.

## Commands 

  * ip route
  * ip neigh
  * brctl

## Configuration 

  * /etc/network/interfaces

## Further Reading 

  * [ip neighbor documenation](http://linux-ip.net/html/tools_ip_neighbor.html)
  * [RFC 4861 - The Neighbor Discovery Protocol](https://tools.ietf.org/html/rfc4861#section_7.3.2)

## Know Your Neighbors 

In order to communicate with a host on an Ethernet LAN you must know the host's MAC address. This information is typically not known by the user. Instead the user requests communication with a host by IP address. For example:

```
$ ping6 2001:db8::1
```

Linux must determine the MAC address from the IP address automatically. This is the job of two protocols: The Neighbor Discovery Protocol (NDP) for IPv6 addresses and the Address Resolution Protocol (ARP) for IPv4. Though they have the same function the protocols behave differently. That's beyond the scope of this class. Linux maintains a list of IP address to MAC address mappings. You can access the list with the command:

```
$ ip neigh
```

Here's an example from my computer:

```
$ ip neigh
fe80::250:56ff:feaf:2a21 dev eth0 lladdr 00:50:56:af:2a:21 STALE
2607:f380:80f:f830:192::1 dev eth0 lladdr 00:50:56:af:2a:21 STALE
fe80::f830:1 dev eth0 lladdr 24:e9:b3:24:fc:80 router STALE
172.20.0.1 dev eth0 lladdr 24:e9:b3:24:fc:80 DELAY
```

Each line shows an IP address followed by the device that IP address is connected to and the state of the neighbor association. The last word is the reachability state of the host. Those states are defined in [Section 7.3.2 of RFC 4861](https://tools.ietf.org/html/rfc4861#section_7.3.2). If a host is in the "DELAY", "STALE" or "REACHABLE" state Linux will attempt to contact the host directly. If a host is missing or in the "INCOMPLETE" OR "PROBE" states a new ARP request or ND request will be sent before Linux can attempt to contact the host.

### Adding and Removing Neighbors 

You can add a neighbor by simply attempting to contact them:

```
$ ping6 2607:f380:80f:f830:192::1
```

You can manually add them too. You shouldn't do that unless you really know what you're doing. You can remove neighbors, that will force Linux to redo ARP or ND with the command:

```
$ sudo ip neigh del <ip-address> dev <device>
```

The device must be specified because it's possible to have the same IP address connected on two devices. This is especially common in IPv6 where link-local addresses are very common. 

## Routing 

Every host makes routing decisions. Routing decisions are based on the host's routing table. On Linux you can inspect the routing table with the command:

```
$ ip route
```

Here's an example from my VM:

```
$ ip route
default via 172.20.0.1 dev eth0
10.192.0.0/16 dev eth1 proto kernel scope link src 10.192.0.1
172.20.0.0/16 dev eth0 proto kernel scope link src 172.20.192.13
```

The routing table has three routes. The first is the route to the default gateway. If an outgoing packet does not match any locally connected network the packet will be routed there. The next two entries show the directly connected networks. Here's an example from my home machine that has two physical and several virtual interfaces:

```
$ ip route
default via 10.2.0.1 dev br0
10.0.3.0/24 dev lxcbr0 proto kernel scope link src 10.0.3.1
10.2.0.0/16 dev br0 proto kernel scope link src 10.2.5.3
10.2.9.0/24 dev virbr3 proto kernel scope link src 10.2.9.1
10.200.0.0/24 dev virbr4 proto kernel scope link src 10.200.0.1
169.254.0.0/16 dev br0 scope link metric 1000
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.42.1
192.168.100.0/24 dev virbr1 proto kernel scope link src 192.168.100.1
192.168.122.0/24 dev virbr0 proto kernel scope link src 192.168.122.1
192.168.200.0/24 dev virbr2 proto kernel scope link src 192.168.200.1
```

The "virbr" and "docker" interfaces are created for virtual machine networking. `169.254.0.0/16` is an APIPA subnet. It's primarily used for Windows interoperation. Unlike the ip neigh command the ip route command only shows IPv4 or IPv6, not both. To see your IPv6 routing table you use the command:

```
$ ip -6 route
2607:f380:80f:f830::/64 dev eth0 proto kernel metric 256
fe80::/64 dev eth0 proto kernel metric 256
fe80::/64 dev eth1 proto kernel metric 256
default via fe80::f830:1 dev eth0 proto ra metric 1024 expires 1741sec hoplimit 64
```

Notice that in IPv6 there are matching routes to the same interface. Those are for link local addresses. You can manipulate the routing table. This is common if you're setting up a router that needs static routes. It's also common to manually set a default route. This is usually required if you setup networking manually (rather than using /etc/network/interfaces). An example of setting the network manually is:

```
$ sudo ifconfig eth0 10.2.0.2 netmaksk 255.255.255.0
```

Now you have the link up but Linux doesn't know what your default route is. You tell it like this:

```
$ sudo ip route add default via 10.2.0.1 dev eth0
```

After the default gateway is configured you should be able to communicate off of your local network. This page describes how to setup the Ethernet bridging functions of Linux. This makes Linux an Ethernet switch.

## Bridging  

In order to configure bridging you need the 'brctl' command. The command has several sub-commands. For help run it with no arguments:

```
$ brctl
Usage: brctl [commands]
commands:
	addbr     	<bridge>		add bridge
	delbr     	<bridge>		delete bridge
	addif     	<bridge> <device>	add interface to bridge
	delif     	<bridge> <device>	delete interface from bridge
	hairpin   	<bridge> <port> {on|off}	turn hairpin on/off
	setageing 	<bridge> <time>		set ageing time
	setbridgeprio	<bridge> <prio>		set bridge priority
	setfd     	<bridge> <time>		set bridge forward delay
	sethello  	<bridge> <time>		set hello time
	setmaxage 	<bridge> <time>		set max message age
	setpathcost	<bridge> <port> <cost>	set path cost
	setportprio	<bridge> <port> <prio>	set port priority
	show      	[ <bridge> ]		show a list of bridges
	showmacs  	<bridge>		show a list of mac addrs
	showstp   	<bridge>		show bridge stp info
	stp       	<bridge> {on|off}	turn stp on/off
```

Most of the sub commands aren't useful to us, they control the Spanning Tree Protocol (STP). You must leave STP off on our VMs otherwise VMware becomes upset. To see what bridges exist run this:

```
$ brctl show
```

By default Linux won't create any bridges. A bridge interface is special. It's used to bond one or more interfaces together. Bonded interfaces cannot have IP addresses of their own. Once your switch's interfaces are bonded into bridge mode you have to set the IP address for the host on the bridge interface. Here's how to turn your switch VM into a switch. Start by adding a bridge interface:

```
$ sudo brctl addbr br0
```

Now you should see the bridge interface in the list of Ethernet interfaces:

```
$ ifconfig br0
```

Once the bridge is established you add interfaces to it:

```
$ sudo brctl addif br0 eth192
$ sudo brctl addif br0 eth224
$ sudo brctl addif br0 ens256
```

Adding interfaces to the bridge doesn't automatically bring them up. Make sure that they are up and none have an IP address assigned:
```
$ sudo ifconfig ens192 0.0.0.0 up
$ sudo ifconfig ens224 0.0.0.0 up
$ sudo ifconfig ens256 0.0.0.0 up
```

Your bridge doesn't need an IP address to function but having an IP address is handy if you want to login to the machine remotely.

```
$ sudo ifconfig br0 10.192.0.2 netmask 255.255.0.0 up
```

You don't have a default route set yet. Set it to your router:

```
$ sudo ip route add default 10.192.0.1 via br0
```

This doesn't really matter yet because your router is not routing yet.

### Permanent Bridge Configuration 

In Ubuntu it's easy to make your bridge configuration permanent. Add your bridge to the /etc/network/interfaces file. Here's an example of how to create a bridge:

```
auto br0
iface br0 inet static
 address 10.192.0.2
 netmask 255.255.0.0
 network 10.192.0.0
 broadcast 10.192.255.255
 dns-nameservers 2607:f380:80f:f425::252 and 2607:f380:80f:f425::253
 bridge_ports ens192 ens224 ens256

iface br0 inet6 auto
```

Be sure you DELETE the configuration of ens192!
