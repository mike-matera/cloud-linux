Lecture slides are [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1CySdUethVMRhMA45mh8yuA6rTmi0mpfkE9-fBI-iR7s/edit?usp=sharing).
The Final StepsThe final step in your project is to be able to host an interactive website from your domain. The following links point to the official Ubuntu documentation for popular PHP-based web sites:
  * [Mediawiki](https://help.ubuntu.com/community/MediaWiki)- The engine that drives Wikipedia
  * [Drupal](https://help.ubuntu.com/community/Drupal) - A popular content management system (example:[csumb.edu](http://csumb.edu/))
  * [Wordpress](https://help.ubuntu.com/community/WordPress) - A popular content management system (example: [techcrunch.com](http://techcrunch.com/))

Common ConfigurationYou can use the tasksel command to install a group of related packages on your server. This this simplifies the setup tasks for certain things. Execute the following commands on your web server to ensure that it's ready with PHP and MySQL.
apt-get install taskseltasksel install lamp-server
Errata for Ubuntu Documentation
  * Drupal

  * I tested Drupal 7
  * The Drupal installer creates database users for you. You don't have to do the "Manual installation steps"
  * Before you can use Drupal you must go to the setup link http://<your-server>/drupal7/install.php

  * Wordpress

  * The Wordpress instructions are badly out of date.
  * DO NOT enable the universe repo
  * Make this symlink instead of the one specified

  * sudo ln -s /usr/share/wordpress /var/www/wordpress

  * You do not need to run the gzip command
  * Running thebash /usr/share/doc/wordpress/examples/setup-mysql command instructs you to go to http://localhost. You should go to http://<your-server>/wordpress instead.

Understanding Database ManagementDatabases are a broad and complex topic. In this class we will learn the basic nuts and bolts of setting up a database on your Linux host. For that purpose it's important to understand the following basic topics:
  - How to install and configure the database
  - How to authorize users and programs to use your database
  - How to view and modify the data in it

Installing MySQLInstalling MySQL on Ubuntu is very easy. If you've already followed the steps to install Drupal, Wordpress or Mediawiki you should have it installed already. If you want to install it by itself you can run this command:
apt-get install mysql-server
MySQL and others (like Postgress) have a server and a client side component. Once installed a daemon is launched and getting information from the database must go through that daemon. This helps organize access to the data when many clients are involved. Simpler databases (like SQLite) run entirely inside a client program and therefore cannot share data. The configuration for the MySQL daemon is found in:
/etc/mysql
The following is the default my.conf file (the primary configuration file):
## The MySQL database server configuration file.## This will be passed to all mysql clients# It has been reported that passwords should be enclosed with ticks/quotes# escpecially if they contain "#" chars...# Remember to edit /etc/mysql/debian.cnf when changing the socket location.[client]port = 3306socket = /var/run/mysqld/mysqld.sock
# Here is entries for some specific programs# The following values assume you have at least 32M ram[mysqld]## * Basic Settings#user = mysqlpid-file = /var/run/mysqld/mysqld.pidsocket = /var/run/mysqld/mysqld.sockport = 3306basedir = /usrdatadir = /var/lib/mysqltmpdir = /tmplc-messages-dir = /usr/share/mysqlskip-external-locking## Instead of skip-networking the default is now to listen only on# localhost which is more compatible and is not less secure.bind-address = 127.0.0.1
# Error log - should be very few entries.#log_error = /var/log/mysql/error.log
# Here you can see queries with especially long duration#log_slow_queries = /var/log/mysql/mysql-slow.log#long_query_time = 2#log-queries-not-using-indexes## The following can be used as easy to replay backup logs or for replication.# note: if you are setting up a replication slave, see README.Debian about#    other settings you may need to change.#server-id = 1#log_bin = /var/log/mysql/mysql-bin.logexpire_logs_days = 10max_binlog_size     = 100M
# * IMPORTANT: Additional settings that can override those from this file!#  The files must end with '.cnf', otherwise they'll be ignored.#!includedir /etc/mysql/conf.d/
The above configuration is an abbreviated version of the file that comes default with Ubuntu. Like most things on Ubuntu you can override or extend the default configuration by placing specific configuration files in the /etc/mysql/conf.d directory.
Managing the DatabaseMySQL is managed using several tools. The most popular of them are:
  * mysql - Connect to the database. This has the functionality of all other tools if you know SQL language.
  * mysqladmin - A tool to add/remove databases and users
  * mysqldump - Dump the contents of a database for purposes of making a backup
  * mysqlimport - Import a dumped database

Understanding Database OrganizationNOTE: Even though we often call MySQL a "database" that is not the correct word. MySQL is a Database Management System (DBMS). The word "database" is supposed to refer to the actual data that the DBMS manages. In this section I will use "database" properly.
The data in MySQL is organized into databases. Each application (e.g. Mediawiki) will create it's own database. The database is divided into tables and all data is stored in tables. MySQL keeps a separate set of users who are authorized to use one or more databases. The permissions structure itself is maintained in a special database called "mysql".
Managing The Data in Your DatabaseThe mysql command gives you access to your database. You mustsupply a username and password when you connect to your database. This username and password are not necessarily the same as your UNIX username and password. Connect to your database with the following command. The command assumes that the administrator on your database is named "root". This is not necessarily the case!
# mysql -u root -pEnter password:Welcome to the MySQL monitor. Commands end with ; or \g.Your MySQL connection id is 137Server version: 5.5.37-0ubuntu0.12.04.1 (Ubuntu)
Copyright (c) 2000, 2014, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or itsaffiliates. Other names may be trademarks of their respectiveowners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
Once you're in the database you are presented with the mysql prompt. Here's a cheat sheet for common mysql administrative commands:
NOTE: The semicolons are REQUIRED!CommandMeaningshow databases;Show all the databases in the system.use <database-name>;Enter the selected database. This gives you access to the tables in that database.show tables;Show all the tables in your selected database.describe <table-name>;Display information about the data that is contained in the table. select * from <table-name>;Dump the entire contents of the selected table.select <row-name1> [, <row-name2>...] from <table-name>;Dump just the selected rows of a table.create database <database-name>;Create a new databasedrop database <database-name>;Delete a database (be careful!)create user '<user>'@'<host>' identified by '<password>';Create a user of the DBMS and assign them a passwordgrant all on <database-name>.* to '<user>'@'<host>';Give the user permission to do all things to the named database.

