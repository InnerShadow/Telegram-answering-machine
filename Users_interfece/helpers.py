
from colorama import Fore

#Main menu helper
def main_helper():
    print(Fore.YELLOW +
        "\nThis is main menu. This has next options:"
        "\n1) 'Victim menu', that has all manipulations with victims like create new victim or link model with victim and other;"
        "\n2) 'Model menu' that has all manipulations with models like creation, training models and other;"
        "\n3) 'Run igniging' willignoge all victims with their parameters;"
        "\n4) 'Exit' option will close the application.\n")
    print(Fore.GREEN + "\n How to use it:"
        "\nTo start ignoring some one you should go Models -> Train new model. After this you will have ready to use model."
        "\nNext you should go to Victims -> Get new victim -> Selcet victim by id -> Select some one -> Set model by id -> Select some model -> Back to victim menu -> Add to ignoring list."
        "\nNow that you can add as may victims as you want. After that you should back to main menu and use 'Run ignoring' option. All selected victims will be ignored!"
        "\nThere are also some other features. You can read about them using 'Help' option in each modul.\n")
    

#Victim menu helper
def victim_helper():
    print(Fore.YELLOW + "\nThis is victim menu. It contains next options:"
        "\n1) 'Show all victims' simply shows all possible victims. It includes victims with empty configuration!"
        "\n2) 'Select victim by id' provides you to 'selected victim menu' this option helps you to connect victim and model. "
        "You should select victim before start ignoring it;"
        "\n3) 'Get new victim' options creates empty victim configuration, after filling that will be use in ignoring module;"
        "\n4) 'Add to ignoring list' option will add victim to ignoring list. Then you can use 'Run igniging' option of main menu to start igrnoring all victims."
        "\nYou should select victim before start ignoring it;"
        "\n5) 'Back to main menu' simply returns you to main menu.\n")
    

#Selected vicitm menu helper
def selected_victim_help():
    print(Fore.YELLOW + "\nThis is 'selected victim' menu. It provides:"
          "\n1) 'Set model by id' will connect selected victim with model by id. This option will fill victim configuration, that need in ignoring option;"
          "\n2) 'Display info' will display all information about victim and model connection;"
          "\n3) 'Back to victim menu' simply returns you to victim menu.\n")
    

#Models helper 
def models_helper():
    print(Fore.YELLOW + "\nThis is models menu. It contains next options:"
          "\n1) 'Show all models' option simply show all trained models;"
          "\n2) 'Get model info by id' option shows all models and provides information about selected model. "
          "It includes model configuration parameters and model architecture;"
          "\n3) 'Train new model' provides opportunity to train new model. You can choose train conversation, number of hidden layer neurons, batch size and other parameters."
          "\nMy recommendation about model parameters: "
          "\n     3.1) Number of messages - 40k or None (full conversation);"
          "\n     3.2) Size of vocabulary - 15k-20k or more [This is max number of unic most common words from you're conversion];"
          "\n     3.3) Lower - True or '1' [This means that all words will have only low register characters. This is better for training];"
          "\n     3.4) Number of hidden LSTM layer neurons - 512 or more [This parameter that determ neural network complexity. This doesn't means that more neurons = more flexible neural network];"
          "\n     3.5) Number of epochs - 200 or more [This parameter means number of times that you're conversation will pass through neural network];"
          "\n     3.6) Batch size - 8 - 32 [This parameter sets after what number of messages model will try to correct parameters. Bigger batch size = faster learning = more vague answers];"
          "\n     3.7) Number messages per pack - 64 - 256 [Basicly algorith need many RAM to process data. This parameter will cut conversation by parts and train neural network step by step to avoid lack of memory];"
          "\n     3.8) Sequences length - 20 - 50 [This parameter will cut long messages and fill with zeros short one. This need to standardize neural network neurons];"
          "\n4)'Train more for model' will train more for existtable model. It can helps for models that train well, but you set not enough epochs. Also you can try to learn more with other person conversation;"
          "\n5)'Back to main menu' simply returns you to main menu.\n")


#Default answer helper
def default_answer_helper():
    print(Fore.YELLOW + "\nThis is default answer menu. It contains next options:"
          "\n1) 'Show default answer' simply shows pre_loaded default answer. This is answer That will be send if you're vocabulary do not contains words of current message;"
          "\n2) 'Set default answer' allows you to set you're own default answer;"
          "\n3) 'Back to main menu' simply returns you to main menu.\n")
    
