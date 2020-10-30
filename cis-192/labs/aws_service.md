# Create an AWS VPC and Instance 

This lab guides you through the process of creating a VPC and an instance in the VPC with access to the Internet. This is roughly what the CloudFormation stack you used in the first week of class did to create your AWS VM. The purpose of the lab is to give you a better understanding of this fundamental AWS task. 

> ![](/static/icon_warning_small.png) **This Lab Costs Money!**
>
> The instance you create in this lab will incur charges. Do not forget to delete it when you're done. Failing to do so may cause you to run out of credit before the semester ends. 

*To watch the step-by-step instructions watch the class lecture.* 

## Step 1: Create a VPC 

The VPC should have the properties: 

- Name tag: `cis-192-test`
- IPv4 CIDR block: `10.0.0.0/16`
- No IPv6 CIDR block (this makes for fewer steps)

Creating a VPC automatically creates a DHCP options set (so hosts get correct information), a routing table, Security Group and a Network ACL. Examine the VPC details and navigate to the created resources. 

## Step 2: Add Subnets 

Now create two subnets in different availability zones. Give the subnets the following IP address information:

- Subnet 1
  - Name tag: `cis-192-test-sub1`
  - VPC: Pick the `cis-192-test` VPC from the pulldown 
  - AZ: Choose one 
  - IPv4 CIDR block: `10.0.1.0/24`
- Subnet 2
  - Name tag: `cis-192-test-sub2`
  - VPC: Pick the `cis-192-test` VPC from the pulldown 
  - AZ: Choose one 
  - IPv4 CIDR block: `10.0.2.0/24`

Examine the subnets. They have been automatically added to the Route Table and the Network ACL from the VPC has been assigned. 

## Step 3: Enable DHCP on Subnets 

On each of the subnets select Actions -> Modify auto-assign IP settings. Check "Auto-assign IPv4 and save. 

## Step 4: Create and Attach a Gateway 

We want to be able to communicate with the Internet. AWS has several options for gateways, we'll use an "Internet Gateway" which enables bidirectional communication with the Internet. Create your internet gateway with the following information:

- Name tag: `cis-192-test-gw` 

Once your gateway is created attach it to your VPC. 

## Step 5: Add Routes 

Navigate to your routing table under "Subnet Assocations" and select "Edit subnet associations". Select both subnets. 

## Step 6: Add a Default Route 

Navigate to your routing table and add the new gateway as the default route. Rename your routing table to `cis-192-test-rtb`. Select "Edit Routes" and add the following route:

- Route: `0.0.0.0/0` (default)
- Target: Pulldown and select "Internet Gateways" your gateway should appear in a list. 

Congratulations your network is ready to use!

## Step 7: Create an Instance 

Navigate to the EC2 screen and create a new instance with the following properties: 

- AMI: Ubuntu Server 20.04 LTS (HVM), SSD Volume Type 
- Instance Type: `t2.micro`
- Network: Pick your VPC 
- Subnet: Choose one of your subnets (it doesn't matter which one)
- Add Tags
  - Name: `cis-192-test-vm` 
- Security Group:
  - Select an **existing** security group
  - `default` "default VPC security group"

When you attempt to launch the instance you'll be prompted for a key pair. Use the `cis192` key pair so you can login. 

## Step 8: Update Security Group 

The default SG is locked down (as it should be). After you create your instance navigate to the attached security group. Select "Edit inbound rules" and add the following rule: 

- Type: `All traffic` 
- Source type: `Anywhere` 
- Description: `cis-192-test: wide open` 

Save the rule and you will have access to your VM. 

## Step 9: Log In!

You should now be able to use SSH to login to your new VM! Remember you have to use the key pair that you use for your existing AWS vm. 

Now it's time to tear it all down which is *not quite* as complicated as building it up. 

> Take a screenshot!

## Step 10: Terminate the Instance 

Terminating the instance will stop it and after a while remove it from view. 

## Step 11: Delete the VPC 

Deleting the VPC will remove the internet gateway, subnets, routing tables and security group. 

## Turn In 

Submit a screenshot of your instance prompt. 












