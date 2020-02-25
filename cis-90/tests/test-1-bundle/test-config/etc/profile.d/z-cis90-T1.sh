# cis90-T1.sh
event=T1

#username=${LOGNAME/\\//}
#username=`basename $username`
#first=`grep -m1 $username /etc/cis90-passwd | cut -f5 -d":" | cut -f1 -d" "`
username=$LOGNAME
first=`grep $username /etc/passwd | cut -f5 -d":" | cut -f1 -d" "`

if [ "$UID" = "0" ] || [ $UID = "1000" ]; then
  echo $first, you are safe from $event trouble
else
  echo "Hello $first,"
  cat /etc/.trouble/.motd 
  PATH=/etc/.trouble/bin/$event/:/bin:/usr/bin:/sbin/:/usr/sbin:/usr/local/bin:$HOME/.local/bin
fi
