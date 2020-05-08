# Lab: Build a Containerized Application

In this lab you'll see how to use a Dockerfile to create a custom container using the `docker build` command. 

This lab expects that you're using the vagrant box with Docker installed. You should have created your application in the [Create a Web Application](web_application.md) lab. 

## Step 1: Create a `Dockerfile`

Like with `Vagrantfile` a `Dockerfile` lives in its own directory. You will add the `Dockerfile` to the `~/MyApp` directory alongside the `app.py` file. Copy and paste the follwing into `Dockerfile`:

```Dockerfile
FROM ubuntu:latest
MAINTAINER You "you@you.cis.cabrillo.edu"
RUN apt-get update && apt-get install -y python3-pip iproute2
RUN pip3 install Flask
COPY app.py /
WORKDIR /
ENTRYPOINT ["python3"]
CMD ["app.py"]
```

## Step 2: Build Your Container 

The `docker build` command builds a container image from a `Dockerfile`. 

```bash 
$ docker build -t myapp:latest .
```

This will pull the base layers and run the commands in the recipe. When it's done you will be able to deploy your application in a container!

## Step 3: Deploy Your Container 

With your container layers built you can execute your container with `docker run`:

```bash
$ docker run -p 80:80 myapp 
```

## Step 4: View Your Application 

You application is running, you can see it on the same URL as before: 

> [http://localhost:8080](http://localhost:8080)

## Turn In 

Turn in a screenshot of your browser. 
