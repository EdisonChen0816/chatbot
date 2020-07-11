# encoding=utf8
from src import tokens


class Parser:

    @staticmethod
    def get_tokens(info):
        if info[1] == "Year":
            return tokens.Year(info)
        elif info[1] == "Month":
            return tokens.Month(info)
        elif info[1] == "Day":
            return tokens.Day(info)
        elif info[1] == "City":
            return tokens.City(info)
        elif info[1] == "Holiday":
            return tokens.Holiday(info)
        elif info[1] == 'Rubbish':
            return tokens.Rubbish(info)
        elif info[1] == 'RelDay':
            return tokens.RelDay(info)
        else:
            return tokens.Term(info)

    def parse(self, terms):
        tokens_list = []
        for info in terms:
            t = self.get_tokens(info)
            if len(tokens_list) == 0:
                tokens_list.append(t)
            else:
                try:
                    tt = tokens_list[-1].reduce(t)
                    if tt is None:
                        tokens_list.append(t)
                    else:
                        tokens_list[-1] = tt
                except:
                    tokens_list.append(t)
        return tokens_list
