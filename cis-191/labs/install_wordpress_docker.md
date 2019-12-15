# Lab: Install Wordpress using Docker 

In this lab you will install the Wordpress blog software using Docker Compose. Docker Compose is a tool for building applications that contain multiple linked containers. It allows you to build complex applications easily. 

This lab expects that you're using the vagrant box that was built in the [Using a Vagrant Configuration Script](vagrant_configuration_script.md) lab. 

## Step 1: Create a Directory for Your Application 

Docker Compose works just like Vagrant. You put a configuration file into a directory and run the configuration from that directory. On your VM create a directory for the application: 

```bash
$ mkdir ~/wordpress
$ cd ~/wordpress
```

## Step 2: Specify the Application 

Docker Compose is configured with a YAML file. Copy and paste the following code into a file called `docker-compose.yaml` in the `~/wordpress` directory: 

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

The YAML file specifies an application with two containers, `wordpress` which uses Apache and PHP and `mysql` which is a database that Wordpress needs to store data. 

## Step 3: Build your Application

With your application defined all you need to do is `up` it: 

```bash
$ docker-compose up
```
The containers will be built and run. You will see the container output on the command line. 

## Step 4: Configure Wordpress

Once the containers are started you can access your new Wordpress application from your browser from the link:

> [http://localhost:8080](http://localhost:8080)

## Turn In

Turn in a screenshot of Wordpress (it's okay to use the configuration screen). 
