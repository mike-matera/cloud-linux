# Setup Email with Alpine 

Alpine is a modern version of the [Pine](https://en.wikipedia.org/wiki/Pine_(email_client)) email client. Pine is a menu-driven way to check your email on a UNIX system. Believe it or not, this was the easy way to send and receive email on in the early 90's. This guide will show you how to setup Alpine on opus3. 

## Initial Configuration 

When you first start `alpine` it complains that a few settings are missing. You can go through the configuration process to fix the settings as shown below: 

<script id="asciicast-5zBmidWVGedFMAWxf4X1e199f" src="https://asciinema.org/a/5zBmidWVGedFMAWxf4X1e199f.js" async></script>

Here's the step-by-step instructions: 

1. Run `alpine`
2. Hit `Enter` to get past the welcome screen 
3. Type `s` for setup
4. Type `c` for Config 
5. Navigate with the arrow keys and `Enter` to select Personal Name 
6. Change your name
7. Type `e` to exit setup 
8. Type `y` to save your settings 

## Check Your Messages 

I've sent everyone a message. Use `alpine` to read and reply to the message I sent you. Here's a walk through. Notice that there's a menu at the bottom of the screen. You can learn all the keys you need using the menu.

<script id="asciicast-n92LbPioV8MvS6HTwEfSDuOUQ" src="https://asciinema.org/a/n92LbPioV8MvS6HTwEfSDuOUQ.js" async></script>

## Sending Mail with `mail` 

Alpine is the easy way. The older `mail` program. The `mail` program is driven by simpler menus. It can also be used to send a message from the command line. The following command will send me an email with the subject, "Hello Mike."

```bash 
$ mail -s "Hello Mike" mmatera@opus.cis.cabrillo.edu 
```

The `mail` program will ask for a list of people to send a carbon copy to. You can leave that blank. Type your message and when you're done type `ctrl-d`. Look at the procedure below: 

<script id="asciicast-SYMuENtwZLhI7WXdSXfrLsvba" src="https://asciinema.org/a/SYMuENtwZLhI7WXdSXfrLsvba.js" async></script>


