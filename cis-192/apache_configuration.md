This how-to will help you get Apache setup for the first time. The lecture slide are [here](https://docs.google.com/presentation/d/1L4_radfiCERtwLKogoesyfkEAMXMT_XA7DVCKre9qcI/edit?usp=sharing).

### Commands 

  * apt-get
  * wget
  * netstat
  * dig
  * a2ensite, a2dissite

### Configuration 

  * /etc/apache2/*
  * /var/www

Contents
  - [1 Commands](#TOC_Commands)
  - [1.1 Configuration](#TOC_Configuration)

  - [2 Introduction](#TOC_Introduction)
  - [3 Install Apache](#TOC_Install_Apache)
  - [4 Firewall Rule](#TOC_Firewall_Rule)
  - [5 Setup DNS](#TOC_Setup_DNS_)
  - [6 Update Your Web Site](#TOC_Update_Your_Web_Site)
  - [7 Create a Virtual Host](#TOC_Create_a_Virtual_Host)

## Introduction  

On Ubuntu it's easy to get Apache started. All it takes is an apt-get. But that's not quite the whole story. For the last few weeks we've been working on other, intermingled systems that need to be updated in order to have a successful web presence. This document will take you through that procedure.

## Install Apache 

You should install Apache on your web-servermachine:

```
web-server$ sudo apt-get install apache2
```

Once Apache is installed you it will put up a welcome page. You can access that page from inside your VM network but you won't be able to from outside until you make a firewall rule on your router. Test the start page from your web server using the following command:

```
web-server$ wget localhost
--2016-04-14 14:52:08-- http://localhost/
Resolving localhost (localhost)... ::1, 127.0.0.1
Connecting to localhost (localhost)|::1|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 11510 (11K) [text/html]
Saving to: âindex.htmlâ
100%[===================================================================================================>] 11,510   --.-K/s  in 0s   
2016-04-14 14:52:08 (171 MB/s) - âindex.htmlâ saved [11510/11510]
```

You can also verify that Apache is listening on port 80 using the netstat command:

```
web-server$ sudo netstat -lntp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address      Foreign Address     State    PID/Program name
tcp    0   0 0.0.0.0:22       0.0.0.0:*        LISTEN   7590/sshd   
tcp6    0   0 :::80          :::*          LISTEN   8348/apache2  
tcp6    0   0 :::22          :::*          LISTEN   7590/sshd   
```

Now you need to make your web server accessible from the Internet.

## Firewall Rule 

On your router you must setup a forwarding rule. The rule must allow new connections coming from the internet destined for TCP/80 to be forwarded to your web server. Make sure you alter the following command to reflect the IPv6 address of your webserver:

```
router$ sudo ip6tables -I
FORWARD 1 -m state --state NEW -p tcp -d 2607:f380:80f:f901:250:56ff:feaf:c5d1 --dport 80 -j ACCEPT
```

With the firewall rule established you will be able to connect to your web server with your browser if you're on the CIS network or you have IPv6 at home. When you put an IPv6 address into the browser you need to use square brackets. Like this:

```
 
http://[2607:f380:80f:f901:250:56ff:feaf:c5d1]/
```

If you don't have IPv6 and you want to test your connection you can use an IPv6 proxy site:
  * [http://www.ipv6proxy.net/](http://www.ipv6proxy.net/)
  * [http://ipv6proxy.org/](http://ipv6proxy.org/)

Those sites let you type in an IPv6 address and they will load the page for you.
  WARNING: DO NOT USE IPv6 PROXIES FOR ANY PERSONAL BROWSING. THEY ARE INSECURE.
Typing your IPv6 address every time is a pain. Next you will setup an name for your server in DNS.

## Setup DNS 

Having a DNS record that points to your server makes life much easier. You only need to setup an IPv6 (AAAA) address because your IPv4 address isn't useful (even for the CIS network). In your domain file add a record like the following. Be sure to replace the IPv6 address in my example with the address of your server:

```
www IN AAAA 2607:f380:80f:f901:250:56ff:feaf:c5d1
```

Be sure to update your serial number! Reload your DNS configuration with the command:

```
router$ sudo service bind9 reload
```

Test that your record works with dig:

```
router$ dig www.mydomain.cis.cabrillo.edu @localhost
```

If you get an answer you should now be able to browse to your webserver directly:

```
  http://www.mydomain.cis.cabrillo.edu/
```

But what about the "naked" domain? Most of time we go to "amazon.com" not "www.amazon.com." The concept of a "naked" domain is a problem for DNS. The way domains handle it is against the standard, but it's so common now that it just works everywhere. To make entering the domain address reach the webserver you must add the following record.

```
@ IN AAAA <your-wwww-server-ipv6-address>
```

After reloading your DNSconfiguration(with the updated serial number) you should be able to access your web server this way:

```
  http://mydomain.cis.cabrillo.edu/

```

You're now on the Internet for real.

## Update Your Web Site 

Your web server is now serving the default web page. In this section we'll see the configuration the enables the default page and update it to something custom. Apache's configuration lives in:

```
  /etc/apache2
```

Apache is a huge and complicated program, we'll just scratch the surface in this class. Apache can server multiple websites from a single host. This is called virtual hosing and it's extremely useful. Each site you can host is listed in:

```
  /etc/apache2/sites-available
```

Sites that are currently begin hosted are listed in:

```
  /etc/apache2/sites-enabled
```

The files in sites-enables are symbolic links to the corresponding files in sites-available. Update the contents of your 000-default.conf file with your email address. Don't set ServerName (that's illegal in the default configuration). 

```
<VirtualHost *:80>
ServerAdmin mike@dontteltheinternet.com
DocumentRoot /var/www/html
ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Note: I have omitted the comments. You should leave them in.
The HTML files for your default site (as you can see) are located in /var/www/html. Update index.html in that directory with a page of your choosing. 
## Create a Virtual Host 

Apache's virtual hosting mechanism is extremely useful. In the old days you needed on (expensive!) computer per website. Now you can host thousands of websites from a single VM. In the sites-available directory copy the default site to a new configuration. We'll use this configuration next week when we setup PHP. Call your new site configuration:

```
  001-dynamic.conf
```

Your new configuration should have the following settings:
  * ServerName: php.yourdomain.cis.cabrillo.edu (required for virtual hosts!)
  * ServerAdmin: Your email address
  * DocumentRoot: /var/www/html/php-site

Leave the other settings as they are. Once your configuration is finished you must enablethe site using an Apache command:

```
web-server$ sudo a2ensite 001-dynamic
Enabling site 001-dynamic.
To activate the new configuration, you need to run:
 service apache2 reload
```

If you ever want to disable a site you can do that with the command

```
 
a2dissite <site-name>
```

Your change won't be reflected until you run the command:

```
$ sudo service apache2 reload
```

Be sure to add an index.html file in the document root. Your site is available but your work isn't done. In order for a virtual host to work it needs a record in DNS. On your router add the following record to your domain:

```
php IN CNAME www
```

Don't forget to increase the serial number and reload bind9. Now when a browser looks for php.yourdomain it will get the IP address of your webserver. How does the webserver know what site the browser is looking for? Use Wireshark to find out. Test your virtual host using your browser:

```
 
http://php.yourdomain.cis.cabrillo.edu/
```

You should see the alternate HTML file you created.