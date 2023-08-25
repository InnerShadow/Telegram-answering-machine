import re

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

youtube_pattern0 = r"https://www\.youtube\.com/watch\?v=[\w-]+"
youtube_pattern1 = r"https://www\.youtu\.be/[\w-]+"

tiktok_pattern = r"https://vm\.tiktok\.com/[\w-]"

#Save conversation into .txt if nedeed
async def SaveConversationTXT(name):

    global youtube_pattern0, youtube_pattern1, tiktok_pattern

    session_file = "session.session"

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        #Try to load session
        try :
            await client.start(session_file = session_file)
        except Exception:
            await client.start(GetPhoneNumber())

            #Save session
            with open(session_file, "w") as f:
                f.write(client.session.save())

        #Get messages
        user = await client.get_entity(name)
        data = await client.get_messages(user, limit = 1000)

        #Write1000 it into txt file
        with open(str(name) + ".txt", 'w') as f:
            for i in range(len(data)):
                msg = ""
                #Check if companion send audio or vidio message
                if data[i].media:
                    if isinstance(data[i].media, MessageMediaDocument):
                        size = data[i].media.document.size
                        if data[i].media.document.mime_type == "audio/ogg":
                            msg += "Audio " + str(size) 
                        if data[i].media.document.mime_type == "video/mp4":
                            msg += "Video " + str(size)

                #Else check if companion send some links:
                else:
                    youtube_links_len = 0
                    youtube_links = re.findall(youtube_pattern0, data[i].text)
                    youtube_links_len += len(youtube_links)
                    youtube_links += re.findall(youtube_pattern1, data[i].text)
                    youtube_links_len += len(youtube_links)

                    tiktok_links = re.findall(tiktok_pattern, data[i].text)
                    other_links = re.split(f"{youtube_pattern0}|{tiktok_pattern}|{youtube_pattern1}", data[i].text)

                    if youtube_links_len > 0:
                        msg += "Youtube link "
                    if len(tiktok_links) > 0:
                        msg += "Tiktock link "
                    if len(other_links) > 0:
                        msg += "Other link "
                        
                #Else add text of the message
                msg += data[i].text
                        
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


async def GetTrainDataByName(name):
    global youtube_pattern0, youtube_pattern1, tiktok_pattern

    session_file = "session.session"

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        #Try to load session
        try :
            await client.start(session_file = session_file)
        except Exception:
            await client.start(GetPhoneNumber())

        self_id = client.get_me()

        #Get messages
        user = await client.get_entity(name)
        data = await client.get_messages(user, limit = None)

        #Do not use np.array to avoid coppy a lot of data
        #X - request - you're companion message
        X = []
        #Y - response you're answer
        Y = []

        for i in range(GetFirstRequest(data, self_id), -1, -1):
            iterator = i
            request = ""
            for j in range(iterator, -1, -1):
                if data[j].peer_id.user_id != self_id:
                    request += str(data[j].text) + ". "
                    i += 1
                else :
                    break

            X.append(request)

            iterator = i
            response = ""
            for j in range(iterator, -1, -1):
                if data[j].peer_id.user_id == self_id:
                    response += str(data[j].text) + ". "
                    i += 1
                else :
                    break

            Y.append(response)