from .base import TA, WindowTA, DualWindowTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy


class MinX(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_min"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") MIN"


    def __init__(self, session, dataName, windowSize: int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.name = MinX.GetName(dataName, windowSize)
        self.slug = MinX.GetSlug(dataName, windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            if len(self.data) > self.windowSize:
                val = cmath.MinOfRange(self.data, -self.windowSize, len(self.data))
                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return
        '''
        if len(self.data) < self.windowSize:
            return
        '''


    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = cmath.MinOfRange(self.data, -self.windowSize, len(self.data))
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            val = cmath.MinOfRange(self.data, -self.windowSize, len(self.data))
            self.values[-1] = val

class MaxX(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_max"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") MAX"

    def __init__(self, session, dataName, windowSize: int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.name = MaxX.GetName(dataName, windowSize)
        self.slug = MaxX.GetSlug(dataName, windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            if len(self.data) > self.windowSize:
                val = cmath.MaxOfRange(self.data, -self.windowSize, len(self.data))
                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return
        '''
        if len(self.data) < self.windowSize:
            return
        '''

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = cmath.MaxOfRange(self.data, -self.windowSize, len(self.data))
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            val = cmath.MaxOfRange(self.data, -self.windowSize, len(self.data))
            self.values[-1] = val


class MinXY(DualWindowTA):
    @staticmethod
    def GetSlug(xDataName, xWindowSize, yDataName, yWindowSize):
        return xDataName +"-"+str(xWindowSize)+"_"+yDataName+"-"+str(yWindowSize)+"_min"

    @staticmethod
    def GetName(xDataName, xWindowSize, yDataName, yWindowSize):
        return xDataName+"("+str(xWindowSize)+") "+yDataName+"("+str(yWindowSize)+") MIN"

    def __init__(self, session, xDataName, xWindowSize:int, yDataName, yWindowSize:int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        isIntraDay = False
        resolution = "1D"
        if utilities.IsIntraDayData(xDataName) or utilities.IsIntraDayData(yDataName):
            isIntraDay = True
            resolution = session.strategy.signalResolution

        super().__init__(session, xWindowSize, yWindowSize, resolution, isIntraDay, isSave)
        self.xDataName = xDataName
        self.yDataName = yDataName
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.name = MinXY.GetName(xDataName, xWindowSize, yDataName, yWindowSize)
        self.slug = MinXY.GetSlug(xDataName, xWindowSize, yDataName, yWindowSize)

        self.xData = utilities.GetDataByName(session, xDataName)
        self.yData = utilities.GetDataByName(session, yDataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            if len(self.xData) > self.xWindowSize and len(self.yData) > self.yWindowSize:
                #today daily date do not invole
                xVal = cmath.MinOfRange(self.xData, -self.xWindowSize, len(self.xData))
                yVal = cmath.MinOfRange(self.yData, -self.yWindowSize, len(self.yData))
                val = yVal
                if xVal < yVal:
                    val = xVal

                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.xData) <= self.xWindowSize:
            return
        if len(self.yData) <= self.yWindowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            # today daily date do not involed so no need to update in day end
            pass


    def Calculate(self, bar):
        if len(self.xData) <= self.xWindowSize:
            return
        if len(self.yData) <= self.yWindowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                xVal = cmath.MinOfRange(self.xData, -self.xWindowSize, len(self.xData))
                yVal = cmath.MinOfRange(self.yData, -self.yWindowSize, len(self.yData))
                val = yVal
                if xVal < yVal:
                    val = xVal
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            # today daily date do not involed so no need to update in each bar
            pass

class MaxXY(DualWindowTA):
    @staticmethod
    def GetSlug(xDataName, xWindowSize, yDataName, yWindowSize):
        return xDataName +"-"+str(xWindowSize)+"_"+yDataName+"-"+str(yWindowSize)+"_max"

    @staticmethod
    def GetName(xDataName, xWindowSize, yDataName, yWindowSize):
        return xDataName+"("+str(xWindowSize)+") "+yDataName+"("+str(yWindowSize)+") MAX"

    def __init__(self, session, xDataName, xWindowSize:int, yDataName, yWindowSize:int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        resolution = "1D"
        if utilities.IsIntraDayData(xDataName) or utilities.IsIntraDayData(yDataName):
            resolution = session.strategy.signalResolution

        super().__init__(session, xWindowSize, yWindowSize, resolution, isIntraDay, isSave)
        self.xDataName = xDataName
        self.yDataName = yDataName
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.name = MaxXY.GetName(xDataName, xWindowSize, yDataName, yWindowSize)
        self.slug = MaxXY.GetSlug(xDataName, xWindowSize, yDataName, yWindowSize)

        self.xData = utilities.GetDataByName(session, xDataName)
        self.yData = utilities.GetDataByName(session, yDataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            if len(self.xData) > self.xWindowSize and len(self.yData) > self.yWindowSize:
                #today daily date do not invole
                xVal = cmath.MaxOfRange(self.xData, -self.xWindowSize, len(self.xData))
                yVal = cmath.MaxOfRange(self.yData, -self.yWindowSize, len(self.yData))
                val = yVal
                if xVal < yVal:
                    val = xVal

                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)


    def OnDayEnd(self):
        if len(self.xData) <= self.xWindowSize:
            return
        if len(self.yData) <= self.yWindowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            # today daily date do not involed so no need to update in day end
            pass


    def Calculate(self, bar):
        if len(self.xData) <= self.xWindowSize:
            return
        if len(self.yData) <= self.yWindowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                xVal = cmath.MaxOfRange(self.xData, -self.xWindowSize, len(self.xData))
                yVal = cmath.MaxOfRange(self.yData, -self.yWindowSize, len(self.yData))
                val = yVal
                if xVal < yVal:
                    val = xVal
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            # today daily date do not involed so no need to update in each bar
            pass

class MinPreviousX(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_previousMin"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") PreviousMin"


    def __init__(self, session, dataName, windowSize: int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.name = MinPreviousX.GetName(dataName, windowSize)
        self.slug = MinPreviousX.GetSlug(dataName, windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            if len(self.data) > self.windowSize:
                #today daily date do not invole
                val = cmath.MinOfRange(self.data, -self.windowSize-1, len(self.data)-1)
                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            # today daily date do not involed so no need to update in day end
            pass

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = cmath.MinOfRange(self.data, -self.windowSize-1, len(self.data)-1)
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            # today daily date do not involed so no need to update in each bar
            pass

class MaxPreviousX(WindowTA):
    @staticmethod
    def GetSlug(dataName, windowSize):
        return dataName +"-"+str(windowSize)+"_previousMax"

    @staticmethod
    def GetName(dataName, windowSize):
        return dataName+"("+str(windowSize)+") PreviousMax"

    def __init__(self, session, dataName, windowSize: int, isIntraDay, isSave=True):
        resolution = session.strategy.signalResolution

        super().__init__(session, windowSize, resolution, isIntraDay, isSave)
        self.dataName = dataName
        self.name = MaxPreviousX.GetName(dataName, windowSize)
        self.slug = MaxPreviousX.GetSlug(dataName, windowSize)
        self.data = utilities.GetDataByName(session, dataName)

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            if len(self.data) > self.windowSize:
                #today daily date do not invole
                val = cmath.MaxOfRange(self.data, -self.windowSize-1, len(self.data)-1)
                self.values.append(val)
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            # today daily date do not involed so no need to update in day end
            pass

    def Calculate(self, bar):
        if len(self.data) <= self.windowSize:
            return

        self.isReady = True
        if self.isIntraDay:
            if self.resolution == bar.resolution:
                val = cmath.MaxOfRange(self.data, -self.windowSize-1, len(self.data)-1)
                self.values[self.currentDate].append(val)
                self.valuesTimestamp[self.currentDate].append(bar.timestamp)

                self.continueValues.append(val)
                self.continueValuesTimestamp.append(bar.timestamp)
        else:
            # today daily date do not involed so no need to update in each bar
            pass