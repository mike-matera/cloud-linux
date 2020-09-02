# Make Your Own Opus  

In this lab you'll use Vagrant to create your own version of Opus running on your computer. You will have full root authority on your own opus. 

> **Note:** Your own opus is new this year. There might be bugs! 

## Step 1: Download the Files 

I've created a `Vagrantfile` and an Ansible Playbook for this class. Together they create a mini-opus just for you. The `Vagrantfile` is a standard Ubuntu 18.04 Server VM. Download the two files using the links below:

```eval_rst
:Download: 
  | :download:`Vagrantfile <../../boxes/bionic64-nodisks/Vagrantfile>`
  | :download:`playbook.yaml  <../../boxes/bionic64-nodisks/playbook.yaml>`
```

Create a new folder on your computer and put the two files into it. They should be the only files in the folder.

## Step 2: Get a Shell 

This step is OS dependent. On Mac and Linux start a Terminal. On Windows start Powershell. 

  - **MacOS:** Applications -> Utilities -> Terminal 
  - **Windows:** Click Start, type PowerShell, and then click Windows PowerShell.
  - **Linux:** Press `Ctrl-Alt-T`

Use the `cd` command to change into the folder you created in the previous step. 

## Step 3: Use Vagrant to Bring Up your VM

In the folder you created execute the command:

```
$ vagrant up 
``` 

The `vagrant up` command will download the image of the VM. This could take a long time on slow connections. 

## Step 4: SSH Into your Vagrant VM

Vagrant gives you an easy way to SSH into a VM. Once you have used `vagrant up` you can simply run the `vagrant ssh` command to connect. 

```
$ vagrant ssh 
```

That will connect you. To get your host prompt back simply exit. 

```bash
exit 
```

## Step 5: View your VM in VirtualBox 

Vagrant drives VirtualBox. The VirtualBox application doesn't have to be open for Vagrant to work. Open VirtualBox and you'll see that your new Ubuntu VM has been added. Open the VM and login.

> Tip: The username is "vagrant" and the password is "vagrant" on all Vagrant VMs.

**Take a screenshot of you logged into your new VM**

## Step 6: (Optional) Remove the VM

You can shutdown your VM from VirtualBox. You can also shut it down using the command:

```
$ vagrant halt
```

You can also remove your VM and all of its disks with the command:

```
$ vagrant destroy -f
```

When you destroy a VM the download that was done by `vagrant up` is still cached, so the next time you do a `vagrant up` it will be much quicker. 

## Turn In 

  1. The screenshot from Step 5
  