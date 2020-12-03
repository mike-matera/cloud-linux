# Build an Application with Docker Compose 

This lab will take you through unifying the container work you've done so far in the class to build a modern application with multiple components. 

## Introduction 

It take many containers to build a real application. Up until now we've deployed containers one at a time. That's tedious, accident prone and time consuming. There's a better way using [Docker Compose](https://docs.docker.com/compose/). This lab will guide you through making a complex application. 

## Step 1: Install Docker Compose 

On recent Ubuntu systems like the ones we're using you can install the `docker-compose` command using `apt`:

```
$ apt-install docker-compose 
```

Easy!

## Step 2: Gather All Your Containers in One Place 

In the course we've built the following containers over the weeks: 

1. Apache (we'll use this for serving static files)
1. DNS 
1. HelloApp (the simple app server we created)

Let's put them into a single directory structure so we can build them as a group. The directory should look like this: 

```
$ tree 
.
├── Apache
│   └── html
│       └── index.html
├── DNS
│   ├── db.mike.cis.cabrillo.edu
│   ├── db.mike-ipv4
│   ├── db.mike-ipv6
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── named.conf
├── HelloService
│   ├── Dockerfile
│   └── hello.py
```

We'll add more containers to this tree in future steps. 

## Step 3: Create a `docker-compose.yaml` File 

Docker compose works like Docker, it wants a description file in a directory. For compose that's a file called `docker-compose.yaml`. Let's start with a version that shows the awesome power of Docker compose. This file comes from the excellent [sample apps](https://docs.docker.com/compose/samples-for-compose/) on Docker's website. 

```yaml
version: '3.3'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: somewordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
       WORDPRESS_DB_NAME: wordpress
volumes:
    db_data: {}
```

Source: [Quickstart: Compose and Wordpress](https://docs.docker.com/compose/wordpress/)

## Step 4: Test it!

Now let's run our application: 

```
$ docker-compose up 
```

If everything worked your application will be running on `localhost`. 

> [http://localhost:8000](http://localhost:8000) 

## Step 5: Add DNS

Now let's add instructions for our DNS server: 

```yaml
  dns:
    build: DNS   
    restart: always 
    ports:
      - "53000:53/udp"
```

This will build the `Dockerfile` in the `DNS` directory. 

```
$ docker-compose build 
$ docker-compose up 
``` 

## Step 6: Add an Apache Server for Files 

We want to be able to serve files with a plain, fast Apache server. We want the files to be easily accessible from the host so we'll specify a volume that's a host path. Add the following to your services: 

```yaml 
  static: 
    image: httpd:2
    volumes:
      - htdocs:/usr/local/apache2/htdocs
```

Now add this to your volumes: 

```yaml
    htdocs: 
      driver: local
      driver_opts:
        o: bind
        type: none
        device: /var/www/html
```

## Step 7: Create our Hello Application 

Let's add a Python application to our site. We'll reuse the Hello app from a few weeks ago. Add the following to your services: 

```yaml
  hello:
    build: HelloService 
```

That will build and run our HelloService container. 

## Step 6: Add a Proxy Server 

Finally, it's time to glue all of our services together. We want them to all be accessible from a single host. We'll use a front-end load balancer and proxy to enable access to different parts of our application. The [Caddy](https://caddyserver.com/) web server is fast, easy, efficient and made for containerization. Create a directory called `Proxy` and put two file in it `Dockerfile` and `Caddyfile`. 

### Step 6.1: Dockerfile 

```Dockerfile 
FROM caddy:2
COPY Caddyfile /etc/caddy/Caddyfile
```

### Step 6.2: Caddyfile 

``` 
# The name of your host:
#  Use localhost for testing 
#  Replace this with your real host when you're ready to deploy
localhost

# URL patter to access our Hello app
route /hello/* {
	uri strip_prefix /hello
    reverse_proxy hello:5000
} 

# URL patter to access our static files
route /static/* {
	uri strip_prefix /static
    reverse_proxy static:80
} 

# Default URL pattern goes to Wordpress
reverse_proxy * wordpress:80
```

## Step 6.3: Add the Proxy 

Now let's add the proxy service to our `docker-compose.yaml` file. 

```yaml
  proxy:
    build: Proxy 
    depends_on:
      - dns 
      - wordpress
      - hello
      - static
    restart: always
    ports:
      - "8000:80"
      - "8443:443"
```

Caddy enable SSL by default so we must expose 80 and 443. The dependencies say that we should not start the proxy server until all of the other services are ready. 

## Step 7: Test the Stack

Now let's test the full stack. 

```
$ docker-compose build
$ docker-compose up 
``` 

If it works the following URL will be available: 

1. Wordpress: [https://localhost:8443/](https://localhost:8443/)
1. HelloApp: [https://localhost:8443/hello](https://localhost:8443/hello)
1. Files in `/var/www`: [https://localhost:8443/static](https://localhost:8443/static)

## Step 8: Go to Production 

Moving the stack to your AWS machine takes a few tweaks. Do the following: 

1. Change port numbers in `docker-compose.yaml` to be production ports:
  1. 8000 -> 80 
  1. 8443 -> 443 
  1. 53000 -> 53/udp
1. Change the passwords for the MySQL root user and the wordpress user. 
1. Replace `localhost` in `Caddyfile` with the name of your server. 

The last step is important if you want a real certificate issued to you by Let's Encrypt. 

