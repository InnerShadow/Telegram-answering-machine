from colorama import Fore

from Users_interfece.interface import *
from Users_interfece.helpers import *

#Recurrent function that provide users interface in "Selected victim" menu
def selected_victim_handler(victim, command = None):

    #If last command finished ask again
    if command == None:
        command = selected_victim_menu()

    #Switch case on different commands
    match command:

        #Connect selected victim & model 
        case "Selected victim set":
            models = get_all_models()

            #Back to selected_victim_handler if there is no avaible models
            if len(models) == 0:
                print(Fore.LIGHTRED_EX + "\nCreate a model first!\n")
                selected_victim_handler(victim)
                return

            try:
                model_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect model by id: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nThis module does not exist!\n") #You should select existable model!
                selected_victim_handler(victim)
                return 
            
            #Selected index out of range
            if model_id > len(models):
                print(Fore.LIGHTRED_EX + "\nThis module does not exist!\n")
                selected_victim_handler(victim)
                return 
            
            #Successful selection 
            print(Fore.LIGHTGREEN_EX + "\n" + models[model_id - 1][5:len(models[model_id - 1]) - 3] + " model has been selected!\n")
            with open(str(victim), 'w') as f:
                f.write(str(models[int(model_id) - 1]) + "\n")
                f.write(str(models[int(model_id) - 1])[:len(str(models[int(model_id) - 1])) - 3] + "_tokenizer.json")

            #Back to selected_victim_handler with no command
            selected_victim_handler(victim)
            return 
        
        #Show connected model & tokenizer on selected victim
        case "Selected victim info":
            with open(str(victim), 'r') as f:
                model_name = f.readline()
                tokinazer_name = f.readline()
                print(Fore.LIGHTGREEN_EX + "\nModel: " + model_name[5:len(model_name) - 4] + "\nTokinazer: " + tokinazer_name[5:len(tokinazer_name) - 5] + "\n")

            #Back to selected_victim_handler with no command
            selected_victim_handler(victim)
            return 
        
        #Print information about all commands in this module
        case "Selected victim help":
            selected_victim_help()

            #Back to selected_victim_handler with no command
            selected_victim_handler(victim)
            return

        #Return to victim menu
        case "Selected victim back":
            return 
    return 

