"""
The Conversation v1 service
(https://www.ibm.com/watson/developercloud/conversation.html)
"""

from watson_developer_cloud import WatsonDeveloperCloudService


class Conversation_FW(WatsonDeveloperCloudService):
    """Client for the Conversation service"""

    #TODO: Swap out default_url
    default_url = 'https://gateway.watsonplatform.net/conversation/api'
    #TODO: Swap out latest_version
    latest_version = '2016-09-20'

    def __init__(self, version, url=default_url, tf_embed_url=None, tf_process_url=None, **kwargs):
        WatsonDeveloperCloudService.__init__(self, 'conversation_FW', url, **kwargs)
        self.tf_embed_url=tf_embed_url
        self.tf_process_url=tf_process_url
        self.version = version

    def message(self, workspace_id, message_input=None, context=None, entities=None, intents=None, output=None,
                alternate_intents=False):
        """
        Retrieves information about a specific classifier.
        :param workspace_id: The workspace to use
        :param message_input: The input, usually containing a text field
        :param context: The optional context object
        :param entities: The optional entities
        :param intents: The optional intents
        :param alternate_intents: Whether to return more than one intent.
        :param output: The optional output object
        """

        params = {'version': self.version}

        TF_data = {'input': message_input, 'output': output}

        if self.tf_embed_url!=None:
            #reformat request to tf_embed layer
            return self.request(method='POST', url=self.tf_embed_url, params=params,
                            json=TF_data, accept_json=True)


        data = {'input': message_input,
                'context': context,
                'entities': entities,
                'intents': intents,
                'alternate_intents': alternate_intents,
                'output': output}


        return self.request(method='POST', url='/v1/workspaces/{0}/message'.format(workspace_id), params=params,
                            json=data, accept_json=True)