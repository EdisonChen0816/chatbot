# encoding=utf-8
from src.nlu import NLU
from gensim.models import KeyedVectors
import json
from flask import Flask
from flask import request
from flask_json import FlaskJSON, as_json
from src.index.index import Index
from src.ner import EntityRec
from src.util.logger import setlogger
from src.util.yaml_util import loadyaml


# flask
app = Flask(__name__)
flask_json = FlaskJSON(app)

# 加载配置文件和日志
config = loadyaml('conf/chatbot.yaml')
logger = setlogger(config)

ner_path = './data/entity'
intent_path = './data/intent'
faq_path = './data/faq'
chat_path = './data/chat'

# 加载资源
w2v = KeyedVectors.load(config['w2v_path'])
ner = EntityRec(config['ner_path'])
intent_index = Index(config['intent_path'], w2v)
faq_index = Index(config['faq_path'], w2v)
chat_index = Index(config['chat_path'], w2v)

nlu = NLU(ner, intent_index, faq_index, chat_index)


@app.route("/chatbot", methods=["POST"])
@as_json
def server():
    response = {}
    try:
        data = request.get_json(force=False, silent=False)
        request_encoder = json.loads(json.dumps(data))
        user = request_encoder['user']
        text = request_encoder['text']
        response = nlu.nlu_rec(text)
        response['err_no'] = 0
        logger.info('user:' + str(user) + ' ,text:' + str(text) + ' ,resp:' + json.dumps(response, ensure_ascii=False))
    except Exception as e:
        logger.error(e)
        response['err_no'] = 1
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=58888)