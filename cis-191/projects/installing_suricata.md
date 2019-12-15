# Project: Install Suricata Three Ways 

In this project you'll install the Suricata Network Intrusion Detection System (NIDS) three different ways.

## Introduction 

Installing and removing software on Linux has become easier with the advent of package management. In this lab you'll use the apt package manager to install Suricata from the default repositories. Then you'll install a newer version using a PPA. Finally you'll compile the most recent copy for your self. This is how we used to do it1

## Install Suricata 

Before you install Suricata use apt-cache to determine what packages are needed by Suricata. Store the list in a file called dependencies.txt and submit them with the project. Now installin Suricata the easy way:

```
$ sudo apt install suricata
```

Check to see if Suricata is running:

```
$ systemctl status suricata
```

Is the suricata program running? What version of suricata did you install?

## Get the Leading Edge Suricata 

Let's replace the stable suricata with a more leading-edge version. To do that you should first remove the copy you just installed:

```
$ sudo apt purge suricata
$ sudo apt autoremove
```

Then follow the instructions here to add the PPA:
 [https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Ubuntu_Installation_-_Personal_Package_Archives_%28PPA%29#Beta-releases](https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Ubuntu_Installation_-_Personal_Package_Archives_(PPA)#Beta_releases)

What version of suricata did you install?

## Compile Your Own Copy 

Install Suricata the hard way. Start by using the git program to check out the latest source files:

```
$ cd ~
$ git clone -b suricata-4.1.3 https://github.com/inliniac/suricata.git

```

That will create a ~/suricata directory. Before you can suricata you should install some packages that contain essential elements of Ubunut's C/C++ compiler and others:

```
$ sudo apt install pkg-config autoconf autogen build-essential
```

There are more packages needed to build suricata (you will need to figure out which ones). But with the above installed you can get started. Here's the build procedure:

```
$ cd ~/suricata
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
```

Autogen and Configure will fail telling you that things aren't found. Use apt-cache to search for a development package that provides what's missing and try again. You will need to rerun configure many times, each time installing a new "dev" dependency. Stick with it. If you get through the make step successfully you will have a built copy of suricata in your home directory. When surricata is installed you should be able to execute it:  

```
$ LD_LIBRARY_PATH=/usr/local/lib /usr/local/bin/suricata 
Suricata 4.1.0-dev (rev 45f2fdc)
USAGE: /usr/local/bin/suricata [OPTIONS] [BPF FILTER]

	-c <path>                            : path to configuration file
	-T                                   : test configuration file (use with -c)
	-i <dev or ip>                       : run in pcap live mode
	-F <bpf filter file>                 : bpf filter file
	-r <path>                            : run in pcap file/offline mode
	-s <path>                            : path to signature file loaded in addition to suricata.yaml settings (optional)
	-S <path>                            : path to signature file loaded exclusively (optional)
	-l <dir>                             : default log directory
	-D                                   : run as daemon
	-k [all|none]                        : force checksum check (all) or disabled it (none)
	-V                                   : display Suricata version
	-v[v]                                : increase default Suricata verbosity
	--list-app-layer-protos              : list supported app layer protocols
	--list-keywords[=all|csv|<kword>]    : list keywords implemented by the engine
	--list-runmodes                      : list supported runmodes
	--runmode <runmode_id>               : specific runmode modification the engine should run.  The argument
	                                       supplied should be the id for the runmode obtained by running
	                                       --list-runmodes
	--engine-analysis                    : print reports on analysis of different sections in the engine and exit.
	                                       Please have a look at the conf parameter engine-analysis on what reports
	                                       can be printed
	--pidfile <file>                     : write pid to this file
	--init-errors-fatal                  : enable fatal failure on signature init error
	--disable-detection                  : disable detection engine
	--dump-config                        : show the running configuration
	--build-info                         : display build information
	--pcap[=<dev>]                       : run in pcap mode, no value select interfaces from suricata.yaml
	--pcap-file-continuous               : when running in pcap mode with a directory, continue checking directory for pcaps until interrupted
	--pcap-file-delete                   : when running in replay mode (-r with directory or file), will delete pcap files that have been processed when done
	--pcap-buffer-size                   : size of the pcap buffer value from 0 - 2147483647
	--af-packet[=<dev>]                  : run in af-packet mode, no value select interfaces from suricata.yaml
	--simulate-ips                       : force engine into IPS mode. Useful for QA
	--erf-in <path>                      : process an ERF file
	--set name=value                     : set a configuration value


To run the engine with default configuration on interface eth0 with signature file "signatures.rules", run the command as:

/usr/local/bin/suricata -c suricata.yaml -s signatures.rules -i eth0 
```

Submit the executable with the assignment.

## Turn In 

  - dependencies.txt from the first part
  - Answers to the part 1 and part 2 questions.
  - /var/log/apt/history.log from your VM
  - A screenshot of running `/usr/local/bin/suricata` from the last part. 

Submit your project on canvas.
