from enum import IntEnum

'''
class OHLC(object):
    IS_DISPLAY_IN_OPTION = False
    def __init__(self):
        pass
'''


class DataType(IntEnum):
    TICK = 0
    OHLC = 1


class OHLC():
    IS_DISPLAY_IN_OPTION = False

    def __init__(self, row):
        timestamp, openPrice, highPrice, lowPrice, closePrice, vol, ticker, resolution, resolutionInSec, adjustedDate, adjustedTime = row

        self.type = DataType.OHLC
        self.ticker = ticker
        self.resolution = resolution
        self.timestamp = timestamp
        self.openPrice = openPrice
        self.highPrice = highPrice
        self.lowPrice = lowPrice
        self.closePrice = closePrice
        self.volume = vol
        self.adjustedDate = adjustedDate
        self.adjustedTime = adjustedTime


class TickData():
    IS_DISPLAY_IN_OPTION = False

    def __init__(self, ticker, timestamp, bid, ask, adjustedDate=None, adjustedTime=None):
        self.type = DataType.TICK
        self.ticker = ticker
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.closePirce = (bid + ask) / 2
        self.adjustedDate = adjustedDate
        self.adjustedTime = adjustedTime