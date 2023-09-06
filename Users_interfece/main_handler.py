import asyncio

from Model.QA_model import *
from Model.Tokenizer import *
from Users_interfece.interface import *
from Telegram.MonitoringByName import *
from Data_manupulation.test_selection import *
from Users_interfece.helpers import *

from colorama import Fore, Style


def selected_victim_handler(victim, command = None):
    print(Style.RESET_ALL)

    if command == None:
        command = selected_victim_menu()

    match command:
        case "Selected victim set":
            models = get_all_models()
            model_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect model by id: "))
            if model_id > len(models):
                print(Fore.LIGHTRED_EX + "\nSelect existable model!\n")
                selected_victim_handler(victim)
                print(Style.RESET_ALL)
                return 
            
            print(Fore.LIGHTLIGHTGREEN_EX_EX + "\n" + models[model_id - 1][5:len(models[model_id - 1]) - 3] + " model has been selected!\n")
            with open(str(victim), 'w') as f:
                f.write(str(models[int(model_id) - 1]) + "\n")
                f.write(str(models[int(model_id) - 1])[:len(str(models[int(model_id) - 1])) - 3] + "_tokenizer.json")

            print(Style.RESET_ALL)

            selected_victim_handler(victim)
            return 
        
        case "Selected victim info":
            with open(str(victim), 'r') as f:
                print(Fore.LIGHTGREEN_EX + "\nModel: " + f.readline() + "\nTokinazer: " + f.readline() + "\n")

            print(Style.RESET_ALL)
            
            selected_victim_handler(victim)

            return 
        
        case "Selected victim help":
            selected_victim_help()
            selected_victim_handler(victim)
            return

        case "Selected victim back":
            return 
    return 


async def victim_handler(client, command = None, victim = None):
    print(Style.RESET_ALL)

    if command == None:
        command = victim_menu()

    match command:
        case "Victim show all":
            get_all_victiums()

            await victim_handler(client)
            return 
        
        case "Victim select":
            victims = get_all_victiums()

            victim_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect victim by id: "))
            if victim_id > len(victims):
                print(Fore.LIGHTRED_EX + "\nYou should select existable victim\n")
                print(Style.RESET_ALL)
                await victim_handler(client, command)
                return 
            
            victim = victims[victim_id - 1]
            print(Fore.LIGHTGREEN_EX + "\n" + victim[5:len(victim) - 4] + " has been selected as victim!\n")
            print(Style.RESET_ALL)
            selected_victim_handler(victim)
            await victim_handler(client, victim = victim)
            return 
        
        case "Victim new":
            victim = input(Fore.LIGHTWHITE_EX + "\nEnter telegram link of victim as @My_frind: ")
            if victim[0] != "@":
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_frind\n")
                print(Style.RESET_ALL)
                await victim_handler(command)
                return 

            victim = "Data/" + victim + ".txt"
            with open(str(victim), 'w') as f:
                f.write(" ")
            
            await victim_handler(client, victim = victim)
            return 
        
        case "Victim do ignore":
            if victim == None:
                print(Fore.LIGHTRED_EX + "\nPlease, select the victim!\n")
                print(Style.RESET_ALL)
                await victim_handler(client)
                return 
            
            model_name = ""
            tokinazer_name = ""
            with open(str(victim), 'r') as f:
                model_name = f.readline()[:len(model_name) - 1]
                tokinazer_name = f.readline()
            
            if model_name == "" or tokinazer_name == "":
                print(Fore.LIGHTRED_EX + "\nVictim configuration should not be empty! Set the model to ignore victim!\n")
                print(Style.RESET_ALL)
                await victim_handler(client)
                return 
            
            model = full_path_load_QA_model(model_name)
            tokenizer = full_path_load_tokinazer(tokinazer_name)

            try:
                with open("Data/" + model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                    maxWordsCount = int(f.readline())
                    sequences_len = int(f.readline())
            except Exception:
                print(Fore.LIGHTRED_EX + "\nModel configuration cannot be empty!\n")
                print(Style.RESET_ALL)
                await victim_handler(client)
                return
            
            asyncio.run(await MonitoringByName(victim, client, model, tokenizer, sequences_len))
            await victim_handler(client)
            return 

        case "Victim back":
            return 
        
        case "Victim help":
            victim_helper()
            await victim_handler(client)
            return

    return 


async def models_handler(client, command = None):
    print(Style.RESET_ALL)

    if command == None:
        command = models_menu()

    match command:
        case "Models show":
            get_all_models()

            await models_handler(client)
            return 
        
        case "Models info":
            models = get_all_models()

            selected_model_id = int(input(Fore.LIGHTWHITE_EX + "\nEnter model id: "))
            if selected_model_id > len(models):
                print(Fore.LIGHTRED_EX + "\n" + str(selected_model_id) + " model does not exist!\n")
                print(Style.RESET_ALL)
                await models_handler(client)
                return 
            
            model = full_path_load_QA_model(models[int(selected_model_id) - 1])
            model.summary()

            model_name = models[int(selected_model_id) - 1]
            with open("Data/" + model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + "\nmaxWordsCount: " + str(maxWordsCount) + ", sequences_len: " + str(sequences_len) + "\n")
            print(Style.RESET_ALL)
            
            await models_handler(client)
            return 
        
        case "Models train":
            train_victim = input(Fore.LIGHTWHITE_EX + "\nEnter person and model will train base on your conversation (like @My_frind): ")
            if train_victim[0] != "@":
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_frind\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 
            
            num_messages = input(Fore.LIGHTWHITE_EX + "\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                print(Fore.YELLOW + "\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")
                print(Style.RESET_ALL)
            else :
                try:
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    print(Fore.LIGHTRED_EX + "\nPlease enter number of messages!\n")
                    print(Style.RESET_ALL)
                    await models_handler(client, command)
                    return 
                
            print(Fore.YELLOW + "\nStart loading data. This can take a while!\n") 
            X, Y = await GetTrainDataByName(train_victim, client, num_messages)
            print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")
            print(Style.RESET_ALL)

            try:
                maxWordsCount = int(input(Fore.LIGHTWHITE_EX + "\nEnter size of vocabulary: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter size of vocabulary!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
            
            try:
                lower = int(input(Fore.LIGHTWHITE_EX + "\nEnter 1 if you want only low register messeges, 0 for high & low register messages: "))
                if lower == 1:
                    lower = True
                elif lower == 0:
                    lower = False
                else:
                    print(Fore.LIGHTRED_EX + "\nYou should enter 1 or 0 to set register!\n")
                    print(Style.RESET_ALL)
                    await models_handler(client, command)
                    return 
            except (TypeError, ValueError):
                    print(Fore.LIGHTRED_EX + "\nYou should enter 1 or 0 to set register!\n")
                    print(Style.RESET_ALL)
                    await models_handler(client, command)
                    return 
            
            try:
                latent_dim = int(input(Fore.LIGHTWHITE_EX + "\nEnter hidden LSTM layer neurons: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter number of hidden LSTM layer neurons!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 
            tokenizer = get_Tokinazer(X, Y, maxWordsCount, lower, False)
            save_tokinazer(train_victim[1:], tokenizer)
            model = Get_RNN_QA(int(maxWordsCount), latent_dim)

            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + "\nEnter number of epochs: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter number of epochs!\n")
                print(Style.RESET_ALL)
                await models_handler(client, model)
                return 
            
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + "\nEnter batch size: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter batch size!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 
            
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + "\nEnter messages per pack: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter number messeages per pack!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 
            
            try:
                sequences_len = int(input(Fore.LIGHTWHITE_EX + "\nEnter sequences length: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter sequences length!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 

            print(Fore.LIGHTGREEN_EX + "\nStart training model!\n")
            model = QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print(Fore.LIGHTGREEN_EX + "\nModel has been traind!\n")
            save_QA_model(train_victim[1:], model)
            print(Style.RESET_ALL)

            with open("Data/" + train_victim[1:] + "_model_configuration.txt", 'w') as f:
                f.write(str(maxWordsCount) + "\n")
                f.write(str(sequences_len) + "\n")
            
            await models_handler(client)
            return
        
        case "Models learn more":
            models = get_all_models()
            try:
                model_id = int(input(Fore.LIGHTWHITE_EX + "\nSelect model by id acording the list: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should select existable model!\n")
                print(Style.RESET_ALL)
                models_handler(client)
                return
            print(Fore.LIGHTGREEN_EX + "\n" + str(models[int(model_id) - 1]) + " has been selected!\n")
            print(Style.RESET_ALL)
            model = full_path_load_QA_model(models[int(model_id) - 1])
            tokenizer = full_path_load_tokinazer(get_Tokinazer_by_model(models[int(model_id) - 1]))

            model.summary()

            model_name = models[int(model_id) - 1]
            with open("Data/" + model_name[:len(model_name) - 3] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + "\nmaxWordsCount: " + str(maxWordsCount) + ", sequences_len: " + str(sequences_len) + "\n")
            print(Style.RESET_ALL)

            train_victim = input(Fore.LIGHTWHITE_EX + "\nEnter person and model will train base on your conversation (like @My_frind): ")
            if train_victim[0] != "@":
                print(Fore.LIGHTRED_EX + "\nYou should enter link like @My_frind\n")
                print(Style.RESET_ALL)
                await models_handler(client, command, train_victim)
                return 

            num_messages = input(Fore.LIGHTWHITE_EX + "\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                print(Fore.YELLOW + "\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print(Fore.LIGHTGREEN_EX + "\nData has been loaded!\n")
                print(Style.RESET_ALL)
            else :
                try:
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    print(Fore.LIGHTRED_EX + "\nPlease enter number of messages!\n")
                    print(Style.RESET_ALL)
                    await models_handler(client, command)
                    return 
                X, Y = await GetTrainDataByName(train_victim, client, num_messages)

            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + "\nEnter number of epochs: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter number of epochs!\n")
                print(Style.RESET_ALL)
                await models_handler(client, model)
                return 
            
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + "\nEnter batch size: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter batch size!\n")
                print(Style.RESET_ALL)
                await models_handler(client, command)
                return 
            
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + "\nEnter messages per pack: "))
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + "\nYou should enter number messeages per pack!\n")
                await models_handler(client, command)
                return 
            
            with open("Data/" + train_victim[1:] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.LIGHTGREEN_EX + "\nStart training model!\n")
            model = QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print(Fore.LIGHTGREEN_EX + "\nModel has been traind!\n")
            print(Style.RESET_ALL)
            save_QA_model(train_victim[1:], model)
            await models_handler(client)
            return
            
        case "Models back":
            return 
        
        case "Models help":
            models_helper()
            await models_handler(client)
            return

    return 


async def main_handler(client, command = None):
    print(Style.RESET_ALL)

    if command == None:
        command = main_menu()

    match command:
        case "Victim munu":
            await victim_handler(client, victim_menu())
            await main_handler(client)
            return

        case "Models menu":
            await models_handler(client, models_menu())
            await main_handler(client)
            return

        case "Main help":
            main_helper()
            await main_handler(client)
            return

        case "Exit":
            print(Fore.YELLOW + "\nHave a good day!\n")
            print(Style.RESET_ALL)
            exit()

