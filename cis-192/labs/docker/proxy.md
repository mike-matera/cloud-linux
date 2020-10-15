# Use Nginx as a Proxy 

In this lab you'll combine Nginx and your Hello application into a single service. 

## Step 1: Create a Directory for you Nginx Container 

Start in a fresh directory: 

```
$ mkdir Nginx 
$ cd Nginx 
``` 

## Step 1: Get the Default Configuration 

We're going to customize the configuration of Nginx. It's best to start with working so let's get the default configuration out of the Nginx container. Run the default container:

```bash
 $ docker run -it --rm nginx:stable /bin/bash
```

The default configuration is in `/etc/nginx/conf.d/default.conf`. Let's look at it:

```
$ cat /etc/nginx/conf.d/default.conf 
``` 

Copy and paste the contents into a file called `default.conf` in your `Nginx` directory. 

## Step 2: Customize the Configuration 

Add the following stanza to the configuration inside of the `server` declaration: 

```
location /app/ {
    proxy_pass http://helloapp:5000/;
}
```

## Step 2: Build the Container

Now create a `Dockerfile` with instructions to customize the configuration: 

```Dockerfile 
FROM nginx:stable
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Build your container using `docker build`:

```
$ docker build -t proxy:test1 .
```

## Step 3: Create a Docker Network 

Your two containers must talk to each other. You need to put them on their own network if you want to do that: 

```
$ docker network create cis-192
```

Check to make sure it worked: 

```
$ docker network ls 
```

## Step 4: Launch Your Application Server 

Now launch your custom application: 

```
$ docker run -it --rm --name=helloapp --network=cis-192 myapp:test1
```

You should see it's output.

## Step 5: Launch Your Web Proxy 

Now launch Nginx:

```
docker run -it --rm --name proxy --network cis-192 -p 8080:80 proxy:test1
```

You should see the output of Nginx. If everything worked you can now browse here to see the HTML:

> [http://localhost:8080/](http://localhost:8080/)

And here to see your application: 

> [http://localhost:8080/app/](http://localhost:8080/app/)

**Take a screenshot of both pages**

## Turn In 

Turn in your screenshots on Canvas.
