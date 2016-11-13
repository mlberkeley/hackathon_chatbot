from twilio.rest import TwilioRestClient
import json
from flask import Flask, render_template, request, Response, stream_with_context
import requests
import os
app = Flask(__name__)

class TwilioService:


    def __init__(self):
        ACCOUNT_SID = "ACa703617b4913594018f631be3c2b2cdb"
        AUTH_TOKEN = "810efbfaa704414400ab324a75661eea"
        self.NUMBER = "+16503628351"
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def get_recent_messages(self):

        messages = self.client.messages.list()
        recipient_nums = set([m.__dict__['from_'] for m in messages if m.__dict__['from_'] != self.NUMBER])

        json_list = []
        messages_dict = {}

        for num in recipient_nums:
            msgs_for_sender = self.client.messages.list(From=num)
            body_list = [msg.body for msg in msgs_for_sender]
            recent_messages = ' '.join(' '.join([w for w in body_list]).split()[:10])
            if len(recent_messages) != 0:
                messages_dict['number'] = num
                messages_dict['text'] = recent_messages
                messages_dict['service'] = 'twilio'

            if len(messages_dict) != 0:
                json_list.append(messages_dict)
        print (json_list)
        return json_list

    def send_message(self,msg,user):
        client = self.client
        client.messages.create(
            to=user,
            from_=self.NUMBER,
            body=msg)


@app.route('/', methods=['GET'])
def index():
    messages=twiliosesh.get_recent_messages()

    url='http://127.0.0.1:3000/synthesize'

    json_mssg = [messages[0]]
    s = json.dumps(json_mssg) #convert to json
    res = requests.get(url, json=s)

    data = json.loads(res.text)
    twiliosesh.send_message(data['text'], json_mssg[0]['number'])

    return render_template('index.html')

twiliosesh=None
if __name__ == "__main__":
    twiliosesh = TwilioService()

    # Get host/port from the Bluemix environment, or default to local
    #TODO: Change this so that it can run on cycle
    HOST_NAME = os.getenv("VCAP_APP_HOST", "0.0.0.0")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "8888"))

    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
