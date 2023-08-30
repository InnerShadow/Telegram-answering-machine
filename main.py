import asyncio

from telethon.sync import TelegramClient

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT, GetTrainDataByName

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

from Model.RNN_model import load_RNN_model, Get_RNN_word_continue, full_sequence_RNN_train
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


    #
    #asyncio.run(SaveConversationTXT('@Mazar_Nozol'))

    name = "@Mazar_Nozol"
    maxWordsCount = 10000
    sequences_len = 25
    batch_size = 64
    epochs = 50
    
    try:
        tokenizer = load_tokinazer(name)
    except Exception:
        X, Y = await (GetTrainDataByName(name, client, 2000))
        tokenizer = get_Tokinazer(X, Y, maxWordsCount = maxWordsCount)
        #save_tokinazer(name, tokenizer)

    text = "А то он испугался".lower()

    #model = Get_RNN_word_continue(maxWordsCount = maxWordsCount)
    #model = full_sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount)
    model = load_RNN_model(name)

    print(Word_level_answer(model, tokenizer, text, sequences_len, len(text) * 2))

    asyncio.run(await MonitoringByName(name, client, model, tokenizer, sequences_len))


if __name__ == '__main__':
    asyncio.run(__main__())

# TODO: Tokenazer jeson load