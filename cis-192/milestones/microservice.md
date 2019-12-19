# Milestone: Microservice

When you have completed this milestone you will have web pages hosted from your custom domain. In class we setup Docker and created a microservice. For this milestone you'll get a web page up after following the instructions here:

 [Docker Microservice](../pages/dockerfile_and_container_management.md)

Double check your setup with a browser as instructed in the HowTo. On canvas you will submit two URLs. One for each of the virtual hosts.

## Updated Firewall 

Remember, your must update your Firewall before this will work. The following chains should be updated from your previous configuration to look like this: 

### IPv6 FORWARD Chain (Policy: DROP) 

| Rule | Selection | Target |  
| --- | --- | --- |
| 1 | Input from device ens224, output to ens192 | ACCEPT | 
| 2 | ICMPv6 Protocol | ACCEPT | 
| 3 | NEW packets to TCP port 22 | ACCEPT | 
| 4 | NEW packets to TCP port 25 of infra | ACCEPT | 
| 5 | NEW packets to TCP port 80 of app | ACCEPT | 
| 6 | RELATED or ESTABLISHED packets | ACCEPT | 
| 7 | UDP/53 to the IPv6 of infra | ACCEPT | 
| 8 | ALL packets | LOG | 

## Updated DNS Records 

You should also update DNS to contain an entry for "www" in your domain. You should also have a "naked" domain redirect described in the lecture notes. 

## Turn In 

  - A URL that links to your microservice
  - The output of the command "docker ps"

Submit your work on canvas.