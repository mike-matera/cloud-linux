eIn this lab you will enable HTTPs using a certifiicate created by LetsEncrypt.org. 

## Introduction 

In order to secure the users of your users your website should support end-to-end encryption. This protects your login pages (if you have them) and content from man in the middle attacks. The Let's Encrypt project was started to make it possible to get free certificates that allow you to enable HTTPs. Before Let's Encrypt obtaining certificates was a costly and complex process.

## Let's Encrypt 

Follow the getting started instructions on Let's Encrypt's web page on your web server:
 https://letsencrypt.org/getting-started/
The document works for multiple Linuxes. You are running Ubuntu which is Debian based, so be sure you run the right commands. The Let's Encrypt client will automatically detect what domains you want to have certificates for. Unfortunately, Let's Encrypt has a "rate limit" that prevents too many certificates from being issued to one domain. As far as Let's Encrypt's rate limit is concerned all "cabrillo.edu" domains are the same. The first five or so of you will get a valid certificate each week. You don't have to wait for this lab, take a screenshot of the result of running the Let's Encrypt client for credit.
Turn In
  - A screenshot of the output of Let's Encrypt's client (success or failure)

