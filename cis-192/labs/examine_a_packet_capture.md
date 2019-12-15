# Examine a Packet Capture 

In this lab you'll create a packet capture on your router then bring it to a local computer and analyze it using Wireshark.

## Before you Begin 

You will need to have a copy of Wireshark on your local machine. The CIS machines have Wireshark installed already. If you're doing this lab at school you can safely skip this step. If you're at home download and install Wireshark from here: 

[https://www.wireshark.org/](https://www.wireshark.org/)

Make sure you have read and understand this week's lesson:
 [Debugging and Advanced SSH](debugging_and_advanced_ssh.html)

## Capture and View Packets 

Get in the habit of having two or more SSH connections to your VM. It's very useful to be able to switch between two shells. Open two SSH sessions to your router VM. In the first session run the command:

```
$ sudo tcpdump -i ens192 not port ssh
```

In the second session run the following commands:

```
$ wget -o /dev/null http://opus.cis.cabrillo.edu/cgi-bin/confirmation.cgi
$ ping www.google.com
$ ping6 www.google.com
```

When you run those commands you should see packets going by. If not, be sure you're running tcpdump properly. \

## Capture and Retrieve Packets 

Quit your running `tcpdump` command and start it again, saving the output to a file:

```
$ sudo tcpdump -i ens192 -w capturelab.pcap
```

In the second session re-run the commands above. After you've run the commands end the `tcpdump` command with `CTRL-C`. Now use SSH to bring the packets back to your computer.

## Examining the Packets 

Wireshark shows you much more information about the packet capture. Tcpdump only displays a summary of the packet. Wireshark can dig down into each one. Using Wireshark answer the following questions:

  - What is the MAC address of your VM?
  - What is the MAC address of your VM's default gateway?

The `wget` command fetched a simple web page with a number in it. Find one of the packets that belonged to that conversation and select it. Right click on the packet and in the context menu pick "Follow TCP Stream" or "Follow -> TCP Stream" depending on what version you're using. Doing this will reveal the secret number in the HTTP reply. What is it?

## Turn In 

When you're done turn in the answers to the questions on Canvas.
