import asyncio

from telethon.events import NewMessage

from Data_manupulation.Words_level import Word_level_QA_answer
from Data_manupulation.test_selection import message_preprocessing

#Send message if it sends from a companion
async def message_handler(event, model, tokinazer, sequences_len):
    #Get sleep for 5 seconds to avoid requests spamming
    await asyncio.sleep(5)
    sender_id = event.sender_id
    self_id = await event.client.get_me()
    if sender_id != self_id.id:
        await event.reply(Word_level_QA_answer(model, tokinazer, str(message_preprocessing(event)), sequences_len, len(event.text.split()) * 2))


#Function to monitor person's activity in Telegram by his name.
async def MonitoringByName(name, client, model, tokenizer, sequences_len):
        
    user = await client.get_entity(name[5:len(name) - 4])

    #Add message_handler to event_handler to track when you get new message
    eveny_handler = NewMessage(from_users = [user.id])
    client.add_event_handler(lambda event : message_handler(event, model, tokenizer, sequences_len), eveny_handler)

    print("\n" + name[5:len(name) - 4] + " ignoring succsefully!\n")

    await client.run_until_disconnected()

