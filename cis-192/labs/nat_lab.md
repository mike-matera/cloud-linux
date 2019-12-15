# Lab: Visualizing NAT 

In today's lab you will enable NAT and watch as packets traverse your router. You must first follow the instructions in [IPTables Howto](../pages/ipchains_howto.md). Be sure you have NAT enabled and you can ping from your switch VM to google using IPv4.

## Capture on Two Interfaces 

Capture packets using tcpdump on the internal and external interfaces:

```
router$ sudo tcpdump -i ens192 -w ens192-capture.pcap icmp &
router$ sudo tcpdump -i ens224 -w ens224-capture.pcap icmp &
```

## Ping From Your Switch 

With both captures running execute the following command on your switch:

```
switch$ ping 8.8.8.8
```

Your captures should record the pings as they pass through your router.

## Analyze your Pings 

After you have a few pings bring both files onto your machine and examine them in Wireshark. You should be able to answer the following question by looking at your packets:

  - What's the IP address of your switch as seen on ens192?
  - What's the IP address of your switch as seen on ens224?

## Turn In 

Submit both of your packet captures on Canvas.
