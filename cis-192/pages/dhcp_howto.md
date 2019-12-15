# DHCP 

Ubuntu comes with the DHCP client installed by default. The DHCP client is the software responsible for obtaining leases from a DHCP server and every host should have one. The DHCP server is not commonly installed and is responsible for generating and handing out leases. This is an important job on the network but few hosts need to do it. This lesson will show you how to setup your DHCP server. 

The presentation slides are [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1WNeupEJD5vkjxMnFA14FrHZoVkTPGvLMEVmDEFzQMUc/edit?usp=sharing).

## Commands 

* apt-get
* service
* netstat

## Configuration 

* /etc/dhcp/dhcpd.conf
* /etc/default/isc-dhcp-server

## Install the DHCP Server 

Use apt:

```
router$ sudo apt-get install isc-dhcp-server
```

This installs DHCP server for both IPv4 and IPv6. They have very different roles on the network and we will not need DHCPv6 in our networks. By default your DHCP server will have an empty configuration so it won't give out IP addresses until you have changed things.

## Setup Your Network 

Now it's time to configure DHCP for your network. The configuration is located in `/etc/dhcp/dhcpd.conf`. There are some key options that you should set in the file: 

```
# Set your internal domain name
option domain-name "yourname.cis.cabrillo.edu";

# Name servers can be referenced by name, they will be turned into IP addresses automatically by the server
option domain-name-servers 8.8.8.8; 

# Short lease times are good for debugging
default-lease-time 600; 
max-lease-time 1200;
```

Notice that you have setup your router's IP address as the DNS server. Since your hosts don't yet have IPv4 connectivity they can't use Cabrillo's IPv4 nameservers anyway. Soon your router will run DNS and this will work. These global options are sufficient for your network. A complicated network will have multiple scopes. Yours only has one so there's no real difference between global and local options. Add the following zone to your configuration file:

```
subnet 10.192.0.0 netmask 255.255.0.0 {
  option routers 10.192.0.1; 
  option broadcast-address 10.192.255.255; 
  range 10.192.5.1 10.192.5.100;
}
```

The DHCP server is started with an option that restricts which Ethernet devices that it will hand out addresses on. That option is located in `/etc/default/isc-dhcp-server`. Make sure the `INTERFACES` variable is set like this:

```
# This is /etc/default/isc-dhcp-server
INTERFACES="ens224"
```

<div class="alert alert-danger">
<b>WARNING:</b> Do not put ens192 in the list!
</div>

Now you are ready to test your DHCP server. You can restart the daemon by running:

```
router$ sudo systemctl restart isc-dhcp-server
```

If you have everything setup correctly you will see lines similar to the following lines in `/var/log/syslog`:

```
router dhcpd[7116]: Listening on LPF/ens224/00:50:56:99:6d:3a/10.192.0.0/16
router sh[7116]: Listening on LPF/ens224/00:50:56:99:6d:3a/10.192.0.0/16
router dhcpd[7116]: Sending on   LPF/ens224/00:50:56:99:6d:3a/10.192.0.0/16
router sh[7116]: Sending on   LPF/ens224/00:50:56:99:6d:3a/10.192.0.0/16
router dhcpd[7116]: Sending on   Socket/fallback/fallback-net
router sh[7116]: Sending on   Socket/fallback/fallback-net
router dhcpd[7116]: Server starting service.
```

You can also see that DHCP is listening by running the command:

```
router$ sudo ss -lnup
State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
UNCONN     0      0            *:67                       *:*                   users:(("dhcpd",pid=7116,fd=7))
UNCONN     0      0            *:34181                    *:*                   users:(("dhcpd",pid=7116,fd=20))
UNCONN     0      0           :::546                     :::*                   users:(("dhcp6c",pid=2679,fd=4))
UNCONN     0      0           :::48961                   :::*                   users:(("dhcpd",pid=7116,fd=21))
```

The output of the `ss` command shows that the DHCP server is listening on UDP port 67. That's good!

## Create a Reservation 

Last week you observed your servers futilely attempting to receive an IPv4 address over DHCP. If you have your server setup correctly they should now get an address. Verify that they are doing so by using `tcpdump` to observer the DHCP conversation. On your router run the following command:

```
router$ sudo tcpdump -i ens224 udp
```

If you used the default lease time of 600 seconds each server will renew every five minutes. If you don't want to wait that long you could reboot your server. The switch is statically configured so don't wait for it. The IP addresses your servers get are from the pool but not entirely predicable. That's bad news for servers because you need their addresses to stay the same. Fix this by reserving a DHCP address for each server by MAC address. You should have collected MAC addresses in the previous week's lab. Add a declaration like the following to your DHCP configuration file:

```
host app-server {
 hardware ethernet 00:50:56:bd:0a:6c;
 fixed-address 10.192.0.4;
}

host infra-server {
 hardware ethernet 00:50:56:bd:0a:7c;
 fixed-address 10.192.0.3;
}
```

Be sure to change the MAC address to match your hosts! Also, be sure that the IP address you have listed is NOT in the pool.
