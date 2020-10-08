# Install Docker 

This lab takes you through the installation of Docker on your local machine and your AWS host. How you install docker depends greatly on the OS you're using and there will be different tradeoffs for different systems. What makes Docker so special is that your home laptop or desktop environment can be made exactly the same as the AWS production environment which speeds up testing and deployment. 


## General Setup Information 

Containers are similar to VMs but there is only one operating system kernel. That means that Linux containers run on Linux, Windows containers run on Windows and Mac containers run on Mac. However, all of the useful containers that you see in production are Linux containers. If you're on a Windows or Mac machine installing Docker also installs a Linux VM for your containers. Installing Docker can be done in one of three ways:

1. **Installing it natively** (Linux and ChromeOS)
1. **Installing Docker Desktop** (Windows and Mac). Docker desktop creates a Linux VM. 
1. **Creating your own VM** with Vagrant (Windows, Mac, Linux)

*Choose an installation mode that fits your home environment* 

## Native Installation (AWS, Linux and ChromeOS)

Ubuntu comes with Docker available in the repository. The version of Docker isn't the latest but it's new enough to be useful. You can install it with just two commands. The first command installs the Docker engine: 

```
$ sudo apt install docker.io 
``` 

Docker commands are only available to users in the `docker` group. This command adds the current user to the `docker` group: 

```
$ sudo usermod -a -G docker $USER 
``` 

You have to logout and login again before you get the new group. Verify that you have successfully installed Docker by running the command:

```
$ docker run docker/whalesay cowsay "Hello CIS-192"
```

You should see a greeting!

> Repeat this procedure on your computer if you use Linux or ChromeOS 

## Docker Desktop Installation (Mac and Windows)

If you want Docker to manage your VM you can simply install Docker Desktop. Download it and follow the instructions here: 

> [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

With Docker Desktop installed you should be able to use the local command prompt (BASH or PowerShell) to execute the command: 

```
$ docker run docker/whalesay cowsay "Hello CIS-192"
```

Verify that you can see the greeting!

## Docker Inside of Vagrant (Mac, Windows and Linux)

If you want to isolate your Docker installation into its own VM Vagrant is a good choice. On Mac and Windows you need a VM anyway and on Linux it makes it possible to "turn Docker off" if you don't want to keep using it. Download the attached Vagrantfile and playbook:

```eval_rst
- :download:`Vagrantfile`
- :download:`playbook.yaml`
```

Put the two files in a directory by themselves and from that directory run the command:

```
$ vagrant up 
``` 

The command will bring up the VM and install Docker on it. Once complete you can login to the VM with the command:

```
$ vagrant ssh 
```

Everything should be in place. Verify that Docker is working by running: 

```
$ docker run docker/whalesay cowsay "Hello CIS-192"
```

## Turn In 

Turn in a screenshot of Whalesay on **both** your AWS instance and your local machine. 

