# Dynamic Addressing: SLAAC 

This page will help you get Router Advertisement (RA) and Stateless Address Autoconfiguration (SLAAC) working on your router. Lecture slides are [here](https://docs.google.com/presentation/d/1zO7pIglYaegFsGGOsybzQQUtbEZypmS_fEd2nsS7UZI/edit?usp=sharing).

## Commands 

  * sysctl
  * service

## Configuration 

  * /etc/radvd.conf
  * /etc/wide-dhcpv6/dhcp6c.conf
  * /etc/rc2.d/S20wide-dhcpv6-client
  * /etc/sysctl.conf

## Introduction 

Router configuration is much simpler with IPv6 than it has been in the past. These instructions will show you how to use your router to get a pool of addresses (called a prefix) from a DHCP server then advertise that prefix to downstream machines. This process will give all of your VMs a direct connection to the Internet with real, routable addresses. In the (hopefully near) future your home DSL/Cable routers will enable this feature so that your home devices can take full advantage of the Internet.

## Before You Begin 

For the first time you'll be configuring and restarting system services. If you cause an error the service will fail to start and show you something like this:

```
$ sudo systemctl restart wide-dhcpv6-client
* Stopping WIDE DHCPv6 client dhcp6c               [ OK ]
* Starting WIDE DHCPv6 client dhcp6c               [fail]
```

You will find the cause of the error in `/var/log/syslog`. You should keep a window open for the sole purpose of running this command which will continuously monitor your system log:

```
$ tail -f /var/log/syslog
```

From now on I will ask you to post your syslog file when you have problems that you report to the mail list!

## Using DHCPv6 

In IPv6 DHCP servers have a very different role. Most of what has been previously done by DHCP servers is now done using the Router Advertisement (RA) protocol. There is, however a new and very important function of a DHCPv6 server: Prefix delegation. Instead of asking for a single address your router will ask for 18,446,744,073,709,551,616 (18 quintillion) addresses. Start by installing the WIDE-DHCP client:

```
router$ sudo apt-get install wide-dhcpv6-client
```

The installer will ask you what network interfaces the client should send requests on. Change `eth0` to `ens192`. The default configuration won't work. Replace the configruation in `/etc/wide-dhcpv6/dhcp6c.conf` with this (copy-and-paste it):

```
##
## This is/etc/wide-dhcpv6/dhcp6c.conf
##
## Replace the existing configuration with this one.

# Send a PD request on the external facing interface
# send ia-pd says ask for a prefix
# the script is run when the prefix is acquired
interface ens192 {
 send ia-pd 1;
 script "/etc/wide-dhcpv6/dhcp6c-script";
};

# Upon receiving a prefix use the
# information to set the internal facing interface
id-assoc pd 1 {
 prefix-interface ens224 {
  ifid 1;
  sla-id 1;
  sla-len 0;
 };
};

## End of config.
```

This tells the DHCP client that it needs a prefix, not just an address and that address is to be applied to ens224. There's a slight problem in the `/etc/wide-dhcpv6/dhcp6c-script` file. You will need to edit it to solve the problem. Edit the file and add the following lines just before the `exit 0` line:

```
# Add this line to restart the RADVD server
( sleep 10 ; service radvd reload )& 

# Put it before the exit... 
exit 0
```

The above change is a bit of a hack, but it works. Once you have the changes in place, restart the DHCP client with the following command:

```
router$ sudo systemctl restart wide-dhcpv6-client
```

NOTE: If you see this message:

```
Job for wide-dhcpv6-client.service failed because the control process exited with error code. See "systemctl status wide-dhcpv6-client.service" and "journalctl -xe" for details.
```

Run the `journalctl -xe` command to see what the problem is. DO NOT attempt to move forward unless the service starts properly.If your command worked you should now have a public IPv6 address assigned to your `ens224` interface:

```
router$ ifconfig ens224
ens224    Link encap:Ethernet  HWaddr 00:50:56:99:6d:3a  
          inet addr:10.192.0.1  Bcast:10.192.255.255  Mask:255.255.0.0
          inet6 addr: 2607:f380:80f:f900::1/64 Scope:Global
          inet6 addr: fe80::250:56ff:fe99:6d3a/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:19401 errors:0 dropped:30 overruns:0 frame:0
          TX packets:11 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:6626118 (6.6 MB)  TX bytes:946 (946.0 B)
```

Now we need Linux to hand out that prefix to the downstream machines.

## Setting up Router Advertisements 

The Router Advertisement deamon (`radvd`) on Linux creates RA packets. The RA packets will be picked up by your other VMs and used to generate addresses. Install radvd on your router with the command:

```
router$ sudo apt-get install radvd
```

The `radvd` program will not start automatically. It waits for you to configure it. Enter the following configuration for `radvd`. Note: The `/etc/radvd.conf` file doesn't exist by default, you will create it. 

```
## this is /etc/radvd.conf
interface ens224
{ 
  AdvSendAdvert on;
  prefix ::/64  
  {
    AdvOnLink on;
    AdvAutonomous on;
 
  };
  RDNSS 2607:f380:80f:f425::252 2607:f380:80f:f425::253
  {
  };
};
```

This simple and generic configuration says to use the upper 64 bits of the address assigned to ens224 as the prefix and send advertisements. The AdvOnLink and the AdvAutonomous flags set the O and the A bits in the RA message. The radvd program is configured but will not start because Linux will not act as a router unless you explicitly tell it to do so. You do that by turning on features that are controlled in the `/proc` filesystem.

```
# See if ipv6 forwarding is turned on (0 is disabled, 1 is enabled):
router$ cat /proc/sys/net/ipv6/conf/all/forwarding
0
# Turn on forwarding
router$ echo 1 | sudo tee /proc/sys/net/ipv6/conf/all/forwarding
```

Changing things in the `/proc` filesystem changes them in memory only. If you want the change to be permanent you have to edit the file `/etc/sysctl.conf` and uncomment the following line:

```
net.ipv6.conf.all.forwarding=1
```

Notice the similarity between the `/proc` path and the `sysctl` line. It's not a coincidence. There's one more thing you have to do. Linux knows it's default IPv6 gateway from listening to RAs on `ens192`. When you configure Linux for packet forwarding it stops listening to RAs. This will eventually break IPv6. To fix that you set a different /proc flag:

```
router$ echo 2 | sudo tee /proc/sys/net/ipv6/conf/ens192/accept_ra
```

And add the corresponding flag to your `/etc/sysctl.conf` file:

```
net.ipv6.conf.ens192.accept_ra = 2
```

Once you have all of the configuration in place restart the radvd program:

```
router$ sudo systemctl status radvd
```

Check to make sure that your router is sending RAs out:

```
router$ sudo tcpdump -i ens224 -n icmp6
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens192, link-type EN10MB (Ethernet), capture size 65535 bytes
20:43:38.927469 IP6 fe80::250:56ff:feaf:7da3 > ff02::1: ICMP6, router advertisement, length 56
20:43:54.942110 IP6 fe80::250:56ff:feaf:7da3 > ff02::1: ICMP6, router advertisement, length 56
20:44:10.958459 IP6 fe80::250:56ff:feaf:7da3 > ff02::1: ICMP6, router advertisement, length 56
```

By default you should see one about every 60 seconds.

## Testing It Out 

If you see RAs coming from the `ens224` interface on your router everything should be ready to go. Your other VMs should already be working! Go to each of them and run ifconfig. You should see IPv6 addresses assigned to their interface (the bridge interface in the case of your switch). You should also now be able to run the following ping command on your switch:

```
switch$ ping6 www.google.com
```

Despite having an address your other VMs do not have DNS server information yet. But pinging by IP address will work:

```
switch$ ping6 2a00:1450:4013:c00::63
```

Next week we'll use DHCPv4 to automatically assign DNS addresses to your server VMs.
