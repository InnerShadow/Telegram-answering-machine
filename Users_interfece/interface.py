import os
import glob

from colorama import Fore

from Users_interfece.save_load_functions import *

#Gove helpul information to user
def first_launch():
    #Hello message
    print(Fore.GREEN + 
          "\nWelcome to telegram answering machine. This application will helps you to ignore annoying people in telegram."
          "\nThis mean that neural network that was train base your previous conversation will generate messengers to person you don't want to talk right now!"
          "\nEnjoy the calm!\n")
    
    data = glob.glob(os.path.join("Data/", '*.txt'))
    if len(data) == 0:
        #Firts launch helper
        print(Fore.YELLOW + 
              "\nIf it is your first launch you should go to https://my.telegram.org/auth \n"
              "and get api hash & api id to continue using this application.\n")
        
    #Save default answer
    save_default_answer()
        

#Main choise manu
def main_menu():
    print(Fore.GREEN + 
          "\n1: Victims."
          "\n2: Models."
          "\n3: Run ignoring."
          "\n4: Default answer."
          "\n5: Exit"
          "\n6: Help\n")
    
    try:
        state = int(input(Fore.LIGHTWHITE_EX + 
                          "\nSelect modul: "))

    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + 
              "\nNot a number!\n")
        
        return main_menu()
    
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should select existable modul!\n")
        
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
    print(Fore.GREEN + 
          "\n1: Show all victims." 
          "\n2: Select victim by id."
          "\n3: Get new victim."
          "\n4: Add to ignoring list."
          "\n5: Back to main menu"
          "\n6: Help\n")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))

    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + 
              "\nNot a number!!\n")
        
        return victim_menu()
    
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should select existable action!\n")
        
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
    print(Fore.GREEN + 
          "\n1: Set model by id."
          "\n2: Display info"
          "\n3: Back to victim menu"
          "\n4: Help\n")
    
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))

    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + 
              "\nNot a number!\n")
        
        return victim_menu()
    
    if state > 4 or state == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should select existable action!\n")
        
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
    print(Fore.GREEN + 
          "\n1: Show all models"
          "\n2: Get model info by id"
          "\n3: Train new model"
          "\n4: Train more for model"
          "\n5: Back to main menu"
          "\n6: Help")
    try:
        state = int(input(Fore.LIGHTWHITE_EX + "\nSelect modul: "))

    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + 
              "\nNot a number!!\n")
        
        return victim_menu()
    
    if state > 6 or state == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should select existable action!\n")
        
        return models_menu()
    
    match state:
        case 1: 
            return "Models show"
        
        case 2:
            return "Models info"
        
        case 3:
            return "Models train"
        
        case 4: 
            return "Models train more"
        
        case 5:
            return "Models back"
        
        case 6: 
            return "Models help"
        

#Default answer choise menu
def default_answer_menu():
    print(Fore.GREEN + 
          "\n1: Show default answer"
          "\n2: Set default answer"
          "\n3: Back to main menu"
          "\n4: Help.")
    
    try:
        state = int(input(Fore.LIGHTWHITE_EX + 
                          "\nSelect modul: "))
        
    except (TypeError, ValueError):
        print(Fore.LIGHTRED_EX + 
              "\nNot a number!!\n")
        
        return victim_menu()
    
    if state > 4 or state == 0:
        print(Fore.LIGHTRED_EX + 
              "\nYou should select existable action!\n")
        
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

