#!/usr/bin/python3

import requests

tarantino = requests.post("https://www.tarantino-family.com/wp-admin/admin-ajax.php", 
				data = {"action": "ajax_register_user", 
				"step":"1",
				"phone":"380951500486", 
				"smscode":"",
				"security_login":"4bfcebbb19"})