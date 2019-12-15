# Linux Processes 

**Commands**

  * ps
  * kill
  * nice
  * renice
  * time

**Configuration**

  * /proc

## Introduction 

When a program executes it becomes a process. If a program on disk is a book then reading it is a process. Linux allocates the computer's resources to processes as they need them. There are three categories of resources that a process uses:

  - **CPU time**. A process consumes processor time as it executes. A CPU can only execute one process at a time, so the amount of compute time is limited by the number of CPU cores in the computer.
  - **Memory**. Programs must be loaded into memory before they can execute and usually request additional memory to do their work. Memory is a limited resource, when it gets scarce computers run very slowly.
  - **File Handles**. File handles are for more than just files. All I/O functions on Linux are performed using filehandles, including network I/O and communicating with device drivers.

This guide will show you how to control process execution, examine process resources and understand how Linux manages the finite resources of the computer.

## CPU Usage 

![image](../_static/images/process_statescb9b.png)

The drawing is a simplified version of the state machine that is the essence of every Linux process. Every process begins in the ready state. In the ready state a process is awaiting processor time. When the system is not busy processes don't spend much time in the ready state, they go into the executing state right away. In the executing state the process is on the CPU. There are four ways out of the execute state. If the process is interrupted to make way for another ready process it goes back into the ready state. If a process is interrupted by a `CTRL-Z` it's halted and goes into the stopped state where it must wait for a user to resume it, which puts it back into the ready state. If the process requests I/O, like reading data from disk or waiting for a keystroke, it goes into the waiting state. There it will stay until whatever it's waiting for becomes available. Finally, if the program exits the process goes into the zombie state. In the zombie state the process can no longer execute and waits for it's parent process to acknowledge it's exit. A misbehaving program can sometimes forget to release its child processes from the zombie state, filling the system with zombie processes!

The `ps` command will show you what state a process is in:

```
$ ps -ly
S  UID  PID PPID C PRI NI  RSS  SZ WCHAN TTY     TIME CMD
R 1000 6030 15856 0 80  0  892 3544 -   pts/0  00:00:00 ps
S 1000 15856 15846 0 80  0 5208 7021 wait  pts/0  00:00:00 bash
```

The letter in the `S` column reveals what state the process is in. The table below shows you how to decode the letters:

| Code | State |
| --- | --- | 
| D | Waiting (Uninterruptible) |
| R | Ready or Executing | 
| S | Waiting (Interruptible) | 
| T | Stopped |
| Z | Zombie |

The subsequent letters also give useful information. See the manual page of ps for a complete description.

### CPU Time 

Linux keeps track of the time a process spends executing. Execution time is collected as usertime, the time a process spends running it's own instructions, and as systemtime, the time that the Linux kernel spends executing on behalf of the process. Linux executes on behalf of a process when the process requests something from the kernel like reading a file or printing output to the screen. Time spent waiting for the disk doesn't count as system time only the time it took the kernel to initiate the disk operation.

You can ask ps to sort it's output by a column of your choosing. The following command prints processes sorted by time, from the least to the most.

```
$ ps -ely --sort time
S   UID   PID  PPID  C PRI  NI   RSS    SZ WCHAN  TTY          TIME CMD
 [output snipped]
S  1000  3542  2756  0  80   0 10300 129456 poll_s ?       00:00:59 zeitgeist-datah
S     0    80     2  0  99  19     0     0 -      ?        00:01:03 khugepaged
S     0  1828     1  0  80   0  3748 71867 -      ?        00:01:04 accounts-daemon
S  1000 16497 24437 13  80   0 92512 230114 futex_ ?       00:01:21 chrome
S   106  1755     1  0  80   0  4812 109284 -     ?        00:01:26 whoopsie
S     0    11     2  0  80   0     0     0 -      ?        00:01:29 rcuos/3
S     0  2167     1  0  76  -4   764 23496 -      ?        00:01:34 auditd
S  1000  2920  2887  0  80   0 39720 126389 poll_s ?       00:01:37 ibus-ui-gtk3
S     0    10     2  0  80   0     0     0 -      ?        00:01:42 rcuos/2
S  1000  3005  2887  0  80   0  3164 50241 poll_s ?        00:01:48 ibus-engine-sim
S   101   898     1  0  80   0  3192 63970 -      ?        00:01:50 rsyslogd
S     0     8     2  0  80   0     0     0 -      ?        00:01:53 rcuos/0
S     0     9     2  0  80   0     0     0 -      ?        00:02:06 rcuos/1
S  1000  2942  2756  0  80   0 38480 144577 poll_s ?       00:02:09 unity-panel-ser
S     0  1698     1  0  80   0   740  4800 -      ?        00:02:10 irqbalance
S     0   286     2  0  80   0     0     0 -      ?        00:02:27 jbd2/dm-0-8
S     0  3137     1  0  80   0  5172 92863 -      ?        00:02:43 udisksd
S     0    12     2  0  80   0     0     0 -      ?        00:03:46 rcuos/4
S  1000  2887  2756  0  80   0 37444 96472 poll_s ?        00:06:26 ibus-daemon
S     0     7     2  0  80   0     0     0 -      ?        00:06:28 rcu_sched
S  1000 25140 24437  0  80   0 368904 443467 futex_ ?      00:08:04 chrome
S  1000 24735 24437  0  80   0 345592 413394 futex_ ?      00:09:06 chrome
S  1000 25249 24437  0  80   0 374928 336699 futex_ ?      00:09:42 chrome
S  1000  2984  2756  0  69 -11  5120 92434 poll_s ?        00:10:25 pulseaudio
S  1000  3027  2939  0  80   0 69412 388220 poll_s ?       00:10:33 nautilus
S  1000 24514 24421  0  80   0 374168 228887 poll_s ?      00:11:18 chrome
S  1000 24421  2756  1  80   0 362400 328360 poll_s ?      00:21:48 chrome
S     0  1796  1777  0  80   0 85000 127012 -     tty7     01:11:01 Xorg
S  1000  3008  2939  0  80   0 184388 420605 poll_s ?      03:12:40 compiz
```

```
TIME = user time + system time
```

Notice how much more time Google Chrome (chrome) and compiz have spent using the processor than the other processes. Most programs spend almost all of their time waiting. The program with the largest times are the programs that have been historically most active. This was taken on a system that has been up for about 22 days. During that time (528 hours) Xwindows (PID 1796) has only used the CPU for 1 hour 11 minutes and 1 second. 

### Keeping Track of Runtime 

The time command is a useful tool. It acts like a stopwatch but it precisely times the execution of another command or commands:

```
time <command>
```

When the command exits time prints how much time the command spent executing:

```
$ time find / > /dev/null
real   0m27.038s
user   0m2.610s
sys    0m7.824s
```

The output indicates that the command took 27 seconds to finish and that during that time it used 2.6 seconds running user time and 7.8 seconds of system time. We know that find simply listed all the files on my computer and doing so caused a lot of access to the disk. That explains the high system time and waiting for the disk explains why the process spent so much time waiting.

### Priority and Niceness 

When there are more runnable processes than there are processors in the system the processes compete for CPU time. It's the job of the scheduler to efficiently manage the runnable processes by:

  - Giving the highest priority process CPU time.
  - Ensuring that no process is starved for CPU time.
  - Keeping scheduling overhead as low as possible.

The priority of a process changes its share of CPU time in situations where the CPU is scarce. The priority system gives administrators the power to schedule long running CPU-intensive jobs on a workstation without sacrificing performance of interactive programs like web browsers. This is especially desirable on desktop systems where users expect their GUIs to remain snappy. The priority of each process is shown in the `PRI` column in the output of `ps`. Lower numbers are higher priorities. On recent versions of Linux the priorities range from 0 (the highest) to 99 (the lowest). You can't set the priority of a process directly, but you can change it by changing the niceness of the process (the `NI` column). The niceness value ranges from -20 (the least nice or most favorable to the program) to 19 (the most nice and least favorable to the program).

By default the nice value of a program is 0. You can use the nice command to launch a program with a custom niceness level:

```
$ nice -n 19 ps -ly
S  UID  PID PPID C PRI NI  RSS  SZ WCHAN TTY     TIME CMD
S 1000 28004 27994 0 80  0 4196 5757 wait  pts/0  00:00:00 bash
R 1000 28433 28004 0 99 19  888 2503 -   pts/0  00:00:00 ps
```

If you want to reduce the niceness below zero you must be root:

```
$ sudo nice -n -20 ps -ly
[sudo] password for mimatera:
S  UID  PID PPID C PRI NI  RSS  SZ WCHAN TTY     TIME CMD
S   0 28436 28004 0 80  0 2980 24029 poll_s pts/0  00:00:00 sudo
R   0 28440 28436 0 60 -20  884 2503 -   pts/0  00:00:00 ps
```

Notice that the niceness has a direct effect on the priority:

```
priority = 80 + niceness
```

You can change the niceness of program once its running using the `renice` command:

```
renice -n <niceness> <pid>...
```

You can also change the niceness of every process belonging to a particular user or users:

```
renice -n <niceness> -u <user>...
```

To change users other than yourself you must be root. Also, regular users can only make their processes nicer. To make a process less nice you must be root. Processes inherit the niceness of their parent process. Therefore if you wanted to "nice-ify" your shell and all the programs you launch from it you could run:

```
$ renice -n 19 $$
28004 (process ID) old priority 0, new priority 19
$ ps -l
F S  UID  PID PPID C PRI NI ADDR SZ WCHAN TTY     TIME CMD
0 S 1000 28004 27994 0 99 19 - 5757 wait  pts/0  00:00:00 bash
4 R 1000 28490 28004 0 99 19 - 2503 -   pts/0  00:00:00 ps
```

Notice that the `ps` command ran with niceness 19.

### Priority Pitfalls 

The Completely Fair Scheduler algorithm does a very good job. CFS was introduced in 2008 and was a huge step forward because it is able to handle different workloads automatically. Under CFS a long running compute process (like a video encoder) nicely shares the processor with a latency sensitive process (like a web browser) with no intervention. Modern multi-core processors make it less likely that a processes will have to compete for a CPU. So it's rarely necessary to hand-tune niceness.

## Memory Use  

Programs run from memory. Executing a program copies it from the disk into memory. Running programs request memory from the system as they operate, ideally they return memory to the system when they don't need it anymore. When a program exits all memory it used is reclaimed and made available for other programs. Linux tracks how much memory each process uses in different ways. Unfortunately, there is no simple answer to the question "how much memory is a process using?" The ``ps`` command can show you what the kernel knows about a process' memory:

```
$ ps -ly
S  UID  PID PPID C PRI NI  RSS  SZ WCHAN TTY     TIME CMD
R 1000 6105 15856 0 80  0  888 3544 -   pts/0  00:00:00 ps
S 1000 15856 15846 0 80  0 5208 7021 wait  pts/0  00:00:00 bash
```

The two memory columns are:

  - **Resident Set Size (RSS) KiB**. The resident set is the amount of physical memory that the program is using. Memory that's swapped to disk doesn't count.
  - **Virtual Memory Size (SZ) KiB**. This is all the memory that's in use by the process, including memory that's paged out and shared with other programs. SZ is always greater than RSS.

It's often useful to know what programs are using the most memory on a system. To do that you can set the sort order to RSS. The following command shows the 10 programs using the most memory:

```
$ ps -ely --sort rss | tail -n 10
S 1000 5938 4210 0 80  0 100776 224853 futex_ ?   00:00:07 chrome
S 1000 5753 3701 0 90 10 115456 183024 poll_s ?   00:00:02 update-manager
S 1000 4332 3701 0 80  0 122836 985611 poll_s ?   00:03:13 dropbox
S 1000 15192 4210 0 80  0 155480 250722 futex_ ?   00:02:31 chrome
S 1000 4343 4210 0 80  0 159028 314072 futex_ ?   00:01:33 chrome
S 1000 4283 4077 0 80  0 213148 159661 poll_s ?   00:06:39 chrome
S 1000 4047 3881 0 80  0 231856 474842 poll_s ?   00:20:35 compiz
S 1000 4077 3881 0 80  0 276812 340444 poll_s ?   00:22:00 chrome
S 1000 8608 4210 0 80  0 351624 463671 futex_ ?   00:17:08 chrome
S 1000 8888 4210 0 80  0 389140 398256 futex_ ?   00:19:31 chrome
```

Any of these number can change for a process second over second. The ``/proc`` filesystem gives administrators the opportunity to see exactly how the process is using its memory. There is a subdirectory in the ``/proc`` directory for the PID of each running process on the system. There's a wealth of data in that directory. A special directory ``/proc/self`` always contains the information of the current process (BASH if you're using the command line). The ``/proc/self/maps`` file shows you the memory layout of the current process.

```
$ cat /proc/self/maps
00400000-0040b000 r-xp 00000000 fc:01 19267667              /bin/cat
0060a000-0060b000 r--p 0000a000 fc:01 19267667              /bin/cat
0060b000-0060c000 rw-p 0000b000 fc:01 19267667              /bin/cat
01662000-01683000 rw-p 00000000 00:00 0                 [heap]
7ff9f234e000-7ff9f2a30000 r--p 00000000 fc:01 137809           /usr/lib/locale/locale-archive
7ff9f2a30000-7ff9f2beb000 r-xp 00000000 fc:01 28442917          /lib/x86_64-linux-gnu/libc-2.19.so
7ff9f2beb000-7ff9f2dea000 ---p 001bb000 fc:01 28442917          /lib/x86_64-linux-gnu/libc-2.19.so
7ff9f2dea000-7ff9f2dee000 r--p 001ba000 fc:01 28442917          /lib/x86_64-linux-gnu/libc-2.19.so
7ff9f2dee000-7ff9f2df0000 rw-p 001be000 fc:01 28442917          /lib/x86_64-linux-gnu/libc-2.19.so
7ff9f2df0000-7ff9f2df5000 rw-p 00000000 00:00 0
7ff9f2df5000-7ff9f2e18000 r-xp 00000000 fc:01 28442911          /lib/x86_64-linux-gnu/ld-2.19.so
7ff9f2fe3000-7ff9f2fe6000 rw-p 00000000 00:00 0
7ff9f3015000-7ff9f3017000 rw-p 00000000 00:00 0
7ff9f3017000-7ff9f3018000 r--p 00022000 fc:01 28442911          /lib/x86_64-linux-gnu/ld-2.19.so
7ff9f3018000-7ff9f3019000 rw-p 00023000 fc:01 28442911          /lib/x86_64-linux-gnu/ld-2.19.so
7ff9f3019000-7ff9f301a000 rw-p 00000000 00:00 0
7fffe386b000-7fffe388d000 rw-p 00000000 00:00 0             [stack]
7fffe3902000-7fffe3904000 r-xp 00000000 00:00 0             [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0         [vsyscall]
```

Programmers might be familiar with the `[stack]` and `[heap]` areas. Those are where programs allocate dynamic memory.

## File Descriptors 

File descriptors are how programs communicate with the world. When a process accesses files or the network it requires a file descriptor. Communicating with other processes often also requires the use of a file descriptor. The ``/proc`` filesystem lets you view the file descriptors that any process has open.

```
$ ls -l /proc/self/fd
total 0
lrwx------ 1 maximus maximus 64 Oct 25 21:22 0 -> /dev/pts/14
lrwx------ 1 maximus maximus 64 Oct 25 21:22 1 -> /dev/pts/14
lrwx------ 1 maximus maximus 64 Oct 25 21:22 2 -> /dev/pts/14
lr-x------ 1 maximus maximus 64 Oct 25 21:22 3 -> /proc/31082/fd
```

Notice that the files in this directory are symbolic links. The links point to the file that is open. Each file descriptor is a number. Three numbers are special.

| Number | Name | Description |
| ---- | ---- | ---- |  
| 0 | `STDIN` | **Standard Input**<br/>Command line programs get their input via this file descriptor. It's common to see this FD pointing to a TTY device (like `/dev/pts/14`) | 
| 1 | `STDOUT` | **Standard Output**<br/>This is where a program's output goes. The shell redirection can affect what this is. | 
| 2 | `STDERR` | **Standard Error**<br/>This is where error messages for programs go. |

The shell redirect syntax has a noticeable effect on the `STDOUT` and `STDERR` file descriptors. Redirecting `STDOUT` to a file will show the file set to FD 1

```
$ ls -l /proc/self/fd > ls.out
$ cat ls.out
total 0
lrwx------ 1 maximus maximus 64 Oct 25 21:29 0 -> /dev/pts/14
l-wx------ 1 maximus maximus 64 Oct 25 21:29 1 -> /home/mike/ls.out
lrwx------ 1 maximus maximus 64 Oct 25 21:29 2 -> /dev/pts/14
lr-x------ 1 maximus maximus 64 Oct 25 21:29 3 -> /proc/31150/fd
```

Redirecting both `STDOUT` and `STDERR` to a file will show the file as FD 0 and 1:

```
$ ls -l /proc/self/fd > ls.out 2>&1
$ cat ls.out
total 0
lrwx------ 1 maximus maximus 64 Oct 25 21:29 0 -> /dev/pts/14
l-wx------ 1 maximus maximus 64 Oct 25 21:29 1 -> /home/mike/ls.out
lrwx------ 1 maximus maximus 64 Oct 25 21:29 2 -> /home/mike/ls.out
lr-x------ 1 maximus maximus 64 Oct 25 21:29 3 -> /proc/31150/fd
```

Piping `STDOUT` to another command will show a special FD set as FD 1:

```
$ ls -l /proc/self/fd | tee ls.out
total 0
lrwx------ 1 maximus maximus 64 Oct 25 21:31 0 -> /dev/pts/14
l-wx------ 1 maximus maximus 64 Oct 25 21:31 1 -> pipe:[947967]
lrwx------ 1 maximus maximus 64 Oct 25 21:31 2 -> /dev/pts/14
lr-x------ 1 maximus maximus 64 Oct 25 21:31 3 -> /proc/31165/fd
```

## Signals 

When the kernel needs to get a process' attention it sends the process a signal. When a process receives a signal it momentarily stops what it was doing to acknowledge that it's received the signal. Depending on what signal was received the process may continue or it may exit. Signals can come from two sources, they can be sent directly by the kernel or they can come from other programs. The kill command sends signals to processes from the command line. Despite it's name kill does not necessarily kill a process. Signals are numbered, and the signals meaning is based on it's number. To see a list of all signals available run the kill command:

```
$ kill -l 
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL	 5) SIGTRAP
 6) SIGABRT	 7) SIGBUS	 8) SIGFPE	 9) SIGKILL	10) SIGUSR1
11) SIGSEGV	12) SIGUSR2	13) SIGPIPE	14) SIGALRM	15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD	18) SIGCONT	19) SIGSTOP	20) SIGTSTP
21) SIGTTIN	22) SIGTTOU	23) SIGURG	24) SIGXCPU	25) SIGXFSZ
26) SIGVTALRM	27) SIGPROF	28) SIGWINCH	29) SIGIO	30) SIGPWR
31) SIGSYS	34) SIGRTMIN	35) SIGRTMIN+1	36) SIGRTMIN+2	37) SIGRTMIN+3
38) SIGRTMIN+4	39) SIGRTMIN+5	40) SIGRTMIN+6	41) SIGRTMIN+7	42) SIGRTMIN+8
43) SIGRTMIN+9	44) SIGRTMIN+10	45) SIGRTMIN+11	46) SIGRTMIN+12	47) SIGRTMIN+13
48) SIGRTMIN+14	49) SIGRTMIN+15	50) SIGRTMAX-14	51) SIGRTMAX-13	52) SIGRTMAX-12
53) SIGRTMAX-11	54) SIGRTMAX-10	55) SIGRTMAX-9	56) SIGRTMAX-8	57) SIGRTMAX-7
58) SIGRTMAX-6	59) SIGRTMAX-5	60) SIGRTMAX-4	61) SIGRTMAX-3	62) SIGRTMAX-2
63) SIGRTMAX-1	64) SIGRTMAX	
```

There may be different signals on different UNIX systems, but most are common. The manual for signal(7) describes each of the signals fully. There are a few signals that every admin should know.

  * `SIGHUP` (1). Hangup. This signal causes some programs to reload their configuration files or display some information.
  * `SIGINT` (2). Interrupt. This is the signal that BASH sends to a program when you type `CTRL-C` on the keyboard.
  * `SIGQUIT` (2). Quit. This is the signal that BASH sends to a program when you type `CTRL-\` on the keyboard, it's like `SIGINT` but the program should do a core dump as it quits.
  * `SIGKILL` (9). Kill. With extreme prejudice. Programs cannot recover from a `SIGKILL`. They will die immediately.
  * `SIGUSR1` (10). User defined. Programs respond differently. The dd program prints a status update when it receives a `SIGUSR1`.
  * `SIGSTOP` (19). The program is frozen. This is the signal that BASH sends to a program when you type `CTRL-Z`
  * `SIGCONT` (18). Unfreeze the program. This signal is sent when your run the fg or bg command in BASH.
  * `SIGPIPE` (13). Broken pipe. This happens when the program on the right side of a pipe (|) exits before the program on the left is done writing output or when a network connection is closed on the remote end.
  * `SIGBUS` (7), `SIGSEGV` (11). Bus error and segmentation fault, respectively. Programmers will recognize these as the dreaded messages that happen when there's a bug in your program.

You send a signal to a process using the kill command:

```
kill [-<number>] <pid> ...
```

For example, to kill the process with PID 12345 you would run this command:

```
$ kill 12345
```

Kill will send a `SIGTERM` if you don't specify a signal. If that doesn't work run this command:

```
$ kill -9 12345
```

Nothing can survive a `kill -9`. Normal users can only send signals to processes that belong to them. Root can send a signal to any process.


