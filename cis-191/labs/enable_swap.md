# Enabling Swap on Your VM

Your Vagrant VM does not have swap enabled. In this lab you'll format a spare disk and use it as swap. 

## Step 1: Format a Swap Device 

A swap device has to be formatted, just like a filesystem. The `mkswap` command does that: 

```bash
$ sudo mkswap -L vagrant-swap /dev/sdc 
mkswap: /dev/sdc: warning: wiping old swap signature.
Setting up swapspace version 1, size = 1024 MiB (1073737728 bytes)
LABEL=vagrant-swap, UUID=bf9b4309-695b-4e2e-8a60-f49a66a7f5d2
```

Notice that our swap space was given a UUID and we specified a label. 

## Step 2: Turn on Swap 

The `swapon` command does what `mount` does for filesystems. You can turn on swap for a particular UUID or label using this command: 

```bash
$ sudo swapon LABEL=vagrant-swap
```

## Step 3: Check for Swap Space 

```bash
$ grep Swap /proc/meminfo 
SwapCached:            0 kB
SwapTotal:       1048572 kB
SwapFree:        1048572 kB
```

Notice there's swap now! 

## Step 4: Make it Permanent 

Swap, just like filesystems, is made permanent by adding it to `/etc/fstab`. Begin by turning swap off:

```bash 
$ sudo swapoff LABEL=vagrant-swap 
```

Now add this line to `/etc/fstab`:

```
LABEL=vagrant-swap      swap    swap    defaults 0 0 
```

Now test to be sure your `/etc/fstab` is correct: 

```bash
$ sudo swapon -a 
```

## Step 4: Reboot 

With `/etc/fstab` updated swap will be started each time the VM boots. Reboot your vm and verify that this is the case. 


## Turn In 

Turn in your `/etc/fstab` file. 

