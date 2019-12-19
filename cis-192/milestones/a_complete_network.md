# Milestone: A Complete Network 

When you complete this milestone you will have a complete working network between your VMs. With the switch functioning your VMs will be able to communicate with each other. This is an important milestone for your network. You will set a static IP address on your switch but leave the two servers set for DHCP and automatic configuration. Next week you will get IPv6 autoconfiguration working.

## Configure the Switch 

Follow the instructions in [Routing and Switching](../pages/routing_and_switching.md). The instructions show you how to bond the three interfaces on your switch into a bridge. Test that your configuration has worked by rebooting your switch and running the following commands:

```
switch$ brctl show
```

Do you see the bridge? Are all three interfaces attached? 
## Configure the IP Settings on the Switch 

Your switch should be configured with the following IP information:

Hostname: switch

IPv4:
  - Address: 10.192.0.2
  - Netmask: 255.255.0.0
  - Gateway: 10.192.0.1 
  - Nameservers: 2607:f380:80f:f425::252 and 2607:f380:80f:f425::253

IPv6:
  - Address: auto
  
Be sure to update /etc/hostname and /etc/hosts! Reboot your switch to be sure you have it setup correctly. After rebooting you should be able to ping it from your router:

```
switch$ ping 10.192.0.2
```

You should also be able to SSH into it from your router:

```
ruoter$ ssh student@10.192.0.2
```

## Configure the IP Settings on Your Servers 

### Infrastructure Server 

Hostname: infra-server

IPv4:
  - Address: 10.192.0.3
  - Netmask: 255.255.0.0
  - Gateway: 10.192.0.1 
  - Nameservers: 2607:f380:80f:f425::252 and 2607:f380:80f:f425::253

IPv6:
  - Address: auto

### Application Server 

Hostname: app-server

IPv4:
  - Address: 10.192.0.4
  - Netmask: 255.255.0.0
  - Gateway: 10.192.0.1 
  - Nameservers: 2607:f380:80f:f425::252 and 2607:f380:80f:f425::253

IPv6:
  - Address: auto

## Update /etc/hosts on your Router 

On your router edit the /etc/hosts file to add a line for your switch. This will make it more convenient to access your switch from your router. Here's what your /etc/hosts file should look like:

```
127.0.0.1    localhost
127.0.1.1    router
10.192.0.2   switch
# The following lines are desirable for IPv6 capable hosts
::1   localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

Now you should be able to SSH into your switch like this:

```
router$ ssh student@switch
```

## Capture Packets on the Switch 

Your switch is an ideal place to capture packets. All packets on your network travel through your switch. When you have your switch configured and ready you can start tcpdump with the following command:

```
switch$ sudo tcpdump -i br0 -n ip host not 10.192.0.1
```

Notice there's a capture filter. That's there in case you are using SSH (like you should) to access the switch. That will suppress SSH traffic between the switch and the router. With tcpdump capturing turn on or reboot your server VMs. You should notice them attempting to get a DHCP address. They won't get one yet, but that's okay. When you're sure you are capturing the right packets stop the capture above and repeat it. This time save the packets to a file called switch-traffic.pcap.

```
switch$ sudo tcpdump -i br0 -w switch-traffic.pcap
```

You will submit that file for your milestone.

# Turn In

  - The output of the `ip neigh` command on your switch
  - The output of `brctl show` command on your switch
  - The output of `brctl showmacs br0` on your switch
  - The `switch-traffic.pcap` file
 