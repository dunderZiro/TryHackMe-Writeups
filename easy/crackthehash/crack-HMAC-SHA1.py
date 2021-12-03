# Python3
import sys
from hashlib import sha1 # SHA1
import hmac # hmac
import argparse

# Define Parser
parser = argparse.ArgumentParser()
parser.add_argument('--hash', action="store", dest="hash", default=0)
parser.add_argument('--salt', action="store", dest="salt", default=0)
parser.add_argument('--wordlist', action="store", dest="wordlist", default=0)

args = parser.parse_args()

# Check if all args haven't been set
if len(sys.argv) != 4:
    print("usage: crack-HMAC-SHA1.py [-h] [--hash HASH] [--salt SALT] [--wordlist WORDLIST]")
    sys.exit(1)

crackme = args.hash
salt = args.salt
wordlist_path = args.wordlist

def generate_hash(salt, password):
    hashed = hmac.new(salt.encode("utf-8"), password.encode("utf-8"), sha1)
    return(hashed.hexdigest())

print(generate_hash("tryhackme", "481616481616"))

with open(wordlist_path) as infile:
    count = 0
    for line in infile:
        count += 1
        if count == 12312613:
            x = line
            print(x) 
            print(generate_hash("tryhackme", x))
        if generate_hash(salt, str(line)) == crackme:
            print(count + ":" + line + ":" + generate_hash(salt, line))
