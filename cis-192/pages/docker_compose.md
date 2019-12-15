# Docker Compose 

In this lesson you'll create a simple web application from scratch and "containerize" it. Last week you used a Dockerfile to create a container instance. Your container ran a single, simple web application. Most web applications, however, require you to have multiple different services. In the Docker world each services belongs in its own container. Docker Compose is an easy way to specify multiple, interlinked, containers and start them all at once. Docker Compose makes it possible to bundle an entire web application into a single file describing how to build the application.

## Further Reading 

  - [Overview of Docker Compose](https://docs.docker.com/compose/)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)
  - [Get Started with WordPress](https://docs.docker.com/compose/wordpress/)
  - [Compose File Reference](https://docs.docker.com/compose/compose-file/)
  
## Installation 

Docker Compose is still very new. To install it you should get the latest version from GitHub and place it in `/usr/local/bin`:

```
app$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
app$ sudo chmod +x /usr/local/bin/docker-compose
```

If done correctly you should be able to run the `docker-compose` command. Test what version you have: 

```
app$ docker-compose --version
docker-compose version 1.24.1, build 4667896b
```

## Composing a Cluster 

Compose uses a YAML file to describe your application. Start by creating a directory for your composed application:

```
app$ mkdir ~/Wordpress
app$ cd ~/Wordpress
```

Now create a file called `docker-compose.yaml` in that directory and paste the following contents into it:

```
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
       - "80:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
       WORDPRESS_DB_NAME: wordpress
volumes:
    db_data: {}
```

Save the file and run the following command.

```
app$ docker-compose up
```

Wait for the downloads to complete and you now have a Wordpress blog.
