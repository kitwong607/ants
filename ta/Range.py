from abc import ABCMeta, abstractmethod
from .base import TA, WindowTA
from .. import utilities, static
import datetime
import numpy as np, copy


class RangeTA(object):
    __metaclass__ = ABCMeta

    def __init__(self, session, resolution="1T", isSave=True):
        self.session = session
        self.lastTimestamp = None
        self.resolution = resolution
        self.strategy = self.session.strategy

        self.isSave = isSave

        self.continueValue = []
        self.continueValueTimestamp = []


        self.currentDate = None
        self.values = {}
        self.valuesTimestamp = {}
        self.valuesAdjustedTimestamp = {}

        self.strategy.AddIntraDayTA(self)


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)
        self.values[self.currentDate] = []
        self.valuesTimestamp[self.currentDate] = []


    def Calculate(self, bar):
        pass


    def __getitem__(self, key):
        try:
            return self.continueValue[key], self.continueValueTimestamp[key]
        except:
            return False

    def __len__(self):
        return len(self.continueValue)


    def ToDict(self):
        if not self.isSave:
            return

        from .. import static
        from datetime import timedelta
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        print("i missed this think have to think about it")
        #d['windowSize'] = self.windowSize
        d['resolution'] = self.resolution
        d['values'] = self.values

        d['continueValue'] = self.continueValue
        d['continueValueTimestamp'] = []

        for ts in self.continueValueTimestamp:
            d['continueValueTimestamp'].append((ts + timeOffset).timestamp())

        #d['calculatedValues'] = self.calculatedValues

        d['isIntraDay'] = "true"
        d['valuesTimestamp'] = {}
        for dateKey in self.valuesTimestamp:
            d['valuesTimestamp'][dateKey] = []
            for ts in self.valuesTimestamp[dateKey]:
                d['valuesTimestamp'][dateKey].append((ts + timeOffset).timestamp())

        return d


class PreviousDayHighLowRange(RangeTA):
    def __init__(self, session, offset=-2, ratio=1.0, resolution="1T", isSave=True):
        super().__init__(session, resolution, isSave)
        self.name = "PreviousDayHighLowRange(" + str(offset) + ")"
        self.slug = "PreviousDayHighLowRange_" + str(offset)
        self.ratio = ratio
        self.type = "separate"

        self.offset = offset
        self.offsetForList = (offset * -1) - 1


    def PushData(self, bar):
        if bar.resolution != self.resolution:
            return

        self.lastTimestamp = bar.timestamp

        if self.currentDate is None:
            self.OnNewDay(bar.timestamp)

        if len(self.strategy.highD) < self.offset + 1:
            return False

        range = (self.strategy.highD[self.offsetForList] - self.strategy.lowD[self.offsetForList]) * self.ratio

        self.values[self.currentDate].append(range)
        self.valuesTimestamp[self.currentDate].append(bar.timestamp)

        self.continueValue.append(range)
        self.continueValueTimestamp.append(bar.timestamp)

        return self.continueValue[-1], self.continueValueTimestamp[-1]


class MinPreviousDayHighLowRange(RangeTA):
    def __init__(self, session, numOfDay=[-2,-3], resolution="1T", isSave=True):
        super().__init__(session, numOfDay, resolution, isSave)
        self.numOfDayStr = ",".join(numOfDay)
        self.name = "MinPreviousDayHighLowRange(" + self.numOfDayStr + ")"
        self.slug = "MinPreviousDayHighLowRange_" + self.numOfDayStr
        self.type = "separate"


    def PushData(self, bar):
        if bar.resolution != self.resolution:
            return


        self.lastTimestamp = bar.timestamp


        if self.currentDate is None:
            self.OnNewDay(bar.timestamp)

        range = 0
        count = 0
        for day in self.numOfDay:
            if count == 0:
                range = self.strategy.highD[day] - self.strategy.lowD[day]
            else:
                newRange = self.strategy.highD[day] - self.strategy.lowD[day]
                if newRange < range:
                    range = newRange

            count += 1

        self.values[self.currentDate].append(range)
        self.valuesTimestamp[self.currentDate].append(bar.timestamp)

        self.continueValue.append(range)
        self.continueValueTimestamp.append(bar.timestamp)

        return self.continueValue[-1], self.continueValueTimestamp[-1]


class MaxPreviousDayHighLowRange(RangeTA):
    def __init__(self, session, numOfDay=[-2,-3], resolution="1T", isSave=True):
        super().__init__(session, numOfDay, resolution, isSave)
        self.numOfDayStr = ",".join(numOfDay)
        self.name = "MaxPreviousDayHighLowRange(" + self.numOfDayStr + ")"
        self.slug = "MaxPreviousDayHighLowRange_" + self.numOfDayStr
        self.type = "separate"


    def PushData(self, bar):
        if bar.resolution != self.resolution:
            return

        self.lastTimestamp = bar.timestamp
        if self.currentDate is None:
            self.OnNewDay(bar.timestamp)

        range = 0
        count = 0
        for day in self.numOfDay:
            if count == 0:
                range = self.strategy.highD[day] - self.strategy.lowD[day]
            else:
                newRange = self.strategy.highD[day] - self.strategy.lowD[day]
                if newRange > range:
                    range = newRange

            count += 1

        self.values[self.currentDate].append(range)
        self.valuesTimestamp[self.currentDate].append(bar.timestamp)

        self.continueValue.append(range)
        self.continueValueTimestamp.append(bar.timestamp)

        return self.continueValue[-1], self.continueValueTimestamp[-1]


class MinPreviousCandlestickBodyAndShadow(RangeTA):
    def __init__(self, session, numOfDay=-2, resolution="1T", isSave=True):
        super().__init__(session, numOfDay, resolution, isSave)
        self.name = "MinPreviousCandlestickBodyAndShadow(" + str(self.numOfDay) + ")"
        self.slug = "MinPreviousCandlestickBodyAndShadow_" + str(self.numOfDay)
        self.type = "separate"


    def PushData(self, bar):
        if bar.resolution != self.resolution:
            return

        self.lastTimestamp = bar.timestamp
        if self.currentDate is None:
            self.OnNewDay(bar.timestamp)

        range = self.self.strategy.highD[self.numOfDay] - self.strategy.closeD[self.numOfDay]

        newRange = self.self.strategy.closeD[self.numOfDay] - self.strategy.lowD[self.numOfDay]
        if newRange < range:
            range = newRange

        newRange = self.self.strategy.highD[self.numOfDay] - self.strategy.openD[self.numOfDay]
        if newRange < range:
            range = newRange

        newRange = self.self.strategy.openD[self.numOfDay] - self.strategy.lowD[self.numOfDay]
        if newRange < range:
            range = newRange

        self.values[self.currentDate].append(range)
        self.valuesTimestamp[self.currentDate].append(bar.timestamp)

        self.continueValue.append(range)
        self.continueValueTimestamp.append(bar.timestamp)

        return self.continueValue[-1], self.continueValueTimestamp[-1]


class MaxPreviousCandlestickBodyAndShadow(RangeTA):
    def __init__(self, session, numOfDay=-2, resolution="1T", isSave=True):
        super().__init__(session, numOfDay, resolution, isSave)
        self.name = "MaxPreviousCandlestickBodyAndShadow(" + str(self.numOfDay) + ")"
        self.slug = "MaxPreviousCandlestickBodyAndShadow_" + str(self.numOfDay)
        self.type = "separate"


    def PushData(self, bar):
        if bar.resolution != self.resolution:
            return

        self.lastTimestamp = bar.timestamp
        if self.currentDate is None:
            self.OnNewDay(bar.timestamp)

        range = self.self.strategy.highD[self.numOfDay] - self.strategy.closeD[self.numOfDay]

        newRange = self.self.strategy.closeD[self.numOfDay] - self.strategy.lowD[self.numOfDay]
        if newRange > range:
            range = newRange

        newRange = self.self.strategy.highD[self.numOfDay] - self.strategy.openD[self.numOfDay]
        if newRange > range:
            range = newRange

        newRange = self.self.strategy.openD[self.numOfDay] - self.strategy.lowD[self.numOfDay]
        if newRange > range:
            range = newRange

        self.values[self.currentDate].append(range)
        self.valuesTimestamp[self.currentDate].append(bar.timestamp)

        self.continueValue.append(range)
        self.continueValueTimestamp.append(bar.timestamp)

        return self.continueValue[-1], self.continueValueTimestamp[-1]
