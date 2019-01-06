from abc import ABCMeta
from enum import IntEnum



class AbstractDataSource(object):
    IS_DISPLAY_IN_OPTION = False
    __metaclass__ = ABCMeta

    def GetLastClose(self, ticker):
        if self.isTick:
            return (self.lastBar[ticker].bid + self.lastBar[ticker].ask)/2
        return self.lastBar[ticker].closePrice

    def GetLastBidAsk(self, ticker):
        if self.isBar:
            return self.lastBar[ticker].closePrice, self.lastBar[ticker].closePrice
        return self.lastBar[ticker].bid, self.lastBar[ticker].ask

    def GetLastTime(self, ticker):
        return self.lastBar[ticker].timestamp

    def GetLastBar(self, ticker):
        return self.lastBar[ticker]


class AbstractBarDataSource(AbstractDataSource):
    IS_DISPLAY_IN_OPTION = False
    def __init__(self):
        self.dataTickers = []
        self.lastBar = {}
        self.isTick = False
        self.isBar = True

    def StoreData(self, data):
        if not data.ticker in self.dataTickers:
            self.lastBar[data.ticker] = {}
        self.lastBar[data.ticker] = data