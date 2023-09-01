
def GetPhoneNumber():
    try:
        with open ("Data/phone.txt", 'r') as f:
            phone = f.readline()
    except Exception:
        phone = input("Enter phone: ")
        with open ("Data/phone.txt", 'w') as f:
            f.write(phone)
    return phone


def GetAPIID():
    try:
        with open ("Data/apiid.txt", 'r') as f:
            apiid = f.readline()
    except Exception:
        apiid = input("Enter apiid: ")
        with open ("Data/apiid.txt", 'w') as f:
            f.write(apiid)
    return apiid


def GETAPI_Hash():
    try:
        with open ("Data/apihash.txt", 'r') as f:
            apihash = f.readline()
    except Exception:
        apihash = input("Enter apihash: ")
        with open ("Data/apihash.txt", 'w') as f:
            f.write(apihash)
    return apihash

