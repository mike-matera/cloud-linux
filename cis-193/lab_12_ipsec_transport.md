In this lab you will create an IPsec transport connection.
IntroductionTransport connections are easier to setup than tunnels because there's no need for routing. Transport connections are a good way to have a split firewall. One for people with the encryption password and one for everyone else. Before you begin be sure to:
apt-get install strongswan
Create a Transport ConnectCreate a transport connection to the following server:
  * Name: irc.lifealgorithmic.com
  * Password: lefty

Once you are connected you will be able access a webpage on port 8080. That webpage will have a confirmation number submit it for credit.
[http://irc.lifealgorithmic.com:8080/](http://irc.lifealgorithmic.com:8080/)
Turn In
  - Your /etc/ipsec.conf file
  - The confirmation number

Submit your homework on [blackboard](https://cabrillo.blackboard.com/).
Grading
  * 10 points for your configuration file
  * 10 points for a correct confirmation number

