import os
import glob

from telethon.sync import TelegramClient

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

def first_launch():
    print("\nWelcome to telegram answering machine. This application will helps you to ignore annoying people in telegram."
          "\nThis mean that neural network that was train base your previous conversation will send messengers to person you don't want to talk right now!"
          "\nEnjoy the calm!\n")
    data = glob.glob(os.path.join("Data/", '*.txt'))
    if len(data) == 0:
        print("\nIf it is your first launch you should go to https://my.telegram.org/auth \n"
              "and get api hash & api id to continue using this application.\n")
        

def main_menu():
    print("\n1: Victims."
          "\n2: Models."
          "\n3: Exit"
          "\n4: Help\n")
    state = int(input("\nSelect modul: "))
    if state > 4 or state == 0:
        print("\nYou should select existable modul!\n")
        return main_menu()
    
    match state:
        case 1:
            return "Victim munu"
        
        case 2:
            return "Models menu"
        
        case 3:
            return "Exit"
        
        case 4:
            return "Main help"
    

def victim_menu():
    print("\n1: Show all victims." 
          "\n2: Select victim by id."
          "\n3: Get new victim."
          "\n4: Start ignoring."
          "\n5: Back to main menu"
          "\n6: Help\n")
    try:
        state = int(input("\nSelect modul: "))
    except (TypeError, ValueError):
        print("\nYou should select existable action!\n")
        return victim_menu()
    if state > 6 or state == 0:
        print("\nYou should select existable action!\n")
        return victim_menu()
    
    match state:
        case 1:
            return "Victim show all"
        
        case 2:
            return "Victim select"
        
        case 3:
            return "Victim new"
        
        case 4:
            return "Victim do ignore"
        
        case 5:
            return "Victim back"
        
        case 6:
            return "Victim help"


def selected_victim_menu():
    print("\n1: Set model by id."
          "\n2: Display info"
          "\n3: Back to victim menu"
          "\n4: Help\n")
    try:
        state = int(input("\nSelect modul: "))
    except (TypeError, ValueError):
        print("\nYou should select existable action!\n")
        return victim_menu()
    if state > 4 or state == 0:
        print("\nYou should select existable action!\n")
        return selected_victim_menu()
    
    match state:
        case 1:
            return "Selected victim set"
        
        case 2:
            return "Selected victim info"
        
        case 3:
            return "Selected victim back"
        
        case 4: 
            return "Selected victim help"


def models_menu():
    print("\n1: Show all models"
          "\n2: Get model info by id"
          "\n3: Train new model"
          "\n4: Learn more for model"
          "\n5: Back to main menu"
          "\n6: Help")
    try:
        state = int(input("\nSelect modul: "))
    except (TypeError, ValueError):
        print("\nYou should select existable action!\n")
        return victim_menu()
    if state > 6 or state == 0:
        print("\nYou should select existable action!\n")
        return models_menu()
    
    match state:
        case 1: 
            return "Models show"
        
        case 2:
            return "Models info"
        
        case 3:
            return "Models train"
        
        case 4: 
            return "Models learn more"
        
        case 5:
            return "Models back"
        
        case 6: 
            return "Models help"


async def log_in(phone, apiid, apihash):
    print("\nTry to connect to telegram: \n")
    client = TelegramClient(phone, apiid, apihash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            print("\nCannot find previous session, enter following data: \n")
            await client.send_code_request(phone)
            try :
                await client.sign_in(GetPhoneNumber(), code = input('\nEnter the code: \n'))
            except Exception:
                password = input("\nEnter password: \n")
                client = await client.sign_in(password = password)
    except Exception:
        print("\nCannot login Telegram!\n")
        return None

    print("\nConnected succsessfull!\n")

    return client


def application_api():
    phone =  GetPhoneNumber()
    apiid = GetAPIID()
    apihash = GETAPI_Hash()

    return phone, apiid, apihash


def get_all_victiums(Show = True):
    victiums = glob.glob(os.path.join("Data/", "@*.txt"))
    if(Show):
        for i in range(len(victiums)):
            print(str(i + 1) + " : " + str(victiums[i]))
        print("\n")

    return victiums


def get_all_models(Show = True):
    models = glob.glob(os.path.join("Data/", "*.h5"))
    if(Show):
        for i in range(len(models)):
            print(str(i + 1) + " : " + str(models[i]))
        print("\n")

    return models

