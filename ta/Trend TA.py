from .base import TA, WindowTA, DualWindowTA
from .SMA import EMA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy

class MACD(CombinedWindowTA):
class MACD(WindowTA):
    @staticmethod
    def GetSlug(dataName="close", fastWindowSize=12, slowWindowSize=26):
        return dataName +"-"+str(fastWindowSize)+"-"+str(slowWindowSize)+"_macd"

    @staticmethod
    def GetName(dataName, fastWindowSize, slowWindowSize):
        return dataName+"("+str(fastWindowSize)+", "+str(slowWindowSize)+") MACD"


    def __init__(self, session, dataName, fastWindowSize: int, slowWindowSize:int, isSave=True):
        self.fastEMA = EMA(session, dataName, fastWindowSize)
        self.slowEMA = EMA(session, dataName, slowWindowSize)

        resolution = session.strategy.signalResolution
        isIntraDay = utilities.IsIntraDayData(dataName)

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)

        self.dataName = dataName
        self.name = MACD.GetName(dataName, fastWindowSize, slowWindowSize)
        self.slug = MACD.GetSlug(dataName, fastWindowSize, slowWindowSize)
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
            mean = cmath.Average(self.data, self.windowSize)
            self.values[-1] = self.GetRSI()
