#
# Copyright 2014 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

import os
import requests
import json
from flask import Flask, render_template, request, Response, stream_with_context, abort
from watson_developer_cloud import ToneAnalyzerV3
app = Flask(__name__)

class ToneAnalyzerService:
    """Wrapper on the Text to Speech service"""

    def __init__(self):
        """
        Construct an instance. Fetches service parameters from VCAP_SERVICES
        runtime variable for Bluemix, or it defaults to local URLs.
        """
        vcapServices = os.getenv("VCAP_SERVICES")
        # Local variables
        # self.url = "<url>"
        # self.username = "<username>"
        # self.password = "<password>"
        #
        # if vcapServices is not None:
        #     print("Parsing VCAP_SERVICES")
        #     services = json.loads(vcapServices)
        #     svcName = "tone_analyzer"
        #     if svcName in services:
        #         print("Text to Speech service found!")
        #         svc = services[svcName][0]["credentials"]
        #         self.url = svc["url"]
        #         self.username = svc["username"]
        #         self.password = svc["password"]
        #         self.watson_module = ToneAnalyzerV3(
        #             username=self.username,
        #             password=self.password,
        #             url=self.url,
        #             version=ToneAnalyzerV3.latest_version)
        #     else:
        #         print("ERROR: The Text Analysis service you were looking for was not found")


        self.watson_module = ToneAnalyzerV3(
                    username="8dd8976d-adb7-44aa-a1d5-ba57f2051bb2",
                    password="XL2baWIDp5x1",
                    version=ToneAnalyzerV3.latest_version)

    def synthesize(self, text, service='tinder', sentences=None):
        """
        Returns the get HTTP response by doing a GET to
        /v1/synthesize with text, voice, accept
        """
        #if sentences is set then send it to tonal analysis
        if text:
            response = self.watson_module.tone(text,sentences=sentences)
            tfurl = 'http://172.18.0.6:8081/'
            res = requests.post(tfurl, data = {'input': text})        
            return {'text':res.text}
        #TODO: Matt can you add your tonal analysis shit here
        #TODO: ship off to tf_url and return it's response
        return {'text':''}

@app.route('/', methods=['GET'])
def index():
    #TODO: switch this to render a markdown template with blurb about our project
    return render_template('index.html')

@app.route('/synthesize', methods=['GET'])
def synthesize():
    text = request.args.get('text', 'Hello')
    service = request.args.get('service', 'tinder')
    sentences = eval(request.args.get('sentences','True'))
    print(request.args, text)   
    headers = {}
    #
    # if download:
    #     headers['content-disposition'] = 'attachment; filename=transcript.ogg'

    try:
        req = textToSpeech.synthesize(text, service, sentences)
        # return Response(stream_with_context(req.iter_content()),
        print(req.text)
        return Response(req.text)
            #headers=headers, content_type = req.headers['content-type'])
    except Exception as e:
        print(e)
        abort(500)

@app.errorhandler(500)
def internal_Server_error(error):
    return 'Error processing the request', 500

# Global watson service wrapper
textToSpeech = None

if __name__ == "__main__":
    textToSpeech = ToneAnalyzerService()

    # Get host/port from the Bluemix environment, or default to local
    #TODO: Change this so that it can run on cycle
    HOST_NAME = os.getenv("VCAP_APP_HOST", "0.0.0.0")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))

    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
