# Create an Overlay Filesystem  

In this lab you'll experiment with OverlayFS.

## Overlay Parts 

An *overlay* filesystem combines two or more directories into *layers*. Additionally there is a *work* directory that OverlayFS needs to do its work. The table explains the directories required by OverlayFS: 

| Directory | Function | Description | 
| --- | --- | --- | 
| `lower*` | Read-Only | The lower directory contains the "base" filesystem. There can be more than one lower directory, forming a stack of read-only layers. | 
| `upper` | Read-Write | Any changes made to the union filesystem will appear in the upper directory which must be writable. | 
| `work` | Read-Write | This is a work directory for OverlayFS it must be on the same filesystem as the upper directory | 
| `target` | Read-Write | The resulting UnionFS will be mounted onto the target directory. | 


## Before You Begin  

You need some files for your overlay filesystem. Download the tar file that contains the Poems directory from CIS-90: 

```eval_rst 
- :download:`poems.tar.gz`
``` 

Make this file available to your VM. 

## Step 1: Create the Directory Structure 

Create the following directories that will serve as the layers for OverlayFS: 

1. `/mnt/lower`
2. `/mnt/upper`
3. `/mnt/work`
4. `/mnt/target` 

## Step 2: Populate the Lower Directory 

Unzip the `poems.tar.gz` file into `/mnt/lower`. 

```bash
$ cd /mnt/lower; sudo tar -zxvf /vagrant/poems.tar.gz
```

You should see the poems in `/mnt/lower`.

## Step 3: Mount Your Overlay  

Now create the overlay using the `mount` command:

```bash 
$ sudo mount -t overlay overlay -o lowerdir=/mnt/lower,upperdir=/mnt/upper,workdir=/mnt/work /mnt/target 
```

> Problems? Look for kernel error messages using the `dmesg` command. 

Verify the mount worked: 

```bash
$ mount | grep overlay
overlay on /mnt/target type overlay (rw,relatime,lowerdir=/mnt/lower,upperdir=/mnt/upper,workdir=/mnt/work)
```

You can also see the mount with `df`:

```bash
$ df /mnt/target/
Filesystem     1K-blocks    Used Available Use% Mounted on
overlay         10098432 1508992   8573056  15% /mnt/target
```

## Step 4: Add a New Poem 

Add the following poem into `/mnt/target/Poems/Neruda/if_you_forget_me`:

```
I want you to know
one thing.

You know how this is:
if I look
at the crystal moon, at the red branch
of the slow autumn at my window,
if I touch
near the fire
the impalpable ash
or the wrinkled body of the log,
everything carries me to you,
as if everything that exists,
aromas, light, metals,
were little boats
that sail
toward those isles of yours that wait for me.

Well, now,
if little by little you stop loving me
I shall stop loving you, little by little.

If suddenly
you forget me,
do not look for me,
for I shall already have forgotten you.

If you think it long and mad,
the wind of banners
that passes through my life,
and you decide
to leave me at the shore
of the heart where I have roots,
remember
that on that day,
at that hour,
I shall lift my arms
and my roots will set off
to seek another land.

But
if each day,
each hour,
you feel that you are destined for me
with implacable sweetness,
if each day a flower
climbs up to your lips to seek me,
ah my love, ah my own,
in me all that fire is repeated,
in me nothing is extinguished or forgotten,
my love feeds on your love, beloved,
and as long as you live it will be in your arms
without leaving mine.
```

Use your favorite text editor to copy-and-paste the poem. 

## Step 5: Examine the Contents of your Overlay 

Use the `tree` command to look at the `upper` directory: 

```bash
$ tree upper/
upper/
└── Poems
    └── Neruda
        └── if_you_forget_me
``` 

Notice that the new poem is there. Also, use `find` to see where the poem appears. 

```bash
$ find . -name if_you_forget_me 
./target/Poems/Neruda/if_you_forget_me
./upper/Poems/Neruda/if_you_forget_me
```

## Step 4: Make it Permanent 

Remember, to make a mount permanent you have to add it to `/etc/fstab`. Add this line to the file and your mount point will be restored upon reboot. 

```
overlay /mnt/target overlay rw,relatime,lowerdir=/mnt/lower,upperdir=/mnt/upper,workdir=/mnt/work 0 0 
```

## Turn In  

Create a file that shows your mounted filesystem: 

```bash
$ mount | grep overlay > /vagrant/overlayfs.mount.txt 
```

Submit the file on Canvas
