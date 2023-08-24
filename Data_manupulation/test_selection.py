import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

async def SaveConversationTXT(name):

    data = []

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        await client.start(GetPhoneNumber())
        
        user = await client.get_entity(name)

        data = await client.get_messages(user, limit = 1000)

        print(data)

        with open('top1000.txt', 'w') as f:
            for i in range(len(data)):
                msg = ""
                if data[i].media:
                    if isinstance(data[i].media, MessageMediaDocument):
                        size = data[i].media.document.size
                        if data[i].media.document.mime_type == "audio/ogg":
                            msg += "Audio" + str(size) 
                        if data[i].media.document.mime_type == "video/mp4":
                            msg += "Video" + str(size)
                else:
                    msg += data[i].text

                msg += " (" + data[i].sender.username + ")\n"

                f.write(msg)

            f.close()

    