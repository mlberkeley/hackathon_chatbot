import pynder
from flask import Flask, render_template, request, Response, stream_with_context
import requests
import json
import os
app = Flask(__name__)

class PynderService:

    def __init__(self):
        FBID = '122078121605611'
        FBTOKEN = 'EAAGm0PX4ZCpsBAE3Ang4k9gAlcOCwdCgCzzYZCi0Uz0jLvc8yTTFAlRDZAFpxdbBV1PrSkr0LPwrnjlMLQezUEMT2bl9kFiPOFKMvpMktM6Fi7W8ZAYntldPy86gLZCzsmZBRQTeJbaHaJuuXYhLucrduYbODT2oo8t71dtQ2egxn69wSZBK0oGarm0iJY32NlxkZCH3M7h3koqZC4FuLBYJAHOfPRgoOYcWiO9vqzZCifJZCg1GLryqct5'
        self.session = pynder.Session(FBID, FBTOKEN)
    def get_recent_messages(self):
        session=self.session
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

    def like_users(self):
        session=self.session
        users = session.nearby_users()
        for user in users[:3]:
            user.like()

    def send_message(self,msg,user):
        session = self.session
        for match in session.matches():
            if match.user.id==user:
                match.message(msg)

@app.route('/', methods=['GET'])
def index():
    pyndersesh.like_users()
    messages=pyndersesh.get_recent_messages()

    url = 'http://127.0.0.1:3000/'

    json_mssg = [messages[0]]
    s = json.dumps(json_mssg) #convert to json
    print(json.loads(s))
    res = requests.post(url, json=s).json()
    print(res)


    jsondata = requests.get(url)
    data = json.loads(jsondata)
    pyndersesh.send_message(data['text'], data['id'])

    return render_template('index.html')

pyndersesh=None
if __name__ == "__main__":
    pyndersesh = PynderService()

    # Get host/port from the Bluemix environment, or default to local
    #TODO: Change this so that it can run on cycle
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "8080"))

    print(HOST_NAME, PORT_NUMBER)
    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
