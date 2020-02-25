# ~/.profile: executed by Bourne-compatible login shells.

if [ "$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi
fi

mesg n

if [ -f /etc/nologin ]; then echo Logging in disabled; else echo Logging in enabled; fi
