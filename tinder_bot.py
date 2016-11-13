import pynder
import time


FBID = '122078121605611'
FBTOKEN = 'EAAGm0PX4ZCpsBAJJJPffLJYmCXLZAlfIgiq2ZBgx3e7mvHbWR63PztvONLwtNFVOgtWy0ufhCfIXcdQJD2Q43ZAIuE03PfIYFOgbUJ6TOtMjvU1G2QmJsW3wwLPGjFcHRoOQaF6m7w6BZCxfTSIsKv35ZA6vdPAWPk1US9jzTBCfri4H5VpTgff4MdTD73rS9Gxajy4abaLdZCAfpZCVJCDLck5NvHoArLe4VMo7mXFzJZBvfL2fNvSn1'


session = pynder.Session(FBID, FBTOKEN)

def get_recent_messages(session):
    users = session.nearby_users()
    matches = session.matches()
    json_list = []
    for match in matches:
        messages_dict = {}
        messages = match.messages #list of messages for that match
        if len(match.messages)!=0: #make sure messages actually exist
            index_of_last_message_sent_by_user = -1
            recipients = [m.to for m in messages]


            for i, e in reversed(list(enumerate(recipients))):
                if e != session.profile:
                    index_of_last_message_sent_by_user = i

            recent_messages = ' '.join(' '.join([m.body for m in messages[index_of_last_message_sent_by_user+1:]]).split()[:10])
            if len(recent_messages)!=0:
                messages_dict['id'] = match.user.id
                messages_dict['text'] = recent_messages
                messages_dict['service'] = 'tinder'
        if len(messages_dict)!=0:
            json_list.append(messages_dict)
    print(json_list)
    return json_list

def like_users(session):
    users = session.nearby_users()
    for user in users[:50]:
        user.like()


if __name__=='__main__':
    start_time = time.time()
    while True:
        like_users(session)
        get_recent_messages(session)
        time.sleep(10-((time.time() - start_time) % 10.0))
