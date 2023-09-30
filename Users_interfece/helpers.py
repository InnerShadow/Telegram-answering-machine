
from colorama import Fore

#Main menu helper
def main_helper():
    print(Fore.YELLOW +
        "\nMAIN MENU:"
        "\n1) 'Victim menu', provides some actions with victims like 'create a new victim' or 'connect the model to the victim' and other;"
        "\n2) 'Model menu' provides some actions with models like creating, training models and other;"
        "\n3) 'Run ignoring' will ignore all victims according to certain models;"
        "\n4) 'Default answer' allows you to set default answer that will be sent when neural network cannot recognize any words from the last message from victim;"
        "\n5) 'Exit' option will close the application.\n")
    
    #How to use it message
    print(Fore.GREEN + 
        "\nINSTRUCTION FOR USE:"
        "\nTo start ignoring someone you should go Models -> Train new mode, than set up parametrs. After these steps the model will be ready for expluatation;"
        "\nNext step is creating a victim and connecting a model to it." 
        "Go Victim menu -> Get new victim -> Selcet victim by id -> Select a victim -> Set model by id -> Select a model -> Back to victim menu -> Add to ignoring list;"
        "\nThan you can add as may victims as you want. After that go back to 'MAIN MENU' and choose 'Run ignoring' option. All selected victims will be ignored;"
        "\nThere are also some other features. You can learn more about them using 'help' option in each modul.\n")
    

#Victim menu helper
def victim_helper():
    print(Fore.YELLOW + 
        "\nVICTIM MENU:"
        "\n1) 'Show all victims' shows all created victims."
        "\n2) 'Select victim by id' redirects you to 'selected victim menu'. This option allows you to connect the model to the victim;"
        "You should select victim to start ignoring it;"
        "\n3) 'Get new victim' creates new victim with no connected model;"
        "\n4) 'Add to ignoring list' adds chosen victim to the ignoring list. Then go back to 'MAIN MENU' and choose 'Run ignoring' option to start ignoring all victims;"
        "\nYou should select victim to start ignoring it;"
        "\n5) 'Back to MAIN MENU' redirects you to 'MAIN MENU'.\n")
    

#Selected vicitm menu helper
def selected_victim_help():
    print(Fore.YELLOW + 
          "\nDISPATCHER OF VICTIMS"
          "\n1) 'Set model by id' connects the model with the selected victim by id;"
          "\n2) 'Display info' displays all information about the victim and the connected model;"
          "\n3) 'Back to VICTIM MENU' returns you to 'VICTIM MENU'.\n")
    

#Models helper 
def models_helper():
    print(Fore.YELLOW + 
          "\nMODEL MENU:"
          "\n1) 'Show all models' shows all trained models;"
          "\n2) 'Get model info by id' shows all models and provides information about the selected model by id. "
          "This includes model parameters and model architecture;"
          "\n3) 'Train new model' allows you to train a new model. You can select the training data, number of hidden layer neurons, batch size and other parameters;"
          "\nRecommended model parameters: "
          "\n     3.1) Number of messages (training data) - 40K or 'None' (full conversation);"
          "\n     3.2) Size of vocabulary - 15K-20K or more [This is the maximum number of the most common words in your conversation];"
          "\n     3.3) Lower - 'True' (or 1) [There will be only low registers in your messages (Better for model training)];"
          "\n     3.4) Higher - 'False' (or 0) [There will be both low and high registers in your messages];"   
          "\n     3.5) Number of hidden LSTM layer neurons - 512 or more [This parameter determs neural network complexity. (More neurons != more flexible neural network)];"
          "\n     3.6) Number of epochs - 200 or more [This parameter determs a number of times that neural network will pass through your conversation];"
          "\n     3.7) Batch size - 8 - 32 [Bigger batch size = faster learning = more vague answers];"
          "\n     3.8) Number of messages per pack - 64 - 256 [Algorithm needs many RAM to process data."
          "       This option will cut the conversation into pieces and train the neural network step by step to avoid running out of memory];"
          "\n     3.9) Sequence length - 20 - 50 [This parameter defines the length to which all messages will be shortened/expanded during processing];"
          "\n4)'Train model further' will train existting model further. It can help the trained model to develop. (You can use different training data to train the model);"
          "\n5)'Back to MAIN MENU' redirects you to 'MAIN MENU'.\n")


#Default answer helper
def default_answer_helper():
    print(Fore.YELLOW + 
          "\nDEFAULT ANSWER MENU:"
          "\n1) 'Show default answer' shows default answer. This reply will be sent if your vocabulary does not contain words from the current message;"
          "\n2) 'Set default answer' allows you to change default answer;"
          "\n3) 'Back to MAIN MENU' redirects you to 'MAIN MENU'.\n")
    
