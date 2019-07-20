from .base import TA, WindowTA, DualWindowTA, TALibTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy

import talib


# region ATR related
class ATR(TALibTA):
    @staticmethod
    def GetSlug(dataName="close", windowSize=14):
        return dataName +"-"+str(windowSize)+"_atr"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") ATR"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = ATR.GetName(self.dataName, self.windowSize)
        self.slug = ATR.GetSlug(self.dataName, self.windowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")

    def GetATR(self):
        npHigh = np.asarray(self.high[-self.windowSize-1:], dtype=np.float64)
        npLow = np.asarray(self.low[-self.windowSize-1:], dtype=np.float64)
        npClose = np.asarray(self.close[-self.windowSize-1:], dtype=np.float64)
        atr = talib.ATR(npHigh, npLow, npClose, timeperiod=self.windowSize)
        return atr[-1]

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetATR())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.high) < self.windowSize + 1:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetATR()

    def Calculate(self, bar):
        if len(self.high) <= self.windowSize + 1:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = self.GetATR()
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetATR()


class MaxPreviousATR(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize, compareWindowSize):
        return dataName +"-"+str(windowSize)+"-"+str(compareWindowSize)+"_previousMaxATR"

    @staticmethod
    def GetName(dataName, windowSize, compareWindowSize):
        return dataName+"("+str(windowSize)+", "+str(compareWindowSize)+") PreviousMaxATR"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]
        self.compareWindowSize = self.params["compareWindowSize"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = MaxPreviousATR.GetName(self.dataName, self.windowSize, self.compareWindowSize)
        self.slug = MaxPreviousATR.GetSlug(self.dataName, self.windowSize, self.compareWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")

        self.atrVal = []

    def GetMaxPreviousATR(self):
        npHigh = np.asarray(self.high[-self.windowSize-1:], dtype=np.float64)
        npLow = np.asarray(self.low[-self.windowSize-1:], dtype=np.float64)
        npClose = np.asarray(self.close[-self.windowSize-1:], dtype=np.float64)
        atr = talib.ATR(npHigh, npLow, npClose, timeperiod=self.windowSize)
        self.atrVal.append(atr[-1])
        if len(self.atrVal) <= self.compareWindowSize:
            return False

        val = cmath.MaxOfRange(self.atrVal, -self.compareWindowSize-1, len(self.atrVal)-1)
        return val

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetMaxPreviousATR())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.high) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetMaxPreviousATR()

    def Calculate(self, bar):
        if len(self.high) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = self.GetMaxPreviousATR()
                if val == False:
                    self.isReady = False
                    return
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:

            val = self.GetMaxPreviousATR()
            if val == False:
                self.isReady = False
                return

            self.values[-1] = val


class MinPreviousATR(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize, compareWindowSize):
        return dataName +"-"+str(windowSize)+"-"+str(compareWindowSize)+"_previousMinATR"

    @staticmethod
    def GetName(dataName, windowSize, compareWindowSize):
        return dataName+"("+str(windowSize)+", "+str(compareWindowSize)+") PreviousMinATR"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]
        self.compareWindowSize = self.params["compareWindowSize"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = MinPreviousATR.GetName(self.dataName, self.windowSize, self.compareWindowSize)
        self.slug = MinPreviousATR.GetSlug(self.dataName, self.windowSize, self.compareWindowSize)

        if self.isIntraDay:
            self.high = utilities.GetDataByName(self.session, "high")
            self.low = utilities.GetDataByName(self.session, "low")
            self.close = utilities.GetDataByName(self.session, "close")
        else:
            self.high = utilities.GetDataByName(self.session, "highD")
            self.low = utilities.GetDataByName(self.session, "lowD")
            self.close = utilities.GetDataByName(self.session, "closeD")

        self.atrVal = []

    def GetMinPreviousATR(self):
        npHigh = np.asarray(self.high[-self.windowSize-1:], dtype=np.float64)
        npLow = np.asarray(self.low[-self.windowSize-1:], dtype=np.float64)
        npClose = np.asarray(self.close[-self.windowSize-1:], dtype=np.float64)
        atr = talib.ATR(npHigh, npLow, npClose, timeperiod=self.windowSize)
        self.atrVal.append(atr[-1])
        if len(self.atrVal) <= self.compareWindowSize:
            return False

        val = cmath.MinOfRange(self.atrVal, -self.compareWindowSize-1, len(self.atrVal)-1)
        return val

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetMinPreviousATR())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.high) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetMinPreviousATR()

    def Calculate(self, bar):
        if len(self.high) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = self.GetMinPreviousATR()
                if val == False:
                    self.isReady = False
                    return
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:

            val = self.GetMinPreviousATR()
            if val == False:
                self.isReady = False
                return

            self.values[-1] = val
# endregion
