This guide will help you get a working copy of Wordpress installed on your web server.
IntroductionIt's never been easier to get a complicated Web Application to run on your own domain. Beware, it's simple to make it work but keeping it secure still takes a skilled administrator. Of course, you'll never gain those skills unless you do it yourself. This guide get you to a working Wordpress instance. There are also guides online that will help you with [Drupal](https://help.ubuntu.com/community/Drupal) and [MediaWiki](https://help.ubuntu.com/community/MediaWiki) (the engine that powers Wikipedia). If you follow one of those guides, remember you already have MySQL running on Server2, do not install it again on Server1.
Note: To do this task you will run command on Server1 and Server2. Watch out for the prompts, that's how I tell you which one to enter a command on.
Setup Your DatabaseIn this step you will setup your database so that it can be accessed on Server1. It's important to only allow remote users to access the database that is of interest. You should not allow remote administrators if you can help it. The following steps should be done on Server2:
Server2> mysql -u root -p...mysql> create database wordpress ;mysql> grant all on wordpress.* to 'wordpress'@'%' identified by '<insert-password-here>' ;mysql> flush privileges ;
Verify that you can connect to Server2 from Server1 by running the following command:
Server1> sudo apt-get install mysql-clientServer1> mysql -u wordpress -p -h server2Password: ........mysql>
If you get the mysql> prompt you're connected. If you can't connect verify that you have setup the database correctly. 
Configure WordpressYou can host many different instances of Wordpress from a single server. This is useful if you're a hosting service. The configuration of Wordpress is specific to the URL of the site you'll be hosting. Be sure you get the configuration file name correct. The site-specific configuration file is:
/etc/wordpress/config-<SERVER-FQDN>.php
For example, my site (www.matera.cis.cabrillo.edu) uses the configuration file:
/etc/wordpress/config-www.matera.cis.cabrillo.edu.php
The contents should be:
<?phpdefine('DB_NAME', 'wordpress');define('DB_USER', 'wordpress');define('DB_PASSWORD', '!!!you-password-here!!!');define('DB_HOST', 'db');define('WP_CONTENT_DIR', '/usr/share/wordpress/wp-content');?>
Be sure the above values match your configuration. 
Make Wordpress an Available SiteTo add wordpress to the available sites on your web server create the following file:
# This is /etc/apache2/sites-available/wordpress.conf
Alias /blog /usr/share/wordpress
<Directory /usr/share/wordpress> Options FollowSymLinks AllowOverride Limit Options FileInfo DirectoryIndex index.php Order allow,deny Allow from all</Directory>
<Directory /usr/share/wordpress/wp-content> Options FollowSymLinks Order allow,deny Allow from all</Directory>
Now you can make a symlink in sites-enabled to enable your wordpress site. There's fool-proof way to do that:
Server1> a2ensite wordpress
Server1> service apache2 restart 

Wordpress ConfigurationYour Wordpress site was activated on your default virtual host on a URL that ends with /blog/. My URL is:
[http://www.matera.cis.cabrillo.edu/blog/](http://www.matera.cis.cabrillo.edu/blog/)
You can move the location if you like but Wordpress must have the /blog/ at the end. If you want Wordpress to appear when you type the URL without /blog/ consider using a [meta redirect](http://webmaster.iu.edu/tools-and-guides/maintenance/redirect_meta_refresh.phtml). When you hit the page for the first time Wordpress will ask you to do some setup:


![image](../images/wordpressb7d6.png)



All you have to do now it plug in your settings and you're done!
