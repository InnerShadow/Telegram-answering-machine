import asyncio

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import GetConversationByName

def __main__():
    #asyncio.run(MonitoringByName('@Mazar_Nozol'))
    asyncio.run(GetConversationByName('@Mazar_Nozol'))


if __name__ == '__main__':
    __main__()

