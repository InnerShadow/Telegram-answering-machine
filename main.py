import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import asyncio

from Users_interfece.interface import first_launch, application_api, main_menu, log_in
from Users_interfece.main_handler import main_handler
from Telegram.MonitoringByName import reIgnoreVictims
from colorama import init

#Main function that provides to console interface
async def __main__():
    init()

    #Get hello message & info about telegram application
    first_launch()

    #Get params from txt or create new
    phone, apiid, apihash = application_api()

    #Try to log in Telegram
    client = await log_in(phone, apiid, apihash)
    if client == None:
        return 
    
    #Reload precious ignoring victims
    #await reIgnoreVictims(client)

    #Go to console interface
    asyncio.run(await main_handler(client, main_menu()))
    

if __name__ == '__main__':
    asyncio.run(__main__())


# TODO: Make ignoring in diffrent thread
# TODO: Make auto-load ignoring 
# TODO: Make better parametrs recomendation