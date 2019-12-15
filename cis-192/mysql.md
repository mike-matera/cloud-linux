This guide will show you how to install and enable MySQL.

### Commands 

  * apt-get

### Configuration 

  * /etc/mysql

Contents
  - [1 Commands](#TOC_Commands)
  - [1.1 Configuration](#TOC_Configuration)

  - [2 Introduction](#TOC_Introduction)
  - [3 Install MySQL](#TOC_Install_MySQL)
  - [4 Networked MySQL](#TOC_Networked_MySQL)
  - [5 Connecting PHP](#TOC_Connecting_PHP)
  - [6 Administer your Database from the Web](#TOC_Administer_your_Database_from_the_Web)

## Introduction 

MySQL is the most popular database program on Linux. It's the "M" in LAMP (Linux, Apache, MySQL and PHP). You will notice that in the past weeks you've setup all the other pieces. When you have MySQL working on your network you will be able to host web applications like WordPress and MediaWiki with ease.

## Install MySQL 

If you haven't run apt-get in a while (like on your db-server) it's possible that the package lists are out of date. The following command will refresh them:

```
db-server$ sudo apt-get update
```

Once your package lists are refreshed install MySQL with the command:

```
db-server$ sudo apt-get install mysql-5.5 mysql-server-5.5
```

You will also be prompted for the password for the database administrator.MySQL's installer will ask to install pinba-engine. Sayyes.MySQL (like most databases) has a permission system that is separate and different from Linux's. This allows DB admins to work without having access to the root password. That's good. You should set the DB admin's password to "Cabri11o", a.k.a. funny Cabrillo so you don't get it mixed up. Once MySQL is installed you can access it from the command line locally with the following command:

```
db-server$ mysql -u root -p
Enter password:
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 37
Server version: 5.5.49-0ubuntu0.14.04.1 (Ubuntu)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
```

You now have MySQL running. However, for security purposes MySQL only makes itself available on the local machine. Next we'll configure MySQL to work over the network.

## Networked MySQL 

Most installations of MySQL operate over a network socket. This allows administrators to place MySQL and Apache on separate machines, which helps when you want to scale. Keeping the Internet two steps away from your database also improves security. Now we'll setup MySQL so that you can connect over the network. We'll grant the root user access only from your web server. Start by editing /etc/mysql/my.cnf. Change the directive bind-address to this:

```
bind-address = ::0
```

Restart mysql after making the change:

```
db-server$ sudo service mysql restart
```

You should now verify that MySQL is listening to an external network socket:

```
db-server$ sudo netstat -lntp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address      Foreign Address     State    PID/Program name
tcp    0   0 0.0.0.0:22       0.0.0.0:*        LISTEN   1036/sshd   
tcp6    0   0 :::22          :::*          LISTEN   1036/sshd   
tcp6    0   0 :::3306         :::*          LISTEN   26835/mysqld  
```

Now we have to allow the root user account to use MySQL from a different server. You must use the MySQL command line (as shown above). From the MySQL prompt enter the command:

```
mysql> grant all on *.* to 'root'@'%' identified by 'Cabri11o';
Query OK, 0 rows affected (0.00 sec)
mysql> flush privileges ;
Query OK, 0 rows affected (0.00 sec)
```

Test Your DatabaseIf you have your DB setup correctly you should be able to access it from your web-server using the mysql command. You will have to install the mysql command:

```
web-server$ sudo apt-get install mysql-5.5
```

Note: This only installs the client, not the server. When the client asks to configure pinba-db say No.With the client installed you should be able to connect from your web-server to your db-server with the following command:

```
web-server$ mysql -h db-server -u root -p
```

Your web server can now access your db-server.

## Connecting PHP 

You now need to add the php modules that allow you to connect to a database. Do that with the following command:

```
web-server$ sudo apt-get install php5-mysqllibapache2-mod-php5 php5-mcrypt
web-server$ sudo service apache2 restart
```

Once installed PHP programs will be able to access your database. Replace your starter PHP program from last lesson with the following code:

```
<html>
<head>
<title>My first PHP document</title>
</head>
<body>
<h1>Welcome to my PHP page.</h1>
<?php
$servername = "server";
$username = "user";
$password = "password";
// Create connection
$conn = mysqli_connect($servername, $username, $password);
// Check connection
if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}
echo "Connected successfully";
?>
</body>
</html>
```

Change the variables near the top to match your db-server, root and password. If you have done it correctly you should see "Connected successfully" on your PHP page.

## Administer your Database from the Web 

The adminer PHP program helps you administer your database from your website. It's a nice tool for admins (but you should keep it away from the Internet). Adminer is a single PHP script. Download it into your document root with the following command:

```
web-server$ wgethttps://www.adminer.org/static/download/4.2.4/adminer-4.2.4-mysql-en.php
web-server$ln -s adminer-4.2.4-mysql-en.php adminer.php
```

You will be able to access adminer from the URL:

```
 http://php.<yourdomain>.cis.cabrillo.edu/adminer.php
```

You can add and drop users, databases and perform queries, right from the web!