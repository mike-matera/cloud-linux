# Docker Volumes 

So far the containers we've created have been self contained and haven't had a way to permanently store data. In this lecture you'll learn how Docker uses *volumes* to store precious data so that it survives after a container is deleted. Precious data could be database files containing registered users and their posts, or the HTML of your website. There are lots of different ways to connect a volume to a container. This lecture will show you how to use a directory on your app server to hold volume data. 

## A Container with No Volumes 

In a previous lecture we created an Apache container with no volumes like this: 

```
app$ docker run --rm -p 80:80 --name apache httpd
```

Run this command again and notice that when you visit your URL you see the "It Works!" page. **You may have to stop your containers from last week.**. Where does the It Works come from? The [official image documentation](https://hub.docker.com/_/httpd) tells us that data for Apache is in the `/usr/local/apache2/htdocs` directory. Let's verify that by running `ls` in the container. 

```
app$ docker exec -it apache ls -la /usr/local/apache2/htdocs 
total 12
drwxr-xr-x 2 root     root     4096 Oct 30 23:33 .
drwxr-xr-x 1 www-data www-data 4096 Oct 30 23:33 ..
-rw-r--r-- 1 root     src        45 Jun 11  2007 index.html
```

We can also see the HTML if we like: 

```
$ docker exec -it apache cat /usr/local/apache2/htdocs/index.html
<html><body><h1>It works!</h1></body></html>
```

If we make changes the changes are reflected in the top-level, writable layer of the container. But that layer only lives as long as the container. If we stop and start the container again, or launch a replica the changes will be lost. So how do we make custom HTML?

## Adding a Volume 

Adding a volume to the container shared a directory on the host with the container. Directories on the host are not deleted when the container stops so they're perfect for storing HTML and other data that we want to keep. Start by creating a data directory on your app server: 

```
app$ mkdir ~/VolumeData
```

Now create an `index.html` file inside of `~/VolumeData` that has the following contents:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>My CIS-192 Project</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</head>
<body>

<div class="jumbotron text-center">
  <h1>This is my CIS-192 Project</h1>
  <p>This HTML is located in a volume.</p> 
</div>

<div class="container">
  <div class="row">
    <div class="col-sm-4">
      <h3>Column 1</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
    <div class="col-sm-4">
      <h3>Column 2</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
    <div class="col-sm-4">
      <h3>Column 3</h3>        
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
  </div>
</div>

</body>
</html>
```

Now you just need to redirect the `/usr/local/apache2/htdocs` directory in the container to `/home/student/VolumeData` in your VM. You can easily do that with `docker run` using the `-v` option. Execute the following command:

```
app$ docker run --rm -p 80:80 -v /home/student/VolumeData:/usr/local/apache2/htdocs --name apache httpd
```

Now visit your page to ensure you're serving the right data. Changes to your HTML are reflected immediately. Try changing the HTML and reloading the page.


