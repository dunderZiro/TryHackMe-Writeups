# Crack the hash
https://tryhackme.com/room/crackthehash

## Level 1
### 48bb6e862e54f2a795ffc4e541caed4d
Hash Idenfitied as MD5 using https://www.tunnelsup.com/hash-analyzer/
`john 1.txt --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt`
`john 1.txt --show=Raw-MD5`

### CBFDAC6008F9CAB4083784CBD1874F76618D2A97
Hash Idenfitied as SHA1 using https://www.tunnelsup.com/hash-analyzer/
`john 2.txt --wordlist=/usr/share/wordlists/rockyou.txt`
`john 2.txt --show`

### 1C8BFE8F801D79745C4631D09FFF36C82AA37FC4CCE4FC946683D7B336B63032
Hash Idenfitied as SHA2-256 using https://www.tunnelsup.com/hash-analyzer/
`john 3.txt --wordlist=/usr/share/wordlists/rockyou.txt`
`john 3.txt --show`

### $2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom
Hash Idenfitied as bcrypt using https://www.tunnelsup.com/hash-analyzer/
`john 4.txt --wordlist=/usr/share/wordlists/rockyou.txt`
`john 4.txt --show`

### 279412f945939ba78ce0758d3fd83daa
Hash Idenfitied as MD4 using https://www.tunnelsup.com/hash-analyzer/

`john 5.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD4`
`john 5.txt --show --format=Raw-MD4`

Found nothing in rockyou.txt, checked crackstation and found "Eternity22"

## Level 2
### F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85
Hash Type: SHA2-256
`john 1.txt --format=Raw-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt`
`john 1.txt --show --format=Raw-SHA256`

### 1DFECA0C002AE40B8619ECF94819CC1B
Hash Type: NTLM
`john 2.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt`
`john 2.txt --show --format=NT`

### $6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.
Hash Type: sha512_crypt
Salt: aReallyHardSalt
`john 3.txt --wordlist=/usr/share/wordlists/rockyou.txt`
`john 3.txt --show`

### e5d8870e5bdd26602cab8dbe07a942c8669e56d6
Hash Type: HMAC-SHA1
Salt: tryhackme

I was aunable to perform this using john as they don't support **HMAC-SHA1 (key = $salt)** which is what is being used.

Tried to create my own script _crack-HMAC-SHA1.py_ however format of rockyou.txt was incorrect.

_EDIT: Could have fixed this by running `iconv -f ISO-8859-1 -t UTF-8 /usr/share/wordlists/rockyou.txt > /usr/share/wordlists/rockyou_utf8.txt`_ and converting the rockyou.txt to real UTF-8

Instead I used hashcat on my host machine
`hashcat -D 2 -m 160 <e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme> <rockyou.txt>`
