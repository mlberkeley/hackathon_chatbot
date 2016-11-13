import json
from flask import Flask, request
import os
import tensorflow as tf
import chatbot
import data_utils
app = Flask(__name__)

class TFService:


    def __init__(self):
        chatbot.FLAGS.train_dir = 'tmp'
        chatbot.FLAGS.data_dir = 'tmp'
        self.sess = tf.InteractiveSession()
        self.model = chatbot.create_model(self.sess, True)
        self.model.batch_size = 1
        data_dir = 'tmp'
        input_vocab_size = 40000
        output_vocab_size = 40000
        input_vocab_path = os.path.join(data_dir,
                                 "vocab%d.in" % input_vocab_size)
        output_vocab_path = os.path.join(data_dir,
                                 "vocab%d.out" % output_vocab_size)
        self.in_vocab, _ = data_utils.initialize_vocabulary(input_vocab_path)
        _, self.rev_out_vocab = data_utils.initialize_vocabulary(output_vocab_path) 

@app.route('/', methods=['POST'])
def index():

    sentence = request.form['input']
    print(sentence)
    response = chatbot.forward(sentence, server.in_vocab, server.sess, server.model, server.rev_out_vocab)
    print(response)
    return response

server = None
if __name__ == "__main__":
    server = TFService()

    HOST_NAME = "0.0.0.0"
    port = 8081
    app.run(host=HOST_NAME, port=port, debug=False)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
