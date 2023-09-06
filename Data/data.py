
from colorama import Fore

def GetPhoneNumber():
    try:
        with open ("Data/phone.txt", 'r') as f:
            phone = f.readline()
    except Exception:
        phone = input(Fore.LIGHTWHITE_EX + "Enter phone: ")
        with open ("Data/phone.txt", 'w') as f:
            f.write(phone)
    return phone


def GetAPIID():
    try:
        with open ("Data/apiid.txt", 'r') as f:
            apiid = f.readline()
    except Exception:
        apiid = input(Fore.LIGHTWHITE_EX + "Enter api id: ")
        with open ("Data/apiid.txt", 'w') as f:
            f.write(apiid)
    return apiid


def GETAPI_Hash():
    try:
        with open ("Data/apihash.txt", 'r') as f:
            apihash = f.readline()
    except Exception:
        apihash = input("Enter api hash: ")
        with open (Fore.LIGHTWHITE_EX + "Data/apihash.txt", 'w') as f:
            f.write(apihash)
    return apihash

