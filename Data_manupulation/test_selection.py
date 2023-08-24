import re

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument

from Data.data import GETAPI_Hash, GetAPIID, GetPhoneNumber

youtube_pattern0 = r"https://www\.youtube\.com/watch\?v=[\w-]+"
youtube_pattern1 = r"https://www\.youtu.be\.com/watch\?v=[\w-]+"

tiktok_pattern = r"https://www\.tiktok\.com/\@[\w-]+/video/\d+"

#Save conversation into .txt if nedeed
async def SaveConversationTXT(name):

    global youtube_pattern, tiktok_pattern

    data = []

    session_file = "session.session"

    async with TelegramClient(StringSession(), GetAPIID(), GETAPI_Hash()) as client:

        #Try to load session
        try :
            await client.start(session_file = session_file)
        except Exception:
            await client.start(GetPhoneNumber())

        #Get messages
        user = await client.get_entity(name)
        data = await client.get_messages(user, limit = 1000)

        #Write it into txt file
        with open(str(name) + ".txt", 'w') as f:
            for i in range(len(data)):
                msg = ""
                #Check if companion send audio or vidio message
                if data[i].media:
                    if isinstance(data[i].media, MessageMediaDocument):
                        size = data[i].media.document.size
                        if data[i].media.document.mime_type == "audio/ogg":
                            msg += "Audio" + str(size) 
                        if data[i].media.document.mime_type == "video/mp4":
                            msg += "Video" + str(size)

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
                        msg += "Other link"
                        #Else add text of the message
                    else:
                        msg += data[i].text

                #Write down the auther
                msg += " (" + data[i].sender.username + ")\n"

                f.write(msg)

            f.close()

        #Save session
        with open(session_file, "w") as f:
            f.write(client.session.save())

    