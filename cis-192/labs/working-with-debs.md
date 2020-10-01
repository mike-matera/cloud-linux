# Working with DEB Packages 

In this lab you'll install a deb package on your AWS machine. 

## Step 1: Download the Package 

You can see a list of all of the repository versions of the `tree` command at this URL:

> [http://us-east-1.ec2.archive.ubuntu.com/ubuntu/pool/universe/t/tree/](http://us-east-1.ec2.archive.ubuntu.com/ubuntu/pool/universe/t/tree/)

Note the different versions and architectures available. The version that matches Ubuntu Bionic is 1.8.0. Download the 64-bit version with wget: 

```
$ wget http://us-east-1.ec2.archive.ubuntu.com/ubuntu/pool/universe/t/tree/tree_1.8.0-1_amd64.deb
```

You should see the deb file in the current directory. 

## Step 2: Examine the Package Contents 

The package contains all of the binary files that will be installed. You can extract them without installing them using the `dpkg` command. 

```
$ mkdir temp
$ dpkg -x tree_1.8.0-1_amd64.deb temp/
```

Now examine the contents of `temp/`. Can you find the executable? What other files are present? 

## Step 3: Examine the Package Information 

The package has *metadata* that lists the dependencies and maintainer. Use the `dpkg` command to list the metadata:

```
$ dpkg --info tree_1.8.0-1_amd64.deb 
```

Who is the maintainer? How big is the package once installed? What packages does it depend on? 

## Step 4: Install the Package 

Now install the package. This package has all of it's dependencies installed already so there will be no problem:

```
$ sudo dpkg -i tree_1.8.0-1_amd64.deb 
```

> Note you have to be root!

What do you think would happen if dependencies were missing? 

## Step 5: Unintall the Package (Optional)

You can get rid of a package just as easily as installing it: 

```
$ dpkg -r tree 
```

> Note: Removal uses the *package name* not the package file. 

## Turn In

Turn in answers to the questions in the lab. 




