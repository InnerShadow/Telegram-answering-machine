import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.events import NewMessage

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

async def GetConversationByName(name):

    data = []

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        await client.start(GetPhoneNumber())
        
        user = await client.get_entity(name)

        print(1010)

        data = await client.get_messages(user, limit = None)

        print(1111)

        print(data)

        print(1212)

        with open('data.txt', 'w') as f:
            for i in range(len(data)):
                f.write(str(data[i].text) + "(" + str(data[i].sender.username) + ")\n")

            f.close()

        print(1313)

    