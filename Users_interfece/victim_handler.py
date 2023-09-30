from colorama import Fore

from Users_interfece.interface import *
from Telegram.MonitoringByName import *
from Users_interfece.helpers import *
from Users_interfece.selected_victim_handler import *

#Recurrent function that provide users interface in "Victim" menu
async def victim_handler(client, command = None, victim = None):

    #If last command finished ask again
    if command == None:
        command = victim_menu()

    #Switch case on different commands
    match command:
        #Show all creted victims
        case "Victim show all":
            #Show all victims
            get_all_victiums()

            #Back to victim_handler with no command
            await victim_handler(client)
            return 
        
        #Select victim by id handler
        case "Victim select":
            #Show all victims
            victims = get_all_victiums()

            #If there is no avaible victims, back to victim menu
            if len(victims) == 0:
                print(Fore.LIGHTRED_EX + 
                      "\nCreate a victim first!\n")
                
                await victim_handler(client)
                return 

            #Try to choose victim 
            try:
                victim_id = int(input(Fore.LIGHTWHITE_EX + 
                                      "\nSelect victim by id: "))
                
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + 
                      "\nThis victim does not exist!\n")
                
                await victim_handler(client)
                return 

            #Selected index out of range
            if victim_id > len(victims):
                print(Fore.LIGHTRED_EX + 
                      "\nThis victim does not exist!\n")
                
                await victim_handler(client)
                return 
            
            #Successful selection
            victim = victims[victim_id - 1]
            print(Fore.LIGHTGREEN_EX + 
                  "\n" + victim[5:len(victim) - 4] + " has been selected as victim!\n")

            #Go to selected_victim_handler
            selected_victim_handler(victim)

            #Back to victim_handler with no command, but with victim name
            await victim_handler(client, victim = victim)
            return 
        
        #Create new victim handler
        case "Victim new":
            #Try to find telegram accaunt
            victim = input(Fore.LIGHTWHITE_EX + 
                           "\nEnter telegram link of victim as @My_friend: ")

            #Victims name should starts with '@'
            if victim[0] != "@":
                #If not back to victim_handler
                print(Fore.LIGHTRED_EX + 
                      "\nError! Correct form: @My_friend\n")
                
                await victim_handler(command)
                return 

            #Create empty .txt victim configuration
            victim = "Data/" + victim + ".txt"
            with open(str(victim), 'w') as f:
                f.write(" ")
            
            #Back to victim menu
            await victim_handler(client, victim = victim)
            return 
        
        #Add victim to ingroning list 
        case "Victim ignore":
            #If victim do not selected back to victim_handler
            if victim == None:
                print(Fore.LIGHTRED_EX + 
                      "\nPlease, select the victim!\n")
                
                await victim_handler(client)
                return 
            
            #If victim was selected try to upload params from victim configuration
            model_name = ""
            tokinazer_name = ""
            with open(str(victim), 'r') as f:
                model_name = f.readline()[:len(model_name) - 1]
                tokinazer_name = f.readline()
            
            #Check if victim configuration if empty
            if model_name == "" or tokinazer_name == "":
                print(Fore.LIGHTRED_EX + 
                      "\nError! Set a model to ignore the victim!\n")
                
                await victim_handler(client)
                return 
            
            #If victim configuration is not empty load models & tokinazer names
            model = full_path_load_QA_model(model_name)
            tokenizer = full_path_load_tokinazer(tokinazer_name)

            #Try to load models configurations
            try:
                with open(model_name[:len(model_name) - 6] + "_model_configuration.txt", 'r') as f:
                    maxWordsCount = int(f.readline())
                    sequences_len = int(f.readline())

            except Exception:
                #If model confuguration empty - back to victim_handler
                print(Fore.LIGHTRED_EX + 
                      "\nWrog parameters of model training. Retrain the model!\n")
                
                await victim_handler(client)
                return
            
            #Add victim cinfiguration to ignoting list
            await MonitoringByName(victim, client, model, tokenizer, sequences_len)

            #Save ignoring persion in do_ignore .txt file
            with open("Data/do_ignore.txt", 'a') as f:
                f.write(victim + "\n")

            #await MonitoringByName()
            await victim_handler(client)
            return 

        #Back to victim menu
        case "Victim back":
            return 
        
        #Get information about all comands in menu
        case "Victim help":
            victim_helper()
            await victim_handler(client)
            return

    return 

