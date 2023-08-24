import asyncio

from Telegram.MonitoringByName import MonitoringByName
from Data_manupulation.test_selection import SaveConversationTXT

def __main__():
    #asyncio.run(MonitoringByName('@Mazar_Nozol'))
    asyncio.run(SaveConversationTXT('@Mazar_Nozol'))


if __name__ == '__main__':
    __main__()

