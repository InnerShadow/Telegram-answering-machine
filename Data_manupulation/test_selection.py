import re
import pickle

from telethon.tl.types import MessageMediaDocument

youtube_pattern0 = r"https://www\.youtube\.com/watch\?v=[\w-]+"
youtube_pattern1 = r"https://www\.youtu\.be/[\w-]+"

tiktok_pattern = r"https://vm\.tiktok\.com/[\w-]+"

other_links_patter = r"https://[\w-]+"

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
        other_links = re.findall(other_links_patter, str(data.text))

        if youtube_links_len > 0:
            msg += "Youtube link. "
        if len(tiktok_links) > 0:
            msg += "Tiktock link. "
        if len(other_links) > 0:
            msg += "Other link. "
        if youtube_links_len != 0 or len(tiktok_links) != 0 or len(other_links) != 0:
            return msg
            
    #Add text of the message
    msg += data.text

    return msg


#Save conversation into .txt if nedeed
async def SaveConversationTXT(name, client):

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
    for i in range(len(data) - 1, 0, -1):
        if data[i].sender_id != self_id:
            return i


#Get training data to train model
async def GetTrainDataByName(name, client, limit = None):

    self_id = (await client.get_me()).id

    #Get messages
    user = await client.get_entity(name)
    data = await client.get_messages(user, limit = limit)

    #Do not use np.array to avoid coppy a lot of data
    #X - request - you're companion message
    X = []
    #Y - response you're answer
    Y = []

    #Start with the first conversation message and ends with the lst one
    #Beat data into requests-response 
    i = GetFirstRequest(data, self_id)
    it = 0
    while i >= 0:
        request = ""

        #Get k-th request
        for j in range(i, -1, -1):
            if data[j].sender_id != self_id:
                request += str(message_preprocessing(data[j])) + ". "
                i -= 1
            else :
                break

        X.append(request)

        response = ""

        #Get k-th response
        for j in range(i, -1, -1):
            if data[j].sender_id == self_id:
                response += str(message_preprocessing(data[j])) + ". "
                i -= 1
            else :
                break

        Y.append(response)

        print(str(it) +  ": (" + request + ") -- [", response + "]")

        #i -= 1
        it += 1

    #Save into txt (temporary solution)
    with open("X.txt", 'w') as f:
        for i in X:
            f.write(i)
            f.write("\n")

    with open("Y.txt", 'w') as f:
        for i in Y:
            f.write(i)
            f.write("\n")

    return X, Y

