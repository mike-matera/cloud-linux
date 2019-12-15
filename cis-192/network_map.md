In today's lab you'll make a map of your network. This lab assumes that you have [setup your DHCP](dhcp_howto.html) server and you have completed the steps for "[An IPv6 Network](capturing_dhcpv6_and_ra.html)"

## Introduction 

Now that you have internal IP addresses and a prefix you are ready to make a complete map of your Linux network. The map is a very handy thing to have when you're working on a network. Most networks have more than four hosts and it can quickly become impossible to remember what addresses you have assigned.

## Get your MAC Address Table 

The MAC addresses you collected the previous week are the starting point for this lab. Make a table of this form:
HostnameMAC AddressPrivate IPv4 Address
IPv6 Addressrouter00:50:56:af:da:0a (eth1)10.192.0.12607:f380:80f:f901::1 (eth1)switch00:50:56:af:14:16 (br0)10.192.0.22607:f380:80f:f901:250:56ff:feaf:1416 (br0)db-server00:50:56:af:69:d710.192.0.32607:f380:80f:f901:250:56ff:feaf:69d7web-server00:50:56:af:c5:d110.192.0.42607:f380:80f:f901:250:56ff:feaf:c5d1
Now that you have your MAC address table you should update the /etc/hosts file on each VM to reflect your network. Given my network the host files would look like this:

```
# The router's /etc/hosts file.
# NOTICE that the 127.0.1.1 line is still set and the new entries are below.
127.0.0.1
localhost
127.0.1.1
router
# The following lines are desirable for IPv6 capable hosts
::1   localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.192.0.1 router
10.192.0.2 switch
10.192.0.3 db-server
10.192.0.4 web-server
2607:f380:80f:f901::1 router
2607:f380:80f:f901:250:56ff:feaf:1416 switch
2607:f380:80f:f901:250:56ff:feaf:69d7 db-server
2607:f380:80f:f901:250:56ff:feaf:c5d1 web-server
```

With your hosts files setup correctly you should be able to ping your VMs by name from anywhere inside your network. Submit your table with this lab.

## Get Ready for DNS 

In two weeks you will setup a DNS server. The DNS server will give you a real domain name. Your domain name will be:

```

  <your-name-here>.cis.cabrillo.edu
```

When you submit this lab tell me what name you want and what external (eth0) static IP addresses of your router is.

## Turn In 

  - Your IP address table
  - Your requested domain name
  - The external (eth0) IPv4 and IPv6 addresses of your router

Submit the lab on canvas.