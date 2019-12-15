# Controlling a Fork Bomb with `ulimit`

# A Famous Fork Bomb 

This BASH code creates new processes as fast as possible. 

```bash
 :(){ :|:& };:
```

Running it in a terminal will render a machine unusable quickly. 

## Limits with `ulimit`

The `ulimit` command sets limits on how many resources a user can consume. On a shared system it's important to set user limits to prevent one user from taking down the machine (accidentally or on purpose). 

## Step 1: Nuke Your VM 

Run the fork bomb on your VM. Once started are you able to stop it? 

## Step 2: Read the `ulimit` Manual 

The `ulimit` command is built into BASH. It doesn't have a manula page of its own. Look in the BASH manual: 

``` 
$ man bash 
```

Here's what's possible to limit: 

``` 
       ulimit [-HSabcdefiklmnpqrstuvxPT [limit]]
              Provides control over the resources available to the shell and to processes started by it, on systems that allow such control.  The -H and -S options specify
              that the hard or soft limit is set for the given resource.  A hard limit cannot be increased by a non-root user once it is set; a soft limit may be increased
              up to the value of the hard limit.  If neither -H nor -S is specified, both the soft and hard limits are set.  The value of limit can be a number in the unit
              specified  for  the  resource  or  one of the special values hard, soft, or unlimited, which stand for the current hard limit, the current soft limit, and no
              limit, respectively.  If limit is omitted, the current value of the soft limit of the resource is printed, unless the -H option is given.  When more than one
              resource is specified, the limit name and unit are printed before the value.  Other options are interpreted as follows:
              -a     All current limits are reported
              -b     The maximum socket buffer size
              -c     The maximum size of core files created
              -d     The maximum size of a process's data segment
              -e     The maximum scheduling priority ("nice")
              -f     The maximum size of files written by the shell and its children
              -i     The maximum number of pending signals
              -k     The maximum number of kqueues that may be allocated
              -l     The maximum size that may be locked into memory
              -m     The maximum resident set size (many systems do not honor this limit)
              -n     The maximum number of open file descriptors (most systems do not allow this value to be set)
              -p     The pipe size in 512-byte blocks (this may not be set)
              -q     The maximum number of bytes in POSIX message queues
              -r     The maximum real-time scheduling priority
              -s     The maximum stack size
              -t     The maximum amount of cpu time in seconds
              -u     The maximum number of processes available to a single user
              -v     The maximum amount of virtual memory available to the shell and, on some systems, to its children
              -x     The maximum number of file locks
              -P     The maximum number of pseudoterminals
              -T     The maximum number of threads

              If  limit  is given, and the -a option is not used, limit is the new value of the specified resource.  If no option is given, then -f is assumed.  Values are
              in 1024-byte increments, except for -t, which is in seconds; -p, which is in units of 512-byte blocks; -P, -T, -b, -k, -n, and -u, which are unscaled values;
              and,  when  in Posix mode, -c and -f, which are in 512-byte increments.  The return status is 0 unless an invalid option or argument is supplied, or an error
              occurs while setting a new limit.
```

## Step 3: Check Limits 

Let's see the current limits: 

``` 
$ ulimit -a 
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 31156
max locked memory       (kbytes, -l) 16384
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 31156
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

Notice that we can fork 31156 processes! That's way to many. 

## Step 4: Reduce the Process Limit 

Let's reduce the number of processes to a much lower (but still healthy) number: 

```
ulimit -u 100 
```

> Now re-run the fork bomb! 

## Turn In 

Take a screenshot of the terminal after you ran the fork bomb in step 4. 

