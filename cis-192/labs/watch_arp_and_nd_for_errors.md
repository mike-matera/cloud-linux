# Watch ARP and ND 

In this lab you'll watch ARP and ND for tell-tale signs of misconfiguration. 

## Introduction 

You don't need to be an expert to see some kinds of network misconfiguration. You just need the right kind of eyes. In this lab you'll use tcpdump to look at the ARP traffic on your internal network.

## Configure Your Switch 

Before you start the lab make sure that you've properly configured bridging on your switch. You should be able successfully ping your router from your switch.

## Ping a Working Address 

Check your ARP table:

```
switch$ arp -n
```

If it contains the IP address of your router, evict it like this:

```
switch$ sudo arp -d 10.192.0.1
```

Now, start a packet capture on your router:

```
router$ sudo tcpdump -i ens224 -n -l arp | tee arp-capture.out
```

With the capture going ping your router from your switch:

```
switch$ ping 10.192.0.1
```

You should see ARP packets. Now, on your switch, ping a bogus IP address on the same network:

```
switch$ ping 10.192.0.5
```

You should see ARP requests but not replies. The tee command created a file called arp-capture.out. Submit that file with this lab.

## Turn In
  - `arp-capture.out` (The IPv4 capture)

Submit your homework on canvas.
