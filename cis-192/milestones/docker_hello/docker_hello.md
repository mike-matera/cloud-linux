# Milestone: Deploy a Docker Container 

To reach this milestone you will create a container on your local machine and deploy it to AWS. This is the typical workflow with Docker and, though at first it seems complicated, it's the standard process for all modern network services because it's so powerful. With practice you'll come to understand this process. 

## Introduction 

Start by completing the labs from this week. For the milestone you will repeat the procedure with customized HTML. You must also give your built container a version number in the *tag*. If you leave the tag as `test1` you will have problems because docker won't pull the new image, thinking it's the same version. 

## Custom HTML 

Your custom HTML doesn't need to be fancy, but it should contain the name of your custom domain (the *.cis.cabrillo.edu domain). 

## Version Tagging 

Your container should be tagged with a version number. For this milestone use date-based versions as shown in the example: 

| Year | Month | Day | Version | 
| --- | --- | --- | --- | 
| 2020 | 10 | 08 | 01 | 

So the first version you create on a particular day will be tageed like: 

```
myhtml:2020100801 
```

If you create a second version on the same day it would be: 

```
myhtml:2020100802
```

And so on. 

## Turn In 

Turn in the following: 

1. The name and tag of your container so I can `docker run` it myself. 
1. A screenshot of your container running on AWS
