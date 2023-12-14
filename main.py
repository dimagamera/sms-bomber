import sys
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods import DeleteMessage
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types.input_file import BufferedInputFile
from aiogram.enums import ParseMode 
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import logging
import asyncio
import requests
from bs4 import BeautifulSoup


dp = Dispatcher()
@dp.message(CommandStart())
async def CommandStart_heandler(message: Message):
    await message.answer(
        '''Привіт, я бот для скачування відео з TikTok та Instagram.\n\n
        На підтримці Stories & Reels.\n\n
        Просто надішліть мені посилання на відео\n\n
        Увага! Сторінка повинна бути відкрита!
        ''')



@dp.message()
async def echo_handler(message: types.Message):
    stored_message = message.text
    id_msg = message.message_id
    #await message.bot.delete_message(message.chat.id, id_msg)
    try:
        if 'tiktok.com/' in stored_message:
            await message.answer('Обробка...\nЗачекайте будь ласка.')
            cookies = {
                '_ga': 'GA1.1.320230884.1702548890',
                '_ga_ZSF3D6YSLC': 'GS1.1.1702548889.1.1.1702549092.0.0.0',
            }

            headers = {
                'authority': 'ssstik.io',
                'accept': '*/*',
                'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'cookie': '_ga=GA1.1.320230884.1702548890; _ga_ZSF3D6YSLC=GS1.1.1702548889.1.1.1702549092.0.0.0',
                'hx-current-url': 'https://ssstik.io/ru',
                'hx-request': 'true',
                'hx-target': 'target',
                'hx-trigger': '_gcaptcha_pt',
                'origin': 'https://ssstik.io',
                'referer': 'https://ssstik.io/ru',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }

            params = {
                'url': 'dl',
            }

            data = {
                'id': f'{stored_message}',
                'locale': 'ru',
                'tt': 'a3EydXBm',
            }

            response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

            soup = BeautifulSoup(response.text, 'html.parser')
            insta_without_water = soup.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active notranslate')
            url_insta_without_water = insta_without_water.get('href')
            download_video = requests.get(url_insta_without_water)
            with open('tiktok.mp4', 'wb') as file:
                file.write(download_video.content)
                video_path = 'tiktok.mp4'

            with open(video_path, 'rb') as file:
                input_video = BufferedInputFile(file.read(), 'tiktok.mp4')
                await message.bot.send_video(message.chat.id, input_video)
        
        elif 'instagram.com/reel' in stored_message:
            await message.answer('Обробка...\nЗачекайте будь ласка.')
            cookies = {
            'random_n': 'eyJpdiI6InNHOGpPR1BjNUU4MklvZTkxYjlGM0E9PSIsInZhbHVlIjoiMzhwd0k2STRFNlZvcDJ3Z0xzdXdjUUlyTVo2akVmWnVwYno4K1Q0L1dmRFRhQjJIU0RwMEJ0eEFjb3RUdEdGZiIsIm1hYyI6Ijk5N2NkNTFjZTk5YmExYTQwZmNmNDA1ZGMzN2YzMGFmZDJjYWM3NjZkZGZmNGJjNTk0YTM2YzRmZDQxZjljNjMiLCJ0YWciOiIifQ%3D%3D',
            'XSRF-TOKEN': 'eyJpdiI6IlpzQzJ1LzBycld0LzdGYzRjZ2EyL0E9PSIsInZhbHVlIjoiSFh2QndoWk56NnI3TGpSVHpFbmhvUTg0bDk2bm9GYmpzbnFSdEJHTTlGTHhRODdzNTdidzBKRXFuaG9vSmE4ZDJUclBZRDhFaEg2bWIycm42NjdiN3N1ck04NHdHY3BFYllDbUhZQTVoc2J4azVSZ1NBSnFlamc1WUdsZERxUVQiLCJtYWMiOiJhNzEyY2IxNTYwMjYwMDc1ZDUwZTlhYzZkNzU3YTE1OWQ5MzY4ZTlhYTE4NGI5YjNlOWRmNTZmNmQwMWVlODVjIiwidGFnIjoiIn0%3D',
            'sssinstagram_session': 'eyJpdiI6Iis1KzFTNWR3aEo5RGtJNDBPeURlYkE9PSIsInZhbHVlIjoiNVFLbVZob25GQVlrUzdlcFRGaStuSWxOUkxVUEhEb0k0MkFveHAzTHJtQktrMzlscnprTDdCWUtVaWw3a3VXTFYrd1RXbzhDTlJzUFRhcFRzUnZZR0hlUVBCVVQ0ampkRVgyOSs0WGlrUFlaR0pRNS8yUVA5QmFyUG4zZG5vamUiLCJtYWMiOiI0MWJmNDQyNmFhODQ2MjAyYmRiZmQ5M2U3ZTI3ZGRkODM0N2JlYTgzYTY0MTk2YmFjOTMzYTA4ZmFhNTlkOGVmIiwidGFnIjoiIn0%3D',
            '_ga_90WCZ6NHEE': 'GS1.1.1702562621.1.0.1702562621.0.0.0',
            '_ga': 'GA1.2.1224714751.1702562621',
            '_gid': 'GA1.2.157124674.1702562621',
            '_gat_UA-3524196-4': '1',
            '_ga_CN2Z3TL83Y': 'GS1.2.1702562621.1.0.1702562628.53.0.0',
            }

            headers = {
            'authority': 'sssinstagram.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'random_n=eyJpdiI6InNHOGpPR1BjNUU4MklvZTkxYjlGM0E9PSIsInZhbHVlIjoiMzhwd0k2STRFNlZvcDJ3Z0xzdXdjUUlyTVo2akVmWnVwYno4K1Q0L1dmRFRhQjJIU0RwMEJ0eEFjb3RUdEdGZiIsIm1hYyI6Ijk5N2NkNTFjZTk5YmExYTQwZmNmNDA1ZGMzN2YzMGFmZDJjYWM3NjZkZGZmNGJjNTk0YTM2YzRmZDQxZjljNjMiLCJ0YWciOiIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IlpzQzJ1LzBycld0LzdGYzRjZ2EyL0E9PSIsInZhbHVlIjoiSFh2QndoWk56NnI3TGpSVHpFbmhvUTg0bDk2bm9GYmpzbnFSdEJHTTlGTHhRODdzNTdidzBKRXFuaG9vSmE4ZDJUclBZRDhFaEg2bWIycm42NjdiN3N1ck04NHdHY3BFYllDbUhZQTVoc2J4azVSZ1NBSnFlamc1WUdsZERxUVQiLCJtYWMiOiJhNzEyY2IxNTYwMjYwMDc1ZDUwZTlhYzZkNzU3YTE1OWQ5MzY4ZTlhYTE4NGI5YjNlOWRmNTZmNmQwMWVlODVjIiwidGFnIjoiIn0%3D; sssinstagram_session=eyJpdiI6Iis1KzFTNWR3aEo5RGtJNDBPeURlYkE9PSIsInZhbHVlIjoiNVFLbVZob25GQVlrUzdlcFRGaStuSWxOUkxVUEhEb0k0MkFveHAzTHJtQktrMzlscnprTDdCWUtVaWw3a3VXTFYrd1RXbzhDTlJzUFRhcFRzUnZZR0hlUVBCVVQ0ampkRVgyOSs0WGlrUFlaR0pRNS8yUVA5QmFyUG4zZG5vamUiLCJtYWMiOiI0MWJmNDQyNmFhODQ2MjAyYmRiZmQ5M2U3ZTI3ZGRkODM0N2JlYTgzYTY0MTk2YmFjOTMzYTA4ZmFhNTlkOGVmIiwidGFnIjoiIn0%3D; _ga_90WCZ6NHEE=GS1.1.1702562621.1.0.1702562621.0.0.0; _ga=GA1.2.1224714751.1702562621; _gid=GA1.2.157124674.1702562621; _gat_UA-3524196-4=1; _ga_CN2Z3TL83Y=GS1.2.1702562621.1.0.1702562628.53.0.0',
            'origin': 'https://sssinstagram.com',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': 'eyJpdiI6IlpzQzJ1LzBycld0LzdGYzRjZ2EyL0E9PSIsInZhbHVlIjoiSFh2QndoWk56NnI3TGpSVHpFbmhvUTg0bDk2bm9GYmpzbnFSdEJHTTlGTHhRODdzNTdidzBKRXFuaG9vSmE4ZDJUclBZRDhFaEg2bWIycm42NjdiN3N1ck04NHdHY3BFYllDbUhZQTVoc2J4azVSZ1NBSnFlamc1WUdsZERxUVQiLCJtYWMiOiJhNzEyY2IxNTYwMjYwMDc1ZDUwZTlhYzZkNzU3YTE1OWQ5MzY4ZTlhYTE4NGI5YjNlOWRmNTZmNmQwMWVlODVjIiwidGFnIjoiIn0=',
        }

            json_data = {
                'link': f'{stored_message}',
                'token': '',
            }

            response = requests.post('https://sssinstagram.com/ru/r', cookies=cookies, headers=headers, json=json_data).json()

            for item in response['data']['items']:
                url = item['urls'][0]['urlDownloadable']

            download = requests.get(url).content

            with open ('insta.mp4', 'wb') as file:
                file.write(download)
            with open('insta.mp4', 'rb') as file:
                input_video = BufferedInputFile(file.read(), 'insta.mp4')
                await message.bot.send_video(message.chat.id, input_video)
        elif 'instagram.com/stories' in stored_message:
            await message.answer('Обробка...\nЗачекайте будь ласка.')
            cookies = {
            'random_n': 'eyJpdiI6InNHOGpPR1BjNUU4MklvZTkxYjlGM0E9PSIsInZhbHVlIjoiMzhwd0k2STRFNlZvcDJ3Z0xzdXdjUUlyTVo2akVmWnVwYno4K1Q0L1dmRFRhQjJIU0RwMEJ0eEFjb3RUdEdGZiIsIm1hYyI6Ijk5N2NkNTFjZTk5YmExYTQwZmNmNDA1ZGMzN2YzMGFmZDJjYWM3NjZkZGZmNGJjNTk0YTM2YzRmZDQxZjljNjMiLCJ0YWciOiIifQ%3D%3D',
            '_ga_90WCZ6NHEE': 'GS1.1.1702562621.1.0.1702562621.0.0.0',
            '_ga': 'GA1.2.1224714751.1702562621',
            '_gid': 'GA1.2.157124674.1702562621',
            '_gat_UA-3524196-4': '1',
            'XSRF-TOKEN': 'eyJpdiI6InpTcDNTWVpMV1hNUnVpTmsxYkhzTWc9PSIsInZhbHVlIjoicWs4UlJCZ2hINEpPVk1lYzhqV01iRUVtRWNQNlhvYVA5UHNVbEhQbzdHUDR4bUJoK2svZzZGM0t2em9GT09NenRIbmxtYXM4Q3lXZ0RjcmVBelp0OTZmd2ZLRjE4WVhUbEtEOGM3a3NmMzE0SlBENnBtenV1Q0M3Nkl4dTFGRFIiLCJtYWMiOiIzNjRlNDM0N2IzYzQyY2MxYTQ2MzdiZDhjYzJhNjYzYTYzMzk1ZGVhOTFjMTJhNTc5NmVkNDlkMWI5YThlNWJhIiwidGFnIjoiIn0%3D',
            'sssinstagram_session': 'eyJpdiI6IlJxOHVDKzZnd0cwaWhNSU5qZjUzeHc9PSIsInZhbHVlIjoiT1VuMkhGOFJCUkYra2dXOWdCQVhoU1lHMEN6bjNnY0tVZ240R0ZOVE5kWStFWDJuSmlwVERkdmd6a0VQajZHUWtIMzZLSkgxZnJob3h3aCtGVnJSU2RIWm0rMXQvOE9MVE1hREdaMHY0MXFRdjFSMTRMK3o5TERJOXdwYlZOemgiLCJtYWMiOiI3OTdhMTNjYjMwZDI4YWY4NWFhMWIxYTFhMzdlOGMwYjM2MDgwZGM2MWJhOGZhYWQ0ZmU5YTAzMTc5ZmZkMmM2IiwidGFnIjoiIn0%3D',
            '_ga_CN2Z3TL83Y': 'GS1.2.1702562621.1.1.1702563901.47.0.0',
        }

            headers = {
                'authority': 'sssinstagram.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
                'content-type': 'application/json;charset=UTF-8',
                # 'cookie': 'random_n=eyJpdiI6InNHOGpPR1BjNUU4MklvZTkxYjlGM0E9PSIsInZhbHVlIjoiMzhwd0k2STRFNlZvcDJ3Z0xzdXdjUUlyTVo2akVmWnVwYno4K1Q0L1dmRFRhQjJIU0RwMEJ0eEFjb3RUdEdGZiIsIm1hYyI6Ijk5N2NkNTFjZTk5YmExYTQwZmNmNDA1ZGMzN2YzMGFmZDJjYWM3NjZkZGZmNGJjNTk0YTM2YzRmZDQxZjljNjMiLCJ0YWciOiIifQ%3D%3D; _ga_90WCZ6NHEE=GS1.1.1702562621.1.0.1702562621.0.0.0; _ga=GA1.2.1224714751.1702562621; _gid=GA1.2.157124674.1702562621; _gat_UA-3524196-4=1; XSRF-TOKEN=eyJpdiI6InpTcDNTWVpMV1hNUnVpTmsxYkhzTWc9PSIsInZhbHVlIjoicWs4UlJCZ2hINEpPVk1lYzhqV01iRUVtRWNQNlhvYVA5UHNVbEhQbzdHUDR4bUJoK2svZzZGM0t2em9GT09NenRIbmxtYXM4Q3lXZ0RjcmVBelp0OTZmd2ZLRjE4WVhUbEtEOGM3a3NmMzE0SlBENnBtenV1Q0M3Nkl4dTFGRFIiLCJtYWMiOiIzNjRlNDM0N2IzYzQyY2MxYTQ2MzdiZDhjYzJhNjYzYTYzMzk1ZGVhOTFjMTJhNTc5NmVkNDlkMWI5YThlNWJhIiwidGFnIjoiIn0%3D; sssinstagram_session=eyJpdiI6IlJxOHVDKzZnd0cwaWhNSU5qZjUzeHc9PSIsInZhbHVlIjoiT1VuMkhGOFJCUkYra2dXOWdCQVhoU1lHMEN6bjNnY0tVZ240R0ZOVE5kWStFWDJuSmlwVERkdmd6a0VQajZHUWtIMzZLSkgxZnJob3h3aCtGVnJSU2RIWm0rMXQvOE9MVE1hREdaMHY0MXFRdjFSMTRMK3o5TERJOXdwYlZOemgiLCJtYWMiOiI3OTdhMTNjYjMwZDI4YWY4NWFhMWIxYTFhMzdlOGMwYjM2MDgwZGM2MWJhOGZhYWQ0ZmU5YTAzMTc5ZmZkMmM2IiwidGFnIjoiIn0%3D; _ga_CN2Z3TL83Y=GS1.2.1702562621.1.1.1702563901.47.0.0',
                'origin': 'https://sssinstagram.com',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-xsrf-token': 'eyJpdiI6InpTcDNTWVpMV1hNUnVpTmsxYkhzTWc9PSIsInZhbHVlIjoicWs4UlJCZ2hINEpPVk1lYzhqV01iRUVtRWNQNlhvYVA5UHNVbEhQbzdHUDR4bUJoK2svZzZGM0t2em9GT09NenRIbmxtYXM4Q3lXZ0RjcmVBelp0OTZmd2ZLRjE4WVhUbEtEOGM3a3NmMzE0SlBENnBtenV1Q0M3Nkl4dTFGRFIiLCJtYWMiOiIzNjRlNDM0N2IzYzQyY2MxYTQ2MzdiZDhjYzJhNjYzYTYzMzk1ZGVhOTFjMTJhNTc5NmVkNDlkMWI5YThlNWJhIiwidGFnIjoiIn0=',
            }

            json_data = {
                'link': f'{stored_message}',
                'token': '',
            }

            response = requests.post('https://sssinstagram.com/ru/r', cookies=cookies, headers=headers, json=json_data).json()
            a = response['data']['items'][0]['urls'][0]['url_downloadable']
            download = requests.get(a).content

            with open ('insta.mp4', 'wb') as file:
                file.write(download)
            with open('insta.mp4', 'rb') as file:
                input_video = BufferedInputFile(file.read(), 'insta.mp4')
                await message.bot.send_video(message.chat.id, input_video)

    except:
        await message.answer('Виникла помилка.\nСторінка закрита, або не існує\n Попробуйте ще раз...')

async def main():
    bot = Bot(token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
