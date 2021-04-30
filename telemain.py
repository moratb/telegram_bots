#!/home/environments/botenv/bin/python3

from telethon import TelegramClient, events
import requests
import re
import time
import sys
sys.stdout = open('bot.log', 'w')


telegram_bot_token = ''
pass2fa = ''
telegram_api_id = 123456789
telegram_api_hash = ''
telegram_phone_number = ''
forward_to = -123456789
main_acc = 123456789
test_acc = 123456789
channel1 = 123456789
channel2 = -123456789




def telegram_bot_sendtext(bot_message, bot_token=telegram_bot_token, bot_chatID=str(main_acc)):
    send_text = 'https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text='+ bot_message
    print(send_text)
    return requests.get(send_text).json()


def get_last_messages(avail_time=120, bot_token=telegram_bot_token, bot_chatID=str(main_acc)):
    while True:
        time.sleep(15)
        tmp = requests.get('https://api.telegram.org/bot'+ bot_token + '/getUpdates?limit=1&offset=-1').json()
        try:
            code_time = tmp['result'][0]['message']['date']
        except:
            print('no message')
            continue
        diff_time = time.time() - code_time
        if diff_time<avail_time:
            print('code is fresh!')
            code = re.findall('\d+', tmp['result'][0]['message']['text'])
            print(code[0])
            return code[0]
        else:
            print('code_is_old')
            requests.get('https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id='+ bot_chatID +'&text=waiting_for_code').json()


async def auth_tg():
    await telegram_client.send_code_request(telegram_phone_number, force_sms=False)
    res = get_last_messages()
    return res

## telegram auth
telegram_client = TelegramClient(session=None,
                        api_id=telegram_api_id,
                        auto_reconnect=True,
                        api_hash=telegram_api_hash)
telegram_client.start(phone=telegram_phone_number, password=pass2fa, code_callback=auth_tg)




## Main loop
@telegram_client.on(events.NewMessage(incoming=True, chats=(channel1, channel2, test_acc)))
async def normal_handler(event):
    print(event.message, flush=True)
    time.sleep(5)
    await telegram_client.forward_messages(forward_to, event.message)


with telegram_client:
    telegram_client.run_until_disconnected()




async def main():
    async for dialog in telegram_client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

telegram_client.loop.run_until_complete(main())


async def main():
    mes =  await telegram_client.get_messages(channel2, 1)
    print(mes)

telegram_client.loop.run_until_complete(main())