import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.events import NewMessage

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

#Send message if it sends from a companion
async def message_handler(event, send_msg):
    #Get sleep for 5 seconds to avoid requests spamming
    await asyncio.sleep(5)
    sender_id = event.sender_id
    self_id = await event.client.get_me()
    if sender_id != self_id.id:
        await event.reply(event.text)


#Function to monitor person's activity in Telegram by his name.
async def MonitoringByName(name, client):

    send_msg = "Робот, робот, робот"
        
    user = await client.get_entity(name)

    #Add message_handler to event_handler to track when you get new message
    eveny_handler = NewMessage(from_users = [user.id])
    client.add_event_handler(lambda event : message_handler(event, send_msg), eveny_handler)

    await client.run_until_disconnected()


