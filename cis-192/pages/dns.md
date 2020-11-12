# DNS 

The Domain Name System, or DNS, is one of the Internet's fundamental building blocks. It is the global, hierarchical, and distributed host information database that's responsible for translating names into addresses and vice versa, routing mail to its proper destination, and many other services.

BIND (Berkeley Internet Name Domain) is an implementation of the DNS protocol and provides an openly redistributable reference implementation of the major components of the Domain Name System, including:

* Domain Name System server
* Domain Name System resolver library
* Tools for managing and verifying the proper operation of the DNS server
 
The BIND DNS Server, named, is used on the vast majority of name serving machines on the Internet, providing a robust and stable architecture on top of which an organization's naming architecture can be built.

This guide will show you how to setup DNS with BIND version 9, the reference implementation of the Domain Name System (DNS) using Docker.

## Commands 

  * dig

## Configuration 

  * /etc/bind/*

## Further Reading 

  * [Ubuntu Server Guide](https://help.ubuntu.com/12.04/serverguide/index.html) has an excellent section about DNS
  * [Linux DNS HowTo](http://www.tldp.org/HOWTO/DNS_HOWTO.html)

## Installing BIND 

Bind is installed on Ubuntu using `apt`. We will use a Dockerfile based on Ubuntu Focal. 

```Dockerfile
FROM ubuntu:focal as main
RUN apt-get update -q -y && apt-get upgrade -y && apt-get install -y -q bind9
RUN rm -f /etc/bind/named.conf
COPY --chown=bind:bind db.* /etc/bind/
COPY --chown=bind:bind named.conf /etc/bind/
COPY entrypoint.sh /
EXPOSE 53/udp 
CMD ["/bin/sh", "/entrypoint.sh"]
```

Copy this code into a `Dockerfile` in an empty directory. We will need a few more files before we're ready to build. 

## A Custom Entrypoint

If you were simply running bind9 on Ubuntu it would be started by `systemd`. In a container we need to start it manually. The easiest way to do this is to create a simple shell script that starts the daemon. This gives us maximal flexibility in how we want to start the server, including making it possible to use environment variables to tweak settings after the container is built. Create a file called `entrypoint.sh` in the same directory as the `Dockerfile` and put this inside of it: 

```bash
#! /bin/sh 

/usr/sbin/named -g -c /etc/bind/named.conf -u bind 
```

## Configure BIND

BIND has the following default configuration files. We'll override one of them in our Dockerfile and copy a custom zone file. 

```
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

The top level configuration file for bind is `/etc/bind/named.conf` and it controls how the bind daemon works. Bind is also configured to use *zone* files. Zones are databases that contain the name-to-ip-address maps that bind serves on the internet. The `Dockerfile` overrides the default configuration file. Create a file called `named.conf` in the same directory as the `Dockerfile` and copy the following contents:

```conf
acl "trusted" {
     10.192.0.0/16;
     localhost;
 };

options {
	directory "/var/cache/bind";
    allow-query { any; };
    allow-recursion { trusted; }; 

    forwarders {
        8.8.8.8;
        8.8.4.4;
    };

    dnssec-enable no;
    dnssec-validation no;
};

# Fix to match your domain.
zone "mike.cis.cabrillo.edu" IN {
    type master;
    file "/etc/bind/db.mike.cis.cabrillo.edu"; 
    allow-update { none; };
    allow-transfer { none; };
};
```  

Finally, we need a file that is the contents of the DNS database, the one that contains the host name to IP address mappings. The default configuration file calls this `db.mike.cis.cabrillo.edu`. You should rename the file to match your domain: 

```conf
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
ns1             IN A    34.204.242.206 ; FIXME
ns1             IN AAAA 2600:1f18:bb3:f901:aaeb:d61:3176:8f8f ; FIXME

; Host records
www             IN A    34.204.242.206 ; FIXME
www             IN AAAA 2600:1f18:bb3:f901:aaeb:d61:3176:8f8f ; FIXME
```

### Stop and Test! 

Starting with my configuration, build the DNS container and use `dig` to make sure it's serving records correctly. 

```
$ docker build -t dns:latest .
$ docker run -it --rm -p 53000:53/udp --name dns-test dns:latest 
```

> **NOTE:** If you're trying this on opus pick a different port than `53000` so that your port doesn't collide with another student's!** 

Check the output for errors. You should see something this: 

``` 
05-Nov-2020 19:19:46.555 zone mike.cis.cabrillo.edu/IN: loaded serial 1
05-Nov-2020 19:19:46.559 all zones loaded
05-Nov-2020 19:19:46.559 running
```

Also, use the `ss` command to verify that the DNS container is listening on UDP/53000. 

```
$ sudo ss -lnup | grep 53000 
UNCONN 0   0   *:53000  *:*  users:(("docker-proxy",pid=900223,fd=4)) 
```

Finally, use `dig` to make sure that your infra server is able to forward requests:

```
$ dig -p 53000 @localhost A www.mike.cis.cabrillo.edu 

; <<>> DiG 9.16.1-Ubuntu <<>> -p 53000 @localhost A www.mike.cis.cabrillo.edu
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7860
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: e157a7da853901ff010000005fa455a08efa989f0572bf05 (good)
;; QUESTION SECTION:
;www.mike.cis.cabrillo.edu.     IN      A

;; ANSWER SECTION:
www.mike.cis.cabrillo.edu. 600  IN      A       34.204.242.206

;; Query time: 3 msec
;; SERVER: 127.0.0.1#53000(127.0.0.1)
;; WHEN: Thu Nov 05 11:42:24 PST 2020
;; MSG SIZE  rcvd: 98
```

The response to `dig` should contain the answer shown. 

## Configure Your Forward Zone 

Now that your server is ready to serve you can update the DNS zones and records to mach your domain name and IP address. A *zone* is a group of records for one domain. Start by adding a *forward* zone, that's a zone that finds a number for a name:

Change zone name and file name: 

```
# Fix to match your domain.
zone "mike.cis.cabrillo.edu" IN {
    type master;
    file "/etc/bind/db.mike.cis.cabrillo.edu"; 
    allow-update { none; };
    allow-transfer { none; };
};
```

> *Replace mike.cis.cabrillo.edu with your domain!*

Now create the records in your zone. The records belong in the file you named in the `file "...."` directive. Change the name in the example to a file named after your domain. 

### Stop and Test! 

Now check to make sure your configuration is working. Restart your DNS server and check the system log. Look for a line like this: 

```
infra-server named[3907]: zone mike.cis.cabrillo.edu/IN: loaded serial 1
```

If your zone loaded you can now use `dig` to lookup your own hosts. Try this with all of your host names. Don't move on until dig shows you all of the names you expect and make sure the IP addresses are correct! 

## Configure a Reverse Zone (Optional)

> Your reverse zones will not work on AWS but you can still test them.

A reverse zone does the *opposite* of a normal lookup. A reverse zone establishes a number to name translation. It's customary to create reverse zones so that people on the internet can lookup your IP addresses. 

Create a reverse zone for IPv4 and IPv6 by adding zones in your `named.conf`:

```
zone "242.204.34.in-addr.arpa" {
 type master;
 notify no;
 file "/etc/bind/db.mike-ipv4";
};

zone "1.0.9.f.3.b.b.0.8.1.f.1.0.0.6.2.ip6.arpa" {
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
206     IN PTR          ns1.mike.cis.cabrillo.edu.
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
f.8.f.8.6.7.1.3.1.6.d.0.b.e.a.a IN PTR ns1.mike.cis.cabrillo.edu.
```

### Stop and Test! 

Restart your DNS server and make sure all zones loaded. Then use dig to test reverse zones: 

```
$ dig -p 53000 @localhost -x 34.204.242.206
$ dig -p 53000 @localhost -x 2600:1f18:bb3:f901:aaeb:d61:3176:8f8f
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

In order for DNS to work for hosts outside of your network you must change the firewall on your router to allow the traffic. This is easy for IPv6. Add rules to do the following:

* Allow IPv4/UDP traffic on port 53
* Allow IPv6/UDP traffic on port 53

## Deploy DNS 

Ready to have your own domain? Make sure that all of the work you have done with `dig` shows that your DNS server is working on your local machine. Once you deploy DNS the internet will remember your records for the time in `$TTL`. If you took my value that is set to one hour so corrections will take that long to propagate.

Verify that:

1. All of your records can be accessed with `dig`
1. You have replaced the serial number with a dated version
1. You have opened your firewall to allow DNS 
1. You have given me your domain name and external IP information

> **Note:** Watch out for port 53 being busy 

Deploy on your AWS instance using this command:

```
$ docker run -d -p 10.192.1.101:53:53/udp [your-container-tag-here]
```
