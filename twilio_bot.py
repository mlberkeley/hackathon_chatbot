from twilio.rest import TwilioRestClient 
import json
 
ACCOUNT_SID = "ACa703617b4913594018f631be3c2b2cdb" 
AUTH_TOKEN = "810efbfaa704414400ab324a75661eea" 
NUMBER = "+16503628351"
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def get_recent_messages(client):

	messages = client.messages.list()
	recipient_nums = set([m.__dict__['from_'] for m in messages if m.__dict__['from_'] != NUMBER])

	json_list = []
	messages_dict = {}

	for num in recipient_nums:
		msgs_for_sender = client.messages.list(From=num)
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

if __name__=='__main__':
	get_recent_messages(client)