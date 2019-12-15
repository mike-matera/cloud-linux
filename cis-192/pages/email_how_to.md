# Email How To 

This lesson will take you through setting up Postfix on your router. Email is first killer app of the Internet. Sending and receiving email on your own domain is an important business and marketing tool. You don't have to install your own MTA to have email on a custom domain, but you should know how.

The lecture slides are [here](https://docs.google.com/presentation/d/1pN1RbnkOkWiaBJ5_Vu1goIbMKqwUlW0QVNz6vaIwGxI/edit?usp=sharing).

## Commands 

  * apt-get
  * dpkg-reconfigure

## Configuration 

  * /etc/named/db.<yourdomain>

## Further Reading 

There are multiple mail agents that you can use in Ubuntu. Each with it's pros and cons. The default MTA is Postfix. Here's Ubuntu's official Postfix documentation: 

 * [https://help.ubuntu.com/community/Postfix](https://help.ubuntu.com/community/Postfix)

## Install Postfix 

Setting up postfix itself is quite easy. You must first install it:

```
infra$ sudo apt-get install postfix
```

The installation will trigger a menu. Make the following choices: 

  1. Internet Site 
  2. System name: Your domain name. (e.g. mike.cis.cabrillo.edu)

If you want to get the menu again you can run the following command:

```
infra$ dpkg-reconfigure postfix
```

The menu from `dpkg-reconfigure` has more options. Leave them at their defaults. 

## Setup DNS Records 

The DNS system is used to figure out who handles mail for a given domain. You may have noticed that when you send email to your friends with a Gmail account you send the mail to "friend@gmail.com". The name "gmail.com" does not name a machine but a domain. The MTA must find out using a special DNS query:

```
$ dig mx gmail.com

; <<>> DiG 9.10.3-P4-Ubuntu <<>> mx gmail.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6887
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 13, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;gmail.com.			IN	MX

;; ANSWER SECTION:
gmail.com.		3599	IN	MX	20 alt2.gmail-smtp-in.l.google.com.
gmail.com.		3599	IN	MX	10 alt1.gmail-smtp-in.l.google.com.
gmail.com.		3599	IN	MX	30 alt3.gmail-smtp-in.l.google.com.
gmail.com.		3599	IN	MX	5 gmail-smtp-in.l.google.com.
gmail.com.		3599	IN	MX	40 alt4.gmail-smtp-in.l.google.com.

;; Query time: 65 msec
;; SERVER: 10.192.0.3#53(10.192.0.3)
;; WHEN: Thu Oct 31 08:18:17 PDT 2019
;; MSG SIZE  rcvd: 372
```

The answer contains a prioritized list of the servers that handle mail for gmail.com. Servers are supposed to pick the lowest number first. In order to handle mail you must modify your DNS records to contain a mail server. Here's what I did to my zone file to add support for a mail server:

```
@               IN MX   10      mail
mail            IN AAAA <infra-ipv6>
@               IN TXT  "v=spf1 ip6:<infra-ipv6>/128 -all"
```

The first entry is the MX or mail server record. That contains the name of my domain (abbreviated @) and the name of the mail server (mail). Since my mail server is my infra server the record points to the IPv6 address of my infra server. Finally I've added an SPF record stating that I can send email from my infra-server IPv6 address and that's it!

## Checking Your DNS Records 

Once you have your DNS record setup you should check to make sure that other hosts on the Internet can find your mail server. Use dig for that:

```
infra$ dig MX <yourdomain>.cis.cabrillo.edu @localhost
```

You should see an answer with the proper email address. Also, check your SPF record:

```
infra$ dig TXT <yourdomain>.cis.cabrillo.edu @localhost
```

## Checking Your Mail Logs 

The file:

```
 /var/log/mail.log
```

Will contain the record of any failed attempts to deliver email. That's a very useful place to look for problems.

## Allowing Inbound Mail Connections 

The firewall on your router doesn't allow incoming mail. To do that you'll need to open port 25 in the IPv6 FORWARD chain. You'll need to do that for packets destined for the EUI-64 of your infra server. The command to do that is:

 * Filter FORWARD chain:
   * Destination IPv6: The IPv6 of your infra server
   * State: NEW
   * Protocol: TCP
   * Port: 25
   * ACCEPT 

You cannot receive email using IPv4 because you don't have a real public address. You can check to be sure that it's working using telnet from Opus or Tux

```
opus$ telnet <infra-server-ipv6-address> 25
```

Don't forget to save your firewall after you've made this change!!
