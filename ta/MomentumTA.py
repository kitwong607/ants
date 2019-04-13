from .base import TA, WindowTA, DualWindowTA, TALibTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy

import talib


# region RSI related
class RSI(WindowTA):
    @staticmethod
    def GetSlug(dataName="close", windowSize=14):
        return dataName +"-"+str(windowSize)+"_rsi"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") RSI"


    def __init__(self, session, dataName, windowSize: int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.name = RSI.GetName(dataName, windowSize)
        self.slug = RSI.GetSlug(dataName, windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def GetRSI(self):
        return cmath.RSI(self.data, -self.windowSize, len(self.data))

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetRSI())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetRSI()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetRSI())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetRSI())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetRSI()
# endregion


# region MACD related
class MACD(TALibTA):
    @staticmethod
    def GetSlug(dataName, fastWindowSize, slowWindowSize, signalWindowSize):
        return dataName +"-"+str(fastWindowSize)+"-"+str(slowWindowSize)+"-"+str(signalWindowSize)+"_macd"

    @staticmethod
    def GetName(dataName, fastWindowSize, slowWindowSize, signalWindowSize):
        return dataName+"("+str(fastWindowSize)+","+str(slowWindowSize)+","+str(signalWindowSize)+") MACD"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastWindowSize = self.params["fastWindowSize"]
        self.slowWindowSize = self.params["slowWindowSize"]
        self.signalWindowSize = self.params["signalWindowSize"]

        self.windowSize = self.slowWindowSize + (self.signalWindowSize - 1)

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = MACD.GetName(self.dataName, self.fastWindowSize, self.slowWindowSize, self.signalWindowSize)
        self.slug = MACD.GetSlug(self.dataName, self.fastWindowSize, self.slowWindowSize, self.signalWindowSize)
        self.data = utilities.GetDataByName(self.session, self.dataName)

    def GetMACD(self):
        npArray = np.asarray(self.data[-self.windowSize:], dtype=np.float64)
        macd, macdsignal, macdhist = talib.MACD(npArray, fastperiod=self.fastWindowSize, slowperiod=self.slowWindowSize, signalperiod=self.signalWindowSize)
        return macd[-1]

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetMACD())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetMACD()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetMACD())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetMACD())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetMACD()


class MACDSignalLine(TALibTA):
    @staticmethod
    def GetSlug(dataName, fastWindowSize, slowWindowSize, signalWindowSize):
        return dataName +"-"+str(fastWindowSize)+"-"+str(slowWindowSize)+"-"+str(signalWindowSize)+"_macd-signal-line"

    @staticmethod
    def GetName(dataName, fastWindowSize, slowWindowSize, signalWindowSize):
        return dataName+"("+str(fastWindowSize)+","+str(slowWindowSize)+","+str(signalWindowSize)+") MACDSignalLine"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastWindowSize = self.params["fastWindowSize"]
        self.slowWindowSize = self.params["slowWindowSize"]
        self.signalWindowSize = self.params["signalWindowSize"]

        self.windowSize = self.slowWindowSize + (self.signalWindowSize - 1)

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = MACDSignalLine.GetName(self.dataName, self.fastWindowSize, self.slowWindowSize, self.signalWindowSize)
        self.slug = MACDSignalLine.GetSlug(self.dataName, self.fastWindowSize, self.slowWindowSize, self.signalWindowSize)
        self.data = utilities.GetDataByName(self.session, self.dataName)

    def GetMACDSignalLine(self):
        npArray = np.asarray(self.data[-self.windowSize:], dtype=np.float64)
        macd, macdsignal, macdhist = talib.MACD(npArray, fastperiod=self.fastWindowSize, slowperiod=self.slowWindowSize, signalperiod=self.signalWindowSize)
        return macdsignal[-1]

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetMACDSignalLine())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetMACDSignalLine()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetMACDSignalLine())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetMACDSignalLine())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetMACDSignalLine()
# endregion



# region Stochastic related
class StochasticSlowK(TALibTA):
    @staticmethod
    def GetSlug(fastKWindowSize, slowKWindowSize, slowDWindowSize):
        return "stochastic-slow-k_" + str(fastKWindowSize)+"-"+str(slowKWindowSize)+"-"+str(slowDWindowSize)

    @staticmethod
    def GetName(fastKWindowSize, slowKWindowSize, slowDWindowSize):
        return "StochasticSlowK ("+str(fastKWindowSize)+","+str(slowKWindowSize)+","+str(slowDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.slowKWindowSize = self.params["slowKWindowSize"]
        self.slowDWindowSize = self.params["slowDWindowSize"]

        self.windowSize = self.fastKWindowSize + self.slowKWindowSize + self.slowDWindowSize

        super().__init__(params)
        self.name = StochasticSlowK.GetName(self.fastKWindowSize, self.slowKWindowSize, self.slowDWindowSize)
        self.slug = StochasticSlowK.GetSlug(self.fastKWindowSize, self.slowKWindowSize, self.slowDWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticK(self):
        high = np.asarray(self.high[-self.windowSize:], dtype=np.float64)
        low = np.asarray(self.low[-self.windowSize:], dtype=np.float64)
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCH(high, low, close, fastk_period=self.fastKWindowSize, slowk_period=self.slowKWindowSize, slowk_matype=0, slowd_period=self.slowDWindowSize, slowd_matype=0)
        return k[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticK())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticK()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticK())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticK())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticK()

class StochasticSlowD(TALibTA):
    @staticmethod
    def GetSlug(fastKWindowSize, slowKWindowSize, slowDWindowSize):
        return "stochastic-slow-d_" + str(fastKWindowSize)+"-"+str(slowKWindowSize)+"-"+str(slowDWindowSize)

    @staticmethod
    def GetName(fastKWindowSize, slowKWindowSize, slowDWindowSize):
        return "StochasticSlowD ("+str(fastKWindowSize)+","+str(slowKWindowSize)+","+str(slowDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.slowKWindowSize = self.params["slowKWindowSize"]
        self.slowDWindowSize = self.params["slowDWindowSize"]

        self.windowSize = self.fastKWindowSize + self.slowKWindowSize + self.slowDWindowSize

        super().__init__(params)
        self.name = StochasticSlowD.GetName(self.fastKWindowSize, self.slowKWindowSize, self.slowDWindowSize)
        self.slug = StochasticSlowD.GetSlug(self.fastKWindowSize, self.slowKWindowSize, self.slowDWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticD(self):
        high = np.asarray(self.high[-self.windowSize:], dtype=np.float64)
        low = np.asarray(self.low[-self.windowSize:], dtype=np.float64)
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCH(high, low, close, fastk_period=self.fastKWindowSize, slowk_period=self.slowKWindowSize, slowk_matype=0, slowd_period=self.slowDWindowSize, slowd_matype=0)
        return d[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticD())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticD()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticD())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticD())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticD()

class StochasticFastK(TALibTA):
    @staticmethod
    def GetSlug(fastKWindowSize, fastDWindowSize):
        return "stochastic-fast-k_" + str(fastKWindowSize)+"-"+str(fastDWindowSize)

    @staticmethod
    def GetName(fastKWindowSize, fastDWindowSize):
        return "StochasticFastK ("+str(fastKWindowSize)+","+str(fastDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.fastDWindowSize = self.params["fastDWindowSize"]

        self.windowSize = self.fastKWindowSize + self.fastDWindowSize

        super().__init__(params)
        self.name = StochasticFastK.GetName(self.fastKWindowSize, self.fastDWindowSize)
        self.slug = StochasticFastK.GetSlug(self.fastKWindowSize, self.fastDWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticK(self):
        high = np.asarray(self.high[-self.windowSize:], dtype=np.float64)
        low = np.asarray(self.low[-self.windowSize:], dtype=np.float64)
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCHF(high, low, close, fastk_period=self.fastKWindowSize, fastd_period=self.fastDWindowSize, fastd_matype=0)
        return k[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticK())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticK()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticK())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticK())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticK()

class StochasticFastD(TALibTA):
    @staticmethod
    def GetSlug(fastKWindowSize, fastDWindowSize):
        return "stochastic-fast-d_" + str(fastKWindowSize)+"-"+str(fastDWindowSize)

    @staticmethod
    def GetName(fastKWindowSize, fastDWindowSize):
        return "StochasticFastD ("+str(fastKWindowSize)+","+str(fastDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.fastDWindowSize = self.params["fastDWindowSize"]

        self.windowSize = self.fastKWindowSize + self.fastDWindowSize

        super().__init__(params)
        self.name = StochasticFastD.GetName(self.fastKWindowSize, self.fastDWindowSize)
        self.slug = StochasticFastD.GetSlug(self.fastKWindowSize, self.fastDWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticD(self):
        high = np.asarray(self.high[-self.windowSize:], dtype=np.float64)
        low = np.asarray(self.low[-self.windowSize:], dtype=np.float64)
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCHF(high, low, close, fastk_period=self.fastKWindowSize, fastd_period=self.fastDWindowSize, fastd_matype=0)
        return d[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticD())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticD()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticD())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticD())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticD()


class StochasticRSIK(TALibTA):
    @staticmethod
    def GetSlug(rsiWindowSize, fastKWindowSize, fastDWindowSize):
        return "stochastic-rsi-k_" + str(rsiWindowSize)+"-" + str(fastKWindowSize)+"-"+str(fastDWindowSize)

    @staticmethod
    def GetName(rsiWindowSize, fastKWindowSize, fastDWindowSize):
        return "StochasticRSIK ("+str(rsiWindowSize)+","+str(fastKWindowSize)+","+str(fastDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.rsiWindowSize = self.params["rsiWindowSize"]
        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.fastDWindowSize = self.params["fastDWindowSize"]

        self.windowSize = self.rsiWindowSize + self.fastKWindowSize + self.fastDWindowSize

        super().__init__(params)
        self.name = StochasticRSIK.GetName(self.rsiWindowSize, self.fastKWindowSize, self.fastDWindowSize)
        self.slug = StochasticRSIK.GetSlug(self.rsiWindowSize, self.fastKWindowSize, self.fastDWindowSize)

        if self.isIntraDay:
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticK(self):
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCHRSI(close, timeperiod=self.rsiWindowSize, fastk_period=self.fastKWindowSize, fastd_period=self.fastDWindowSize, fastd_matype=0)
        return k[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticK())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticK()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticK())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticK())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticK()

class StochasticRSID(TALibTA):
    @staticmethod
    def GetSlug(rsiWindowSize, fastKWindowSize, fastDWindowSize):
        return "stochastic-rsi-d_" + str(rsiWindowSize)+"-"+str(fastKWindowSize)+"-"+str(fastDWindowSize)

    @staticmethod
    def GetName(rsiWindowSize, fastKWindowSize, fastDWindowSize):
        return "StochasticRSID ("+str(rsiWindowSize)+","+str(fastKWindowSize)+","+str(fastDWindowSize)+")"


    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution


        self.rsiWindowSize = self.params["rsiWindowSize"]
        self.fastKWindowSize = self.params["fastKWindowSize"]
        self.fastDWindowSize = self.params["fastDWindowSize"]

        self.windowSize = self.rsiWindowSize + self.fastKWindowSize + self.fastDWindowSize

        super().__init__(params)
        self.name = StochasticRSID.GetName(self.rsiWindowSize, self.fastKWindowSize, self.fastDWindowSize)
        self.slug = StochasticRSID.GetSlug(self.rsiWindowSize, self.fastKWindowSize, self.fastDWindowSize)

        if self.isIntraDay:
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.close = utilities.GetDataByName(self.session, "closeD")


    def GetStochasticD(self):
        close = np.asarray(self.close[-self.windowSize:], dtype=np.float64)
        k, d = talib.STOCHRSI(close, timeperiod=self.rsiWindowSize, fastk_period=self.fastKWindowSize, fastd_period=self.fastDWindowSize, fastd_matype=0)
        return d[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetStochasticD())
            self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.close) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetStochasticD()

    def Calculate(self, bar):
        if len(self.close) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetStochasticD())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetStochasticD())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetStochasticD()
# endregion