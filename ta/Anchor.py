from .base import TA, OffsetTA
from .. import utilities, static
from ..cmath import cmath
import datetime
import numpy as np, copy


class PivotPoint(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPoint_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPoint.GetName(dataName, offset)
        self.slug = PivotPoint.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                val = (high + low + close) / 3
                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointR1(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointR1_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point R1 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointR1.GetName(dataName, offset)
        self.slug = PivotPointR1.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = pivotPoint + (pivotPoint - low)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointS1(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointS1_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point S1 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointS1.GetName(dataName, offset)
        self.slug = PivotPointS1.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = pivotPoint - (high - pivotPoint)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointR2(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointR2_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point R2 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointR2.GetName(dataName, offset)
        self.slug = PivotPointR2.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = pivotPoint + (high - low)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointS2(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointS2_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point S2 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointS2.GetName(dataName, offset)
        self.slug = PivotPointS2.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = pivotPoint - (high - low)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointR3(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointR3_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point R3 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointR3.GetName(dataName, offset)
        self.slug = PivotPointR3.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = high + 2 * (pivotPoint - low)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return

class PivotPointS3(OffsetTA):
    @staticmethod
    def GetSlug(dataName, offset):
        return "pivotPointS3_" + str(offset)

    @staticmethod
    def GetName(dataName, offset):
        return "Pivot Point S3 ("+str(offset)+")"


    def __init__(self, session, dataName, offset = 1, isIntraDay = False):
        isIntraDay = False
        super().__init__(session, dataName, offset, isIntraDay)

        self.resolution = "1D"
        self.dataName = dataName
        self.name = PivotPointS3.GetName(dataName, offset)
        self.slug = PivotPointS3.GetSlug(dataName, offset)

        self.highD = utilities.GetDataByName(session, "highD")
        self.lowD = utilities.GetDataByName(session, "lowD")
        self.closeD = utilities.GetDataByName(session, "closeD")

    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            raise ValueError("Pivot Point only support daily bar")
        else:
            #do pre calculation before TA
            if len(self.closeD) > self.offset:
                self.isReady = True
                #today daily date do not invole
                high = self.highD[self.offsetForList]
                low = self.lowD[self.offsetForList]
                close = self.closeD[self.offsetForList]

                pivotPoint = (high + low + close) / 3
                val = low - 2 * (high - pivotPoint)

                self.values.append(int(val))
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        return

    def Calculate(self, bar):
        return