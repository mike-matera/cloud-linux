This howto will guide you through setting up MySQL on Server2.
IntroductionMySQL is a Database Management System (DBMS). The data contained inside of it is called the database. MySQL is powerful, stable and free. On your network you will install MySQL onto Server2 and grant access for certain uses on Server1. Keeping the web server and database separate has security and performance advantages but is not strictly necessary.
Install MySQLMySQL has two parts, client and server. The server manages the data, it can be connected to by one or more clients. Large database systems may have many separate databases all controlled by a single server instance and connected to by many clients. Start by installing both the client and server on Server2:
Server2# sudo apt-get install mysql-server
The installer will ask you for a default root password. Don't confuse this password with the password of the root user, they are not the same. You probably should pick funny Cabrillo so you remember.
Basic MySQLNow that you have MySQL server installed you can access it with the client:
Server2# mysql -u root -pWelcome to the MySQL monitor. Commands end with ; or \g.Your MySQL connection id is 176Server version: 5.5.43-0ubuntu0.14.04.1 (Ubuntu)
Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or itsaffiliates. Other names may be trademarks of their respectiveowners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
SQL is a beautiful and rich language. There's a lot to know. Here I'll introduce some commands that will help you navigate MySQL. Some of the commands are specific to MySQL and some will work on and SQL DBMS. Every command requires a semicolon at the end of the line. It's not complete until you add one.
DescriptionCommandSQL?show databases ;See all databases in the systemNouse <database> ;Select a database for use. Future commands will operate on that database only.Noshow tables ;Show the list of tables in the currently selected database.Nodescribe <tablename> ;Show the column names and types in a table.Nocreate database <db-name> ;
drop database <db-name> ;Create and delete a database named db-name.Yesselect * from <table-name> ;Show all the information in a tableYesselect * from <table-name>
  where <column-name> = '<value>' ;Show only the matching rowsYesgrant all on <db-name>.* to 'user'@'host'
 identified by 'password' ;Grant a user access to a particular database. If the username doesn't exist it is created.Yesflush privileges ;Make "grant" actions take effectYes
Grant Access From Server1MySQL is setup to allow access from the host that it's installed on but will not allow remote connections unless you tell it to do so. First you must edit it's configuration file so that it listens on interfaces other than the loopback interface. Edit the configuration file/etc/mysql/my.cnfand change the bind-address line:
bind-address = 0.0.0.0
Don't forget to restart MySQL:
Server2#service mysql stopServer2#service mysql start
Verify that MySQL is listening on an external interface with the netstat command. Now you should grant access to MySQL from Server1. How to do that is covered in the article on setting up specific web applications.