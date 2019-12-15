# Milestone: Send and Receive Email 
 
In this milestone you will send (and receive) your first email. Before you begin you should verify your MX and SPF records are in place using dig. If they're not don't try to send email, you will poison DNS and have to wait for the TTL to expire on your broken DNS records.

## Updated Firewall 

Remember, your must update your Firewall before this will work. The following chains should be updated from your previous configuration to look like this: 

### IPv6 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT | 
| 2 | ICMPv6 Protocol | ACCEPT | 
| 3 | NEW packets to TCP port 22 | ACCEPT | 
| 4 | NEW packets to TCP port 25 of infra | ACCEPT | 
| 5 | RELATED or ESTABLISHED packets | ACCEPT | 
| 6 | UDP/53 to the IPv6 of infra | ACCEPT | 
| 7 | ALL packets | LOG | 

## Install Alpine and Send me Email 

Install the command line MUA called alpine:

```
infra$ sudo apt install alpine
```

Once you have alpine installed send email to yourself at Opus:

```
<your-login>@opus.cis.cabrillo.edu
```

Alpine is installed on Opus. When you can receive and reply to your own email, send an email to me:

```
mmatera@opus.cis.cabrillo.edu
```

## Send Yourself Email 

Use your existing personal account (e.g. Gmail) to send email to yourself on your own domain:

```
student@<yourdomain>.cis.cabrillo.edu
```

If your DNS, firewall and Postfix are setup properly you will receive the email. When you have forward it to me at my Opus address. 

## Turn In

  - Copy-and-paste the emails you sent me into Canvas (I will verify it on Opus)

Submit your homework on canvas.