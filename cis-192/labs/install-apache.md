# Install the Apache Web Server

In this lab you'll use `apt` to install the Apache web server. Installing software with apt is easy!

## Step 1: Update the Package Cache 

Before you install software it's important to update the package cache. This is usually done periodically by the system, but when you have a new VM or your host has been switched off for a while you should do it manually. 

```
$ sudo apt update 
```

## Step 2: Install Apache 

Now that you have the latest repository metadata you can install Apache: 

```
$ sudo apt install apache2 
``` 

## Step 3: Verify that Apache is Running 

First, let's look to see apache is running: 

```
$ systemctl status apache2 
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2020-10-01 18:50:40 UTC; 27s ago
       Docs: https://httpd.apache.org/docs/2.4/
   Main PID: 30475 (apache2)
      Tasks: 55 (limit: 560)
     Memory: 5.6M
     CGroup: /system.slice/apache2.service
             ├─30475 /usr/sbin/apache2 -k start
             ├─30477 /usr/sbin/apache2 -k start
             └─30478 /usr/sbin/apache2 -k start

Oct 01 18:50:40 awsmonster systemd[1]: Starting The Apache HTTP Server...
Oct 01 18:50:40 awsmonster apachectl[30464]: AH00558: apache2: Could not reliably determine the server's fully qua>
Oct 01 18:50:40 awsmonster systemd[1]: Started The Apache HTTP Server.
```

If your output looks like mine move on. Now let's look at what port Apache is listening on:

```
$ sudo ss -lntp 
State          Recv-Q         Send-Q                 Local Address:Port                  Peer Address:Port         Process                                                                                                            
LISTEN         0              4096                   127.0.0.53%lo:53                         0.0.0.0:*             users:(("systemd-resolve",pid=365,fd=13))                                                                         
LISTEN         0              128                          0.0.0.0:22                         0.0.0.0:*             users:(("sshd",pid=4489,fd=3))                                                                                    
LISTEN         0              511                                *:80                               *:*             users:(("apache2",pid=30478,fd=4),("apache2",pid=30477,fd=4),("apache2",pid=30475,fd=4))                          
LISTEN         0              128                             [::]:22                            [::]:*             users:(("sshd",pid=4489,fd=4)) 
```

You can see that Apache is listening on port 80. You can now browse to your VM: 

> http://your-ip-address-here/ 

## Turn In 

Turn in a screenshot of your browser at the default apache page. 




