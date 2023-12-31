import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import asyncio

from Users_interfece.interface import first_launch, application_api, main_menu, log_in
from Users_interfece.main_handler import main_handler
from colorama import init, Fore

#Main function that provides to console interface
async def __main__():
    init()

    #Get hello message & info about telegram application
    first_launch()

    #Get params from txt or create new
    phone, apiid, apihash = application_api()

    #Try to log in Telegram
    try :
        client = await log_in(phone, apiid, apihash)

    except Exception:
        print(Fore.LIGHTRED_EX + 
              "Cannot log in telegram!")
        
        return
        
    if client == None:
        return 
    
    #Reset do_ignore file
    with open("Data/do_ignore.txt", 'w') as f:
        f.truncate(0)

    #Go to console interface
    await main_handler(client, main_menu())
    

if __name__ == '__main__':
    asyncio.run(__main__())

