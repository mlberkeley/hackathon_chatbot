import pynder
from flask import Flask, render_template, request, Response, stream_with_context
app = Flask(__name__)

class PynderService:

	def __init__(self):
		FBID = '122078121605611'
		FBTOKEN = 'EAAGm0PX4ZCpsBACTtykJouoGL3zSikIZCX0rc1eanvqzjeNJ3E3HXp8mQw29pMSReQ1SwjGEsUZA6ZBbBbkZCIjrZBgGWyZBGR8ZAZC9cjcytELDqrUyZCJaYwi9dzod4yyLVYYVWNd4EGVkgLnienbWh46EwxrakQE8NYsFUiz7RrMAtdo49N5hnZB9Y44qv7fhRj7zWSC4gGvKIijT5k3hBbbSggXKRJKziGNajsO4BOE9FXmq5aqSRcL'
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
		pass

@app.route('/', methods=['GET'])
def index():
    pyndersesh.like_users()
    messages=pyndersesh.get_recent_messages()
    #TODO: send messages[0] to main flask server

    #TODO: send response from flask server back to tinder with pyndersesh.send_message
    
    return render_template('index.html')

pyndersesh=None
if __name__ == "__main__":
    pyndersesh = PynderService()

    # Get host/port from the Bluemix environment, or default to local
    #TODO: Change this so that it can run on cycle
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))

    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))