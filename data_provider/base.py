from abc import ABCMeta
from enum import IntEnum

class DataType(IntEnum):
    TICK = 0
    BAR = 1

class BarData():
    def __init__(self, ticker, resolution, timestamp, open_price, high_price, low_price, close_price, vol):
        self.type = DataType.BAR
        self.ticker = ticker
        self.resolution = resolution
        self.timestamp = timestamp
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = vol

class TickData():
    def __init__(self, ticker, timestamp, bid, ask):
        self.type = DataType.TICK
        self.ticker = ticker
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.close_pirce = (bid + ask) / 2

class AbstractDataProdiver(object):
    __metaclass__ = ABCMeta

    def get_last_close(self, ticker):
        if self.is_tick:
            return (self.last_bar[ticker].bid + self.last_bar[ticker].ask)/2
        return self.last_bar[ticker].close_price

    def get_last_bid_ask(self, ticker):
        if self.is_bar:
            return self.last_bar[ticker].close_price, self.last_bar[ticker].close_price
        return self.last_bar[ticker].bid, self.last_bar[ticker].ask

    def get_last_timestamp(self, ticker):
        return self.last_bar[ticker].timestamp

    def get_last_bar(self, ticker):
        return self.last_bar[ticker]

class AbstractBarDataProdiver(AbstractDataProdiver):
    def __init__(self):
        self.data_tickers = []
        self.last_bar = {}
        self.is_tick = False
        self.is_bar = True

    def _store_data(self, data):
        if not data.ticker in self.data_tickers:
            self.last_bar[data.ticker] = {}
        self.last_bar[data.ticker] = data