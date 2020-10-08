# Deploy a Custom Service 

In this lab you will deploy the service you built in the previous lab to Dockerhub. Once there you will launch it on your AWS VM. 

## Step 1: Tag and Push 

When you have a container image that you want on Dockerhub you have to tag it using your Dockerhub username. The docker tag command does this. 

```
$ docker tag myweb:test1 [your-username-here]/myweb:test1
```

You should see your tagged image in the list:

```
$ docker image ls 
```

You can now push the image to Dockerhub: 

```
$ docker push [your-username-here]/myweb:test1
```

Browse to Dockerhub and verify that the image is present. **Take a screenshot**. 

## Step 2: Launch on AWS 

Now you're ready to launch your custom container on AWS. You should already have Docker installed on your AWS VM. Login to that VM and launch your `myweb` container: 

```
docker run -it --rm -p 80:80 [your-username-here]/myweb:test1
```

Now browse to your AWS IP address and look for the hello world message. **Take a screenshot of the message.** The `-it` and `--rm` options make the container run in the foreground. When you hit CTRL-C the container will be automatically deleted (which saves a step). 

## Turn In 

Turn in the screenshot of your Dockerhub repo and your deployed container. 
