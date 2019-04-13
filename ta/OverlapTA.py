from .base import TA, WindowTA, DualWindowTA, TALibTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy

import talib


# region KAMA related
class KAMA(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_kama"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") KAMA"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = KAMA.GetName(self.dataName, self.windowSize)
        self.slug = KAMA.GetSlug(self.dataName, self.windowSize)
        self.data = utilities.GetDataByName(self.session, self.dataName)

        self.sampleSizeMultipler = 10


    def GetKAMA(self):
        npArray = np.asarray(self.data[-self.windowSize*self.sampleSizeMultipler:], dtype=np.float64)
        kama = talib.KAMA(npArray, self.windowSize)
        return kama[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetKAMA())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize*self.sampleSizeMultipler:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetKAMA()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetKAMA())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetKAMA())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetKAMA()
# endregion


# region BBands related
class BBandsUpper(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize, nbdev):
        return dataName +"-"+str(windowSize)+"-"+str(nbdev)+"_bbands-upper"

    @staticmethod
    def GetName(dataName, windowSize, nbdev):
        return dataName+"("+str(windowSize)+", "+str(nbdev)+") BBandsUpper"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]
        self.nbdev = self.params["nbdev"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = BBandsUpper.GetName(self.dataName, self.windowSize, self.nbdev)
        self.slug = BBandsUpper.GetSlug(self.dataName, self.windowSize, self.nbdev)
        self.data = utilities.GetDataByName(self.session, self.dataName)


    def GetUpperBand(self):
        npArray = np.asarray(self.data[-self.windowSize:], dtype=np.float64)
        upperband, middleband, lowerband = talib.BBANDS(npArray, timeperiod=self.windowSize, nbdevup=self.nbdev, nbdevdn=self.nbdev, matype=0)
        return upperband[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetUpperBand())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetUpperBand()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetUpperBand())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetUpperBand())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetUpperBand()


class BBandsMiddle(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize, nbdev):
        return dataName +"-"+str(windowSize)+"-"+str(nbdev)+"_bbands-middle"

    @staticmethod
    def GetName(dataName, windowSize, nbdev):
        return dataName+"("+str(windowSize)+", "+str(nbdev)+") BBandsMiddle"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]
        self.nbdev = self.params["nbdev"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = BBandsMiddle.GetName(self.dataName, self.windowSize, self.nbdev)
        self.slug = BBandsMiddle.GetSlug(self.dataName, self.windowSize, self.nbdev)
        self.data = utilities.GetDataByName(self.session, self.dataName)


    def GetMiddleBand(self):
        npArray = np.asarray(self.data[-self.windowSize:], dtype=np.float64)
        upperband, middleband, lowerband = talib.BBANDS(npArray, timeperiod=self.windowSize, nbdevup=self.nbdev, nbdevdn=self.nbdev, matype=0)
        return middleband[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetMiddleBand())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetMiddleBand()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetMiddleBand())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetMiddleBand())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetMiddleBand()


class BBandsLower(TALibTA):
    @staticmethod
    def GetSlug(dataName, windowSize, nbdev):
        return dataName +"-"+str(windowSize)+"-"+str(nbdev)+"_bbands-lower"

    @staticmethod
    def GetName(dataName, windowSize, nbdev):
        return dataName+"("+str(windowSize)+", "+str(nbdev)+") BBandsLower"

    def __init__(self, params):
        self.params = params
        self.params["isSave"] = True
        self.params["resolution"] = resolution = self.params['session'].strategy.signalResolution
        self.windowSize = self.params["windowSize"]
        self.nbdev = self.params["nbdev"]

        super().__init__(params)
        self.dataName = self.params['dataName']
        self.name = BBandsLower.GetName(self.dataName, self.windowSize, self.nbdev)
        self.slug = BBandsLower.GetSlug(self.dataName, self.windowSize, self.nbdev)
        self.data = utilities.GetDataByName(self.session, self.dataName)


    def GetLowerBand(self):
        npArray = np.asarray(self.data[-self.windowSize:], dtype=np.float64)
        upperband, middleband, lowerband = talib.BBANDS(npArray, timeperiod=self.windowSize, nbdevup=self.nbdev, nbdevdn=self.nbdev, matype=0)
        return lowerband[-1]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            self.values.append(self.GetLowerBand())
            self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            self.values[-1] = self.GetLowerBand()

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                self.values[self.currentDate].append(self.GetLowerBand())
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(self.GetLowerBand())
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            self.values[-1] = self.GetLowerBand()
# endregion