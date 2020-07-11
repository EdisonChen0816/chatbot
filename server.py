# encoding=utf-8
from src.nlu import NLU
from gensim.models import KeyedVectors
import json
from flask import Flask
from flask import request
from flask_json import FlaskJSON, as_json


app = Flask(__name__)
flask_json = FlaskJSON(app)

ner_path = './data/entity'
intent_path = './data/intent'
faq_path = './data/faq'
chat_path = './data/chat'
w2v = KeyedVectors.load('./model/w2v/w2v.model')
nlu = NLU(ner_path, intent_path, faq_path, chat_path, w2v)


@app.route("/chatbot", methods=["POST"])
@as_json
def server():
    response = {}
    try:
        data = request.get_json(force=False, silent=False)
        request_encoder = json.loads(json.dumps(data))
        text = request_encoder['text']
        response = nlu.nlu_rec(text)
        response['err_no'] = 0
    except:
        import traceback
        traceback.print_exc()
        response['err_no'] = 1
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=51666)