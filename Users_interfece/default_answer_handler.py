from colorama import Fore

from Users_interfece.interface import *
from Users_interfece.helpers import *

#Default answer handler
def default_answer_handler(command = None):
    if command == None:
        command = default_answer_menu()

    match command:
        #Show Default answer
        case "Default show":
            with open("Data/default_answer.txt", 'r') as f:
                default_answer = f.read()
                print(Fore.LIGHTGREEN_EX + "\nDefault answer: " + default_answer + "\n")
            default_answer_handler()
            return
        
        #Set Default answer
        case "Default set":
            #Get default answer from user
            default_answer = input(Fore.WHITE + "\nEnter default answer: ")

            #If user do nothing
            if len(default_answer) == 0:
                print(Fore.LIGHTRED_EX + "\nYou should enter some default answer!\n")
                default_answer_handler()
                return

            #Else save it into .txt file 
            with open("Data/default_answer.txt", 'w') as f:
                f.write(default_answer)

            default_answer_handler()
            return
        
        case "Default back":
            return
        
        case "Default help":
            default_answer_helper()
            default_answer_handler()
            return
        
    return

