import asyncio

from Model.QA_model import *
from Model.Tokenizer import *
from Users_interfece.interface import *
from Telegram.MonitoringByName import *
from Data_manupulation.test_selection import *
from Users_interfece.helpers import *

from colorama import Fore

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
                print(Fore.LIGHTRED_EX + "\nYou should has at least one model to select it!\n")
                selected_victim_handler(victim)
                return

            try:
                model_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect model by id: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should select existable model!\n")
                selected_victim_handler(victim)
                return 
            
            #Selected index out of range
            if model_id > len(models):
                print(Fore.LIGHTRED_EX + "\nSelect existable model!\n")
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
                print(Fore.LIGHTGREEN_EX + "\nModel: " + model_name[5:len(model_name) - 3] + "\nTokinazer: " + tokinazer_name[5:len(tokinazer_name) - 5] + "\n")

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
            if len(victim) == 0:
                print(Fore.LIGHTRED_EX + "\nYou should has at least one victim to select it!\n")
                await victim_handler(client)
                return 

            #Try to choose victim 
            try:
                victim_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect victim by id: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should select existable victim!\n")
                await victim_handler(client)
                return 

            #Selected index out of range
            if victim_id > len(victims):
                print(Fore.LIGHTRED_EX + "\nYou should select existable victim\n")
                await victim_handler(client)
                return 
            
            #Successful selection
            victim = victims[victim_id - 1]
            print(Fore.LIGHTGREEN_EX + "\n" + victim[5:len(victim) - 4] + " has been selected as victim!\n")

            #Go to selected_victim_handler
            selected_victim_handler(victim)

            #Back to victim_handler with no command, but with victim name
            await victim_handler(client, victim = victim)
            return 
        
        #Create new victim handler
        case "Victim new":
            #Try to find telegram accaunt
            victim = input(Fore.LIGHTWHITE_EX + "\nEnter telegram link of victim as @My_friend: ")

            #Victims name should starts with '@'
            if victim[0] != "@":
                #If not back to victim_handler
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_friend\n")
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
                print(Fore.LIGHTRED_EX + "\nPlease, select the victim!\n")
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
                print(Fore.LIGHTRED_EX + "\nVictim configuration should not be empty! Set the model to ignore victim!\n")
                await victim_handler(client)
                return 
            
            #If victim configuration is not empty load models & tokinazer names
            model = full_path_load_QA_model(model_name)
            tokenizer = full_path_load_tokinazer(tokinazer_name)

            #Try to load models configurations
            try:
                with open(model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                    maxWordsCount = int(f.readline())
                    sequences_len = int(f.readline())
            except Exception:
                #If model confuguration empty - back to victim_handler
                print(Fore.LIGHTRED_EX + "\nModel configuration cannot be empty!\n")
                await victim_handler(client)
                return
            
            #Get new Thread to ignore person
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


#Models handler provides manipulations with models 
async def models_handler(client, command = None):
    #If last command finished ask again
    if command == None:
        command = models_menu()

    #Switch between models commands
    match command:
        #Show all trained models
        case "Models show":
            get_all_models()

            #Back to model menu
            await models_handler(client)
            return 
        
        #Get information about model base on model configuration
        case "Models info":
            #Show all models
            models = get_all_models()

            #Try to get id from user
            try:
                selected_model_id = int(input(Fore.LIGHTWHITE_EX + "\nEnter model id: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should select existable model!\n")
                await models_handler(client)
                return 

            #Selected index out of range
            if selected_model_id > len(models):
                print(Fore.LIGHTRED_EX + "\n" + str(selected_model_id) + " model does not exist!\n")

                #Back to models menu
                await models_handler(client)
                return 
            
            #Load model by name & show models architecture
            model = full_path_load_QA_model(models[int(selected_model_id) - 1])
            model.summary()

            #Show hiddent params that store in model configuration
            model_name = models[int(selected_model_id) - 1]
            with open("Data/" + model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + "\nmaxWordsCount: " + str(maxWordsCount) + ", sequences_len: " + str(sequences_len) + "\n")
            
            #Back to models_menu_handler
            await models_handler(client)
            return 
        
        #Train new model option
        case "Models train":
            #Try to find conversation with person by name
            train_victim = input(Fore.LIGHTWHITE_EX + "\nEnter person and model will train base on your conversation (like @My_friend): ")
            if train_victim[0] != "@":
                #Victims name should starts with '@'
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_friend\n")

                #Back to models_handler
                await models_handler(client)
                return 
            
            #Get number of messages to upload from conversation
            num_messages = input(Fore.LIGHTWHITE_EX + "\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                #If 'None' upload full conversation
                print(Fore.YELLOW + "\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")

            else :
                try:
                    #Try to convert num_messages into int
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    #Catch exception if cannot convert and back to models_handler 
                    print(Fore.LIGHTRED_EX + "\nPlease enter number of messages!\n")
                    await models_handler(client)
                    return 
                
            #Upload num_messages messeges from conversation 
            print(Fore.YELLOW + "\nStart loading data. This can take a while!\n") 
            X, Y = await GetTrainDataByName(train_victim, client, num_messages)
            print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")

            #Try to get vocabulary size
            try:
                maxWordsCount = int(input(Fore.LIGHTWHITE_EX + "\nEnter size of vocabulary: "))
            except (TypeError, ValueError):
                #If cannot covert to int back to models_handler
                print(Fore.LIGHTRED_EX + "\nYou should enter size of vocabulary!\n")
                await models_handler(client)
            
            #Get 'lower' param
            try:
                lower = int(input(Fore.LIGHTWHITE_EX + "\nEnter 1 if you want only low register messeges, 0 for high & low register messages: "))
                if lower == 1:
                    lower = True
                elif lower == 0:
                    lower = False
                else:
                    #If input not 0 or 1 back to models_handler
                    print(Fore.LIGHTRED_EX + "\nYou should enter 1 or 0 to set register!\n")
                    await models_handler(client)
                    return 
            except (TypeError, ValueError):
                    #If input not int
                    print(Fore.LIGHTRED_EX + "\nYou should enter 1 or 0 to set register!\n")
                    await models_handler(client)
                    return 
            
            #Get num of LSTM dims
            try:
                latent_dim = int(input(Fore.LIGHTWHITE_EX + "\nEnter hidden LSTM layer neurons: "))
            except (TypeError, ValueError):
                #If not int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter number of hidden LSTM layer neurons!\n")
                await models_handler(client)
                return 
            
            #Try to get sequences_len 
            try:
                sequences_len = int(input(Fore.LIGHTWHITE_EX + "\nEnter sequences length: "))
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter sequences length!\n")
                await models_handler(client)
                return 
            
            #Create model & tokinazer
            tokenizer = get_Tokinazer(X, Y, maxWordsCount, lower, False)
            save_tokinazer(train_victim[1:], tokenizer)
            model = Get_RNN_QA(int(maxWordsCount), latent_dim, sequences_len)

            #Try to get number of epochs
            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + "\nEnter number of epochs: "))
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter number of epochs!\n")
                await models_handler(client, model)
                return 
            
            #Try to get batch size
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + "\nEnter batch size: "))
            except (TypeError, ValueError):
                #If intput is not int go to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter batch size!\n")
                await models_handler(client)
                return 
            
            #Try to get messeges per pack
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + "\nEnter messages per pack: "))
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter number messeages per pack!\n")
                await models_handler(client)
                return 

            #Do train model 
            print(Fore.LIGHTGREEN_EX + "\nStart training model!\n")
            model = QA_model_train(train_victim[1:], model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print(Fore.LIGHTGREEN_EX + "\nModel has been traind!\n")

            #Save model in .h5
            save_QA_model(train_victim[1:], model)

            #Save model configuration
            with open("Data/" + train_victim[1:] + "_model_configuration.txt", 'w') as f:
                f.write(str(maxWordsCount) + "\n")
                f.write(str(sequences_len) + "\n")
            
            #Back to models menu
            await models_handler(client)
            return
        
        #Train more existable model
        case "Models learn more":
            #Show all models
            models = get_all_models()

            #Try to get get model by id
            try:
                model_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect model by id acording the list: "))
            except (TypeError, ValueError):
                #If input is not integer
                print(Fore.LIGHTRED_EX + "\nYou should select existable model!\n")
                await models_handler(client)
                return
            
            #If index out of range back to models menu
            if model_id > len(models):
                print(Fore.LIGHTRED_EX + "\nYou should select existable model!\n")
                await models_handler(client)
                return

            #Upload model & tokinazer
            print(Fore.LIGHTGREEN_EX + "\n" + str(models[int(model_id) - 1]) + " has been selected!\n")
            model = full_path_load_QA_model(models[int(model_id) - 1])
            tokenizer = full_path_load_tokinazer(get_Tokinazer_by_model(models[int(model_id) - 1]))

            model.summary()

            #Get data from model configuration
            model_name = models[int(model_id) - 1]
            with open(model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + "\nmaxWordsCount: " + str(maxWordsCount) + ", sequences_len: " + str(sequences_len) + "\n")

            #Select person to train more model base on prev conversation 
            train_victim = input(Fore.LIGHTWHITE_EX + "\nEnter person and model will train base on your conversation (like @My_friend): ")
            if train_victim[0] != "@":
                #Victim name should starts with '@'
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_friend\n")
                await models_handler(client, command, train_victim)
                return 

            #Choose number of messeges
            num_messages = input(Fore.LIGHTWHITE_EX + "\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                #Upload full conversation
                print(Fore.YELLOW + "\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")
            else :
                try:
                    #Try to convert input into int
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    #If cannot back to models menu
                    print(Fore.LIGHTRED_EX + "\nPlease enter number of messages!\n")
                    await models_handler(client, command)
                    return 
                
                #Upload data from conversation
                print(Fore.YELLOW + "\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client, num_messages)
                print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")

            #Try to get number of epochs
            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + "\nEnter number of epochs: "))
            except (TypeError, ValueError):
                #If cannot conver input in int, back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter number of epochs!\n")
                await models_handler(client, model)
                return 
            
            #Try to get batch_size
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + "\nEnter batch size: "))
            except (TypeError, ValueError):
                #If cannot convert input into int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter batch size!\n")
                await models_handler(client, command)
                return 
            
            #Try to get messages_per_pack
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + "\nEnter messages per pack: "))
            except (TypeError, ValueError):
                #If cannot convert input into int back to models menu
                print(Fore.LIGHTRED_EX + "\nYou should enter number messeages per pack!\n")
                await models_handler(client, command)
                return 
            
            #Do train more model
            print(Fore.LIGHTGREEN_EX + "\nStart training model!\n")
            model = QA_model_train(train_victim[1:], model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print(Fore.LIGHTGREEN_EX + "\nModel has been traind!\n")

            #Save model
            save_QA_model(train_victim[1:], model)

            #Back to models menu
            await models_handler(client)
            return
            
        #BAck to main menu
        case "Models back":
            return 
        
        #Get information about commands in models menu
        case "Models help":
            models_helper()
            await models_handler(client)
            return

    return 


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
                await main_handler(client)
                return
            
            await client.run_until_disconnected()
            await main_handler(client)
            return

        #Get help abut main menu, than back to main menu with no command
        case "Main help":
            main_helper()
            await main_handler(client)
            return

        #Leave the application 
        case "Exit":
            print(Fore.YELLOW + "\nHave a good day!\n")
            exit()

