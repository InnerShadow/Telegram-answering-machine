import re
import pickle

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

youtube_pattern0 = r"https://www\.youtube\.com/watch\?v=[\w-]+"
youtube_pattern1 = r"https://www\.youtu\.be/[\w-]+"

tiktok_pattern = r"https://vm\.tiktok\.com/[\w-]"#

#Try to classify message. it includs links, media etc.
def message_preprocessing(data):
    msg = ""
    #Check if companion send audio or vidio message
    if data.media:
        if isinstance(data.media, MessageMediaDocument):
            size = data.media.document.size
            if data.media.document.mime_type == "audio/ogg":
                msg += "Audio " + str(size) 
            if data.media.document.mime_type == "video/mp4":
                msg += "Video " + str(size)

    #Else check if companion send some links:
    else:
        youtube_links_len = 0
        youtube_links = re.findall(youtube_pattern0, str(data.text))
        youtube_links_len += len(youtube_links)
        youtube_links += re.findall(youtube_pattern1, str(data.text))
        youtube_links_len += len(youtube_links)

        tiktok_links = re.findall(tiktok_pattern, str(data.text))
        other_links = re.split(f"{youtube_pattern0}|{tiktok_pattern}|{youtube_pattern1}", str(data.text))

        if youtube_links_len > 0:
            msg += "Youtube link. "
        if len(tiktok_links) > 0:
            msg += "Tiktock link. "
        if len(other_links) > 0:
            msg += "Other link. "
            
    #Add text of the message
    msg += data.text

    return msg


#Save conversation into .txt if nedeed
async def SaveConversationTXT(name):

    session_file = "session.session"

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        #Try to load session
        try :
            with open(session_file, 'rb') as f:
                session = pickle.load(f)
                client = TelegramClient(StringSession(session), GetAPIID(), GETAPI_Hash())
                await client.start()
        except Exception:
            await client.start(GetPhoneNumber())

            with open(session_file, 'wb') as f:
                pickle.dump(client.session.save(), f)   

        #Get messages
        user = await client.get_entity(name)
        data = await client.get_messages(user, limit = 1000)

        #Write1000 it into txt file
        with open(str(name) + ".txt", 'w') as f:
            for i in range(len(data)):
                msg = message_preprocessing(data[i])
                        
                #Write down the auther
                msg += " (" + data[i].sender.username + ")\n"

                f.write(msg)

            f.close()


#Get first request message index
def GetFirstRequest(data, self_id):
    ind = 0
    for i in range(len(data) - 1, -1, -1):
        if data[i].peer_id.user_id != self_id:
            return i


#Get training data to train model
async def GetTrainDataByName(name):

    session_file = "session.session"

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        #Try to load session
        try :
            with open(session_file, 'rb') as f:
                session = pickle.load(f)
                client = TelegramClient(StringSession(session), GetAPIID(), GETAPI_Hash())
                await client.start()
        except Exception as e:
            print(e)
            await client.start(GetPhoneNumber())

        with open(session_file, 'wb') as f:
            pickle.dump(client.session.save(), f)   

        self_id = await client.get_me()

        #Get messages
        user = await client.get_entity(name)
        data = await client.get_messages(user, limit = 1000)

        #Do not use np.array to avoid coppy a lot of data
        #X - request - you're companion message
        X = []
        #Y - response you're answer
        Y = []

        #Start with the first conversation message and ends with the lst one
        #Beat data into requests-response 
        for i in range(GetFirstRequest(data, self_id), -1, -1):
            iterator = i
            request = ""

            #Get k-th request
            for j in range(iterator, -1, -1):
                if data[j].peer_id.user_id != self_id:
                    request += str(message_preprocessing(data[j])) + ". "
                    i += 1
                else :
                    break

            X.append(request)

            iterator = i
            response = ""

            #Get k-th response
            for j in range(iterator, -1, -1):
                if data[j].peer_id.user_id == self_id:
                    response += str(message_preprocessing(data[j])) + ". "
                    i += 1
                else :
                    break

            Y.append(response)

        #Save into txt (temporary solution)
        with open("X.txt", 'w') as f:
            f.write(X)
            f.close()

        with open("Y.txt", 'w') as f:
            f.write(Y)
            f.close()

    return X, Y

