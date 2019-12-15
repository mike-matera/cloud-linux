# Sorting Processes with `ps`

This lab will show you how to find the programs that have used the most resources by sorting the output of `ps`

## Step 1: A Python Pig

Copy this code into a file called `py_pig.py`: 

```python3
#! /usr/bin/env python3

import os
import time
import random
import tempfile

def main():

    files = []
    for _ in range(random.randint(10, 20)):
        files.append(tempfile.TemporaryFile())

    while True:
        stuff = os.urandom(1024*1042*256)
        time.sleep(1)


if __name__ == '__main__':
    main()
```

This script opens a bunch of files, burns up CPU time and wastes memory --and nothing else. You can run `py_pig.h` using `python3`:

```
$ python3 ./py_pig.py &
```

## Step 2: Finding High Memory Processes 

It's useful to know how much memory programs are using. The `ps` command can sort by many keys. Here's how to sort by memory usage: 

``` 
$ ps -ely --sort=rss | tail -n 10 
S     0  1654  1304  0  80   0  4272 23200 -      ?        00:00:00 sshd
S  1000  1656     1  0  80   0  4448 11320 ep_pol ?        00:00:00 systemd
S     0  2118  1304  0  80   0  4488 23200 -      ?        00:00:00 sshd
S  1000  2177  2176  0  80   0  5092  5353 wait   pts/1    00:00:00 bash
S  1000  1696  1695  0  80   0  5176  5353 wait   pts/0    00:00:00 bash
S     0  1222     1  0  80   0  5420 69295 -      ?        00:00:00 polkitd
S     0  1150     1  0  80   0  5552 68237 -      ?        00:00:00 accounts-daemon
S     0     1     0  0  80   0  5912  9444 -      ?        00:00:00 systemd
S     0  1147     1  0  80   0 26212 75790 -      ?        00:00:01 snapd
R  1000  2254  2177 94  80   0 472212 144366 -    pts/1    00:03:55 python3
```

## Step 3: Finding High CPU Processes 

Here's how you find the process that has used the most CPU time:

```
$ ps -ely --sort=time | tail -n 10 
R  1000  2345  1696  0  80   0  3028  6935 -      pts/0    00:00:00 ps
S  1000  2346  1696  0  80   0   700  1510 pipe_w pts/0    00:00:00 tail
S     0  1147     1  0  80   0 26212 75790 -      ?        00:00:01 snapd
S   107  1156     1  0  80   0  3160 10726 -      ?        00:00:01 dbus-daemon
S     0  2117     2  0  80   0     0     0 -      ?        00:00:01 kworker/1:2
S  1000  1695  1654  0  80   0  3588 23276 -      ?        00:00:03 sshd
S     0  1084     1  0  70 -10  3508  1430 -      ?        00:00:04 iscsid
S     0  1215     1  0  80   0  2504 61350 -      ?        00:00:05 VBoxService
S     0  2102     2  0  80   0     0     0 -      ?        00:00:05 kworker/1:1
S  1000  2254  2177 94  80   0 279496 77677 poll_s pts/1   00:05:43 python3
```

## Turn In 

Turn in a screenshot showing the output of `ps`
