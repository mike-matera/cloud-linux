# Milestone: Testing DNS 

Every domain needs a DNS server, your domain will be fully operational once you complete this milestone. DNS is the system that makes names and numbers work on the Internet. Once you have achieved this milestone your site should be resolvable globally.

## Updated Firewall 

Remember, your must update your Firewall before this will work. The following chains should be updated from your previous configuration to look like this: 

### IPv4 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT |
| 2 | RELATED or ESTABLISHED packets | ACCEPT | 
| 3 | UDP/53 to 10.192.0.3 | ACCEPT | 
| 4 | ALL packets | LOG | 

### IPv6 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT | 
| 2 | ICMPv6 Protocol | ACCEPT | 
| 3 | NEW packets to TCP port 22 | ACCEPT | 
| 4 | RELATED or ESTABLISHED packets | ACCEPT | 
| 5 | UDP/53 to the IPv6 of infra | ACCEPT | 
| 6 | ALL packets | LOG | 


### IPv4 NAT Table PREROUTING Chain (Policy: ACCEPT) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | UDP/53 to the IPv4 of router | DNAT --to=10.192.0.3 | 

## Test from Opus 

When you're testing your domain you should test from Opus. Opus is outside of your network (so firewall rules apply) and you should tell dig to use your nameserver directly by IP address with the following form:

```
$ dig <name-to-lookup> @<dns-server-ip>
```

If you fail to use the `@<dns-server-ip>` and your domain records are broken Cabrillo's nameserver will remember your broken record until `$TTL` expires. That could be a while. Run the dig command to do the following:

```
$ dig rotuer.<my-domain>.cis.cabrillo.edu @<my-dns-server-ip> 
$ dig AAAA infra.<my-domain>.cis.cabrillo.edu @<my-dns-server-ip>
$ dig -x <router-ipv6-address> @<my-dns-server-ip>
$ dig -x <db-server-ipv6-address> @<my-dns-server-ip>
```

Save the output of each dig command and submit them to accomplish this milestone. 

## Try it at Home 

If you're confident that the above dig queries got the right answer do the same thing at home. You can use dig on Linux or MAC. On Windows use the [nslookup](https://technet.microsoft.com/en-us/library/cc725991.aspx) command from the command line. You only need to repeat one of the queries. Whichever you like. Save or screenshot the output and submit it.

## Turn In 

  - The output of each dig command from the first part
  - The output or screenshot from your DNS queries at home.
  - Your firewall rules:
    - `/etc/default/iptables`
    - `/etc/default/ip6tables`
  - **DNS information I need to connect you**:
    - Your domain name (again, sorry)
    - The public IPv4 address of your router 
    - The EUI-64 IPv6 address of infra server

Submit your work on Canvas.