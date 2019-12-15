# Linux Containers 

Containers are a form of virtualization that's flexible and light weight. Containers are the most important new technology in Linux, particularly in the networking world. Containers enable you to quickly build services in a way that's more powerful than you could do with VMs. This page will take you through installing three different container systems [Docker](https://www.docker.com/), [Podman](https://podman.io/) and [LXD](https://linuxcontainers.org/) (pronounced "lex-dee") and discusses the difference in how they're used. 

## What Container do I Need?

No matter what container type you use the technology behind the container is the same. But, there are two essential types of containers:

  1. Containers that encapsulate a single program (like a web server or microservice). Examples: Docker and Podman 
  2. Containers that encapsulate an instance of systemd so they behave like a Linux VM. Examples: LXD
  
Which type you use depends what you need. The first type is the most common because Docker containers are used to create interconnected services that run web applications. The second type is a way to create isolated Linux environments that are much lighter than VMs. 

## Using LXD 

LXD is already installed on your VMs! Execute the following command to make LXD ready to use: 

```
app$ sudo lxd init 
```

The `lxd init` process will ask you a series of questions. Accept all the default answers by pressing enter. The outline of what is happening is:

  1. You need a new storage pool (take the default)
  2. You need to setup container networking (the defaults are best)

At the end of the process you should see: 

``` 
LXD has been successfully configured.
```

### Pick a Version of Linux to Run 

You can find a list of pre-built container images at this URL:

> https://us.images.linuxcontainers.org/

LXD uses repositories just like apt does. You can see where your system looks for container images using this command:

```
app$ lxc remote list 
+-----------------+------------------------------------------+---------------+--------+--------+
|      NAME       |                   URL                    |   PROTOCOL    | PUBLIC | STATIC |
+-----------------+------------------------------------------+---------------+--------+--------+
| images          | https://images.linuxcontainers.org       | simplestreams | YES    | NO     |
+-----------------+------------------------------------------+---------------+--------+--------+
| local (default) | unix://                                  | lxd           | NO     | YES    |
+-----------------+------------------------------------------+---------------+--------+--------+
| ubuntu          | https://cloud-images.ubuntu.com/releases | simplestreams | YES    | YES    |
+-----------------+------------------------------------------+---------------+--------+--------+
| ubuntu-daily    | https://cloud-images.ubuntu.com/daily    | simplestreams | YES    | YES    |
+-----------------+------------------------------------------+---------------+--------+--------+
```
> IMPORTANT: LXD is controlled with the `lxc` command! 

In this example we'll create a Kali Linux container so we can take advantage of the security tools that it offers. Kali Linux is available from the `linuxcontainers.org` repository. When you start a new container use the `lxc launch` command:

```
 lxc launch <repository>:<image-name> <new-container-name>
```

To start Kali the command is: 

```
app$ lxc launch images:kali first-container
Creating first-container
Starting first-container                    
```

Check that your container has started: 

```
$ lxc list 
+-----------------+---------+---------------------+-----------------------------------------------+------------+-----------+
|      NAME       |  STATE  |        IPV4         |                     IPV6                      |    TYPE    | SNAPSHOTS |
+-----------------+---------+---------------------+-----------------------------------------------+------------+-----------+
| first-container | RUNNING | 10.200.71.80 (eth0) | fd60:e109:68e0:ebf1:216:3eff:fe8a:bc45 (eth0) | PERSISTENT | 0         |
+-----------------+---------+---------------------+-----------------------------------------------+------------+-----------+
```

### Accessing Your Container 

The LXD container is just like a VM! You can access it over SSH if SSH is configured in the container. You can also connect to it directly using the `lxc` command. The following command executes BASH on the container and connects you to the prompt:

```
app$ lxc exec first-container bash
root@first-container:~# 
``` 

You are root on your container so use your power to install the `top` program:

```
root@first-container:~# apt install procps 
```

Run `top` on your container and notice how few processes are running compared to a full Linux instance. Now, on your app server run the following command: 

```
$ ps -ef | grep top 
100000   31055 30854  0 09:55 pts/2    00:00:00 top
student  31057 30896  0 09:55 pts/3    00:00:00 grep --color=auto top
``` 

> Look closely!

What does this mean? The container only sees its own processes but outside of the container all processes (including those inside the container) are visible! 

### Cleanup Your Container 

Containers, like VMs, are started and stopped. Stop your new container with the command:

```
app$ lxc stop first-container
```

Delete your container with the command: 

```
app$ lxc delete first-container
```

Check that your container has been removed:

```
app$ lxc list 
+------+-------+------+------+------+-----------+
| NAME | STATE | IPV4 | IPV6 | TYPE | SNAPSHOTS |
+------+-------+------+------+------+-----------+
```

You still have the downloaded image of Kali Linux. If you want to start the container again it will go more quickly. However, it's also using precious disk space. You can see downloaded images with the command:

```
app$ lxc image list
+-------+--------------+--------+-------------------------------------+--------+---------+-----------------------------+
| ALIAS | FINGERPRINT  | PUBLIC |             DESCRIPTION             |  ARCH  |  SIZE   |         UPLOAD DATE         |
+-------+--------------+--------+-------------------------------------+--------+---------+-----------------------------+
|       | be882ed16804 | no     | Kali current amd64 (20191106_17:14) | x86_64 | 74.22MB | Nov 7, 2019 at 5:44pm (UTC) |
+-------+--------------+--------+-------------------------------------+--------+---------+-----------------------------+
```

Cleanup the downloaded image with the command: 

```
app$ lxc image delete <fingerprint-here>
```

The fingerprint of your image may be different than mine. Replace `<fingerprint-here>` with the fingerprint listed by `lxc image list`. 

## Using Docker (and Podman)

Docker and Podman are single-process containers. They are designed to execute a single service like the Apache web server or MySQL database. Despite the term "single-process" it's entirely possible to run multiple processes in a Docker container, Apache and MySQL both use multiple processes to perform their duties. 

### Docker or Podman? 

Podman in most cases can be a drop-in replacement for Docker. This article will show you how to use Docker commands but in all instances you could just replace the `docker` command with the `podman` command and the same things will happen. The difference between the two is that Docker is designed for production environments that rely on remote control. Podman is designed to help you easily run containers on your laptop or desktop machine.

### Installing Docker 

Docker has multiple editions. We will use the Community Edition (CE) because it's free. The Enterprise Edition has features needed for efficiently managing hundreds of containers and requires a subscription. Follow the instructions for installing Docker CE here: 

> https://docs.docker.com/install/linux/docker-ce/ubuntu/

You must also perform the post-installation steps here:

> https://docs.docker.com/install/linux/linux-postinstall/
>
> THESE ARE REQUIRED!

The post-installation steps make it possible for non-root users to use Docker and the rest of the article assumes you have done them. 

> IMPORTANT: After adding the student user to the docker group you have to logout and login again. 

### Start an Apache Container 

Docker uses repositories just like LXD and apt. You can find a public repository of Docker containers at Dockerhub:

> https://hub.docker.com/

We will use the official Apache container for this demonstration. 

```
app$ docker run -dit --name first-docker -p 80:80 httpd
```

That will *pull* and run the container image. Once complete we're returned to the prompt and you can confirm that the container is running: 

```
app$ docker ps 
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS                  NAMES
b7eb218f6562        httpd               "httpd-foreground"   32 seconds ago      Up 30 seconds       0.0.0.0:80->80/tcp   first-docker
```

### Checking the Container Logs 

You can run a `bash` shell in a Docker container, just like you can with LXD but that's not what you typically want to do. When the container started output to the console from the apache program is saved. You can view the output using the `docker logs` command:

```
app$ docker logs first-docker 
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
[Thu Nov 07 20:20:46.851706 2019] [mpm_event:notice] [pid 1:tid 140672752182400] AH00489: Apache/2.4.41 (Unix) configured -- resuming normal operations
[Thu Nov 07 20:20:46.852774 2019] [core:notice] [pid 1:tid 140672752182400] AH00094: Command line: 'httpd -D FOREGROUND'
```

Apache looks like it started! 

### Accessing the Container 

The container is designed to be accessed over the network. We gave an argument to Docker, `-p 80:80` that argument says port 80 on the container maps to port 80 on the host. You can use the `ss` command to verify that the host is listening on port 80:

```
app$ sudo ss -lntp 
State      Recv-Q Send-Q                                                  Local Address:Port                                                                 Peer Address:Port              
LISTEN     0      5                                                         10.200.71.1:53                                                                              *:*                   users:(("dnsmasq",pid=30285,fd=9))
LISTEN     0      128                                                                 *:22                                                                              *:*                   users:(("sshd",pid=17290,fd=3))
LISTEN     0      128                                                                :::80                                                                             :::*                   users:(("docker-proxy",pid=7820,fd=4))
LISTEN     0      5                                              fd60:e109:68e0:ebf1::1:53                                                                             :::*                   users:(("dnsmasq",pid=30285,fd=13))
LISTEN     0      5                                      fe80::ad:99ff:fe6e:14fc%lxdbr0:53                                                                             :::*                   users:(("dnsmasq",pid=30285,fd=11))
LISTEN     0      128                                                                :::22                                                                             :::*                   users:(("sshd",pid=17290,fd=4))
```

Notice that Docker itself is listening on port 80. We can fetch the webpage from the app server using wget: 

```
app$ curl http://localhost
<html><body><h1>It works!</h1></body></html>
```

### Updating the Firewall 

Next week you'll expose your Docker container to the internet using a firewall rule. Here's a preview of what's requried:

 - Add an IPv4 port forward from your router TCP/80 to your app server TCP/80
 - Add forwarding rules to your app server allowing new connections to TCP/80 for both IPv4 and IPv6
 
### Clean Up the Container 

Just like LXD containers Docker containers can be started and stopped. Do this to stop your new container: 

```
app$ docker stop first-docker 
```

The container is still present and can be started again. You can see stopped containers using the command:

```
app$ docker ps -a 
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS                      PORTS               NAMES
73bdcb0fac0f        httpd               "httpd-foreground"   6 minutes ago       Exited (0) 42 seconds ago                       first-docker
```

When a container is stopped it can be removed:

```
app$ docker rm first-docker 
```

Just like with LXD the image is still downloaded using disk space. This is good because starting a new Aapache container will be much quicker. You can view downloaded images using the command:

```
app$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
httpd               latest              d3017f59d5e2        7 days ago          165MB
```

Remove the image with the command:

```
$ docker image rm httpd:latest 
Untagged: httpd:latest
Untagged: httpd@sha256:35fcab73dc9ae55db5c4ac33f5e0c7e76b7735aaddb628366bab04db6f8ae96e
Deleted: sha256:d3017f59d5e25daba517ac35eaf4b862dce70d2af5f27bf40bef5f936c8b2e1f
Deleted: sha256:c015bdd664253fc2ccdff3a425ba085e94b99ce801d6c9c5219ffaad279362b1
Deleted: sha256:c79505e64684e42a92353a6e3430969d8a801f327d24bdde11bd99d41cbef2a0
Deleted: sha256:87158971c3545200bc870118cfa31bf5470204eea10da0b79531388b5f91cea2
Deleted: sha256:0105db3a8b98aea80771956b067b64a26bd630718141bacd6feafdc5b5c0caee
Deleted: sha256:b67d19e65ef653823ed62a5835399c610a40e8205c16f839c5cc567954fcf594
```

## Using Podman 

You can do the same process with Podman. Follow the installation instructions for Podman here:

> https://podman.io/getting-started/installation

You also need to install user mode networking: 

```
app$ sudo apt install slirp4netns
```

You don't need to modify a user's group to use Podman. After installation is complete you should be able to redo all the `docker` commands using `podman` instead with one exception. Podman doesn't use Dockerhub by default so you should specify it when you start the Apache container: 

```
app$ podman run -dit --name first-docker -p 80:80 docker.io/httpd
```

Another change is that Podman is designed to be used by an unprivileged user. An unprivileged user cannot connect to port 80 so the Apache won't have working networking. More on that next week. 
