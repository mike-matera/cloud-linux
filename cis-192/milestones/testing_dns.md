# Milestone: Testing DNS 

Every domain needs a DNS server, your domain will be fully operational once you complete this milestone. DNS is the system that makes names and numbers work on the Internet. Once you have achieved this milestone your site should be resolvable globally.

## Updated Firewall 

Remember, your must update your Firewall before this will work. You must allow UDP packets to access port 53.

## Test from Opus 

When you're testing your domain you should test from Opus. Opus is outside of your network (so firewall rules apply) and you should tell dig to use your nameserver directly by IP address with the following form:

```
$ dig <name-to-lookup> @<your-aws-server-ip>
```

If you fail to use the `@<your-aws-server-ip>` and your domain records are broken Cabrillo's nameserver will remember your broken record until `$TTL` expires. That could be a while. Run the dig command to do the following:

```
$ dig www.<my-domain>.cis.cabrillo.edu @<my-dns-server-ip> 
$ dig AAAA www.<my-domain>.cis.cabrillo.edu @<my-dns-server-ip>
```

Save the output of each dig command and submit them to accomplish this milestone. 

## Try it at Home 

If you're confident that the above dig queries got the right answer do the same thing at home. You can use dig on Linux or MAC. On Windows use the [nslookup](https://technet.microsoft.com/en-us/library/cc725991.aspx) command from the command line. You only need to repeat one of the queries. Whichever you like. Save or screenshot the output and submit it.

## Turn In 

  - The output of each dig command from the first part
  - The output or screenshot from your DNS queries at home.
  - **DNS information I need to connect you**:
    - Your domain name (again, sorry)
    - The public IPv4 address of your instance 
    - The IPv6 address of your instance

Submit your work on Canvas.
