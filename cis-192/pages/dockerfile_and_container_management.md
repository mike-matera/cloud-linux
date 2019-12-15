# Docker Applications 

In this lesson you'll create a simple web application from scratch and "containerize" it. Containers let you take a simple network program and easily make it a service. Containerizing, as it's called, has the benefit that your service is portable (it can move easily from one host or platform to another). Containerization also confers a security benefit because your service is isolated from the host machine. In this lesson you'll create a simple web service using the Python programming language. Then you'll create a Dockerfile to containerize the service. Also, you'll learn about the life cycle of containers, how they use storage and how to manage the storage they use.

The lecture slides are [here](https://drive.google.com/open?id=1gJAGE8OjehWZYJ5RhgJGA7nshrOWaJxIwuZiB6-qlus)

## Commands 

  * docker

## Configuration 

  * Dockerfile

## Further Reading 

  * [Docker Tutorial using Flask](https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04)
  * [Docker and IPv6](https://docs.docker.com/engine/userguide/networking/default_network/ipv6/)

## Network Setup 

Before you can have a service you must configure your firewall and DNS so that:

  - Your app server has a DNS record (preferably www.yourdomain.cis.cabrillo.edu)
  - You allow HTTP traffic from the internet to your app server.

If you have done that already, great. If not follow these instructions.

### Firewall Rule 

On your router you must setup a forwarding rule. The rule must allow new connections coming from the internet destined for TCP/80 to be forwarded to your app server. Make sure you alter the following command to reflect the IPv6 address of your webserver:

```
router$ sudo ip6tables -I FORWARD 1 -m state --state NEW -p tcp -d app-server-ipv6-addr --dport 80 -j ACCEPT
```

With the firewall rule established you will be able to connect to your web server with your browser if you're on the CIS network or you have IPv6 at home. When you put an IPv6 address into the browser you need to use square brackets. Like this:

```
http://[ipv6-address-goes-inside-of-brackets]/
```

If you don't have IPv6 and you want to test your connection you can use an IPv6 proxy site:

  * [http://www.ipv6proxy.net/](http://www.ipv6proxy.net/)
  * [http://ipv6proxy.org/](http://ipv6proxy.org/)

Those sites let you type in an IPv6 address and they will load the page for you.

> **WARNING**: DO NOT USE IPv6 PROXIES FOR ANY PERSONAL BROWSING.THEY ARE INSECURE.

Typing your IPv6 address every time is a pain. Next you will setup an name for your server in DNS. Don't forget to save your firewall rules!

### Setup DNS 

Having a DNS record that points to your server makes life much easier. You only need to setup an IPv6 (AAAA) address because your IPv4 address isn't useful (even for the CIS network). In your domain file add a record like the following. Be sure to replace the IPv6 address in my example with the address of your server:

```
www IN AAAA app-server-ipv6-address
```

Be sure to update your serial number! Reload your DNS configuration with the command:

```
router$ sudo systemctl restart bind9
```

Test that your record works with dig:

```
router$ dig AAAA www.mydomain.cis.cabrillo.edu @localhost
```

If you get an answer you should now be able to browse to your webserver directly:

```
http://www.mydomain.cis.cabrillo.edu/
```

But what about the "naked" domain? Most of time we go to "amazon.com" not "www.amazon.com." The concept of a "naked" domain is a problem for DNS. The way domains handle it is against the standard, but it's so common now that it just works everywhere. To make entering the domain address reach the webserver you must add the following record.

```
@ IN AAAA <your-app-server-ipv6-address>
```

After reloading your DNS configuration (with the updated serial number) you should be able to access your web server this way:

```
http://mydomain.cis.cabrillo.edu/
```

You're now on the Internet for real.

## Your First Service 

The Python programming language makes it easy to run so-called microservices. Those are simple web applications that fulfill a single purpose. For example, you could write a microservice that lets you add and remove users to a host remotely. Microservices are popular in part because they're easy to write and deploy in containers. To start your microservice create a directory from the student user's home directory:

```
app$ mkdir ~/HelloService
app$ cd ~/HelloService
```

Now copy this Python code into a file called `hello.py`:

```python
from flask import Flask
import subprocess
import sys

app = Flask(__name__)


@app.route('/')
def hello_world():
  #ifconfig = subprocess.check_output(['ifconfig', '-a']).decode('UTF-8')
  html = '<html><h2>Hello World!</h2>'
  html += '<p>Python version:</p>'
  html += '<pre>' + str(sys.version) + '</pre>'
  html += '<p>Interfaces:</p>'
  html += '<pre>' + subprocess.check_output(['ip', 'addr']).decode('UTF-8') + '</pre>'
  html += '</html>'
  return html


if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=5000)
```

Now try to run your service on your VM. You'll get an error:

```
app$ python3 ./hello.py 
Traceback (most recent call last):
  File "./hello.py", line 1, in <module>
    from flask import Flask
ImportError: No module named 'flask'
```

The flask library is not installed! You can't install it with apt-get but you can install it using Python's package manager pip. Do that with the following commands:

```
app$ sudo apt install python3-pip
app$ pip3 install flask
```

Notice you don't have to use sudo to install flask. That installs it for the current user only (which is nice for development libraries). Now try to start your application and you'll see it come to life:

```
app$ python3 ./hello.py
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 291-527-383
```

The service runs in the foreground, to stop it hit Ctrl-C on the keyboard. The service listens for connections on port 5000 so that it can be started by a normal user. For now, verify that your service is running using `ss` in a second shell:

```
app$ sudo ss -lntp 
State      Recv-Q Send-Q                                                  Local Address:Port                                                                 Peer Address:Port              
LISTEN     0      128                                                                 *:5000                                                                            *:*                   users:(("python3",pid=32265,fd=4),("python3",pid=32265,fd=3),("python3",pid=32263,fd=3))
LISTEN     0      5                                                         10.200.71.1:53                                                                              *:*                   users:(("dnsmasq",pid=12547,fd=9))
LISTEN     0      128                                                                 *:22                                                                              *:*                   users:(("sshd",pid=17290,fd=3))
LISTEN     0      5                                              fd60:e109:68e0:ebf1::1:53                                                                             :::*                   users:(("dnsmasq",pid=12547,fd=13))
LISTEN     0      5                                      fe80::74ef:d2ff:fe2b:86%lxdbr0:53                                                                             :::*                   users:(("dnsmasq",pid=12547,fd=11))
LISTEN     0      128                                                                :::22                                                                             :::*                   users:(("sshd",pid=17290,fd=4))
```

You should see python3 listening on port 5000. We'll move that to port 80 as a part of the containerization. Your firewall doesn't allow external connections to port 5000 but you can see the page your app is serving using curl:

```
app$ curl http://localhost:5000/
127.0.0.1 - - [14/Nov/2019 12:22:09] "GET / HTTP/1.1" 200 -
<html><h2>Hello World!</h2><p>Python version:</p><pre>3.5.2 (default, Oct  8 2019, 13:06:37) 
[GCC 5.4.0 20160609]</pre><p>Interfaces:</p><pre>1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:99:c4:78 brd ff:ff:ff:ff:ff:ff
    inet 10.192.0.4/16 brd 10.192.255.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 2607:f380:80f:f900:250:56ff:fe99:c478/64 scope global mngtmpaddr dynamic 
       valid_lft 86277sec preferred_lft 14277sec
    inet6 fe80::250:56ff:fe99:c478/64 scope link 
       valid_lft forever preferred_lft forever
7: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:be:86:81:43 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:beff:fe86:8143/64 scope link 
       valid_lft forever preferred_lft forever
13: lxdbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.200.71.1/24 scope global lxdbr0
       valid_lft forever preferred_lft forever
    inet6 fd60:e109:68e0:ebf1::1/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::74ef:d2ff:fe2b:86/64 scope link 
       valid_lft forever preferred_lft forever
</pre></html>
```

Notice the following:

  - You got application code to run.  
  - You **manually** installed packages to make it work
  - It works! 
  
## Containerization and Dockerfile 

The problem with the previous steps is that there are really two parts: the code and the setup. When you containerize tha application you automate the setup so that the container can be deployed anywhere. Now let's move your service into a container. The first step is to create a `Dockerfile`. In the same directory as `hello.py` create a file called Dockerfile and place the following contents in it:

```
FROM ubuntu:latest
MAINTAINER You "you@you.cis.cabrillo.edu"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential iproute2
RUN pip3 install flask
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["hello.py"]
```

Change the MAINTAINER line to have your name and email address. Now build your container with the following command:

```
app$ docker build -t hello-service:latest .
```

Your container will take a little while to build. Notice what's happening:
  - The container starts with the base Ubuntu image.
  - The RUN commands are executed when you build a container. They:
    - run `apt-get` to fetch pip, just like you did on your VM
    - run `pip3` to install flask, just like you did on your VM
    - Copy the contents of the current directory into your container's `/app` directory.

The process will take a while. Rerun the command. It takes almost no time. That's because Docker makes a snapshot of your container after each RUN command. When you rebuild the container it uses the cached snapshots so that apt-get and pip3 do not have to be rerun! 

### Starting and Stopping Your Container 

Now you have a built container. The image will be ready to deploy. You can see the built images with the command:

```
app$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-service       latest              4b8e0a353a28        5 seconds ago       476MB
<none>              <none>              76f95204d20d        7 minutes ago       473MB
ubuntu              latest              775349758637        13 days ago         64.2MB
```

The image can be deployed as many times as you like. Each time you deploy an image you give the running container a name. Also, Docker creates a virtual network for containers and manages port forwarding automatically when you specify the `-p` option. Start an instance of your container by using the docker run command:

```
app$ docker run --name hello-instance -p 80:5000 hello-service:latest
```

Here's what the options do:

  * `--name` gives your instance a name. If you don't specify a name one will be automatically assigned, like "semiotic-abbey"
  * `-p 80:5000` tells docker to proxy connections on the local port 80 to the container's port 5000
  * `hello-service:latest` is the container image to launch.

Using `ss` you should see that docker-proxy is running on port 80:


```
$ sudo ss -lntp 
[sudo] password for student: 
Sorry, try again.
[sudo] password for student: 
State      Recv-Q Send-Q                                                  Local Address:Port                                                                 Peer Address:Port              
LISTEN     0      128                                                                 *:5000                                                                            *:*                   users:(("python3",pid=32265,fd=4),("python3",pid=32265,fd=3),("python3",pid=32263,fd=3))
LISTEN     0      5                                                         10.200.71.1:53                                                                              *:*                   users:(("dnsmasq",pid=12547,fd=9))
LISTEN     0      128                                                                 *:22                                                                              *:*                   users:(("sshd",pid=17290,fd=3))
LISTEN     0      128                                                                :::80                                                                             :::*                   users:(("docker-proxy",pid=9429,fd=4))
LISTEN     0      5                                              fd60:e109:68e0:ebf1::1:53                                                                             :::*                   users:(("dnsmasq",pid=12547,fd=13))
LISTEN     0      5                                      fe80::74ef:d2ff:fe2b:86%lxdbr0:53                                                                             :::*                   users:(("dnsmasq",pid=12547,fd=11))
LISTEN     0      128                                                                :::22                                                                             :::*                   users:(("sshd",pid=17290,fd=4))
```

Test that you can see the hello app from your browser. Remember, if you don't have IPv6 at home you'll need to use a proxy service as shown above. Here's a screenshot of connecting to my hello-app from home:

![image](../../_static/images/screenshot_from_2017_04_23_10_20_10722e.png)

Congratulations you now have a running microservice!

## Management and Cleanup 

Docker run creates a new instance and starts it. If you specify the -d option to docker run the container is run in the background and the prompt comes right back. This is usually how services will be run. While your service is running run this command in a separate shell:

```
app$ docker ps
CONTAINER ID        IMAGE                  COMMAND              CREATED              STATUS              PORTS                  NAMES
e6beab4dc0ea        hello-service:latest   "python3 hello.py"   About a minute ago   Up About a minute   0.0.0.0:80->5000/tcp   hello-instance
```

You can see the instance running. If you use Control-C to stop the service it will no longer appear until you give docker ps the -a argument:

```
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND              CREATED              STATUS                     PORTS               NAMES
e6beab4dc0ea        hello-service:latest   "python3 hello.py"   About a minute ago   Exited (0) 2 seconds ago                       hello-instance
```

Notice a stopped instance has no ports. You can restart the instance with the command:

```
app-server$ docker start hello-instance
```

That will run the service in the background. You can stop it with:

```
app-server$ docker stop hello-instance
```

If you change the `Dockerfile` or you want to change the program in `hello.py` you must rebuild the container image using docker build. Your instance is not automatically updated. To get the new source you have to delete your instance with docker rm and re-run it using docker run.
