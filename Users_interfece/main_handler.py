from colorama import Fore

from Users_interfece.helpers import *
from Users_interfece.victim_handler import *
from Users_interfece.model_handler import *
from Users_interfece.default_answer_handler import *

#Main handler - main users interface function to use application
async def main_handler(client, command = None):
    if command == None:
        command = main_menu()

    match command:
        #Go to victim menu, than back to main menu with no command
        case "Victim munu":
            await victim_handler(client, victim_menu())
            await main_handler(client)
            return

        #Go to models menu, than back to main menu with no command
        case "Models menu":
            await models_handler(client, models_menu())
            await main_handler(client)
            return
        
        #Start ignoging all victims
        case "Run":
            #Try to load victims, if empty say it to user
            try:
                show_ignoring_victims()
            except Exception:
                print(Fore.LIGHTRED_EX + 
                      "\nThere is no selected vicmims! Select one or more!\n")
                await main_handler(client)
                return
            
            await client.run_until_disconnected()
            await main_handler(client)
            return
        
        #Allow to configure default answer
        case "Default":
            default_answer_handler(default_answer_menu())
            await main_handler(client)
            return

        #Get help abut main menu, than back to main menu with no command
        case "Main help":
            main_helper()
            await main_handler(client)
            return

        #Leave the application 
        case "Exit":
            print(Fore.YELLOW + 
                  "\nHave a good day!\n")
            
            exit()

