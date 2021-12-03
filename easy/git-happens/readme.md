# Git Happens
https://tryhackme.com/room/githappens

## Find the Super Secret Password

I performed an nmap scan using `nmap -sC -sV -vv -oN nmap-sc-sv.log $ip` and found a web server running on port 80 along with a Git repository found under **$ip/.git**

I then performed a directory bruteforce using gobuster using the following command `gobuster dir -u http://$ip/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -o dirs.log`

Now, to be able to exploit this I needed to understand how to dump a giot repository and found a tool [arthaud/git-dumper](https://github.com/arthaud/git-dumper) that will allow me to dump the repo from the website. I cloned the tool locally and built it from source and ran the following command `python3 git_dumper.py http://$ip/.git git_dump`

As I use ohmyzshrc my terminal recognised the directory git_dump as a git repository which made working with this easier to work with. I ran `ls -alsh` to list the directory and it's content and `git log .`

Using this I was able to find an early version of the login page under the commit `395e087334d613d5e423cdf8f7be27196a360459`, therefore I ran `git checkout 395e087334d613d5e423cdf8f7be27196a360459` to view the source code at that commit in time.

Looking into the index.html file at this commit exposes a hardcoded password stored in plaintext as **Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!** along with the username **admin**.

**Answer: Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!**