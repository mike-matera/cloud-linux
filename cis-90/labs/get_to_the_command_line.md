# Get to the Command Line 

This lab will get you to the command line on your home or school computer. The process is different depending on your operating system, and there may be multiple ways to do it. On Windows you can install a full copy of Ubuntu Linux from the Windows Store. On Mac --which is based on BSD Unix-- you simply open the Terminal app. This lab is an essential first step toward accessing the materials for the course. 

This lab supports: 

  - Windows 
  - OSX
  - Chromebook 


Of course, if you already have Linux as your operating system, you're ready to go! 

## Windows 10

On Windows 10 you have two options: 

  - Run real Linux using Windows Subsystem for Linux ([instructions](https://docs.microsoft.com/en-us/windows/wsl/install-win10))
  - Use PowerShell to get a non-Unix (but still good) command prompt. 

**Which one should you choose?** WSL uses more resources than PowerShell, but is superior because it's a real Linux command line and supports all of the commands that we will learn in the course. Unless your computer is very old I recommend following the instruction in the WSL link (I will demonstrate the procedure in class) as a first step. If for some reason it won't work for you use PowerShell. 

## Older Windows 

Unfortunately, older versions of Windows do not support the SSH command in PowerShell and do not have WSL. If you are using older Windows please consider an upgrade, your machine is insecure and will certainly be hacked. It's only a matter of time. You have three options for doing course work: 

  - Upgrade to Windows 10 
  - Install Linux or boot your machine with a Live image. ([Ubuntu guide](https://ubuntu.com/tutorials/try-ubuntu-before-you-install#1-getting-started))
  - Install PuTTY for SSH support. ([download](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html))

## Macintosh OSX

Since OSX Macintosh machines are based on FreeBSD, a UNIX operating system. Almost all of the commands you will learn in the class work natively on your Mac. You can open a terminal by looking in your Applications folder under Utilities. That's: 

  Applications -> Utilities -> Terminal 

You can also launch a terminal with the Command-T key sequence. 

## Chromebook 

Chromebooks run Linux but the Linux command prompt is inaccessible for security reasons. There are two options for Chromebooks: 

  - Enable Linux Mode ([instructions](https://support.google.com/chromebook/answer/9145439?hl=en))
  - Install the Secure Shell App ([instructions](https://chrome.google.com/webstore/detail/secure-shell-app/pnhechapfaindjhompbnflcldabbghjo?hl=en))

Just like WSL in Windows, Linux mode on the Chromebook installs a separate copy of Linux in a Virtual Machine. This requires more resources than installing the Secure Shell App but gives you full access to a real Linux command line. 

