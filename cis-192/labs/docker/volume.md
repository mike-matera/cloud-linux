# Customize a Container with Volume Mounts 

In this lab you will build an alternative to customizing Nginx by embedding an HTML page using volume mounts. The volume mount will share Nginx's HTML directory with your host. You should have completed the labs from the previous class before you start this one. 

## Step 1: Make an HTML Directory 

Start in the directory you used last week. You should have an `index.html` file there. Create a directory called `html` and move your `index.html` into it. 

## Step 2: Launch the Nginx Container 

Start the container on your local machine with the command:

```
$ docker run -it --rm -p 8080:80 -v $(pwd)/html:/usr/share/nginx/html nginx:stable
```

Notice the `-v` option. It works like this: 

| Option | Host Path | Container Path |  
| --- | --- | --- | 
| `-v $(pwd)/html:/usr/share/nginx/` | `$(pwd)/html` | `/usr/share/nginx/` | 

Now browse to your page: 

> [http://localhost:8080/](http://localhost:8080/)

## Step 3: Edit `index.html` 

Now use your favorite editor to edit `html/index.html`. Make any change you like. Save the file and reload the browser. You should see the change immediately. 

**Take a screenshot** 

## Turn In 

A screenshot of your changed HTML. 
