#!/usr/bin/python3

import requests

try:
	r = requests.get("https://ukr.net")
	print("send!")
except:
	print("no send!")