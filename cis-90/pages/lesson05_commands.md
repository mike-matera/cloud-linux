# Lesson 5 Commands 

This page has the commands for Lesson 5. They are:

| Command | Action | 
| --- | --- | 
| `touch` | Create a file or update a file's timestamp. |
| `mkdir` | Make a directory | 
| `cp` | Copy a file or files | 
| `mv` | Move or rename files and directories | 
| `rmdir` | Remove a directory | 
| `rm` | Remove a file or directory | 
| `ln` | Make a symbolic link | 
| `tree` | Visually list a directory tree | 

## Making and Removing Directories 

The `mkdir` command simply creates a directory and the `rmdir` command removes one. The `mkdir` command only creates a directory if it doesn't exist and the `rmdir` command only removes one if it's empty. 

## Copying and Moving Files and Directories 

The `cp` and `mv` command copy and move files. They're essential commands that take a little getting used to because they do different things in different situations. The first thing to know is that both commands take *at least* two arguments, the **source** and **destination** in order. For example:

```
$ cp from_this_file to_this_file
$ mv from_this_file to_this_file 
```

It's essential that you remember the oder: **from** then **to**.

### Copy or Move Single File 

A single file copy and move has two arguments: 

```
$ cp letter letter.bak 
```

Moving a single file is the same thing as *renaming* the file. 

```
$ mv letter.bak letter.backup 
``` 

### Copying or Moving Multiple Files 

If you want to copy or move multiple files you can have more sources and the last argument, the destination, must be a directory. Try this:

```bash
$ mkdir shapes fruits 
$ touch square triangle tomato orange 

# Copy shapes
$ cp square triangle shapes 
```

Notice there are now two copies of the shapes files. Now try moving:

```bash
$ mv tomato orange fruits 
``` 

### Copying and Moving Directories 

Moving or renaming a directory is as simple as a file: 

```bash 
$ mv shapes polygons 
``` 

Copying a directory requires the `-r` flag to tell `cp` that you want to *recurse* through a directory structure. 

```bash
$ cp fruits foods 
cp: -r not specified; omitting directory 'fruits'
$ cp -r fruits foods 
```

## Making Links 

There's a special kind of file called a *symbolic link* or a *symlink*. A symbolic link is a reference to another file. It's a very useful way to have a file in two places without having to create a copy. Links are created using the command:

```bash 
ln -s <source_of_link> <name_of_link>
```

Notice that the `-s` flag is specified. Without the flag a *hard* link is created, which is less flexible than symbolic links. 

```bash
$ mkdir menu 
$ ln -s fruits/orange menu/breakfast 
``` 

> Watch out! Creating a symbolic link with a relative path should have a path relative to the destination of the link. 

```bash 
$ rm menu/breakfast 
$ ln -s ../fruits/orange menu/breakfast 
``` 

Links can be made to files and directories. 

## Cleaning Up 

You can remove files with `rm`, which takes multiple arguments if you want to remove multiple files. 

```
rm square triangle
```

By default `rm` doesn't work on directories: 

```
$ rm polygons/
rm: cannot remove 'polygons/': Is a directory
```

You should remove a directory using `rmdir`: 

```
$ rmdir polygons 
rmdir: failed to remove 'polygons': Directory not empty
$ rm polygons/*
$ rmdir polygons 
```

The `rm` command has the **nulcear option**. The `-r` flag makes `rm` *recursive*, meaning it will delete everything in the directory and all subdirectories. The `-f` flags says **force** which makes `rm` work without asking any "are you sure?" questions. 

```
rm -rf menu 
```

