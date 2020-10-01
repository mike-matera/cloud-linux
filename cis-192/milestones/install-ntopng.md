# Install `ntopng`

To complete this milestone you will install the `ntop` network monitoring program on your AWS VM. 

## Step 1: Update

Before you add any software you should always do an `apt update`:

```
$ sudo apt update
```

## Step 2: Install 

Now you're ready to install `ntop`:

```
$ sudo apt install ntopng 
```

## Step 3: Check `ntop`

How do you know if `ntop` is running? There are a few ways:

Ask `systemctl` for status:

```
$ systemctl status ntopng 
● ntop.service - LSB: Start ntop daemon
   Loaded: loaded (/etc/init.d/ntop; bad; vendor preset: enabled)
   Active: active (running) since Thu 2019-04-25 15:20:21 UTC; 57s ago
     Docs: man:systemd-sysv-generator(8)
   CGroup: /system.slice/ntop.service
           └─3347 /usr/sbin/ntop -d -L -u ntop -P /var/lib/ntop --access-log-file /var/log/ntop/access.log -i enp0s3 -p /etc/ntop/protocol.list -O /var/log/ntop
```

Use `ps` and `grep` to search for `ntop`:

```
$ ps -ely  | grep ntop 
S   112  3347     1  0  80   0 32548 215418 -     ?        00:00:00 ntop
```

The `ntop` command listens on a network port. You can see that using `ss`:

```
$ sudo ss -lntp 
State      Recv-Q Send-Q                                           Local Address:Port                                                          Peer Address:Port              
LISTEN     0      128                                                          *:22                                                                       *:*                   users:(("sshd",pid=1328,fd=3))
LISTEN     0      10                                                           *:3000                                                                     *:*                   users:(("ntop",pid=3347,fd=1))
LISTEN     0      128                                                         :::22                                                                      :::*                   users:(("sshd",pid=1328,fd=4))
```


## Step 5: Look at `ntopng`

If `ntop` is running you should be able to visit the URL below and see it running:

http://your-aws-ip-address:3000

Take a screenshot of `ntop`

## Questions

1. What packages does ntop depend on? 
1. After you installed ntop what services are listening on TCP ports? 
1. Do you think ntop is secure? Explain your answer. 

## Turn In 

1. Turn in a screenshot of `ntop`. 
1. Answers to the questions
