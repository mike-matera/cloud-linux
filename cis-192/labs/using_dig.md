# Using dig 

Dig is a utility that probes the domain name system (DNS). It's the most essential tool for understanding what's right and what wrong with your DNS server. If you don't use dig you'll suffer with problems in DNS.

## Testing DNS with dig 

There are easy ways to lookup IP addresses and there are helpful ways to lookup IP addresses. If you're an administrator and you want to know what's really going on there's only one tool for you: dig. Dig can perform any DNS query, iterative or recursive and inform you of the complete result. Dig can also ask any server, not just the one your system is configured to use. This gives you the information you need to fix problems with your DNS configuration.

For a full guide to dig, use it's [manual page](http://manpages.ubuntu.com/manpages/trusty/man1/dig.1.html). This page has some common recipes.

Tell dig to use a particular nameserver (that's not necessarily the system's nameserver). This is very useful for debugging your bind9 configuration before you tell your hosts to use your internal nameserver:

```
dig <query> @<namserver-to-use>
```

Here's an example where I want to test my CIS 192 server from the server itself:

```
$ dig router.mike.cis.cabrillo.edu @localhost
```

The query argument can has two parts. What type of query you want to make and what you are looking for. Common query types are:

  * A and AAAA: Address records for IPv4 and IPv6 respectively
  * NS: Find a nameserver for a domain
  * MX: Find a mail server for a domain

Some examples:

```
 dig A www.google.com   # find IPv4 address
 dig AAAA www.google.com # find and IPv6 address 
 dig MX www.google.com  # find Google's mail server
 dig NS www.google.com  # find Google's nameserver
 dig www.google.com    # Default is "A"
```

There are other useful things that dig can do easily. If you want to lookup the name for an IP address you can use the -x option:

```
dig -x 216.58.216.132
dig -x 2607:f8b0:400a:806::2004
```

If you want dig to do an iterative lookup, starting with the root servers use the +trace option:

```
dig +trace www.google.com
```

## Searching for Domain Records 

Choose a domain. Any domain. Examine the domain of your choosing by using dig to answer the following questions:
  - What are the nameservers for that domain?
  - What server handles mail on that domain?
  - Are there any SPF or other TEXT records for that domain?

## Understanding an Iterative Lookup 

Now you'll use dig to do an iterative lookup with the +trace option. Dig's output will be much larger than a normal lookup because it's showing you the query at every step of the way. Execute the following command:

```
$ dig +trace opus.cis.cabrillo.edu
```

Answer the following:
  - What is the IP address of every DNS server you queried?
  - What type of name record does opus have?

Turn In
  - The answers to the questions.

Submit your homework on canvas.
