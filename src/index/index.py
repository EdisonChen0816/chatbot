# encoding=utf-8
from src.index import text_sim
import numpy as np
import jieba.posseg as pseg
import jieba
import jieba.analyse
from annoy import AnnoyIndex
from src.util.util import load_data_from_dir


class Item:
    def __init__(self, terms, intent):
        self.key = ""
        self.ts = terms
        self.tw = {}
        for t in terms:
            self.tw[t] = 1
        self.intent = intent
        for term in terms:
            if term.startswith("<") and term.endswith(">"):
                self.key += term


class Index:

    def __init__(self, path, w2v):
        self.index = {}
        self.items = {}
        self.path = path
        self.w2v = w2v
        self.u = AnnoyIndex(300)
        self.build_annoy_index()

    def build_annoy_index(self):
        count = 0
        for item in load_data_from_dir(self.path):
            if len(item) == 2:
                terms = []
                temp = ''
                tws = {}
                for term, p in pseg.cut(item[0]):
                    if term == '<':
                        temp += term
                    elif term == '>':
                        temp += term
                        terms.append(temp)
                        temp = ''
                    elif len(temp) > 0:
                        temp += term
                    else:
                        terms.append(term)
                for k, v in jieba.analyse.extract_tags(item[0], topK=10, withWeight=True):
                    tws[k] = v
                self.items[count] = Item(terms, item[1])
                self.u.add_item(count, self.q2v(tws)[0])
            count += 1
        self.u.build(10)

    def seach_vec(self, v, top_num=30):
        return self.u.get_nns_by_vector(v, n=top_num)

    def add(self, i):
        if i.key not in self.index:
            self.index[i.key] = []
        self.index[i.key].append(i)

    def q2v(self, tws):
        v = np.zeros([1, 300]).astype('float32')
        for k in tws:
            if k in self.w2v:
                v += np.array(self.w2v[k]) * tws[k]
        if len(tws) > 0:
            v /= float(len(tws))
        return v

    def search(self, tokens):
        qtw = {}
        qts = []
        s = ''
        for token in tokens:
            qts.append(token.get_term())
            s += token.get_term()
        for k, v in jieba.analyse.extract_tags(s, topK=10, withWeight=True):
            qtw[k] = v
        ids = self.seach_vec(self.q2v(qtw)[0])
        cands = []
        for id in ids:
            item = self.items[id]
            score = text_sim.get_score(qts, item.ts, qtw, item.tw, self.w2v, self.q2v(qtw))
            cands.append((item, score))
        if len(cands) == 0:
            return 'no cand found'
        cand = sorted(cands, key=lambda x: -x[1])[0]
        if cand[1] > 0:
            intent = cand[0].intent
            return intent
        else:
            return 'score too low'