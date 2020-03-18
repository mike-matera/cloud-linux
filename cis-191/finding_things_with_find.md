# Finding Files with `find` 

The find command is one of the most useful and confusing commands in UNIX. It's used to find files and directories. This tutorial contains some useful tips and recipes for finding the things you want.

Every find command works like this:

```
find <where-to-look> <what-to-look-for>
```

Where to look is a directory. This argument is required, a very common mistake is to neglect this argument. If you want find to look starting in the current directory do this:

```
find . <what-to-look-for>
```

What to look for is a list of zero or more predicates. If you don't specify anything find lists everything it finds. For example, to see every file and folder on your computer run this:

```
$ find /
```

If you wanted to count every file and folder do this:

```
$ sudo find / | wc -l
2212870
```

The predicates take the list of all files and folders and reduce them to just what you're looking for. If you wanted to find a file named "foo" somewhere starting in the current directory you would do this:

```
$ find . -name 'foo'
```

Here's a useful trick. You're trying to configure GRUB and you don't know where the configuration is. This find command will show you and files or directories with grub in the name:

```
$ find /etc -name '*grub*'
```

Notice the single quotes (`'`). They are required to keep the BASH from interpreting your wildcard characters (`*`). Never forget the quotes! BASH on Ubuntu tries to help by not interpreting the stars when the command is find but don't expect that kind of nicety from other Linux distributions. What if you only wanted to find directories with grub in the name?

```
$ find /etc -type d -name '*grub*'
```

The ``-type`` flag tells find to only look at directories. Files, symbolic links, directories and devices among others can be found by type. 

Find can take a very long time if you're looking through a lot of files. If you only want to limit how many directories find descends you do this:

```
$ find /haystack -maxdepth 2 -name '*needle*'
```

That only looks in the current directory and the immediate subdirectories.The ``-maxdepth`` argument must be specified first. If you're looking for a file and you have a lot to search through here's a procedure that will save time. Start with a small maxdepth and make it bigger if you don't find what you're looking for:

```
$ find /haystack -maxdepth 2 -name '*needle*'

# not found? Try this:
$ find /haystack -maxdepth 3 -name '*needle*'

# not found? try this:
$ find /haystack -maxdepth 4 -name '*needle*'
```

There are many, many more options you can give to find. You can see a complete list in the manual page.