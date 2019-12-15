# Milestone: A Functioning Network 

When you complete this milestone you will have finished setting up your network. It be ready to run services. When you built your firewall you have mine to use as a reference. But what if you're working without a reference? That's where the `nmap` program comes in. The Nmap program performs a port can on a computer to determine what is permitted through the firewall and what is blocked. Nmap is an important tools for an admin because it's the same tool that hackers use. You should know what the hackers know.

## Firewall Rule Recap 

If you completed the steps in [IPTables Howto](../pages/ipchains_howto.md) you should have a firewall with the following rules:

### IPv4 INPUT Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device lo | ACCEPT| 
| 2 | Input from device ens224 | ACCEPT |
| 3 | ICMP protocol | ACCEPT | 
| 4 | NEW packets to TCP port 22 | ACCEPT | 
| 5 | RELATED or ESTABLISHED packets | ACCEPT | 
| 6 | ALL packets | LOG | 

### IPv4 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT |
| 2 | RELATED or ESTABLISHED packets | ACCEPT | 
| 3 | ALL packets | LOG | 

### IPv4 NAT Table POSTROUTING Chain (Policy: ACCEPT) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from network 10.192.0.0/16, output to ens192 | MASQUERADE | 

### IPv6 INPUT Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device lo | ACCEPT | 
| 2 | Input from device ens224 | ACCEPT | 
| 3 | ICMPv6 protocol | ACCEPT | 
| 4 | Packets to UDP port 546 | ACCEPT | 
| 5 | NEW packets to TCP port 22 | ACCEPT | 
| 6 | RELATED or ESTABLISHED packets | ACCEPT | 
| 7 | ALL packets | LOG | 

### IPv6 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT | 
| 2 | ICMPv6 Protocol | ACCEPT | 
| 3 | NEW packets to TCP port 22 | ACCEPT | 
| 4 | RELATED or ESTABLISHED packets | ACCEPT | 
| 3 | ALL packets | LOG | 

Please verify that your rules match these exactly!!!!!

## Using Nmap 

The `nmap` program is already installed on Opus. Nmap can do more powerful things when run as root, but for our purposes running it as a normal user is just fine. To install nmap on your VMs run the command:

```
$ sudo apt install nmap
```

Nmap's default scan is a connect scan and it can be performed by a regular user. To scan a host (for example my router) run the command:

```
nmap <host-name-or-ip>
```

For example, scanning my router shows:

```
opus$ nmap -Pn 172.19.192.30

Starting Nmap 7.01 ( https://nmap.org ) at 2017-03-09 16:12 PST
Nmap scan report for 172.19.192.30
Host is up (0.00037s latency).
Not shown: 999 filtered ports
PORT  STATE SERVICE
22/tcp open ssh

Nmap done: 1 IP address (1 host up) scanned in 6.59 seconds
```

This is what I expect, port 22 is open and the rest are filtered. If the other ports are "closed" that means the firewall is not applied. By default only a few select ports are probed. To specify what ports you're interested in run nmap with the -p argument:

```
opus$ nmap -Pn -p 1-2048 172.19.192.30

Starting Nmap 7.01 ( https://nmap.org ) at 2017-03-09 16:13 PST
Nmap scan report for 172.19.192.30
Host is up (0.00045s latency).
Not shown: 2047 filtered ports
PORT  STATE SERVICE
22/tcp open ssh

Nmap done: 1 IP address (1 host up) scanned in 6.95 seconds
```

Sometimes you have to use the -Pn option because nmap will won't start a scan unless it can ping a target.

## Scan Your Firewall

Use `nmap` to probe the following:

  - The public IPv4 address of your router (the 172.19.192.x address)
  - The IPv6 address of your router
  - The IPv6 addresses of your switch and server VMs.

Save the output of the scans into text files and submit them.

## Collect your Firewall Rules 

It is absolutely critical that your firewalls match my reference. Subtle differences can mess up your network badly. Do not use any firewall rules you read on StackOverflow, instead figure out the commands and copy my firewall specified in [IPTables Howto](../pages/ipchains_howto.md). When you're happy with your rules be sure to save them and submit the following two files:

  - `/etc/default/iptables`
  - `/etc/default/ip6tables`

Be sure to reboot your router to make sure the rules re-apply.

## Turn In 

- The output of nmap from scanning your hosts: 
    - `router-ipv4-scan.txt`
    - `router-ipv6-scan.txt`
    - `switch-ipv6-scan.txt`
    - `app-server-ipv6-scan.txt`
    - `infra-server-ipv6-scan.txt`
- Your firewall rules:
    - `iptables`
    - `ip6tables`

Submit your files on canvas.