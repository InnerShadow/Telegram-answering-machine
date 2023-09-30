import os
import glob

from telethon.sync import TelegramClient
from colorama import Fore

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

#Get default answer if answer hos no vocabulary recognazed words 
def save_default_answer():
    exist = os.path.exists("Data/default_answer.txt")
    if exist == False:
        with open("Data/default_answer.txt", 'w') as f:
            f.write("👀?")


#Do log in telegram
async def log_in(phone, apiid, apihash):
    print(Fore.YELLOW + 
          "\nTry to connect to telegram: \n")
    
    #Try to connect to telegram base on prev session
    client = TelegramClient(phone, apiid, apihash)
    await client.connect()

    #If cannot connect ask users telegram data 
    try:
        if not await client.is_user_authorized():
            print(Fore.YELLOW + 
                  "\nCannot find previous session, enter following data: \n")
            
            await client.send_code_request(phone)

            try :
                await client.sign_in(GetPhoneNumber(), code = input(Fore.LIGHTWHITE_EX + 
                                                                    '\nEnter the code: \n'))
                
            except Exception:
                password = input(Fore.LIGHTWHITE_EX + 
                                 "\nEnter password: \n")
                client = await client.sign_in(password = password)

    except Exception:
        print(Fore.LIGHTRED_EX + 
              "\nCannot login Telegram!\n")
        
        return None

    print(Fore.LIGHTGREEN_EX + 
          "\nConnected succsessfull!\n")

    return client


#Get main Telegram application params
def application_api():
    phone =  GetPhoneNumber()
    apiid = GetAPIID()
    apihash = GETAPI_Hash()

    return phone, apiid, apihash


#Shows all victims
def get_all_victiums(Show = True):
    victiums = glob.glob(os.path.join("Data/", "@*.txt"))

    if len(victiums) == 0:
        print(Fore.YELLOW + 
              "\nThere is no victims! Create one!\n")

    if(Show):
        for i in range(len(victiums)):
            print(Fore.YELLOW + str(i + 1) + " : " + str(victiums[i])[5:len(victiums[i]) - 4])

        print("\n")

    return victiums


#Show all models
def get_all_models(Show = True):
    models = glob.glob(os.path.join("Data/", "*.keras"))

    if len(models) == 0:
        print(Fore.YELLOW + 
              "\nThere is no trained models! Train some one!\n")

    if(Show):
        for i in range(len(models)):
            print(Fore.YELLOW + str(i + 1) + " : " + str(models[i])[5:len(models[i]) - 6])

        print("\n")

    return models


#Show all selected victims in do_ignore.txt
def show_ignoring_victims():
    size = os.path.getsize("Data/do_ignore.txt")
    if size == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should Select at least one victim!\n")
        
        raise Exception("Empty do_ignore file")
        
    with open("Data/do_ignore.txt", 'r') as f:
        for line in f:
            name = line.strip()
            print(Fore.YELLOW + name[6:len(name) - 4] + 
                  " is ignoring now!")
            
        print(Fore.LIGHTGREEN_EX + 
              "\nEnjoy the calm!")

