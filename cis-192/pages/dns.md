# DNS 

The Domain Name System, or DNS, is one of the Internet's fundamental building blocks. It is the global, hierarchical, and distributed host information database that's responsible for translating names into addresses and vice versa, routing mail to its proper destination, and many other services.

BIND (Berkeley Internet Name Domain) is an implementation of the DNS protocols and provides an openly redistributable reference implementation of the major components of the Domain Name System, including:

 * Domain Name System server
 * Domain Name System resolver library
 * Tools for managing and verifying the proper operation of the DNS server
 
The BIND DNS Server, named, is used on the vast majority of name serving machines on the Internet, providing a robust and stable architecture on top of which an organization's naming architecture can be built.

This guide will show you how to setup DNS with BIND version 9, the reference implementation of the Domain Name System (DNS).

The lecture slides are [here](https://docs.google.com/presentation/d/1M7k9Pm1UFjS5nXwK7oLJrKVd5eKA5vHgvi8qceqbC0Y/edit?usp=sharing).

## Commands 

  * dig

## Configuration 

  * /etc/bind/*

## Further Reading 

  * [Ubuntu Server Guide](https://help.ubuntu.com/12.04/serverguide/index.html) has an excellent section about DNS
  * [Linux DNS HowTo](http://www.tldp.org/HOWTO/DNS_HOWTO.html)

## Installing BIND 

Bind is installed on Ubuntu using `apt`. You should install bind your *infrastructure server*. You'll need to setup port forwarding on your router to make bind available to the internet. 

```
infra$ sudo apt install bind9 
```

Once you have bind installed you should see the configuration files are present: 

```
infra$ tree /etc/bind
/etc/bind
├── bind.keys
├── db.0
├── db.127
├── db.255
├── db.empty
├── db.local
├── db.root
├── named.conf
├── named.conf.default-zones
├── named.conf.local
├── named.conf.options
├── rndc.key
└── zones.rfc1918
```

Bind is configured to work out of the box but you'll need to configure it to serve records on your custom domain. 

## Configuring BIND 

The top level configuration file for bind is `/etc/bind/named.conf` and it controls how the bind daemon works. Bind is also configured to use *zone* files. Zones are databases that contain the name-to-ip-address maps that bind serves on the internet. 

This is the default `/etc/bind/named.conf` on Ubuntu: 

```
// This is the primary configuration file for the BIND DNS server named.
//
// Please read /usr/share/doc/bind9/README.Debian.gz for information on the 
// structure of BIND configuration files in Debian, *BEFORE* you customize 
// this configuration file.
//
// If you are just adding zones, please do that in /etc/bind/named.conf.local

include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";
```

As you can see the top-level configuration file "includes" other files. This is a way to break up the configuration into parts. There are three parts of the configuration: 

  * `named.conf.options` - Top level options and parameters for the nameserver. 
  * `named.conf.local` - Configuration for local domains. You will place your custom domain configuration here. 
  * `named.conf.default-zones` - Zone configuration for the default domains (called *zones*). The default zones map the `localhost` domain, the 127.0.0.0/8, 255.0.0.0/8 and 0.0.0.0/8 ip address zones. 
  
### Configuring Local Options 

There are two configuration changes to make in `/etc/bind/named.conf.options`. We wil disable DNSSEC because we will not configure it and we'll set forwarders. Your DNS server will fill two roles: It will answer queries for your domain (an *authoratative* nameserver) and it will answer general queries for your hosts (a *non-authoratative* nameserver). Turning on forwarders tells your nameserver to "forward" non-authoratative requests to another nameserver. 

Uncomment the forwarders declaration and add Google's nameservers:

```
forwarders {
    8.8.8.8;
    8.8.4.4;
};
```

Disable DNSSEC by adding the `dnssec-enable no;` line: 

```
        dnssec-enable no;
        dnssec-validation auto;
```

#### Stop and Test! 

Before you continue test that your options are correct. Restart bind to make sure that you don't have syntax errors: 

``` 
infra$ sudo systemctl restart bind9
```

Check `/var/log/syslog` for errors. You should see something this: 

``` 
infra-server named[3634]: zone 255.in-addr.arpa/IN: loaded serial 1
infra-server named[3634]: all zones loaded
infra-server named[3634]: running
```

Also, use the `ss` command to verify that the DNS server is listening on UDP/53. 

```
infra$ sudo ss -lnup 
State       Recv-Q Send-Q      Local Address:Port                     Peer Address:Port              
UNCONN      0      0              10.192.0.3:53                                  *:*                   users:(("named",pid=3634,fd=514))
UNCONN      0      0               127.0.0.1:53                                  *:*                   users:(("named",pid=3634,fd=513))
UNCONN      0      0                       *:68                                  *:*                   users:(("dhclient",pid=907,fd=6))
UNCONN      0      0                      :::53                                 :::*                   users:(("named",pid=3634,fd=512))
```

Finally, use `dig` to make sure that your infra server is able to forward requests:

```
infra$ dig www.google.com @localhost 
```

The response to `dig` should contain an answer. 

### Configure Your Forward Zone 

Now that your server is ready to serve you can add DNS zones and records. A *zone* is a group of records for one domain. Start by adding a *forward* zone, that's a zone that finds a number for a name:

Add this to `/etc/named/named.conf.local`

```
zone "mike.cis.cabrillo.edu" {
 type master;
 file "/etc/bind/db.mike";
};
```

> *Replace mike.cis.cabrillo.edu with your domain!*

Now create the records in your zone. The records belong in the file you named in the `file "...."` directive. Change the name in the example to a file named after your domain. In that file add the following DNS records:

```
; The @ sign is a wildcard that is replaced with the full domain name of this zone
; as defined in the zone configuration. In my configuration it's mike.cis.cabrillo.edu

$TTL 600
@ IN SOA ns1 student (
         1 ; Serial
     86400 ; Refresh 
      3600 ; Retry 
    172800 ; Expire 
       600 ; Negative Cache TTL
);

; These are the "glue" records. They tell people who your nameservers are. 

@               IN NS   ns1
ns1             IN A    172.19.192.30
ns1             IN AAAA 2607:f380:80f:f900:250:56ff:fe99:be69

; Now add your hosts internal addresses

router          IN A    10.192.0.1
switch          IN A    10.192.0.2
infra           IN A    10.192.0.3
app             IN A    10.192.0.4

; Now add your hosts IPv6 EUI-64 or static addresses 

router          IN AAAA 2607:f380:80f:f192::30
switch          IN AAAA 2607:f380:80f:f900:250:56ff:fe99:b10
infra           IN AAAA 2607:f380:80f:f900:250:56ff:fe99:be69
app             IN AAAA 2607:f380:80f:f900:250:56ff:fe99:c478
```

> Update this example to match your IP addresses!

#### Stop and Test! 

Now check to make sure your configuration is working. Restart your DNS server and check the system log. Look for a line like this: 

```
infra-server named[3907]: zone mike.cis.cabrillo.edu/IN: loaded serial 1
```

If your zone loaded you can now use `dig` to lookup your own hosts. Try this with all of your host names: 

```
$ dig ns1.mike.cis.cabrillo.edu @localhost 

; <<>> DiG 9.10.3-P4-Ubuntu <<>> ns1.mike.cis.cabrillo.edu @localhost
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54431
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;ns1.mike.cis.cabrillo.edu.	IN	A

;; ANSWER SECTION:
ns1.mike.cis.cabrillo.edu. 600	IN	A	172.19.192.30

;; AUTHORITY SECTION:
mike.cis.cabrillo.edu.	600	IN	NS	ns1.mike.cis.cabrillo.edu.

;; ADDITIONAL SECTION:
ns1.mike.cis.cabrillo.edu. 600	IN	AAAA	2607:f380:80f:f900:250:56ff:fe99:be69

;; Query time: 0 msec
;; SERVER: ::1#53(::1)
;; WHEN: Thu Oct 24 09:21:13 PDT 2019
;; MSG SIZE  rcvd: 112
```

Don't forget to dig for AAAA records: 

```
$ dig AAAA app.mike.cis.cabrillo.edu @localhost

; <<>> DiG 9.10.3-P4-Ubuntu <<>> AAAA app.mike.cis.cabrillo.edu @localhost
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 55879
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;app.mike.cis.cabrillo.edu.	IN	AAAA

;; ANSWER SECTION:
app.mike.cis.cabrillo.edu. 600	IN	AAAA	2607:f380:80f:f900:250:56ff:fe99:c478

;; AUTHORITY SECTION:
mike.cis.cabrillo.edu.	600	IN	NS	ns1.mike.cis.cabrillo.edu.

;; ADDITIONAL SECTION:
ns1.mike.cis.cabrillo.edu. 600	IN	A	172.19.192.30
ns1.mike.cis.cabrillo.edu. 600	IN	AAAA	2607:f380:80f:f900:250:56ff:fe99:be69

;; Query time: 0 msec
;; SERVER: ::1#53(::1)
;; WHEN: Thu Oct 24 09:22:02 PDT 2019
;; MSG SIZE  rcvd: 144
```

Don't move on until dig shows you all of the names you expect and make sure the IP addresses are correct! 

### Configure a Reverse Zone 

A reverse zone does the *opposite* of a normal lookup. A reverse zone establishes a number to name translation. It's customary to create reverse zones so that people on the internet can lookup your IP addresses. 

Create a reverse zone for IPv4 and IPv6 by adding zones in your `/etc/named/named.conf.local`:

```
zone "0.192.10.in-addr.arpa" {
 type master;
 notify no;
 file "/etc/bind/db.mike-ipv4";
};

// Note: Use the IPv6 address for your INTERNAL network
zone "0.0.9.f.f.0.8.0.0.8.3.f.7.0.6.2.ip6.arpa" {
 type master;
 notify no;
 file "/etc/bind/db.mike-ipv6";
};
```

> Change these zones to match your IP addresses! 

Notice that the reverse zones are the IP address **backwards**. This can be a bit hard on the eyes so work carefully! 

Now add your reverse zone database files. This is the IPv4 file:

```
$TTL 600
@ IN SOA ns1.mike.cis.cabrillo.edu. student.mike.cis.cabrillo.edu. (
         1 ; Serial
     86400 ; Refresh 
      3600 ; Retry 
    172800 ; Expire 
       600 ; Negative Cache TTL
);

; Glue record
@       IN NS           ns1.mike.cis.cabrillo.edu.

; Reverse reords
1       IN PTR  router.mike.cis.cabrillo.edu.
2       IN PTR  switch.mike.cis.cabrillo.edu.
3       IN PTR  infra.mike.cis.cabrillo.edu.
4       IN PTR  app.mike.cis.cabrillo.edu.
```

This is the ipv6 file: 

```
$TTL 600
@ IN SOA ns1.mike.cis.cabrillo.edu. root.mike.cis.cabrillo.edu. (
         1 ; Serial
     86400 ; Refresh 
      3600 ; Retry 
    172800 ; Expire 
       600 ; Negative Cache TTL
);

; Glue record
@       IN NS   ns1.mike.cis.cabrillo.edu.

; Reverse records for ipv6
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0 IN PTR router.mike.cis.cabrillo.edu.
0.1.b.0.9.9.e.f.f.f.6.5.0.5.2.0 IN PTR switch.mike.cis.cabrillo.edu.
9.6.e.b.9.9.e.f.f.f.6.5.0.5.2.0 IN PTR infra.mike.cis.cabrillo.edu.
8.7.4.c.9.9.e.f.f.f.6.5.0.5.2.0 IN PTR app.mike.cis.cabrillo.edu.
```

#### Stop and Test! 

Restart your DNS server and make sure all zones loaded: 

```
infra-server named[4097]: zone 0.192.10.in-addr.arpa/IN: loaded serial 1
infra-server named[4097]: zone 0.0.9.f.f.0.8.0.0.8.3.f.7.0.6.2.ip6.arpa/IN: loaded serial 1
infra-server named[4097]: zone mike.cis.cabrillo.edu/IN: loaded serial 1
infra-server named[4097]: all zones loaded
infra-server named[4097]: running
```

Use dig to test reverse zones: 

```
infra$ dig -x 10.192.0.1 @localhost

; <<>> DiG 9.10.3-P4-Ubuntu <<>> -x 10.192.0.1 @localhost
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6645
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;1.0.192.10.in-addr.arpa.	IN	PTR

;; ANSWER SECTION:
1.0.192.10.in-addr.arpa. 604800	IN	PTR	router.mike.cis.cabrillo.edu.

;; AUTHORITY SECTION:
0.192.10.in-addr.arpa.	604800	IN	NS	ns1.mike.cis.cabrillo.edu.

;; Query time: 0 msec
;; SERVER: ::1#53(::1)
;; WHEN: Thu Oct 24 09:46:58 PDT 2019
;; MSG SIZE  rcvd: 119
```

Don't forget IPv6:

```
infra$ dig -x 2607:f380:80f:f900::1 @localhost

; <<>> DiG 9.10.3-P4-Ubuntu <<>> -x 2607:f380:80f:f900::1 @localhost
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37283
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.9.f.f.0.8.0.0.8.3.f.7.0.6.2.ip6.arpa. IN PTR

;; ANSWER SECTION:
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.9.f.f.0.8.0.0.8.3.f.7.0.6.2.ip6.arpa. 604800 IN PTR	router.mike.cis.cabrillo.edu.

;; AUTHORITY SECTION:
0.0.9.f.f.0.8.0.0.8.3.f.7.0.6.2.ip6.arpa. 604800 IN NS ns1.mike.cis.cabrillo.edu.

;; Query time: 0 msec
;; SERVER: ::1#53(::1)
;; WHEN: Thu Oct 24 09:48:01 PDT 2019
;; MSG SIZE  rcvd: 163
```

## Gotchas 

There are a number of things that often trip-up beginners:

  * Don't forget semicolons. They are required almost everywhere. If BIND doesn't start look in /var/log/syslog.
  * Remember absolute and relative paths! Bind cares about the trailing dot, if you leave it off BIND assumes you mean a relative path. 

Here's an example of getting messing up an absolute path:

```
## Assume this is a record for matera.com.
server1 IN A 1.2.3.4               ; This means "server1.matera.com."
server2.matera.com. IN A 1.2.3.5   ; This means "server2.matera.com."
server3.matera.com IN A 1.2.3.6    ; Oops! This means "server3.matera.com.matera.com."
```

## Firewall Updates 

In order for DNS to work for hosts outside of your network you must change the firewall on your router to allow the traffic. This is easy for IPv6. Add a rule to do the following: 

 * Filter FORWARD chain:
   * Destination IPv6: The IPv6 of your infra server
   * Protocol: UDP
   * Port: 53 
   * ACCEPT 
   
The configuration is more complicated for IPv4. Your router has a public IP address but your infra server does not. The router therefore needs to perform NAT to make your DNS server available using the router's IPv4 address. This requires two rules: 

 * Filter FORWARD chain:
   * Destination IPv4: 10.192.0.3 (infra-server)
   * Protocol: UDP
   * Port: 53 
   * ACCEPT 
 * NAT PREROUTING chain:
   * Destination: The public IPv4 of your router
   * Protocol: UDP
   * Port: 53 
   * DNAT --to 10.192.0.3

### Test Your DNS and Firewall 

IF you have everything working you should be able to use dig on opus to query your DNS server. Here are the commands that I used to test my DNS:

```
opus$ dig NS mike.cis.cabrillo.edu @172.19.192.30
opus$ dig NS mike.cis.cabrillo.edu @2607:f380:80f:f900:250:56ff:fe99:be69
```

> ![](/static/icon_warning_small.png) 
> Use your domain and IP addresses and don't forget to save your firewall!

## Update DHCP 

Update your DHCP server to tell your VMs to use your new DNS server. Also, update your router (which doesn't use DHCP) to use infra for DNS. 
