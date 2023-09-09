
from colorama import Fore

#Get phone number or create .txt file with phone number
def GetPhoneNumber():
    try:
        with open ("Data/phone.txt", 'r') as f:
            phone = f.readline()
    except Exception:
        phone = input(Fore.LIGHTWHITE_EX + "Enter phone: ")
        with open ("Data/phone.txt", 'w') as f:
            f.write(phone)
    return phone


#Get api id or create .txt file with api id
def GetAPIID():
    try:
        with open ("Data/apiid.txt", 'r') as f:
            apiid = f.readline()
    except Exception:
        apiid = input(Fore.LIGHTWHITE_EX + "Enter api id: ")
        with open ("Data/apiid.txt", 'w') as f:
            f.write(apiid)
    return apiid


#Get api hash or create .txt file with api hash
def GETAPI_Hash():
    try:
        with open ("Data/apihash.txt", 'r') as f:
            apihash = f.readline()
    except Exception:
        apihash = input("Enter api hash: ")
        with open (Fore.LIGHTWHITE_EX + "Data/apihash.txt", 'w') as f:
            f.write(apihash)
    return apihash

