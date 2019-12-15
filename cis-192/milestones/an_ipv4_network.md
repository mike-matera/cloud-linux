# Milestone: An IPv4 Network 

When you complete this milestone you will have a working IPv4 network but no end-to-end connectivity. That's still a week away. In class you learned about the role of DHCP in an IPv4 network. For this milestone you'll setup a DHCP server on your router to serve addresses to the internal hosts. The DHCP server should have addresses reserved for your servers because they need static IPs. To complete this milestone you will have to complete the instructions here: [DHCP](../pages/dhcp_howto.md)

## Changing Your Host's IP Configuraton 

Now that you have DHCP setup you should change all of the hosts on your internal network to use DHCP (except the router). In short set:

  * switch - set br0 to use DHCP
  * infra-server - set ens192 to use DHCP
  * app-server - set ens192 to use DHCP

Configure your DHCP server to have permanent assignments for these hosts. That will save you some headache.

## Capturing Packets 

To prove that you have completed the task you will capture packets on your router. Your packet capture will show me the DHCP packets that are being sent between your two servers and your router. In order to be complete both servers must have packets in your capture file. You can wait at least five minutes for the servers to renew their leases or you can reboot them from VMware. Run `tcpdump`:

```
router$ sudo tcpdump -i ens224 -w dhcp-v4.pcap udp
```

Copy the capture file to your computer and open it with Wireshark. If you see DHCP packets from both servers submit the file to achieve this milestone.

## Turn In 

  * `dhcp-v4.pcap` showing your DHCP exchange
  * Your DHCPD configuration on your router:
      * `/etc/dhcp/dhcpd.conf`

Submit the files on Canvas.