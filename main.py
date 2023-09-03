import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import asyncio

from telethon.sync import TelegramClient

from Users_interfece.interface import *
from Users_interfece.main_handler import *

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT, GetTrainDataByName

from Model.QA_model import *
from Model.RNN_model import load_RNN_model, Get_RNN_word_continue, full_sequence_RNN_train
from Model.QA_model import QA_model_train, Get_RNN_QA
from Model.Tokenizer import get_Tokinazer, save_tokinazer, load_tokinazer, full_path_load_tokinazer
from Data_manupulation.Words_level import Word_level_RNN_answer, Word_level_QA_answer

async def test():
    client = TelegramClient(GetPhoneNumber(), GetAPIID(), GETAPI_Hash())
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(GetPhoneNumber())
        try :
            await client.sign_in(GetPhoneNumber(), code = input('Enter the code: '))
        except Exception:
            password = input("Enter password: ")
            client = await client.sign_in(password = password)

            client = TelegramClient(GetPhoneNumber(), GetAPIID(), GETAPI_Hash())
            await client.connect()

    name = "@Mazar_Nozol"
    maxWordsCount = 5000
    sequences_len = 20
    batch_size = 128
    epochs = 100
    
    try:
        tokenizer = load_tokinazer(name[1:])
    except Exception:
        X, Y = await (GetTrainDataByName(name, client, 2000))
        tokenizer = get_Tokinazer(X, Y, maxWordsCount = maxWordsCount)
        #save_tokinazer(name, tokenizer)

    text = "А нашел полезного для них человека".lower()

    #model = Get_RNN_QA(maxWordsCount, sequences_len)
    #model = QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount)
    model = load_RNN_model(name)

    print(Word_level_QA_answer(model, tokenizer, text, sequences_len, len(text) * 2))

    asyncio.run(await MonitoringByName(name, client, model, tokenizer, sequences_len))


async def test2():
    first_launch()

    phone, apiid, apihash = application_api()

    client = await log_in(phone, apiid, apihash)
    command = 0

    victum = ""
    victiums = []
    
    model = None
    tokenizer = None
    models = []
    sequences_len = 20

    while True:
        match command:
            case 0:
                command = main_menu()
            case 1:
                vic_state = victim_menu()
                vic_id = 0
                match vic_state:
                    case 1:
                        get_all_victiums()
                    case 2:
                        victiums = get_all_victiums()
                        vic_id = input("\nSelect victim acording the list: ")
                        if int(vic_id) > len(victiums):
                            print("\n" + str(vic_id) + " victim does not exist\n")
                        else :
                            victum = victiums[int(vic_id) - 1]
                            print("\n" + victum + " has been selected!\n")
                            step_1 = selected_victim_menu()
                            match step_1:
                                case 1:
                                    models = get_all_models()
                                    selected_model_id = int(input("\nEnter model id to connet it to victim: "))
                                    print("\n" + models[selected_model_id - 1] + " has been selected!\n")
                                    with open(str(victum), 'w') as f:
                                        #TODO: rewrite data
                                        f.write(str(models[int(selected_model_id) - 1]) + "\n")
                                        f.write(str(models[int(selected_model_id) - 1])[:len(str(models[int(selected_model_id) - 1])) - 3]
                                                 + "_tokenizer.pickle")
                                case 2: 
                                    with open(str(victum), 'r') as f:
                                        print("\nModel: " + f.readline() + "\n Tokinazer: " + f.readline() + "\n")
                                case 3:
                                    step_1 = 0
                                    vic_state = 0

                    case 3:
                        new_victim = input("\nEnter telegram link of victim as @My_frind: ")
                        if new_victim[0] == '@':
                            new_victim = new_victim
                        else:
                            new_victim = ""
                            print("\nYou should enter link like @My_frind\n")
                    case 4:
                        #TODO: Fix ignoring
                        if victum == "":
                            print("\nPlease, select the victim!\n")
                        else:
                            model_name = ""
                            tokinazer_name = ""
                            with open(str(victum), 'r') as f:
                                model_name = f.readline()
                                tokinazer_name = f.readline()
                            if model_name == "" or tokinazer_name == "":
                                print("\nVictim configuration should not be empty! Set the model to ignore victim!\n")
                            else:
                                model = full_path_load_QA_model(model_name)
                                tokenizer = full_path_load_tokinazer(tokinazer_name)
                                asyncio.run(await MonitoringByName(victum, client, model, tokenizer, sequences_len))
                                vic_state = 0
                    case 5:
                        vic_state = 0
                        command = 0

            case 2:
                model_state =  models_menu()
                match model_state:
                    case 1: 
                        models = get_all_models()
                    case 2:
                        selected_model_id = input("\nEnter model id: ")
                        if int(selected_model_id) > len(models):
                            print("\n" + str(selected_model_id) + " model does not exist!\n")
                        else:
                            model = full_path_load_QA_model(models[int(selected_model_id) - 1])
                            tokenizer = full_path_load_QA_model(models[int(selected_model_id) - 1])

                            model.summary()
                            #TODO: Show tokinazer info 
                    case 3:
                        train_victim = input("\nEnter person and model will train base on your conversation (like @My_frind): ")
                        if train_victim[0] != "@":
                            print("\nYou should enter link like @My_frind\n")
                        else:
                            num_messages = int(input("\nEnter number of messages that model will use as train data \n"
                                                "or enter 'None' to use all conversation as training data: "))
                            if num_messages == "None":
                                X, Y = await GetTrainDataByName(train_victim, client)
                            elif int(num_messages) == num_messages:
                                X, Y = await GetTrainDataByName(train_victim, client, num_messages)
                            else :
                                print("\nPlease enter number of messages!\n")
                            if X != None and Y != None:
                                maxWordsCount = input("\nEnter size of vocabulary: ")
                                if int(num_messages) != num_messages:
                                    print("\nYou should enter size of vocabulary!\n")
                                else:
                                    lower = int(input("\nEnter 1 if you want only low register messeges, 0 for high & low register messages: "))
                                    if int(lower) == 1:
                                        lower = True
                                    elif int(lower) == 0:
                                        lower = False
                                    else:
                                        print("\nYou should enter 1 or 0 to set register!\n")
                                    if lower == True or lower == False:
                                        char_level = int(input("\nEnter 1 if you want train model on char level and 0 for word level: "))
                                        if int(char_level) == 1:
                                            char_level = True
                                        elif int(char_level) == 0:
                                            char_level = False
                                        else:
                                            print("\nYou should enter 1 or 0 to set char level!\n")
                                        if char_level == True or char_level == False:
                                            tokenizer = get_Tokinazer(X, Y, int(maxWordsCount), lower, char_level)
                                            save_tokinazer(train_victim[1:], tokenizer)
                                            model = Get_RNN_QA(int(maxWordsCount), sequences_len)
                                            epochs = int(input("\nEnter number of epochs: "))
                                            if int(epochs) != epochs:
                                                print("\nYou should enter number of epochs!\n")
                                            else:
                                                batch_size = int(input("\nEnter batch size: "))
                                                if int(batch_size) != batch_size:
                                                    print("\nYou should enter batch size!\n")
                                                else:
                                                    print("\nStart training model!\n")
                                                    model = QA_model_train(model, X, Y, tokenizer, int(batch_size), int(epochs), sequences_len, int(maxWordsCount))
                                                    print("\nModel has been traind!\n")
                                                    save_QA_model(train_victim[1:], model)
                                                    model_state = 0
                    case 4: 
                        model_state = 0
                        command = 0
            case 3:
                exit()


async def __main__():
    first_launch()

    phone, apiid, apihash = application_api()

    client = await log_in(phone, apiid, apihash)

    await main_handler(client, main_menu())
    

if __name__ == '__main__':
    asyncio.run(__main__())

# TODO: Tokenazer jeson load
# TODO: MAke colarization where need
