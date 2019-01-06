from abc import ABCMeta, abstractmethod
from .. import utilities
from ..ta.base import OffsetTA, WindowTA, DualWindowTA


class AbstractSignal(object):
    __metaclass__ = ABCMeta
    '''
    @abstractmethod
    def GET_ALL_OPTIMIZATION_PARAMETER(parameter_list):
        raise NotImplementedError("Should implement GET_ALL_OPTIMIZATION_PARAMETER()")
    '''


class Signal(AbstractSignal):
    def __init__(self, strategy):
        self.strategy = strategy
        self.session = strategy.session
        self.isTrigger = False

    def IsTAAdded(self, TAClass, taList, para):
        for ta in taList:
            if issubclass(type(ta), DualWindowTA):
                if ta.slug == TAClass.GetSlug(para['xDataName'], para['XWindowSize'], para['yDataName'],
                                              para['yWindowSize']):
                    return ta
            elif issubclass(type(ta), WindowTA):
                if ta.slug == TAClass.GetSlug(para['dataName'], para['windowSize']):
                    return ta
            elif type(ta) == type(OffsetTA):
                if ta.slug == TAClass.GetSlug(para['dataName'], para['offset']):
                    return ta
        return False

    def SetupNewTA(self, TAClass, para):
        if issubclass(TAClass, DualWindowTA) or TAClass == DualWindowTA:
            newTA = TAClass(self.session, para['xDataName'], para['xWindowSize'], para['yDataName'],
                            para['yWindowSize'], para['isIntraDay'])
            return newTA
        elif issubclass(TAClass, WindowTA) or TAClass == WindowTA:
            newTA = TAClass(self.session, para['dataName'], para['windowSize'], para['isIntraDay'])
            return newTA
        else:
            newTA = TAClass(self.session, para['dataName'], para['offset'], para['isIntraDay'])
            return newTA
        return newTA


    def AddTA(self, TAClass, para):
        para['isIntraDay'] = False
        if issubclass(TAClass, DualWindowTA) or TAClass == DualWindowTA:
            if utilities.IsIntraDayData(para['xDataName']) or utilities.IsIntraDayData(para['yDataName']):
                para['isIntraDay'] = True
        else:
            para['isIntraDay'] = utilities.IsIntraDayData(para['dataName'])

        isAdded = False
        if para['isIntraDay']:
            result = self.IsTAAdded(TAClass, self.strategy.intraDayTA, para)
            if result is not False:
                return result
            return self.SetupNewTA(TAClass, para)

        else:
            result = self.IsTAAdded(TAClass, self.strategy.interDayTA, para)
            if result is not False:
                return result
            return self.SetupNewTA(TAClass, para)

    '''
    def AddOffsetTA(self, dataName, offset):
        if utilities.IsIntraDayData(dataName):
            isAdded = False
            for ta in self.strategy.intraDayTA:
                if type(ta) is OffsetTA:
                    if ta.dataName == dataName and ta.offset == offset:
                        isAdded = True
                        return ta
            if isAdded is False:
                newTA = OffsetTA(self.strategy.session, dataName, offset, True)
                return newTA
        else:
            isAdded = False
            for ta in self.strategy.interDayTA:
                if type(ta) is OffsetTA:
                    if ta.dataName == dataName and ta.offset == offset:
                        isAdded = True
                        return ta
            if isAdded is False:
                newTA = OffsetTA(self.strategy.session, dataName, offset, False)
                return newTA
    '''



    def GetData(self, dataName):
        dataName = dataName.lower()
        if dataName == "tr" or dataName=="atr":
            self.strategy.useTR = True
            return self.strategy.TR
        if dataName == "open":
            return self.strategy.open
        elif dataName == "high":
            return self.strategy.high
        elif dataName == "low":
            return self.strategy.low
        elif dataName == "close":
            return self.strategy.close
        elif dataName == "vol" or dataName == "volume":
            return self.strategy.volume


        elif dataName == "opend":
            return self.strategy.openD
        elif dataName == "highd":
            return self.strategy.highD
        elif dataName == "lowd":
            return self.strategy.lowD
        elif dataName == "closed":
            return self.strategy.closeD
        elif dataName == "vold" or dataName == "volumed":
            return self.strategy.volumeD


        elif dataName == "afternoonopend":
            return self.strategy.afternoonOpenD
        elif dataName == "afternoonhighd":
            return self.strategy.afternoonHighD
        elif dataName == "afternoonlowd":
            return self.strategy.afternoonLowD
        elif dataName == "afternoonclosed":
            return self.strategy.afternoonCloseD
        elif dataName == "afternoonvold" or dataName == "afternoonvolumed":
            return self.strategy.afternoonVolumeD


        elif dataName == "ranged":
            return self.strategy.ranged
        elif dataName == "uppershadowd":
            return self.strategy.upperShadowD
        elif dataName == "lowershadowd":
            return self.strategy.lowerShadowD
        elif dataName == "bodyd":
            return self.strategy.bodyD


        elif dataName == "afternoonranged":
            return self.strategy.afternoonRangeD
        elif dataName == "afternoonuppershadowd":
            return self.strategy.afternoonUpperShadowD
        elif dataName == "afternoonlowershadowd":
            return self.strategy.afternoonLowerShadowD
        elif dataName == "afternoonbodyd":
            return self.strategy.afternoonBodyD

    def Label(self):
        return self.name + "(SL:"+str(self.strategy.stopLoss)+")"

    def Reset(self):
        pass

    def OnNewDay(self, bar):
        pass

    def OnDayEnd(self):
        pass

    def CalculateSignal(self, bar):
        return True


class EntrySignal(Signal):
    def __init__(self, strategy):
        super().__init__(strategy)
        self.strategy.entrySignals.append(self)


class ExitSignal(Signal):
    def __init__(self, strategy):
        super().__init__(strategy)
        self.strategy.exitSignals.append(self)
