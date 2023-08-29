import asyncio

from telethon.sync import TelegramClient

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT, GetTrainDataByName

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

from Model.RNN_model import load_RNN_model, RNN_word_continue, RNN_word_edit_QA_model
from Model.Tokenizer import get_Tokinazer, save_tokinazer, load_tokinazer
from Data_manupulation.Words_level import Word_level_answer

from keras.preprocessing.sequence import pad_sequences

async def __main__():

    client = TelegramClient(GetPhoneNumber(), GetAPIID(), GETAPI_Hash())
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(GetPhoneNumber())
        try :
            await client.sign_in(GetPhoneNumber(), code = input('Enter the code: '))
        except Exception:
            password = input("Enter password: ")
            client = await client.sign_in(password = password)


    #asyncio.run(MonitoringByName('@Mazar_Nozol'))
    #asyncio.run(SaveConversationTXT('@Mazar_Nozol'))

    name = "@Mazar_Nozol"
    maxWordsCount = 1000
    sequences_len = 25
    
    try:
        tokenizer = load_tokinazer(name)
    except Exception:
        X, Y = await (GetTrainDataByName(name, client, 2000))
        tokenizer = get_Tokinazer(X, Y, maxWordsCount = maxWordsCount)
        save_tokinazer(name, tokenizer)

    text = "Но пить пиво веселее Чем кодить Имхо".lower()

    model = RNN_word_continue(name, X, Y, tokenizer, maxWordsCount = maxWordsCount, epochs = 25, sequences_len = sequences_len, batch_size = 32)
    #model = load_RNN_model(name)
    
    print("Answ: ", Word_level_answer(model, tokenizer, text, sequences_len = sequences_len))


if __name__ == '__main__':
    asyncio.run(__main__())

# TODO: Tokenazer jeson load