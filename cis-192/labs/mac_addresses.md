# Lab: MAC Addresses 

In this you'll prepare to get your network fully operational by collecting the MAC addresses of each of your hosts. MAC addresses uniquely identify each Ethernet port. That makes them very useful on your network. Your DHCP server will use that information to reserve an IP address for a specific machine. Each machine will also generate a unique IPv6 address using it's [EUI-64](http://packetlife.net/blog/2008/aug/4/eui-64-ipv6/).

## Choose a Domain Name 

In the coming weeks you will choose a domain name. That domain name will be in the form:

>  yourname.cis.cabrillo.edu

Next week I'll setup DNS and I'll register your domain name to you and you'll be able to start using it. Tell me what domain name you want when you submit this lab.

## Gather your MAC Addresses 

VMware knows the MAC address of each machine. Go to your server VMs the same way you did in [the Get Connected Milestone](../milestones/get_connected.md) and expand the "VM Harware" Tab. Expand the "Network Adapter 1" label to reveal the MAC address. Your switch VM is a bit more complicated. The bridge will take a MAC address from one of the interfaces. Which one is not guaranteed so you will have to log into the switch and determine what MAC address the bridge interface got. You don't need to gather the MAC address for your router. Once you're done create a text document that contains the following:

```
Bridge MAC:
infra-server MAC:
app-server MAC:
```

## Calculate your EUI-64 addresses 

This page shows you how an EUI-64 address is generated from a MAC address:

[http://packetlife.net/blog/2008/aug/4/eui-64-ipv6/](http://packetlife.net/blog/2008/aug/4/eui-64-ipv6/) 
 
 If you have not setup [SLAAC](../pages/slaac.md) yet you will not have a prefix (the first 64-bits). That's okay for now. You can complete your text file by writing down your EUI-64 address like this:

```
switch: <prefix>:<host-part>
infra-server: <prefix>:<host-part>
app-server: <prefix>:<host-part>
```

Here's an example from my network. My MAC addresses are:

```
Bridge MAC:00: 50:56:af:14:16
db-server MAC: 00:50:56:af:69:d7
web-server MAC: 00:50:56:af:c5:d1
```

I have DCHP-PD and SLAAC setup and I have received the prefix of2607:f380:80f:f901. My IP addresses therefore are:

```
switch: 2607:f380:80f:f192:250:56ff:feaf:1416
infra-server: 2607:f380:80f:f192:250:56ff:feaf:69d7
app-server: 2607:f380:80f:f192:250:56ff:feaf:c5d1
```

These addresses can function as static addresses with no further configuration. This saves time when compared to IPv4.

## Turn In 

The domain name of your choice and your text file with MAC addresses and IPv6 address (assigned prefix optional).
