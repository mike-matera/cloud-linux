# Deploy CTFd with Docker 

This lab will show you how to build a multi-container application using [Docker Compose](https://docs.docker.com/compose/). Last week we built a simple web application using Docker and a `Dockerfile`. Useful web applications need more than one container. [CTFd](https://ctfd.io/) is a web-based capture the flag game. In order to run CTFd requires an application server written in Python, [MariaDB](https://mariadb.org/) to store data and [Redis](https://redis.io/) to perform caching. The lab will show you how to how to use Docker Compose to build a multi-container system. 

## Prerequisites 

You should have Docker installed on your Vagrant VM. 

## Step 1: Install Docker Compose 

Follow the [Install Docker Compose](https://docs.docker.com/compose/install/) instructions. If successful you should be able to run `docker-compose` from the command line. 

```
$ docker-compose --version
docker-compose version 1.25.5, build 8a1c60f6
```

## Step 2: Get the CTFd Source from GitHub

The source code for CTFd is on [GitHub](https://github.com/CTFd/CTFd). You can clone the repository with the following command: 

```
$ git clone https://github.com/CTFd/CTFd.git
```

The authors of the project have different ways to test the code in a development environment. Look inside the `CTFd` directory and you will see a `Vagrantfile` a `Dockerfile` and a `docker-compose.yml` file. 

## Step 3: Change the Service Port 

Change the contents of `docker-compose.yml` so that the service starts on port `80` of your Vagrant VM. This will give you access to it via your local browser. Change the ports definition to look like the snippet below:

```yaml 
    ports:
      - "80:8000"
```

## Step 4: Bring up the System

Use the `docker-compose` command to bring up the network of containers. 

```
$ docker-compose up 
```

The first run of `docker-compose` will build the CTFd container from the `Dockerfile`. This will take a few moments. Once the containers are built the application will run in the foreground. Hitting `Ctrl-C` will stop CTFd from running. Passing the `-d` option will run the application in the background. 

## Step 5: Visit your CTF 

With everything built you should be able to direct your browser to this link and see the application: 

> [http://localhost:8080/](http://localhost:8080/) 

## Turn In 

Turn in a screenshot of CTFd running. 


