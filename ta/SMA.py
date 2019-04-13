from .base import TA, WindowTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy

###########################################################
#Please also update SMA.py and SMASlop.py
###########################################################

class SMA(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_sma"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") SMA"

    def __init__(self, session, dataName, windowSize: int, isSave=True):
        resolution = session.strategy.signalResolution
        isIntraDay = utilities.IsIntraDayData(dataName)

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName

        self.name = SMA.GetName(self.dataName, self.windowSize)
        self.slug = SMA.GetSlug(self.dataName, self.windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            mean = cmath.AverageOfRange(self.data, -self.windowSize, len(self.data))
            self.values.append(mean)
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            mean = cmath.AverageOfRange(self.data, -self.windowSize, len(self.data))
            self.values[-1] = mean


    def Calculate(self, bar):
        if len(self.data) < self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                mean = cmath.AverageOfRange(self.data, -self.windowSize, len(self.data))
                self.values[self.currentDate].append(mean)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(mean)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            mean = cmath.AverageOfRange(self.data, -self.windowSize, len(self.data))
            self.values[-1] = mean




class EMA(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_ema"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") EMA"

    def __init__(self, session, dataName, windowSize: int, isSave=True):
        #must put the first line of init to let it calculate first
        self.sma = SMA(session, dataName, windowSize, isSave)

        resolution = session.strategy.signalResolution
        isIntraDay = utilities.IsIntraDayData(dataName)

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.multiplier = 2.0 / (self.windowSize + 1)

        self.name = EMA.GetName(self.dataName, self.windowSize)
        self.slug = EMA.GetSlug(self.dataName, self.windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA

            if len(self.values) == 0:
                ema = self.sma[-1]
            else:
                ema = (self.data[-1] - self.values[-1]) * self.multiplier + self.values[-1]

            #mean = cmath.AverageOfRange(self.data, -self.windowSize, len(self.data))
            #self.values.append(mean)
            self.values.append(ema)
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            if len(self.values) == 0:
                ema = self.sma[-1]
            else:
                ema = (self.data[-1] - self.values[-1]) * self.multiplier + self.values[-1]

            self.values[-1] = ema


    def Calculate(self, bar):
        if len(self.data) < self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                if len(self.values) == 0:
                    ema = self.sma[-1]
                else:
                    ema = (self.data[-1] - self.values[-1]) * self.multiplier + self.values[-1]

                self.values[self.currentDate].append(ema)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(ema)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            if len(self.values) == 0:
                ema = self.sma[-1]
            else:
                ema = (self.data[-1] - self.values[-1]) * self.multiplier + self.values[-1]

            self.values[-1] = ema