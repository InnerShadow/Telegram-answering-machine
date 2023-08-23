import time

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

def __main__():

    last_msg = ""

    with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        client.start(GetPhoneNumber())
        
        user = client.get_entity('Mazar_Nozol')

        last_msg = client.get_messages(user, limit = 1)[0]

        while True:
            
            last_message = client.get_messages(user, limit = 1)[0]

            sender_name = last_message.sender.username

            print(last_msg.text, last_message.text, last_message != last_msg, sender_name, '\n', sep = '\n')

            if last_message.text != last_msg.text:
                last_msg = last_message

                client.send_message(user, last_msg)

            time.sleep(5)


if __name__ == '__main__':
    __main__()