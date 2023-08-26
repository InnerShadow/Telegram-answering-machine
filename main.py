import asyncio

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT, GetTrainDataByName
from Data_manupulation.Words_level import setStertEndMarks

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

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

        await client.connect()


    #asyncio.run(MonitoringByName('@Mazar_Nozol'))
    #asyncio.run(SaveConversationTXT('@Mazar_Nozol'))
    await GetTrainDataByName('@Mazar_Nozol', client, 1000)


if __name__ == '__main__':
    asyncio.run(__main__())

