# Lab: Installing `ntop`

In this lab you'll use `apt` to install the `ntop` program and check to see that it works. 

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

Let's move the `ntop` port to `80` so we can see `ntop` from our host machine. 

## Step 4: Configure `ntop`

The configuration for `ntop` is simple. You can find the configuration in `/etc/ntopng.conf`. Edit the file and change the setting shown below: 

```
-w=80
```

Use `systemctl` to restart `ntopng`:

```
$ sudo systemctl restart ntopng
```

Now check to see what port it's listening on: 

```
$ sudo ss -lntp 
State      Recv-Q Send-Q                                           Local Address:Port                                                          Peer Address:Port              
LISTEN     0      10                                                           *:80                                                                       *:*                   users:(("ntop",pid=3635,fd=1))
LISTEN     0      128                                                          *:22                                                                       *:*                   users:(("sshd",pid=1328,fd=3))
LISTEN     0      128                                                         :::22                                                                      :::*                   users:(("sshd",pid=1328,fd=4))
```

Perfect! 

## Step 5: Look at `ntopng`

If you reconfigured `ntop` you should be able to visit the URL below and see it running:

http://localhost:8080

Take a screenshot of `ntop`

## Installing Packages with Ansible 

This play installs and configures `ntopng`: 

```yaml
- hosts: all
  name: Install packages
  become: true
  tasks:
    - name: Install ntopng
      package:
        name:
          - ntopng
        state: latest
    - name: Configure ntopng
      lineinfile:
        path: /etc/ntopng.conf
        regexp: '^-w='
        line: -w=80
    - name: Restart ntopng
      service:
        name: ntopng
        state: restarted
```

## Turn In 

Turn in a screenshot of `ntop`. 
