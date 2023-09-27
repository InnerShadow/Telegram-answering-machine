import asyncio
from colorama import Fore

from telethon.events import NewMessage

from Data_manupulation.Words_level import Word_level_QA_answer
from Data_manupulation.test_selection import message_preprocessing
from Model.QA_model import *
from Model.Tokenizer import *

#Send message if it sends from a companion
async def message_handler(event, client, model, tokinazer, sequences_len, name):
    #Get sleep for 5 seconds to avoid requests spamming
    await asyncio.sleep(5)
    sender_id = event.sender_id
    self_id = await event.client.get_me()
    if sender_id != self_id.id:

        #Get contexts
        user = await client.get_entity(name[5:len(name) - 4])
        contexts = await client.get_messages(user, limit = sequences_len * 2)

        cotexts_data = ""
        i = 0
        while len(cotexts_data.split(" ")) <= 2 * sequences_len:
            cotexts_data += message_preprocessing(contexts[i])
            i += 1

        #Generate answer
        await event.reply(Word_level_QA_answer(model, tokinazer, str(message_preprocessing(event)), cotexts_data, sequences_len))


#Function to monitor person's activity in Telegram by his name.
async def MonitoringByName(name, client, model, tokenizer, sequences_len):
        
    user = await client.get_entity(name[5:len(name) - 4])

    #Add message_handler to event_handler to track when you get new message
    eveny_handler = NewMessage(from_users = [user.id])
    client.add_event_handler(lambda event : message_handler(event, client, model, tokenizer, sequences_len, name), eveny_handler)

    print(Fore.LIGHTGREEN_EX + "\n" + name[5:len(name) - 4] + " has been added to ignoging list!\n")

