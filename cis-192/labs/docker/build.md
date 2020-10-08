# Build and Manage a Custom Container 

This lab will take you through the process of building and customizing an Nginx container on your local machine. This is an important first step to deploying a container. 

## Step 1: Run the Base Container 

The official nginx container is lightweight and comes with a default webpage. The following command runs the container in the background (`-d`), connecting container port 80 to host port 8080 (`-p 8080:80`) and with the name `my_nginx` (`--name`):

```
$ docker run -p 8080:80 --name=my_nginx -d nginx:stable 
```

Verify that the container is running:

```
$ docker ps 
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
acb90cccb559        nginx:stable        "/docker-entrypoint.…"   3 seconds ago       Up 2 seconds        0.0.0.0:8080->80/tcp   my_nginx
```

Make sure you are forwarding to the correct port. If all looks well you should be able to see nginx's default page on the following URL:

> [http://localhost:8080](http://localhost:8080)

If you can see the page you're ready to move on. You won't need the nginx container anymore so stop it and delete it: 

```
$ docker stop my_nginx 
$ docker rm my_nginx
```

## Step 2: Build a Custom Container 

Now we'll use a `Dockerfile` to customize the HTML in the container. In a directory by itself create a `Dockerfile` with the following contents:

```Dockerfile 
FROM nginx:stable 
COPY index.html /usr/share/nginx/html/index.html
```

Now create an `index.html` file in the same directory with a simple message. 

```html
<html>
<h1>Hello CIS-192 World!</h1>
</html>
```

With those two files in place build the custom container:

```
$ docker build -t myweb:test1 . 
```

You should now have a custom image built. Verify that you do with the command: 

```
$ docker image ls 
REPOSITORY                       TAG                 IMAGE ID            CREATED              SIZE
myweb                            test1               e266f5ae5b64        About a minute ago   133MB
nginx                            stable              20ade3ba43bf        2 days ago           133MB
docker/whalesay                  latest              6b362a9f73eb        5 years ago          247MB
```

## Step 3: Launch Your Image 

You can now create a container based on your image the same way you launched the base nginx image: 

```
$ docker run -p 8080:80 --name=my_nginx -d myweb:test1 
```

Verify that your image is running by browsing to:

> [http://localhost:8080](http://localhost:8080)

**Take a screenshot** 

## Turn In 

Turn in a screenshot of your custom container running. 
