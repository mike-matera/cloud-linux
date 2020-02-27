# Install Dokuwiki 

This lab takes you through installing the [Dokuwiki](https://www.dokuwiki.org/dokuwiki) wiki system on your VM. Dokuwiki is installed from the command line from a TAR file. 

## Before You Begin 

Dokuwiki is a web application that uses PHP. Before you begin you should have Apache and PHP installed. Install them with `apt`:

```bash
$ sudo apt install apache2 php 
``` 

You should have a `/var/www/html` directory on your VM and you can access it with the URL:

[http://localhost:8080/](http://localhost:8080/)

## Step 1: Download Dokuwiki 

Use the `wget` command to download the latest version of Dokuwiki:

```bash
$ wget https://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz
```

## Step 2: Extract the TAR File 

Check the contents of the TAR file before you extract it:

```bash 
$ tar -tvf dokuwiki-stable.tgz
```

The files are all in a single directory. You should know what files will be extracted before you extract them. What directory will be created when you extract the file? 

```bash 
$ tar -xvf dokuwiki-stable.tgz
```

## Step 3: Move the Files Into Place 

You should have extracted the files in your home directory. As root move them into the `/var/www/html` directory. 

```bash
$ sudo mv dokuwiki-2018-04-22b /var/www/html/dokuwiki
```

The files won't be accessible to Apache unless you change the ownership of the files. 

```
$ sudo chown -R root:www-data /var/www/html/dokuwiki
$ sudo chmod -R g+w /var/www/html/dokuwiki
```

## Step 4: Configure Your Wiki 

If you succeeded your Wiki can be configured with this URL:

[http://localhost:8080/dokuwiki/install.php](http://localhost:8080/dokuwiki/install.php)

After setup you can access it here: 

[http://localhost:8080/dokuwiki](http://localhost:8080/dokuwiki)

## Step 5: Create a Page 

Once you have configured your Wiki create a page called `cis-191`. Add any content you want to the page. It's important that there be some content. You will backup your Wiki in a subsequent lab. 

## Ansible Equivalent (Optional)

This play performs the tasks in this lab: 

```yaml
- hosts: all
  become: true 
  name: Install Dokuwiki 
  tags: [dokuwiki]
  tasks:
  - name: Installing Apache and PHP
    become: true
    apt:
      pkg:
      - apache2
      - php 
  - name: Create the /var/www/html/dokuwiki
    file:
      path: /var/www/html/dokuwiki
      state: directory
      mode: '0775'
      owner: root
      group: www-data
  - name: Install Dokuwiki
    unarchive:
      src: https://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz
      dest: /var/www/html/dokuwiki
      remote_src: yes
      owner: root
      group: www-data
      mode: g+w 
      extra_opts:
        - --strip 
        - "1"
```

## Submit 

Submit a screenshot of the page you created. 
