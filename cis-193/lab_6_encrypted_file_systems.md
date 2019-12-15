In this lab you will encrypt a filesystem image.
IntroductionIn this lab you will encrypt a filesystem image in a file. You could use this procedure to create a hidden stash for highly sensitive files. With slight modifications you could use this procedure to create an encrypted flash key. Flash keys encrypted with LUKS will be automatically recognized by Linux when they're plugged in. It's a very good way to keep your data private in the face of loss or theft.
Create Your Filesystem ImageIn this part you'll create a 50MB file that will look to Linux just as if it's a 50MB disk. You do that using a loopback device.
# Create the file:dd if=/dev/zero of=crypt.img bs=1M count=50# Bind the loopback device to the filelosetup /dev/loop0 crypt.img
The block device /dev/loop0 is now ready to use.
Create the Encrypted VolumeNow you must create the LUKS volume on /dev/loop0. Once you have the volume created format it with the Microsoft 'vfat' filesystem. The general procedure is:
  - Create the LUKS volume
  - Open the LUKS volume
  - Format the disk
  - Mount the disk
  - Create a file in the encrypted volume

Your LUKS volume should use two keys. One key is based on a password of your choice, the other key is so that I can open your volume with the password of "lefty". Once you have an encrypted volume with a file in it unmount and close it. You can unbind the loop device with the command:
losetup -d /dev/loop0
Turn InYou will be turning in your encrypted volume for me to look at. You must BZIP2 the image file first. Otherwise it is too big for blackboard. Gzip your file with the following command:
bzip2 crypt.img# The file is now crypt.img.bz2
Submit your file on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for a volume with two keys (one of them my password)
  * 10 points for a vfat system with a file

