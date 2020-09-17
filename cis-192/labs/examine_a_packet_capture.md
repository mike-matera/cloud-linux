# Examine a Packet Capture 

In this lab you'll create a packet capture on your router then bring it to a local computer and analyze it using Wireshark.

## Capture and View Packets 

Get in the habit of having two or more SSH connections to your VM. It's very useful to be able to switch between two shells. Open two SSH sessions to your router VM. In the first session run the command:

```
$ sudo tcpdump -i eth0 not port ssh
```

In the second session run the following commands:

```
$ ping www.google.com
$ ping6 www.google.com
```

When you run those commands you should see packets going by. If not, be sure you're running `tcpdump` properly. 

## Long Running Packet Captures 

The `tcpdump` program can run for a long time. When it does you have to select a strategy for storing packets that won't cause your disk to fill up (and crash your VM). To complete this part of the lab you'll start tcpdump and leave it running for a week or so. At the end of the week you'll have a good idea of how much traffic your VM sees. At this stage it's all jerks on the internet performing port scans. 

Use the manual and Google to make `tcpdump` capture packets with the following parameters:

1. Limit capture files to 100MB
1. Capture at most 10 files (using no more than 1GB of disk space)
1. Rotate files so the first file is overwritten when the last file is full
1. Name your capture files `long-captureN` where `N` is a number. 

### Running `tcpdump` in the Background 

You don't need to be logged in the entire time. In order to get `tcpdump` to run in the background use the `&` as shown below: 

```
$ sudo tcpdump .... &
```

The program will continue to run after you log out. 

## Examining your Packets

After a week download one or more of your packet files and examine them with Wireshark. Answer the following questions: 

1. What is the total amount of data captured?
1. How many foreign IP addresses do you see in one capture? 
1. What is the average bandwidth used by your VM? 

## Turn In 

When you're done turn in the answers to the questions on Canvas with screenshots justifying how you came to the answer.
