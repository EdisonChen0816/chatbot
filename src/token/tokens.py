import datetime
import time


class Token(object):

    def __init__(self, info):  # info: (term, label, data, weight)
        self.term = info[0]
        self.label = info[1]
        self.value = info[2]
        self.weight = info[3]


class Term(Token):

    def __init__(self, info):
        Token.__init__(self, info)

    def reduce(self, t):
        return None

    def get_term(self):
        return self.term


class City(Token):
    def __init__(self, info):
        Token.__init__(self, info)

    def reduce(self, t):
        return None

    def get_term(self):
        return '<City>'


class Holiday(Token):

    def __init__(self, info):
        Token.__init__(self, info)

    def reduce(self, t):
        return None

    def get_term(self):
        return '<Holiday>'


class Rubbish(Token):

    def __init__(self, info):
        Token.__init__(self, info)

    def reduce(self, t):
        return None

    def get_term(self):
        return '<Rubbish>'


class Datetime(Token):

    def __init__(self, info):
        Token.__init__(self, info)
        self.datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0)


class Year(Datetime):

    def __init__(self, info):
        Datetime.__init__(self, info)
        if info[1] == "Year":
            self.datetime = self.datetime.replace(year=int(info[2]))
        elif info[1] == "RelYear":
            days = 365
            local_time = time.localtime()
            if ((local_time[0] % 100 != 0 and local_time[0] % 4 == 0)
                    or (local_time[0] % 100 == 0 and local_time[0] % 400 == 0)
                    and local_time[1] > 2):
                # 今年是润年并且月份大于2
                days = 366
            self.datetime = self.datetime + datetime.timedelta(days=int(info[2]) * days)
        else:
            raise("wrong paramater")

    def reduce(self, t):
        if isinstance(t, Month):   
            t.datetime = t.datetime.replace(year=self.datetime.year)
            t.term = self.term + "," + t.term
            t.weight = max(self.weight, t.weight)
            return t
        else:
            return None

    def get_term(self):
        return "<Year>"


class Month(Datetime):

    def __init__(self, info):
        Datetime.__init__(self, info)
        if info[1] == "Month":
            try:
                self.datetime = self.datetime.replace(month=int(info[2]))
            except:
                self.datetime = self.datetime.replace(day=1)
                self.datetime = self.datetime.replace(month=int(info[2]))
        else:
            raise("wrong paramater")

    def reduce(self, t):
        if isinstance(t, Day):
            t.datetime = t.datetime.replace(year=self.datetime.year, month=self.datetime.month)
            t.term = self.term + "," + t.term
            t.weight = max(self.weight, t.weight)
            return t
        else:
            return None

    def get_term(self):
        return "<Month>"


class Day(Datetime):

    def __init__(self, info):
        Datetime.__init__(self, info)
        if info[1] == "Day":
            try:
                self.datetime = self.datetime.replace(day=int(info[2]))
            except:
                self.datetime = self.datetime.replace(month=1)
                self.datetime = self.datetime.replace(day=int(info[2]))
        elif info[1] == "RelDay":
            self.datetime = self.datetime + datetime.timedelta(days=int(info[2]))
        else:
            raise("wrong paramater")

    def reduce(self, t):
        if isinstance(t, Hour):
            t.datetime = t.datetime.replace(
                year=self.datetime.year, month=self.datetime.month, day=self.datetime.day)
            t.term = self.term + "," + t.term
            t.weight = max(self.weight, t.weight)
            return t
        elif isinstance(t, HalfDay):
            t.datetime = t.datetime.replace(
                year=self.datetime.year, month=self.datetime.month, day=self.datetime.day)
            t.term = self.term + "," + t.term
            t.weight = max(self.weight, t.weight)
            return t
        else:
            return None

    def get_term(self):
        return "<Day>"


class RelDay(Datetime):

    def __init__(self, info):
        Token.__init__(self, info)

    def reduce(self, t):
        return None

    def get_term(self):
        return '<RelDay>'


if __name__ == "__main__":
    info = ("dfd", "Year", 2013, 0.5)
    year = Year(info)
    info = ("dfd", "Month", 2, 0.2)
    month = Month(info)
    print(year.reduce(month).datetime)
