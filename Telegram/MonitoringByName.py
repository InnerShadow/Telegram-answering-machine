import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

async def message_handler(event):
    await asyncio.sleep(5)
    sender_id = event.sender_id
    if sender_id != event.client.uid:
        await event.reply(event.text)


async def MonitoringByName(name):

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        await client.start(GetPhoneNumber())
        
        user = await client.get_entity(name)

        last_msg = client.get_messages(user, limit = 1)[0]

        client.add_event_handler(message_handler, event = client.events.NewMessage(chats = [user]))

        await client.run_until_disconnected()