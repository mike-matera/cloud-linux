Lecture notes are [here](https://docs.google.com/a/lifealgorithmic.com/presentation/d/1VOTapkxxiuqZgDSM68BZOFTJR-6TaVG_9yS2Qnl1tBE/edit#slide=id.g382bfdc58_089).
PHP (http://www.php.net/) is a popular language for programming web servers. PHP allows you to run a program every time a browser loads a page. It gives you the flexibility to create dynamic web content. PHP can scale to the largest websites. For example, Facebook uses PHP.
Links
  * [Ubuntu LAMP (Linux, Apache, MySQL, PHP) guide](https://help.ubuntu.com/community/ApacheMySQLPHP)

Installing PHPLike so many things on Ubuntu getting started with PHP is a simple matter of installing the proper software:
# apt-get install php5
Installing PHP also installs modules into Apache2's configuration here:
/etc/apache2/mods-available/php5.conf/etc/apache2/mods-available/php5.load
The installer also enables the PHP modules and restarts Apache.
# ls -la /etc/apache2/mods-enabled/*php*lrwxrwxrwx 1 root root 27 May 2 08:31 /etc/apache2/mods-enabled/php5.conf -> ../mods-available/php5.conflrwxrwxrwx 1 root root 27 May 2 08:31 /etc/apache2/mods-enabled/php5.load -> ../mods-available/php5.load
Once apt-get is complete you are ready to go.
Configuring PHPPHP's configuration can be found in:
# find /etc/php5//etc/php5//etc/php5/conf.d/etc/php5/conf.d/pdo.ini/etc/php5/cli/etc/php5/cli/conf.d/etc/php5/cli/php.ini/etc/php5/apache2/etc/php5/apache2/conf.d/etc/php5/apache2/php.ini
PHP is unusual in that it has two separate configurations. One for running PHP from the command line and one for running PHP via Apache. The reason is that you may want to lock down what can be done via Apache for security reasons. Remember, only users on the system have access to the command line but anyone can access your web server.For the class we're interested in the configuration for Apache, located here:
/etc/php5/apache2/php.ini
php.ini has many configuration settings. You will not need to tune most of them unless you have a high traffic web site. There are a few that are worth understanding when you're starting out. These directives tell PHP where to display script errors. By default they will only be in Apache's logs. This is most secure but it also makes scripts a bit harder to debug if you're not root. Turn them on in your configuration so that you can see script errors in the browser window:
display_errors = Ondisplay_startup_errors = On
You can see more about these options here
  * [http://php.net/display-errors](http://php.net/display_errors)
  * [http://php.net/display-startup-errors](http://php.net/display_startup_errors)

The default php.ini on Ubuntu is a very good start.
Your First PHP ScriptWhen you don't specify a file in the URL string Apache looks for index files (e.g. index.html). If there is no index.html Apache will use index.php. In one of your virtual hosts create an index.php with a basic "Hello World" message:
# cd /var/www# rm index.html# cat > index.php << EOF<html><head> <title>PHP Test</title></head><body><?php echo '<p>Hello World</p>'; ?></body></html>EOF
When you go to your site you should see a simple Hello World message. What happens if you mess up your PHP script? Replace the command:
echo '<p>Hello World</p>';
With this:
brokenecho '<p>Hello World</p>';
If you have configured the display_errors settings properly you should see an error message in the browser. What is it?