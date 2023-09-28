from PIL import Image

from colorama import Fore

from Model.QA_model import *
from Model.Tokenizer import *
from Users_interfece.interface import *
from Data_manupulation.test_selection import *
from Users_interfece.helpers import *

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

            if len(models) == 0:
                print(Fore.LIGHTRED_EX + 
                      "\nCreate a model first!!\n")
                
                await models_handler(client)

            #Try to get id from user
            try:
                selected_model_id = int(input(Fore.LIGHTWHITE_EX + 
                                              "\nEnter model id: "))
                
            except (TypeError, ValueError):
                print(Fore.LIGHTRED_EX + 
                      "\nThis model does not exist!\n")
                
                await models_handler(client)
                return 

            #Selected index out of range
            if selected_model_id > len(models):
                print(Fore.LIGHTRED_EX + "\n" + str(selected_model_id) + 
                      " model does not exist!\n")

                #Back to models menu
                await models_handler(client)
                return 
            
            #Load model by name & show models architecture
            model = full_path_load_QA_model(models[int(selected_model_id) - 1])
            model.summary()

            #Show hiddent params that store in model configuration
            model_name = models[int(selected_model_id) - 1]
            with open(model_name[:len(model_name) - 6] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + 
                  "\nmaxWordsCount: " + str(maxWordsCount) + 
                  ", sequences_len: " + str(sequences_len) + "\n")
            
            #Back to models_menu_handler
            await models_handler(client)
            return 
        
        #Train new model option
        case "Models train":
            #Try to find conversation with person by name
            train_victim = input(Fore.LIGHTWHITE_EX + 
                                 "\nEnter victim to train the model (correct form: @My_friend): ")
            
            if train_victim[0] != "@":
                #Victims name should starts with '@'
                print(Fore.LIGHTRED_EX + 
                      "\nError! Correct form: @My_friend\n")

                #Back to models_handler
                await models_handler(client)
                return 
            
            #Get number of messages to upload from conversation
            num_messages = input(Fore.LIGHTWHITE_EX + 
                                "\nEnter number of messages that model will use as train data \n"
                                "or enter 'None' to use all conversation as training data: ")
            
            if num_messages == "None":
                #If 'None' upload full conversation
                print(Fore.YELLOW + "\nData is loading...\n")

                try:
                    X, Y = await GetTrainDataByName(train_victim, client)
                except Exception:
                    print(Fore.LIGHTRED_EX + 
                          "\nCannot find conversation with " + train_victim[1:] + "\n")
                    
                    await models_handler(client)
                    return
            
                print(Fore.LIGHTGREEN_EX + 
                      "\nData is loaded!\n")

            else :
                try:
                    #Try to convert num_messages into int
                    num_messages = int(num_messages)

                except (TypeError, ValueError):
                    #Catch exception if cannot convert and back to models_handler 
                    print(Fore.LIGHTRED_EX + 
                          "\nNot a number! \n")
                    
                    await models_handler(client)
                    return 
                
            #Upload num_messages messeges from conversation 
            print(Fore.YELLOW + 
                  "\nData is loading...\n") 

            try:
                X, Y = await GetTrainDataByName(train_victim, client, num_messages)
            except Exception:
                print(Fore.LIGHTRED_EX + 
                      "\nCannot find conversation with " + train_victim[1:] + "\n")
                
                await models_handler(client)
                return

            print(Fore.LIGHTGREEN_EX + 
                  "\nData is loaded!\n")

            #Try to get vocabulary size
            try:
                maxWordsCount = int(input(Fore.LIGHTWHITE_EX + 
                                          "\nEnter size of vocabulary: "))
                
            except (TypeError, ValueError):
                #If cannot covert to int back to models_handler
                print(Fore.LIGHTRED_EX + 
                      "\nNot a number!\n")
                
                await models_handler(client)
            
            #Get 'lower' param
            try:
                lower = int(input(Fore.LIGHTWHITE_EX + 
                                  "\nEnter 1 if you want only low register messages, 0 for high & low register messages: ")) # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
                
                if lower == 1:
                    lower = True
                elif lower == 0:
                    lower = False
                else:
                    #If input not 0 or 1 back to models_handler
                    print(Fore.LIGHTRED_EX + 
                          "\nYou should enter 1 or 0 to set register!\n")
                    
                    await models_handler(client)
                    return 
            except (TypeError, ValueError):
                    #If input not int
                    print(Fore.LIGHTRED_EX + 
                          "\nYou should enter 1 or 0 to set register!\n")
                    
                    await models_handler(client)
                    return 
            
            #Get num of LSTM dims
            try:
                latent_dim = int(input(Fore.LIGHTWHITE_EX + 
                                       "\nEnter hidden LSTM layer neurons: "))
                
            except (TypeError, ValueError):
                #If not int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter number of hidden LSTM layer neurons!\n")
                
                await models_handler(client)
                return 
            
            #Try to get sequences_len 
            try:
                sequences_len = int(input(Fore.LIGHTWHITE_EX + 
                                          "\nEnter sequences length: "))
                
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter sequences length!\n")
                
                await models_handler(client)
                return 
            
            #Create model & tokinazer
            tokenizer = get_Tokinazer(X, Y, maxWordsCount, lower, False)
            save_tokinazer(train_victim[1:], tokenizer)
            model = Get_RNN_QA(int(maxWordsCount), latent_dim, sequences_len)

            #Try to get number of epochs
            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + 
                                   "\nEnter number of epochs: "))
                
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter number of epochs!\n")
                
                await models_handler(client, model)
                return 
            
            #Try to get batch size
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + 
                                       "\nEnter batch size: "))
                
            except (TypeError, ValueError):
                #If intput is not int go to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter batch size!\n")
                
                await models_handler(client)
                return 
            
            #Try to get messeges per pack
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + 
                                              "\nEnter messages per pack: "))
                
            except (TypeError, ValueError):
                #If input is not int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter number messeages per pack!\n")
                
                await models_handler(client)
                return 

            #Do train model 
            print(Fore.LIGHTGREEN_EX + 
                  "\nStart training model!\n")
            
            model = QA_model_train(train_victim[1:], model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)

            print(Fore.LIGHTGREEN_EX + 
                  "\nModel has been traind!\n")

            #Save model in .keras
            save_QA_model(train_victim[1:], model)

            #Save model configuration
            with open("Data/" + train_victim[1:] + "_model_configuration.txt", 'w') as f:
                f.write(str(maxWordsCount) + "\n")
                f.write(str(sequences_len) + "\n")
            
            #Back to models menu
            await models_handler(client)
            return
        
        #Train more existable model
        case "Models train more":
            #Show all models
            models = get_all_models()

            if len(models) == 0:
                print(Fore.LIGHTRED_EX + 
                      "\nYou should have at least one model to up train it!\n")
                
                await models_handler(client)

            #Try to get get model by id
            try:
                model_id = int(input(Fore.LIGHTWHITE_EX + 
                                     "\nSelect model by id acording the list: "))
                
            except (TypeError, ValueError):
                #If input is not integer
                print(Fore.LIGHTRED_EX + 
                      "\nYou should select existable model!\n")
                
                await models_handler(client)
                return
            
            #If index out of range back to models menu
            if model_id > len(models):
                print(Fore.LIGHTRED_EX + 
                      "\nYou should select existable model!\n")
                
                await models_handler(client)
                return
            
            model_name = models[int(model_id) - 1]

            #Show previous model traing graphics
            print(Fore.YELLOW + 
                  "\nPrevious learing resualt at the screen!\n")

            #Try to open graphics
            try:
                image = Image.open(model_name[:len(model_name) - 6] + "_graph.png")
                image.show()

            except Exception:
                #Just say that graphics do not exist and continue working!
                print(Fore.LIGHTRED_EX + 
                      "\nFor some reason cannot open graphics!\n")

            #Upload model & tokinazer
            print(Fore.LIGHTGREEN_EX + "\n" + str(models[int(model_id) - 1]) + " has been selected!\n")
            model = full_path_load_QA_model(models[int(model_id) - 1])
            tokenizer = full_path_load_tokinazer(get_Tokinazer_by_model(models[int(model_id) - 1]))

            model.summary()

            #Get data from model configuration
            with open(model_name[:len(model_name) - 6] + "_model_configuration.txt", 'r') as f:
                maxWordsCount = int(f.readline())
                sequences_len = int(f.readline())

            print(Fore.YELLOW + "\nmaxWordsCount: " + str(maxWordsCount) + 
                  ", sequences_len: " + str(sequences_len) + "\n")

            #Select person to train more model base on prev conversation 
            train_victim = input(Fore.LIGHTWHITE_EX + 
                                 "\nEnter person and model will train base on your conversation (like @My_friend): ")
            
            if train_victim[0] != "@":
                #Victim name should starts with '@'
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter link like @My_friend\n")
                
                await models_handler(client, command, train_victim)
                return 

            #Choose number of messeges
            num_messages = input(Fore.LIGHTWHITE_EX + 
                                "\nEnter number of messages that model will use as train data \n"
                                "or enter 'None' to use all conversation as training data: ")
            
            if num_messages == "None":
                #Upload full conversation
                print(Fore.YELLOW + 
                      "\nStart loading data. This can take a while!\n")

                try:
                    X, Y = await GetTrainDataByName(train_victim, client)
                except Exception:
                    print(Fore.LIGHTRED_EX + 
                          "\nCannot find conversation with " + train_victim[1:] + "\n")
                    
                    await models_handler(client)
                    return
                
                print(Fore.LIGHTGREEN_EX + 
                      "\nData has been loaded!\n")
                
            else :
                try:
                    #Try to convert input into int
                    num_messages = int(num_messages)
                except (TypeError, ValueError):
                    #If cannot back to models menu
                    print(Fore.LIGHTRED_EX + 
                          "\nPlease enter number of messages!\n")
                    
                    await models_handler(client, command)
                    return 
                
                #Upload data from conversation
                print(Fore.YELLOW + 
                      "\nStart loading data. This can take a while!\n")

                try:
                    X, Y = await GetTrainDataByName(train_victim, client, num_messages)
                except Exception:
                    print(Fore.LIGHTRED_EX + 
                          "\nCannot find conversation with " + train_victim[1:] + "\n")
                    
                    await models_handler(client)
                    return
                
                print(Fore.LIGHTGREEN_EX + 
                      "\nData has been loaded!\n")

            #Try to get number of epochs
            try:
                epochs = int(input(Fore.LIGHTWHITE_EX + 
                                   "\nEnter number of epochs: "))
                
            except (TypeError, ValueError):
                #If cannot conver input in int, back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter number of epochs!\n")
                
                await models_handler(client, model)
                return 
            
            #Try to get batch_size
            try:
                batch_size = int(input(Fore.LIGHTWHITE_EX + 
                                       "\nEnter batch size: "))
            except (TypeError, ValueError):
                #If cannot convert input into int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter batch size!\n")
                
                await models_handler(client, command)
                return 
            
            #Try to get messages_per_pack
            try:
                messages_per_pack = int(input(Fore.LIGHTWHITE_EX + 
                                              "\nEnter messages per pack: "))
            except (TypeError, ValueError):
                #If cannot convert input into int back to models menu
                print(Fore.LIGHTRED_EX + 
                      "\nYou should enter number messeages per pack!\n")
                
                await models_handler(client, command)
                return 

            #Do train more model
            print(Fore.LIGHTGREEN_EX + 
                  "\nStart training model!\n")
            
            model = QA_model_train(train_victim[1:], model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack)

            print(Fore.LIGHTGREEN_EX + 
                  "\nModel has been traind!\n")

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

