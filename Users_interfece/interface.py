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

#Gove helpul information to user
def first_launch():
    #Hello message
    print(Fore.GREEN + "\nWelcome to telegram answering machine. This application will helps you to ignore annoying people in telegram."
          "\nThis mean that neural network that was train base your previous conversation will generate messengers to person you don't want to talk right now!"
          "\nEnjoy the calm!\n")
    
    data = glob.glob(os.path.join("Data/", '*.txt'))
    if len(data) == 0:
        #Firts launch helper
        print(Fore.YELLOW + "\nIf it is your first launch you should go to https://my.telegram.org/auth \n"
              "and get api hash & api id to continue using this application.\n")
        
    #Save default answer
    save_default_answer()
        

#Main choise manu
def main_menu():
    print(Fore.GREEN + "\n1: Victims."
          "\n2: Models."
          "\n3: Run igniging."
          "\n4: Default answer."
          "\n5: Exit"
          "\n6: Help\n")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return main_menu()
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + "\nYou should select existable modul!\n")
        return main_menu()
    
    match state:
        case 1:
            return "Victim munu"
        
        case 2:
            return "Models menu"
        
        case 3:
            return "Run"
        
        case 4:
            return "Default"

        case 5:
            return "Exit"
        
        case 6:
            return "Main help"
    

#Victim choise menu
def victim_menu():
    print(Fore.GREEN + "\n1: Show all victims." 
          "\n2: Select victim by id."
          "\n3: Get new victim."
          "\n4: Add to ignoring list."
          "\n5: Back to main menu"
          "\n6: Help\n")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return victim_menu()
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return victim_menu()
    
    match state:
        case 1:
            return "Victim show all"
        
        case 2:
            return "Victim select"
        
        case 3:
            return "Victim new"
        
        case 4:
            return "Victim ignore"
        
        case 5:
            return "Victim back"
        
        case 6:
            return "Victim help"


#Selected victim choise menu
def selected_victim_menu():
    print(Fore.GREEN + "\n1: Set model by id."
          "\n2: Display info"
          "\n3: Back to victim menu"
          "\n4: Help\n")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return victim_menu()
    if state > 4 or state == 0:
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
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


#Model choise menu
def models_menu():
    print(Fore.GREEN + "\n1: Show all models"
          "\n2: Get model info by id"
          "\n3: Train new model"
          "\n4: Learn more for model"
          "\n5: Back to main menu"
          "\n6: Help")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return victim_menu()
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
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
        

#Default answer choise menu
def default_answer_menu():
    print(Fore.GREEN + "\n1: Show default answer"
          "\n2: Set default answer"
          "\n3: Back to main menu"
          "\n4: Help.")
    
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return victim_menu()
    if state > 4 or state == 0:
        print(Fore.LIGHTRED_EX + "\nYou should select existable action!\n")
        return models_menu()
    
    match state:
        case 1:
            return "Default show"
        
        case 2:
            return "Default set"
        
        case 3:
            return "Default back"
        
        case 4:
            return "Default help"


#Do log in telegram
async def log_in(phone, apiid, apihash):
    print(Fore.YELLOW + "\nTry to connect to telegram: \n")
    #Try to connect to telegram base on prev session
    client = TelegramClient(phone, apiid, apihash)
    await client.connect()

    #If cannot connect ask users telegram data 
    try:
        if not await client.is_user_authorized():
            print(Fore.YELLOW + "\nCannot find previous session, enter following data: \n")
            await client.send_code_request(phone)
            try :
                await client.sign_in(GetPhoneNumber(), code = input(Fore.LIGHTWHITE_EX + '\nEnter the code: \n'))
            except Exception:
                password = input(Fore.LIGHTWHITE_EX + "\nEnter password: \n")
                client = await client.sign_in(password = password)
    except Exception:
        print(Fore.LIGHTRED_EX + "\nCannot login Telegram!\n")
        return None

    print(Fore.LIGHTGREEN_EX + "\nConnected succsessfull!\n")

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
    if(Show):
        for i in range(len(victiums)):
            print(Fore.YELLOW + str(i + 1) + " : " + str(victiums[i])[5:len(victiums[i]) - 4])
        print("\n")

    return victiums


#Show all models
def get_all_models(Show = True):
    models = glob.glob(os.path.join("Data/", "*.h5"))
    if(Show):
        for i in range(len(models)):
            print(Fore.YELLOW + str(i + 1) + " : " + str(models[i])[5:len(models[i]) - 3])
        print("\n")

    return models


#Show all selected victims in do_ignore.txt
def show_ignoring_victims():
    size = os.path.getsize("Data/do_ignore.txt")
    if size == 0:
        print(Fore.LIGHTRED_EX + "\nYou should Select at least one victim!\n")
        raise Exception("Empty do_ignore file")
    
    with open("Data/do_ignore.txt", 'r') as f:
        for line in f:
            name = line.strip()
            print(Fore.YELLOW + name[6:len(name) - 4] + " is ignoring now!")
        print(Fore.LIGHTGREEN_EX + "\nEnjoy the calm!")

