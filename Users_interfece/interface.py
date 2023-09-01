import os
import glob

from telethon.sync import TelegramClient

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

async def log_in(phone, apiid, apihash):
    client = TelegramClient(phone, apiid, apihash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try :
            await client.sign_in(GetPhoneNumber(), code = input('Enter the code: '))
        except Exception:
            password = input("Enter password: ")
            client = await client.sign_in(password = password)

    return client


def application_api():
    phone =  GetPhoneNumber()
    apiid = GetAPIID()
    apihash = GETAPI_Hash()

    return phone, apiid, apihash


def get_new_victim():
    name = input("Enter nmae: ")
        
    with open ("Data/" + name  + ".txt", 'w') as f:
        f.write(name)


def get_all_victiums():
    victiums = glob.glob(os.path.join("/Data", "@*.txt"))
    for i in range(len(victiums)):
        print(str(i) + " : " + str(victiums[i]))

    return victiums


def save_victum(name):
    name = 1


def select_victum(victiums, i):
    return victiums[i]


def get_all_models():
    models = glob.glob(os.path.join("/Data", "*.h5"))
    for i in range(len(models)):
        print(str(i) + " : " + str(models[i]))

    return models