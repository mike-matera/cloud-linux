# Backup Your Wiki Using TAR 

In this lab you'll use `tar` to backup the configuration and contents of the wiki you created in the [Install Dokuwiki](dokuwiki_install.md) lab. 

## Background 

Dokuwiki is contained entirely in the `/var/www/html/dokuwiki` directory. There are two places where changes are kept:

  1. `config/` - The configuration that you created in the setup step is here. 
  2. `data/` - The pages you create are stored in this directory. 

In most cases it's probably a good idea to back up the entire Dokuwiki installation but in this lab we'll just backup the site data. 

## Step 1: Use TAR

You should start from the `/var/www/html/dokuwiki` directory.

```bash 
$ tar -cvf /vagrant/dokuwiki-backup.tar conf/ data/ 
```

## Turn In 

Turn in your backup tar file. 
