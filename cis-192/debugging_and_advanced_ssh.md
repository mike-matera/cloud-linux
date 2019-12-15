# Debugging and Advanced SSH 

In this lesson you'll learn some of the advanced features of SSH and techniques for finding problems with your VM network using packet debugging tools.

The lecture slides are [here](https://docs.google.com/presentation/d/11TIhoHajEe3iwgLQ6ygz_LyVRql85nWkaQAzgfANdBo/edit?usp=sharing).

## Commands 

  * ssh
  * ssh-keygen
  * tcpdump

## Configuration 

  * ~/.ssh/config
  * ~/.ssh/authorized_keys

## Introduction 

There are two things a good admin does well: Move from host to host and find problems. This lesson will show you the way the pros do it using SSH and Wireshark and friends. In the last class you learned how to use SSH to login and move files back and forth. You probably typed your password a lot of times. No more.

## Going Passwordless 

SSH can use cryptographic keys to verify your identity. Run the following command on Opus to generate a key pair:

```
$ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/robot/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/robot/.ssh/id_rsa.
Your public key has been saved in /home/robot/.ssh/id_rsa.pub.
The key fingerprint is:
d8:e6:d9:0e:55:39:82:e0:1c:e9:cf:b8:85:11:81:d0 robot@swarmathon-builder
The key's randomart image is:
+--[ RSA 4096]----+
| .o .+o          |
| Eooo . .        |
| .o.. . +        |
| oo o .          |
| .*S .           |
| oo++            |
| o+ .            |
| .  o            |
| .               |
+-----------------+
```

It's okay to leave the password blank on Opus. In real life you should protect your private keys with a password if you place them on a shared computer. You can see your new key pair with the command:

```
$ ls ~/.ssh/id_rsa*
/home/mike/.ssh/id_rsa /home/mike/.ssh/id_rsa.pub
```

The *.pub is your public key. You will copy that key to machines where you want to login without a password. Keep your private key safe. If anyone gets that file they can impersonate you!

## Installing Your Public Key 

SSH comes with a very convenient command to move your public key onto a machine.

``` 
$ssh-copy-id user@machine
```

Use this command to copy your public key to your router. Once that's complete you should be able to login with no password from Opus:

```
$ ssh student@<my-ip-address>
Welcome to Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-74-generic x86_64)
* Documentation: https://help.ubuntu.com/
 System information as of Thu Feb 11 15:18:56 PST 2016
 System load: 0.0        Processes:      104
 Usage of /:  6.4% of 30.15GB  Users logged in:   0
 Memory usage: 10%        IP address for eth0: 172.20.192.13
 Swap usage:  0%
 Graph this data and manage this system at:
  https://landscape.canonical.com/
37 packages can be updated.
20 updates are security updates.
Last login: Thu Feb 11 15:18:58 2016 from opus.cis.cabrillo.edu
student@router:~$
```

Where is your public key? On your router run the following command:

```
$ cat ~/.ssh/authorized_keys
ssh-dss AAAAB3NzaC1kc3MAAACBAIFLagN59cSGWaXeMqeUjSEBm3uPylpuZMO30p6cAu4wGSs30V3LwnadkrB8eYYZYo7QcIzhoauMR+lnRgJuIWulUazZEkrbti9KraJttBizc+yAmVCiRgwTLB3PPVkizp+8213rdP+zi3FLoH3J8vKgCHrN0VkumY01A439nBp/AAAAFQCkUGTKKgFZtjVpWE8/kbIMEb091QAAAIAjZh4XwhQfwXrRey8SZJ4Itv4gupwo7ILf1XNpswVOSQW+xMDnfcLm+ifKmj6v9fpwlMZJ65eaMgYVIdn4MxHJ1MsHIi1P2zpWQMnS4FX+HK3HJA9+KkM5qNOWfHxtTVM5KQsY/aJJTXpEJBItO1ftgcAuRHrmenb3kMfEGzSPagAAAIBcuc42nUNeKi7DQZRM5f6U+89OFOispXzKlORw5VORAEZe0xESHWlvt/udRAZbKE/HS3VQYzDjc8BOzbSjCzmAFOoLx9XfmZ9lr6SF/jN0vJAJG+6bVhIv265b8JeGk/nBrpV+S5JI1LgKCgGgM9qOpgXR+9t+TSntKVEnsH16Qg== mmatera@oslab.cis.cabrillo.edu
```

Any public key added to `~/.ssh/authorized_keys` will allow the holder of the private key to login with no password. You can delete keys from this file to cut off access.

### SSH Configuration 

SSH's configuration file gives you the opportunity to automate a lot of typing. Here's an example of my `~/.ssh/config` file that creates a shortcut for logging into my router:

```
Host router
    HostName 172.20.192.13
    User student
```

Now, instead of having to constantly remember my router's IP address I can simply use the word "router" as a shortcut:

```
$ ssh router
```

SSH turns that into:

```
$ ssh student@172.20.192.13
```

The configuration also works for SCP:

```
$ scp issue.net router:/tmp
```

No password, no username. You may want to setup SSH at home to remember that Opus uses a funny port number. You do that by adding a Port declaration:

```
Host opus
    HostName opus.cis.cabrillo.edu
    User mmatera
    Port 2220
```

## Packet Debugging with Tcpdump  

Packets are invisible, which can make debugging hard. The tcpdump program makes the invisible appear.

```
$ sudo tcpdump
```

Every time a packet comes into or out of 'eth0' a line will be printed on the output of tcpudmp describing what's in the packet. If you want to specify another interface for tcpdump you do that with the -i option.

```
$ sudo tcpdump -i ens192
```

Remember that option, it's critical to use tcpdump on the right interface. At this point in your project there won't be any packets on eth1. If you ran the first command while logged in via SSH you may have noticed a lot of traffic. This can be deceiving. You caused a "packet loop," because every line has to be sent to you over SSH, which in turn causes another line to be printed. You can filter out only the packets you're interested in using tcpdump filters. Here's a very useful one:

```
$ sudo tcpdump not host opus.cis.cabrillo.edu
```

This will eliminate any packets going to or from Opus in your filter. Another way to do that is to specify only the host you are interested in:

```
$ sudo tcpdump host myhost.ofinterest.com
```

It's often the case that the packets you are looking for are buried in a blizzard of other packets. Luckily you can tell tcpdump to save the packets in a file that can be opened with [Wireshark](https://www.wireshark.org/).

```
$ sudo tcpdump -i ens192 -w packets.pcap
```

That command will run until you stop it with CTRL-C. Afterwards the packets will be stored in the *.pcap file.
