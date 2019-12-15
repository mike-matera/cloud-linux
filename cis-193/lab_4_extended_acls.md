In this lab you will use extended ACLs and their related tools
IntroductionFor this lab you will implement a file access model on your Ubuntu VMs. The model is based on individual and group membership in a company.
Create the Users and GroupsBefore you begin you will need to create users and groups. In the lab you will assign access to files and directories to them. Start by creating the following users. Each user should have a private group (this is the default):
Users:
  - Bob (UID 2000)
  - Monica(UID 2001)
  - Sally(UID 2002)
  - Jeff(UID 2003)
  - Mike(UID 2004)
  - Fred(UID 2005)
  - Ethan(UID 2006)

Now create the following groups with the following members:
  - Engineering(GID 3000): Bob, Monica and Sally
  - Sales(GID 3001): Jeff, Mike, Fred
  - IT(GID 3002): - Ethan

Download the Directory TreeNow that you have users and groups created, download [this tar file](http://ea994bd4-a-9f1c7e1e-s-sites.googlegroups.com/a/lifealgorithmic.com/cabrillo-home/home/cis-193/lab-4-extended-acls/lab4_directory_tree.tar.gz?attachauth=ANoY7crPrcIG6Uk0UfjQXmAihYK4uy3sNnd6M8AV6DdfWaAK0E_c_Q7ErFox8RorxqIgdLcz7zBNXuaS4nh1jaU8pqTyHP1hLbs44F8yMNULuuBf4f0J8LtAL5PsVqYuHc6rAEkkXbKREcO9mOChJR4qtfMoVXw8xALNaMzCLmd5Eop9H2yhFYl4UPqwAuNT67_mlLnN8QP1ylfwJpqU6htaQn5Uzds7mlb0IdBvx1UMKAfl8tjoguNA2rtLc8MVH5Sk8PX42qjh4RklaYngMCrq9jjyP6pV_HXFqUFdUiN97ceYkJvMNrg%3D&attredirects=0&d=1) onto your VM. The tar file contains the following directory tree:
lab4
âââ Engineering
â  âââ Designs
â  â  âââ productA
â  â  âââ productB
â  â  âââ productC
â  âââ Specs
â    âââ productA
â    âââ productB
â    âââ productC
âââ Sales
  âââ DesignReviews
  â  âââ productA
  â  âââ productB
  â  âââ productC
  âââ Prices
    âââ productA
    âââ productB
    âââ productC

When you have extracted the TAR file be sure to change the group of all the files in "Engineering" to the engineering group and all of the file in "Sales" to the sales group.
Set ACLsThe Engineering directory has the following rules:
  - Other permissions MUST be off (no read, no write, no execute) on all files and directories
  - All files should be in the engineering group
  - Files in the Designs directory should only be readable to people in engineering
  - Designs/productA is owned by Bob
  - Designs/productB is owned by Monica
  - Designs/productC is owned by Sally
  - Files in the Specs directory should be writable to Engineering and readable to Sales
  - Ethan should have full access to everything

The Sales directory has the following rules:
  - Other permissions MUST be off (no read, no write, no execute) on all files and directories
  - All files should be in the sales group
  - Files in the Prices directory should only be readable to people in sales
  - Files in the DesignReviews directory should be writable to Sales and readable to Engineering
  - Ethan should have full access to everything EXCEPT Prices

Turn InWhen you have completed setting the permissions on your folder use the TAR command to re-zip them into a single file. Remember: The TAR command needs a special argument to save your ACLs. Be sure to test that the ACLs are saved.

  - The TAR file that contains your completed permissions structure

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for a TAR file with ACLs
  * 10 points for correctness

