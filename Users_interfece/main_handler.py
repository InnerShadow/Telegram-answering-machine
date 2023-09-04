import asyncio

from Model.QA_model import *
from Model.Tokenizer import *
from Users_interfece.interface import *
from Telegram.MonitoringByName import *
from Data_manupulation.test_selection import *


def selected_victim_handler(victim, command = None):
    if command == None:
        command = selected_victim_menu()
    match command:
        case "Selected victim set":
            models = get_all_models()
            model_id = int(input("\nSelect model by id: "))
            if model_id > len(models):
                print("\nSelect existable model!\n")
                selected_victim_handler(victim)
                return 
            print("\n" + models[model_id - 1] + " has been selected!\n")
            with open(str(victim), 'w') as f:
                f.write(str(models[int(model_id) - 1]) + "\n")
                f.write(str(models[int(model_id) - 1])[:len(str(models[int(model_id) - 1])) - 3] + "_tokenizer.json")
            selected_victim_handler(victim)
            return 
        case "Selected victim info":
            with open(str(victim), 'r') as f:
                print("\nModel: " + f.readline() + "\nTokinazer: " + f.readline() + "\n")
            selected_victim_handler(victim)
            return 
        case "Selected victim back":
            return 
    return 


async def victim_hanfler(client, command = None, victim = None):
    if command == None:
        command = victim_menu()
    match command:
        case "Victim show all":
            get_all_victiums()
            await victim_hanfler(client)
            return 
        case "Victim select":
            victims = get_all_victiums()
            victim_id = int(input("\nSelect victim by id: "))
            if victim_id > len(victims):
                print("\nYou should select existable victim\n")
                await victim_hanfler(client, command)
                return 
            victim = victims[victim_id - 1]
            print("\n" + victim + " has been selected!\n")
            selected_victim_handler(victim)
            await victim_hanfler(client, victim = victim)
            return 
        case "Victim new":
            victim = input("\nEnter telegram link of victim as @My_frind: ")
            if victim[0] != "@":
                print("\nYou should enter link like @My_frind\n")
                await victim_hanfler(command)
                return 
            with open("Data/" + str(victim), 'w') as f:
                f.write(" ")
            victim = "Data/" + victim 
            await victim_hanfler(client, victim = victim)
            return 
        case "Victim do ignore":
            if victim == None:
                print("\nPlease, select the victim!\n")
                await victim_hanfler(client)
                return 
            model_name = ""
            tokinazer_name = ""
            with open(str(victim), 'r') as f:
                model_name = f.readline()[:len(model_name) - 1]
                tokinazer_name = f.readline()
            if model_name == "" or tokinazer_name == "":
                print("\nVictim configuration should not be empty! Set the model to ignore victim!\n")
                await victim_hanfler(client)
                return 
            model = full_path_load_QA_model(model_name)
            tokenizer = full_path_load_tokinazer(tokinazer_name)
            try:
                with open(victim[5:len(victim) - 3] + "_model_configuration.txt", 'r') as f:
                    maxWordsCount = int(f.readline())
                    sequences_len = int(f.readline())
            except Exception:
                print("\nModel configuration cannot be empty!\n")
                await victim_hanfler(client)
                return
            asyncio.run(await MonitoringByName(victim, client, model, tokenizer, sequences_len))
            await victim_hanfler(client)
            return 
        case "Victim back":
            return 
    return 


async def models_handler(client, command = None):
    if command == None:
        command = models_menu()
    match command:
        case "Models show":
            get_all_models()
            await models_handler(client)
            return 
        case "Models info":
            models = get_all_models()
            selected_model_id = int(input("\nEnter model id: "))
            if selected_model_id > len(models):
                print("\n" + str(selected_model_id) + " model does not exist!\n")
                await models_handler(client)
                return 
            model = full_path_load_QA_model(models[int(selected_model_id) - 1])
            model.summary()
            await models_handler(client)
            return 
        case "Models train":
            train_victim = input("\nEnter person and model will train base on your conversation (like @My_frind): ")
            if train_victim[0] != "@":
                print("\nYou should enter link like @My_frind\n")
                await models_handler(client, command, train_victim)
                return 
            num_messages = input("\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                print("\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print("\nData has been loaded!\n")
            else :
                try:
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    print("\nPlease enter number of messages!\n")
                    await models_handler(client, command)
                    return 
                X, Y = await GetTrainDataByName(train_victim, client, num_messages)
            try:
                maxWordsCount = int(input("\nEnter size of vocabulary: "))
            except (TypeError, ValueError):
                print("\nYou should enter size of vocabulary!\n")
                await models_handler(client, command)
            try:
                lower = int(input("\nEnter 1 if you want only low register messeges, 0 for high & low register messages: "))
                if lower == 1:
                    lower = True
                elif lower == 0:
                    lower = False
                else:
                    print("\nYou should enter 1 or 0 to set register!\n")
                    await models_handler(client, command)
                    return 
            except (TypeError, ValueError):
                    print("\nYou should enter 1 or 0 to set register!\n")
                    await models_handler(client, command)
                    return 

            try:
                latent_dim = int(input("\nEnter hidden LSTM layer neurons: "))
            except (TypeError, ValueError):
                print("\nYou should enter number of hidden LSTM layer neurons!\n")
                await models_handler(client, command)
                return 

            tokenizer = get_Tokinazer(X, Y, maxWordsCount, lower, False)
            save_tokinazer(train_victim[1:], tokenizer)
            model = Get_RNN_QA(int(maxWordsCount), latent_dim)
            try:
                epochs = int(input("\nEnter number of epochs: "))
            except (TypeError, ValueError):
                print("\nYou should enter number of epochs!\n")
                await models_handler(client, model)
                return 
            
            try:
                batch_size = int(input("\nEnter batch size: "))
            except (TypeError, ValueError):
                print("\nYou should enter batch size!\n")
                await models_handler(client, command)
                return 
            
            try:
                messages_per_pack = int(input("\nEnter messages per pack: "))
            except (TypeError, ValueError):
                print("\nYou should enter number messeages per pack!\n")
                await models_handler(client, command)
                return 
            
            try:
                sequences_len = int(input("\nEnter sequences length: "))
            except (TypeError, ValueError):
                print("\nYou should enter sequences length!\n")
                await models_handler(client, command)
                return 

            print("\nStart training model!\n")
            model = QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print("\nModel has been traind!\n")
            save_QA_model(train_victim[1:], model)
            await models_handler(client)
            with open(train_victim[1:] + "_model_configuration.txt", 'w') as f:
                f.write(str(maxWordsCount) + "\n")
                f.write(str(sequences_len) + "\n")
            return
        case "Models learn more":
            models = get_all_models()
            try:
                model_id = int(input("\nSelect model by id acording the list: "))
            except (TypeError, ValueError):
                print("\nYou should select existable model!\n")
                models_handler(client)
                return
            print("\n" + str(models[int(model_id) - 1]) + " has been selected!\n")
            model = full_path_load_QA_model(models[int(model_id) - 1])
            tokenizer = full_path_load_tokinazer(get_Tokinazer_by_model(models[int(model_id) - 1]))

            model.summary()

            train_victim = input("\nEnter person and model will train base on your conversation (like @My_frind): ")
            if train_victim[0] != "@":
                print("\nYou should enter link like @My_frind\n")
                await models_handler(client, command, train_victim)
                return 
            num_messages = input("\nEnter number of messages that model will use as train data \n"
                        "or enter 'None' to use all conversation as training data: ")
            if num_messages == "None":
                print("\nStart loading data. This can take a while!\n")
                X, Y = await GetTrainDataByName(train_victim, client)
                print("\nData has been loaded!\n")
            else :
                try:
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    print("\nPlease enter number of messages!\n")
                    await models_handler(client, command)
                    return 
                X, Y = await GetTrainDataByName(train_victim, client, num_messages)

            try:
                epochs = int(input("\nEnter number of epochs: "))
            except (TypeError, ValueError):
                print("\nYou should enter number of epochs!\n")
                await models_handler(client, model)
                return 
            
            try:
                batch_size = int(input("\nEnter batch size: "))
            except (TypeError, ValueError):
                print("\nYou should enter batch size!\n")
                await models_handler(client, command)
                return 
            
            try:
                messages_per_pack = int(input("\nEnter messages per pack: "))
            except (TypeError, ValueError):
                print("\nYou should enter number messeages per pack!\n")
                await models_handler(client, command)
                return 
            
            with open(train_victim[1:] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print("\nStart training model!\n")
            model = QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)
            print("\nModel has been traind!\n")
            save_QA_model(train_victim[1:], model)
            await models_handler(client)
            return
            
        case "Models back":
            return 
    return 


async def main_handler(client, command = None):
    if command == None:
        command = main_menu()
    match command:
        case "Victim munu":
            await victim_hanfler(client, victim_menu())
            await main_handler(client)
        case "Models menu":
            await models_handler(client, models_menu())
            await main_handler(client)
        case "Exit":
            exit()

