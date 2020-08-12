# encoding=utf8
import ahocorasick
from src.util.util import load_data_from_dir


class EntityRec:

    def __init__(self, path):
        self.A = ahocorasick.Automaton()
        for item in load_data_from_dir(path):
            if len(item) == 3:
                self.A.add_word(item[0], "\t".join(item))
        self.A.make_automaton()

    def entity_rec(self, q):
        l = []
        for item in self.A.iter(q):
            end = item[0]
            start = end - len(item[1].split('\t')[0])
            if len(l) > 0 and start == l[-1][0][0] and end >= l[-1][0][1]:
                l[-1] = item[1]
            else:
                l.append(item[1])
        d = {}
        for ll in l:
            tts = ll.split('\t')
            d[tts[0]] = tts + [1.0]
        return d


if __name__ == "__main__":
    s = EntityRec('../data/entity')
    for x in s.entity_rec("易拉罐是什么垃圾"):
        print(x)
