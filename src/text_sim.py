# encoding=utf8
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math


def bm25(q, t):
    k = 1.5
    b = 0.75
    score = 0.0
    sq = 0.0
    for qt in q:
        if qt in t:
            score += q[qt] * t[qt] * (k + 1) / (t[qt] + k * (1 - b + b * len(t) / 10))
        sq += q[qt]
    if sq > 0:
        s = score / sq
        if s > 0.2:
            s = 0.2 + (s - 0.2) * 0.6
        return s
    else:
        return -1


def ctr(q, t):
    s1 = 0.0
    s2 = 0.0
    for qt in q:
        s1 += q[qt]
        if qt in t:
            s2 += t[qt]
    if s1 == 0:
        return 0.0
    else:
        s = s2 / s1
        if s > 0.5:
            s = 0.5 + (s - 0.5) * 0.5
        return s


def cqr(q, t):
    s1 = 0.0
    s2 = 0.0
    for qt in t:
        s1 += t[qt]
        if qt in q:
            s2 += q[qt]
    if s1 == 0:
        return 0.0
    else:
        s = s2 / s1
        if len(q) - len(t) > 0:
            s /= math.sqrt(1 + (len(q) - len(t)))
        if s > 0.5:
            s = 0.5 + (s - 0.5) * 0.4
    return s


def wmd(s1, s2, w2v):
    return math.sqrt(w2v.wmdistance(s1, s2)) * 0.5


def se_sim(qv, tw, w2v):
    fv = np.zeros([1, 300]).astype('float32')
    for term in tw:
        if term in w2v:
            fv += np.array(w2v[term])
    s = cosine_similarity(qv, fv)[0]
    return s


def query_len_penalty(q):
    return math.log(len(q), 2) - 1.5


def title_len_penalty(t):
    return math.log(len(t), 2) - 1.3


def get_score(qts, tts, qws, tws, w2v, qv):
    #print(qts, tts, qws, tws, qv)
    #print(bm25(qws, tws), ctr(qws, tws), cqr(qws, tws), wmd(qts, tts, w2v), se_sim(qv, tts, w2v)[0], query_len_penalty(qts), title_len_penalty(tts))
    return bm25(qws, tws) * 2 + ctr(qws, tws) + cqr(qws, tws) - wmd(qts, tts, w2v) + se_sim(qv, tts, w2v)[0] + query_len_penalty(qts) + title_len_penalty(tts) - 2.0
