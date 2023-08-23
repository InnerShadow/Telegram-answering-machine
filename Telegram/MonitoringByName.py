import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

#Send message if it sends from a companion
async def message_handler(event):
    #Get sleep for 5 seconds to avoid requests spamming
    await asyncio.sleep(5)
    sender_id = event.sender_id
    if sender_id != event.client.uid:
        await event.reply(event.text)


#Function to monitor person's activity in Telegram by his name.
async def MonitoringByName(name):

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        await client.start(GetPhoneNumber())
        
        user = await client.get_entity(name)

        #Add message_handler to event_handler to track when you get new message
        client.add_event_handler(message_handler, event = client.events.NewMessage(chats = [user]))

        await client.run_until_disconnected()


