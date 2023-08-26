import asyncio

from telethon.sync import TelegramClient

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT, GetTrainDataByName
from Data_manupulation.Words_level import setStertEndMarks

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

from Model.RNN_model import load_RNN_model, Get_RNN_model_answer, CreateRNN
from Model.Tokenizer import get_Tokinazer

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
    maxWordsCount = 2000

    X, Y = await (GetTrainDataByName(name, client, 20000))
    
    tokenizer = get_Tokinazer(X, Y, maxWordsCount = maxWordsCount)
    model = CreateRNN(name, X, Y, tokenizer, maxWordsCount = maxWordsCount, epochs = 200)
    #model, tokenizer = load_RNN_model(name)

    print(Get_RNN_model_answer(model, tokenizer, "Мне показалось, что не сработало"))


if __name__ == '__main__':
    asyncio.run(__main__())

