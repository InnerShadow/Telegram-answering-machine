
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
        with open ("Data/apid.txt", 'r') as f:
            apiid = f.readline()
    except Exception:
        apid = input("Enter apid: ")
        with open ("Data/apid.txt", 'w') as f:
            f.write(apid)
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

