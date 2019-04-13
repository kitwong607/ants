from abc import ABCMeta
from collections import deque
from .. import utilities

class TA(object):
    __metaclass__ = ABCMeta



class OffsetTA(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def GetSlug(dataName, offset):
        return dataName +"-"+str(offset)+"_offset"

    @staticmethod
    def GetName(dataName, offset):
        return dataName+"("+str(offset)+") OFFSET"


    def __init__(self, session, dataName, offset, isIntraDay):
        self.session = session
        self.lastTimestamp = None
        self.offset = offset
        self.offsetForList = (offset * -1) - 1
        self.strategy = self.session.strategy
        self.dataName = dataName
        self.dataNameComparsion = self.dataName.lower()
        self.isReady = False


        self.name = OffsetTA.GetName(self.dataName, self.offset)
        self.slug = OffsetTA.GetSlug(self.dataName, self.offset)


        self.isSave = True
        self.isIntraDay = isIntraDay

        self.continueValues = []
        self.values = []
        self.valuesTimestamp = []

        if self.isIntraDay:
            self.resolution = self.strategy.signalResolution
            self.values = {}
            self.valuesTimestamp = {}
            self.continueValues = []
            self.continueValuesTimestamp = []
            self.strategy.AddIntraDayTA(self)
        else:
            self.resolution = "1D"
            self.strategy.AddInterDayTA(self)
        if self.dataName is not "":
            self.data = utilities.GetDataByName(session, self.dataName)


    def Calculate(self, bar):
        if len(self.data) >= self.offset + 1:
            self.isReady = True
            if self.isIntraDay:
                if self.resolution == bar.resolution:
                    if self.currentDate not in self.values:
                        self.values[self.currentDate] = []
                        self.valuesTimestamp[self.currentDate] = []
                    self.values[self.currentDate].append(self.data[self.offsetForList])
                    self.valuesTimestamp[self.currentDate].append(bar.timestamp)
                    self.continueValues.append(self.data[self.offsetForList])
                    self.continueValuesTimestamp.append(bar.timestamp)
            else:
                #update value for every bar if inter day data
                #like highD, lowD, closeD(if previous day's data will not update)
                #but date will update in current day
                self.values[-1] = self.data[self.offsetForList]


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if len(self.data) >= self.offset + 1:
            if self.isIntraDay:
                self.values[self.currentDate] = []
                self.valuesTimestamp[self.currentDate] = []
            else:
                self.values.append(self.data[self.offsetForList])
                self.valuesTimestamp.append(self.currentDate)

    def OnDayEnd(self):
        if len(self.data) >= self.offset + 1:
            if not self.isIntraDay:
                self.values[-1] = self.data[self.offsetForList]

    def __getitem__(self, key):
        if self.isIntraDay:
            return self.continueValues[key]
        return self.values[key]

    def __len__(self):
        if self.isIntraDay:
            return len(self.continueValues)
        return len(self.values)


    def ToDict(self):
        if not self.isSave:
            return

        from .. import static
        from datetime import timedelta
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        d['type'] = "OffsetTA"
        d['resolution'] = self.resolution
        d['offset'] = self.offset
        d['values'] = self.values

        if self.isIntraDay:
            d['isIntraDay'] = "true"
            d['valuesTimestamp'] = {}
            for dateKey in self.valuesTimestamp:
                d['valuesTimestamp'][dateKey] = []
                for ts in self.valuesTimestamp[dateKey]:
                    d['valuesTimestamp'][dateKey].append((ts + timeOffset).timestamp())
        else:
            d['isIntraDay'] = "false"
            d['valuesTimestamp'] = self.valuesTimestamp

        return d


class WindowTA(object):
    __metaclass__ = ABCMeta

    def __init__(self, session, windowSize, resolution, isIntraDay, isSave):
        self.session = session
        self.lastTimestamp = None
        self.windowSize = windowSize
        self.resolution = resolution
        self.strategy = self.session.strategy
        self.isReady = False


        self.isSave = isSave
        self.isIntraDay = isIntraDay

        self.continueValue = []
        self.continueValueTimestamp = []

        if self.isIntraDay:
            self.resolution = self.strategy.signalResolution
            self.currentDate = None
            self.values = {}
            self.valuesTimestamp = {}
            self.continueValues = []
            self.continueValuesTimestamp = []

            self.strategy.AddIntraDayTA(self)
        else:
            self.resolution = "1D"
            self.values = []
            self.valuesTimestamp = []

            self.strategy.AddInterDayTA(self)


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            pass

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            pass

    def __getitem__(self, key):
        if self.isIntraDay:
            return self.continueValues[key]
        return self.values[key]

    def __len__(self):
        if self.isIntraDay:
            return len(self.continueValues)
        return len(self.values)


    def ToDict(self):
        if not self.isSave:
            return

        from .. import static
        from datetime import timedelta
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        d['windowSize'] = self.windowSize
        d['resolution'] = self.resolution
        d['type'] = "WindowTA"

        d['values'] = self.values

        if self.isIntraDay:
            d['isIntraDay'] = "true"

            d['valuesTimestamp'] = {}
            for dateKey in self.valuesTimestamp:
                d['valuesTimestamp'][dateKey] = []
                for ts in self.valuesTimestamp[dateKey]:
                    d['valuesTimestamp'][dateKey].append((ts + timeOffset).timestamp())
        else:
            d['isIntraDay'] = "false"
            d['valuesTimestamp'] = self.valuesTimestamp
        return d


class DualWindowTA(object):
    __metaclass__ = ABCMeta

    def __init__(self, session, xWindowSize, yWindowSize, resolution, isIntraDay, isSave):
        self.session = session
        self.lastTimestamp = None
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.resolution = resolution
        self.strategy = self.session.strategy
        self.isReady = False

        self.isSave = isSave
        self.isIntraDay = isIntraDay

        self.continueValue = []
        self.continueValueTimestamp = []

        if self.isIntraDay:
            self.resolution = self.strategy.signalResolution
            self.currentDate = None
            self.values = {}
            self.valuesTimestamp = {}
            self.continueValues = []
            self.continueValuesTimestamp = []

            self.strategy.AddIntraDayTA(self)
        else:
            self.resolution = "1D"
            self.values = []
            self.valuesTimestamp = []

            self.strategy.AddInterDayTA(self)


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            pass

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            pass

    def __getitem__(self, key):
        if self.isIntraDay:
            return self.continueValues[key]
        return self.values[key]

    def __len__(self):
        if self.isIntraDay:
            return len(self.continueValues)
        return len(self.values)


    def ToDict(self):
        if not self.isSave:
            return

        from .. import static
        from datetime import timedelta
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        d['xWindowSize'] = self.xWindowSize
        d['yWindowSize'] = self.yWindowSize
        d['resolution'] = self.resolution
        d['type'] = "DualWindowTA"

        d['values'] = self.values

        if self.isIntraDay:
            d['isIntraDay'] = "true"

            d['valuesTimestamp'] = {}
            for dateKey in self.valuesTimestamp:
                d['valuesTimestamp'][dateKey] = []
                for ts in self.valuesTimestamp[dateKey]:
                    d['valuesTimestamp'][dateKey].append((ts + timeOffset).timestamp())
        else:
            d['isIntraDay'] = "false"
            d['valuesTimestamp'] = self.valuesTimestamp
        return d


class TALibTA(object):
    __metaclass__ = ABCMeta

    def __init__(self, paramsDict):
        self.session = paramsDict["session"]
        self.lastTimestamp = None
        self.params = paramsDict
        self.resolution = paramsDict["resolution"]
        self.strategy = self.session.strategy
        self.isReady = False

        self.isSave = paramsDict["isSave"]
        self.isIntraDay = paramsDict["isIntraDay"]

        self.continueValue = []
        self.continueValueTimestamp = []

        if self.isIntraDay:
            self.resolution = self.strategy.signalResolution
            self.currentDate = None
            self.values = {}
            self.valuesTimestamp = {}
            self.continueValues = []
            self.continueValuesTimestamp = []

            self.strategy.AddIntraDayTA(self)
        else:
            self.resolution = "1D"
            self.values = []
            self.valuesTimestamp = []

            self.strategy.AddInterDayTA(self)


    def OnNewDay(self, date_ts):
        self.currentDate = utilities.dtGetDateStr(date_ts)

        if self.isIntraDay:
            self.values[self.currentDate] = []
            self.valuesTimestamp[self.currentDate] = []
        else:
            #do pre calculation before TA
            pass

    def OnDayEnd(self):
        if len(self.data) < self.windowSize:
            return

        if not self.isIntraDay:
            # update last bar on day end
            pass

    def __getitem__(self, key):
        if self.isIntraDay:
            return self.continueValues[key]
        return self.values[key]

    def __len__(self):
        if self.isIntraDay:
            return len(self.continueValues)
        return len(self.values)


    def ToDict(self):
        if not self.isSave:
            return

        from .. import static
        from datetime import timedelta
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        d['params'] = self.params
        d['resolution'] = self.resolution
        d['type'] = "TALibTA"

        d['values'] = self.values
        if self.isIntraDay:
            d['isIntraDay'] = "true"

            d['valuesTimestamp'] = {}
            for dateKey in self.valuesTimestamp:
                d['valuesTimestamp'][dateKey] = []
                for ts in self.valuesTimestamp[dateKey]:
                    d['valuesTimestamp'][dateKey].append((ts + timeOffset).timestamp())
        else:
            d['isIntraDay'] = "false"
            d['valuesTimestamp'] = self.valuesTimestamp
        return d