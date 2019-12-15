# Milestone: An IPv6 Network 

In class you learned about the the role of DHCPv6 and Router Advertisement. For this milestone you will setup those features on your router. Once you have done that your VMs will be fully operational on IPv6. In contrast it will take two more weeks to do the same task for IPv4 because you'll have to setup NAT. To complete this milestone you will have to have completed the instructions int the [SLAAC](../pages/slaac.md) lecture.

## Capturing Packets 

To prove that you have completed the task you will capture packets on your router. Your first packet capture will show me the DHCPv6 packets that setup your prefix delegation. Run `tcpdump` in one shell:

```
$ sudo tcpdump -i ens192 -w dhcp-pd.pcap udp port 546 or udp port 547
```

With the packet capture running execute this command in a second shell:

```
$ sudo service wide-dhcpv6-client restart
```

That should re-acquire your prefix. Copy the capture file onto your own computer and open the capture in Wireshark. Verify that the DHCP packets are present. When you're happy with the first capture do the second. The second capture will capture RAs that are sent out on eth1. In your first shell run the following command:

```
$ sudo tcpdump -i ens224 -w router-advert.pcap icmp6
```

Wait at least two minutes to be sure that there are RAs in your capture. Copy the capture file to your computer and open it with Wireshark. If you see RAs then submit both files to achieve this milestone.

## Turn In 

  * `dhcp-pd.pcap` showing your DHCP exchange
  * `router-advert.pcap` showing at least one RA packet coming from your router.

Submit the files on Canvas.