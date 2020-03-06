# Launch an EC2 VM From the Command Line 

This lab will take you through how to launch an ec2 VM in AWS from the command line. 

## Before You Begin 

Before you begin you must have your AWS CLI connected using your access key. 

 - Follow the instructions in the [AWS CLI Lab](aws_cli.md)

You must also have your SSH keypair downloaded. We did that in class last week. If you don't have your keypair instructions at the link below: 

  - Documentation for [Amazon EC2 Keypairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

## Instructions 

Amazon has complete instructions for this process on their site: 

  - [Launching, Listing, and Terminating Amazon EC2 Instances](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-instances.html)

There are missing parts in the lab that you will need to fill in. Here are the values: 

  - The AMI for Ubuntu is `ami-07ebfd5b3428b6f4d`
  - You have to find the ID of your default security group:
	```
	$ aws ec2 describe-security-groups --group-names default 
	```
	Look for the `GroupId` key in the output. 
  - The name of your keypair. You can find it with: 
    ```
	$ aws ec2 describe-key-pairs
	```
  - You **don't** need a subnet ID. Leave that option off. 
  
