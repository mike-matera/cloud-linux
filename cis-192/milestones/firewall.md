# Enable the Firewall 

To complete the milestone you will have to create firewall rules for your VM. You can do it one of two ways: 

1. By modifying the security group in AWS 
1. Using UFW on Linux 

## Allowable Traffic 

Put a firewall on your VM that only allows two things: 

1. SSH 
1. HTTP 

## Alternative 1: AWS 

Add rules to the Security Group created for your AWS vm and take a screenshot. 

## Alternative 2: UFW

> BE CAREFUL! 

Use the following guide to see how to use UFW: 

https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands


## Turn In

Take a screenshot of your security group or the output of running:

```
$ ufw status
``` 

