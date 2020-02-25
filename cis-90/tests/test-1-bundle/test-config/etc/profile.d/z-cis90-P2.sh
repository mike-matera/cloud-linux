# cis90-P2.sh
event=P2
username=$LOGNAME
first=`grep $username /etc/passwd | cut -f5 -d":" | cut -f1 -d" "`
if [ "$UID" = "0" ] || [ $UID = "1000" ]; then
  echo $first, you are safe from $event trouble
else
  #echo "Hello $first,"
  cat /etc/.trouble/.motd-$event 
  PATH="/usr/local/bin"
  #exec /bin/sh
fi
