import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import asyncio

from Users_interfece.interface import first_launch, application_api, main_menu, log_in
from Users_interfece.main_handler import main_handler

async def __main__():
    first_launch()

    phone, apiid, apihash = application_api()

    client = await log_in(phone, apiid, apihash)
    if client == None:
        return 

    await main_handler(client, main_menu())
    

if __name__ == '__main__':
    asyncio.run(__main__())

# TODO: MAke colarization where need
# TODO: Make comments!
# TODO: Make ignoring in diffrent thread
# TODO: Make auto-load ignoring 
# TODO: Make better parametrs recomendation
