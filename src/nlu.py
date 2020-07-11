# encoding=utf8
from src.ner import EntityRec
from src.index import Index
from src.parser import Parser
import jieba.posseg as pseg
import jieba
import jieba.analyse
from src.util import remove_punctuation


class NLU:

    def __init__(self, ner_path, intent_path, faq_path, chat_path, w2v):
        self.ner = EntityRec(ner_path)
        self.intent_index = Index(intent_path, w2v)
        self.faq_index = Index(faq_path, w2v)
        self.chat_index = Index(chat_path, w2v)
        self.parser = Parser()

    def get_tokens(self, query):
        terms = []
        poses = []
        ner_map = self.ner.entity_rec(query)
        for k in ner_map:
            jieba.add_word(k, 999)
        weights = {}
        for s, p in pseg.cut(query):
            terms.append(s)
            poses.append(p)
        for k, v in jieba.analyse.extract_tags(query, topK=10, withWeight=True):
            weights[k] = v
        infos = []
        for i, term in enumerate(terms):
            if term in ner_map:
                infos.append(ner_map[term])
            else:
                infos.append([term, "Term", poses[i], weights[term] if term in weights else 0.5])
        tokens = self.parser.parse(infos)
        return tokens

    def nlu_rec(self, query):
        '''
        先进性意图识别、如果未识别到，再进行faq识别，如果又未识别到，进入到闲聊，还未识别到，返回空
        :param query:
        :return:
        '''
        query = remove_punctuation(query)
        tokens = self.get_tokens(query)
        result = {}
        intent = self.intent_index.search(tokens)
        if intent in ['no cand found', 'score too low']:
            # 进入faq
            faq = self.faq_index.search(tokens)
            if faq in ['no cand found', 'score too low']:
                # 进入闲聊
                chat = self.chat_index.search(tokens)
                if chat not in ['no cand found', 'score too low']:
                    result['chat'] = chat
            else:
                result['faq'] = faq
        else:
            result['intent'] = intent
            slot = {}
            for token in tokens:
                if 'Term' != token.label:
                    slot[token.label] = token.term
            result['slot'] = slot
        return result


if __name__ == "__main__":
    pass