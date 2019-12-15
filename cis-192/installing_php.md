PHP is a language for creating dynamic content on the web. This lesson will show you how to install PHP and put simple dynamic content on your web server.

## Introduction 

PHP is a programming language that runs on your web server. It's job is to produce HTML. This gives your site the ability to have dynamic content, pages that change when they're accessed. Many important web applications and pages (e.g. Wikipedia and Facebook) are built with PHP. YetPHP is simple to install and use.

## Install PHP 

The PHP interpreter is not installed by default. To install it run the command:

```
web-server$ sudo apt-get install php5
```

There are two paces where PHP is configured:

```
/etc/php5/cli/php.ini
/etc/php5/apache2/php.ini
```

The first directory controls how PHP is run if you execute a PHP script from the UNIX command line. The second controls how scripts are run by Apache. It's important that these be different. Only registered users can execute stuff from the command line, anyone in the world may access your web page. There is one critical setting that you must understand. From /etc/apache2/php.ini

```
; This directive controls whether or not and where PHP will output errors,
; notices and warnings too. Error output is very useful during development, but
; it could be very dangerous in production environments. Depending on the code
; which is triggering the error, sensitive information could potentially leak
; out of your application such as database usernames and passwords or worse.
; It's recommended that errors be logged on production servers rather than
; having the errors sent to STDOUT.
; Possible Values:
;  Off = Do not display any errors
;  stderr = Display errors to STDERR (affects only CGI/CLI binaries!)
;  On or stdout = Display errors to STDOUT
; Default Value: On
; Development Value: On
; Production Value: Off
; http://php.net/display-errors
display_errors = Off
```

You should change this to On for your servers, because it will help you debug your PHP scripts. Heed the warning though, never leave a production server with this setting On.

## Hello PHP World 

With PHP installed an running you can replace any index.html with an index.php file. Here's a simple script to test:
 
```
<html>
<head>
<title>My first PHP document</title>
</head>
<body>
<?php

 
echo "<p>Current date and time: " . date("r") . "</p>";

?>
</body>
 </html>
```

Be sure to rename index.html. If there's an index.html and an index.php the PHP file will be ignored!
