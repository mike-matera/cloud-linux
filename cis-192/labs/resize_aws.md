# Resize Your AWS VM 

Have you ever installed more memory or a new processor into your computer? You can do it to a VM too! This lab will take you through the process of upgrading your VM to have more memory. 

## Understanding EC2 Pricing 

The price you pay for a VM depends on the resources you use. There are thousands of billable resources in AWS but the *on demand* VMs we're using for class have three important billable resources:

| Resource | Unit of Measure | 
| --- | --- | 
| CPU Count | per Hour | 
| Main Memory (RAM) | per Hour | 
| Disk Space | per GB per Month | 
| Network Transfer | per GB per Month | 
| Non-Free OS Charges | per Hour | 

AWS pricing varies per region. In regions where data center space is mor expensive or more limited AWS costs more. This is how Amazon provides financial incentives to move customers to the cheapest locations. AWS Educate only operates in the N. Virginia region. 

### Instance Types

CPU count and RAM aren't selected independently. AWS lets you create a VM using a machine type. AWS machine types have pre-selected CPU and RAM resources. So far we've used the `t2.nano` machine type, today we'll switch to `t2.micro`, one size up. 

### Disk Types 

There are a number of disk types available in AWS. Our VMs use Elastic Block Store (EBS) disks, which are the most flexible. EBS disks are charged per GB per month. EBS is *shared* so any VM in the same region can use the EBS volume (although only one can use it at a time). You can also add a fast in-machine SSD to a VM for private storage. That's expensive but great if you need a fast disk!

### Latest Price List 

You can see the latest prices here: 

> **AWS On Demand Instance Pricing**
>
> [https://aws.amazon.com/ec2/pricing/on-demand/](https://aws.amazon.com/ec2/pricing/on-demand/)

Use the price list to answer some questions:

1. How much does it cost per month to run Linux on a `t2.micro` with a 64 GB disk? *Estimate assuming months are 30 days.*
1. If you switch to a `t2.micro` today how much will it cost to run until December 15th?
1. What is the difference in price between Windows and Linux? 

## Step 1: Shutdown Your Instance 

Instance types can only be changed while the instance is off. From the AWS navigate to EC2 -> Instances and select your instance. Stop your instance by selecting Actions -> Instance State -> Stop Instance. **Do not terminate it.** Terminate means "delete" and a VM that's terminated cannot be revived. 

## Step 2: Change Instance Type 

Now change your instance type by selecting Actions -> Instance Settings -> Change Instance Type. You will be presented with a list of instance types to select. Change the type to `t2.micro`. 

## Step 3: Restart Your Instance 

Once your instance has been changed to `t2.micro` restart yur instance. 

## Step 4: Verify the Change 

After your instance starts login using SSH and verify the available memory using the `top` command. Take a screenshot of `top` that shows you have about 1GB of memory. 

## Turn In 

1. Answers to the questions
1. Your screenshot 

