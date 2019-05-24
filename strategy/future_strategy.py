from .base import AbstractStrategy
from .. import utilities
from ..session import SessionMode

from ..order.base import OrderAction, OrderType
from ..data.datamodel import DataType
from ..cmath import cmath
import pandas as pd, time, os


MONTH_CODE = {"1": "F", "2": "G", "3": "H", "4": "J",
             "5": "K", "6": "M", "7": "N", "8": "Q",
             "9": "U", "10": "V", "11": "X", "12": "Z"}

HKEX_FUTURE = ["HSI","MHI","HHI","MCH"]

#call sequence
#1 on_new_date              -> if data is in a new day
#2 calculate_intra_day_ta   -> if data is intra day data, *it also trigger if on_new_date triggered.
#3 calculate_entry_signals  -> if data is intra day data
#4 calculate_exit_signals   -> if data is intra day data and portfolio contain position

class FutureAbstractStrategy(AbstractStrategy):
    IS_DISPLAY_IN_OPTION = False

    STATUS_WAITING = "WAITING"
    STATUS_ENTERED = "ENTERED"
    STATUS_BREAKOUT_SUCCESS = "BREAKOUT_SUCCESS"
    STATUS_BREAKOUT_FAIL = "BREAKOUT_FAIL"
    STATUS_EXITTED = "EXITTED"

    @staticmethod
    def GET_OPTIMIZATION_PARAMETER(OPTIMIZATION_PARAMETER, isPrint=False):
        import itertools, copy

        newOptimizationParameter = copy.deepcopy(OPTIMIZATION_PARAMETER)
        parameterLists = []
        keyOrder = []
        for key in OPTIMIZATION_PARAMETER:
            parameterValueList = []

            isOptimizationParameter = False
            if "min" in newOptimizationParameter[key]:
                isOptimizationParameter = True

            newOptimizationParameter[key].pop('min', None)
            newOptimizationParameter[key].pop('max', None)
            newOptimizationParameter[key].pop('step', None)

            if isOptimizationParameter:
                for i in range(OPTIMIZATION_PARAMETER[key]['min'], OPTIMIZATION_PARAMETER[key]['max'] + 1,
                               OPTIMIZATION_PARAMETER[key]['step']):
                    if isPrint: self.Log(key, i)
                    parameterValueList.append(i)
                keyOrder.append(key)
                parameterLists.append(parameterValueList)

        productList = list(itertools.product(*parameterLists))
        if isPrint: print(newOptimizationParameter)
        finalOptimizationParameterSetList = []

        if isPrint:
            self.Log("ProductList")
            self.Log(keyOrder)
            self.Log(productList)

        for parameter in productList:
            if isPrint: self.Log(parameter)
            singleOptimizationParameterSet = copy.deepcopy(newOptimizationParameter)
            i = 0
            for key in keyOrder:
                singleOptimizationParameterSet[key]['value'] = parameter[i]
                i += 1

            finalOptimizationParameterSetList.append(singleOptimizationParameterSet)

        if isPrint:
            for set in finalOptimizationParameterSetList:
                self.Log(set)

        return finalOptimizationParameterSetList

    @property
    def currentDate(self):
        return self.date[-1]


    def Setup(self, session):
        self.config = session.config
        self.session = session
        self.Log = self.session.Log
        self.orderHandler = self.session.orderHandler
        self.strategy_class = self.config.strategyClass
        self.contract = self.config.contract
        self.parameter = self.config.strategyParameter

        self.inTradePeriod = False
        self.status = self.STATUS_WAITING

        self.isDayEnd = True
        self.rangeFilter = None
        self.range = None

        self.useTR = False
        self.TR = []


        #common
        self.lastTick = None
        self.bars = []
        self.interDayTA = []
        self.intraDayTA = []

        self.entryCount = 0

        self.baseQuantity = self.config.baseQuantity

        self.mktOpenTime = None
        self.mktCloseTime = None
        self.tradeDateData = None
        self.stopLoss = 60
        if "stopLoss" in self.parameter:
            self.stopLoss = self.parameter["stopLoss"]["value"]

        #filter related
        self.action = None

        self.contact = self.config.contract

        self.date = []
        self.openD = []
        self.highD = []
        self.lowD = []
        self.closeD = []
        self.volumeD = []

        self.morningOpenD = []
        self.morningHighD = []
        self.morningLowD = []
        self.morningCloseD = []
        self.morningVolumeD = []

        self.afternoonOpenD = []
        self.afternoonHighD = []
        self.afternoonLowD = []
        self.afternoonCloseD = []
        self.afternoonVolumeD = []

        self.rangeD = []
        self.upperShadowD = []
        self.lowerShadowD = []
        self.bodyD = []

        self.morningRangeD = []
        self.morningUpperShadowD = []
        self.morningLowerShadowD = []
        self.morningBodyD = []

        self.afternoonRangeD = []
        self.afternoonUpperShadowD = []
        self.afternoonLowerShadowD = []
        self.afternoonBodyD = []

        self.timestamp = []
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.volume = []

        self.sl_price = 0
        self.sp_price = 0
        self.entry_price = 0
        self.entry_time = 0
        self.exit_price = 0
        self.exit_time = 0

        self.entrySignals = []
        self.exitSignals = []

        self.tradeLimit = 0
        self.signalResolution = self.config.signalResolution

        self.minsToExitBeforeMarketClose = None
        self.entryHourLimitInAdjustedTime = None

        if self.parameter is None:
            self.parameter = strategy_class.OPTIMIZATION_PARAMETER

        for key in self.parameter:
            self.session.Log("[Stragtegy parameter]", key +":", self.parameter[key]['value'])


    def isEntry(self):
        if self.entryCount == 0:
            return False
        return True


    def EntryQty(self):
        return self.session.portfolio.GetEntryQty()


    def ExitQty(self):
        return self.session.portfolio.GetExitQty()


    def MaxNet(self):
        position = self.session.portfolio.CurrentPosition()
        if position is None:
            return 0
        else:
            return position.maxNet


    def NetQty(self):
        pass
        return self.session.portfolio.maxNet


    def CalculateBidAsk(self, tick):
        bidAsk = int((int(tick.bid) + int(tick.ask))/2)
        if self.CanCalculateExitSignalByBidAsk(bidAsk):
            self.CalculateExitSignalByBidAsk(bidAsk, tick.adjustedDate, tick.adjustedTime)



    def CalculateTick(self, tick):
        if self.lastTick!=None and self.lastTick.adjustedDate == tick.adjustedDate and self.lastTick.adjustedTime == tick.adjustedTime:
            return

        self.lastTick = tick
        bidAsk = int((int(tick.bid) + int(tick.ask)) / 2)
        if self.CanCalculateExitSignalByBidAsk(bidAsk):
            self.CalculateExitSignalByBidAsk(bidAsk, tick.adjustedDate, tick.adjustedTime)


    def CalculateBar(self, bar):
        # 1 is day end
        if bar.resolution == "1D":
            self.isDayEnd = True
            self.OnDayEnd(bar)
        else:   # (bar.resolution in utilities.INTRADAY_BAR_SIZE) #assum all are intra day
            if bar.resolution not in self.config.dataResolution:
                return

            if len(self.bars)>0 and bar.resolution == self.signalResolution:
                lastAdjustedDate = self.bars[-1].adjustedDate
                currentAdjustedDate = bar.adjustedDate
                if lastAdjustedDate != currentAdjustedDate and self.isDayEnd == False:
                    self.isDayEnd = True
                    self.OnDayEnd(self.bars[-1])

            if (self.isDayEnd):
                self.isDayEnd = False

                self.date.append(utilities.clearTimeInDatetime(bar.timestamp))

                self.mktOpenTime = bar.timestamp
                self.mktOpenTime_min = utilities.getTotalMinuteInDatetime(self.mktOpenTime)
                self.invested = False
                self.entryCount = 0

                self.tradeDateData = self.session.dataSource.GetTickerTradeDateDataByDate(self.currentDate)

                closeTime = self.tradeDateData["aht_close_time"]
                if closeTime == 0:
                    closeTime = self.tradeDateData["close_time"]
                closeTime = str(closeTime)
                closeTime = utilities.addTimeToDatetime(self.currentDate, int(closeTime[0:2]),
                                                            int(closeTime[2:4]), int(closeTime[4:]))
                self.mktCloseTime = closeTime

                afternoonCloseTime = str(self.tradeDateData["close_time"])
                self.mktAfternoonCloseTime = utilities.addTimeToDatetime(self.currentDate, int(afternoonCloseTime[0:2]),
                                                            int(afternoonCloseTime[2:4]), int(afternoonCloseTime[4:]))

                self.mktMorningCloseTime = utilities.addTimeToDatetime(self.currentDate, 12, 30, 0)


                self.openD.append(bar.openPrice)
                self.highD.append(bar.highPrice)
                self.lowD.append(bar.lowPrice)
                self.closeD.append(bar.closePrice)
                self.volumeD.append(bar.volume)

                self.upperShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                self.lowerShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                self.bodyD.append(abs(self.openD[-1] - self.closeD[-1]))
                self.rangeD.append(self.highD[-1] - self.lowD[-1])


                if bar.timestamp <= self.mktMorningCloseTime:
                    self.morningOpenD.append(bar.openPrice)
                    self.morningHighD.append(bar.highPrice)
                    self.morningLowD.append(bar.lowPrice)
                    self.morningCloseD.append(bar.closePrice)
                    self.morningVolumeD.append(bar.volume)

                    self.morningUpperShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.morningLowerShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.morningBodyD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.morningRangeD.append(self.highD[-1] - self.lowD[-1])

                if bar.timestamp <= self.mktAfternoonCloseTime:
                    self.afternoonOpenD.append(bar.openPrice)
                    self.afternoonHighD.append(bar.highPrice)
                    self.afternoonLowD.append(bar.lowPrice)
                    self.afternoonCloseD.append(bar.closePrice)
                    self.afternoonVolumeD.append(bar.volume)

                    self.afternoonUpperShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.afternoonLowerShadowD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.afternoonBodyD.append(abs(self.openD[-1] - self.closeD[-1]))
                    self.afternoonRangeD.append(self.highD[-1] - self.lowD[-1])


                self.UpdateContact()
                self.OnNewDay(bar)


            #Update current Open high low close and volume
            if bar.highPrice > self.highD[-1]: self.highD[-1] = bar.highPrice
            if bar.lowPrice < self.lowD[-1]: self.lowD[-1] = bar.lowPrice
            self.closeD[-1] = bar.closePrice
            self.volumeD[-1] += bar.volume

            self.bodyD[-1] = abs(self.openD[-1] - self.closeD[-1])
            self.rangeD[-1] = self.highD[-1] - self.lowD[-1]

            if self.openD[-1] > self.closeD[-1]:
                self.upperShadowD[-1] = self.highD[-1] - self.openD[-1]
                self.lowerShadowD[-1] = self.closeD[-1] - self.lowD[-1]
            else:
                self.upperShadowD[-1] = self.highD[-1] - self.closeD[-1]
                self.lowerShadowD[-1] = self.openD[-1] - self.lowD[-1]


            if bar.timestamp <= self.mktMorningCloseTime:
                if bar.highPrice > self.morningHighD[-1]: self.morningHighD[-1] = bar.highPrice
                if bar.lowPrice < self.morningLowD[-1]: self.morningLowD[-1] = bar.lowPrice
                self.morningCloseD[-1] = bar.closePrice
                self.morningVolumeD[-1] += bar.volume

                self.morningBodyD[-1] = abs(self.morningOpenD[-1] - self.morningCloseD[-1])
                self.morningRangeD[-1] = self.morningHighD[-1] - self.morningLowD[-1]

                if self.morningOpenD[-1] > self.morningCloseD[-1]:
                    self.morningUpperShadowD[-1] = self.morningHighD[-1] - self.morningOpenD[-1]
                    self.morningLowerShadowD[-1] = self.morningCloseD[-1] - self.morningLowD[-1]
                else:
                    self.morningUpperShadowD[-1] = self.morningHighD[-1] - self.morningCloseD[-1]
                    self.morningLowerShadowD[-1] = self.morningOpenD[-1] - self.morningLowD[-1]


            if bar.timestamp <= self.mktAfternoonCloseTime:
                if bar.highPrice > self.afternoonHighD[-1]: self.afternoonHighD[-1] = bar.highPrice
                if bar.lowPrice < self.afternoonLowD[-1]: self.afternoonLowD[-1] = bar.lowPrice
                self.afternoonCloseD[-1] = bar.closePrice
                self.afternoonVolumeD[-1] += bar.volume

                self.afternoonBodyD[-1] = abs(self.afternoonOpenD[-1] - self.afternoonCloseD[-1])
                self.afternoonRangeD[-1] = self.afternoonHighD[-1] - self.afternoonLowD[-1]

                if self.afternoonOpenD[-1] > self.afternoonCloseD[-1]:
                    self.afternoonUpperShadowD[-1] = self.afternoonHighD[-1] - self.afternoonOpenD[-1]
                    self.afternoonLowerShadowD[-1] = self.afternoonCloseD[-1] - self.afternoonLowD[-1]
                else:
                    self.afternoonUpperShadowD[-1] = self.afternoonHighD[-1] - self.afternoonCloseD[-1]
                    self.afternoonLowerShadowD[-1] = self.afternoonOpenD[-1] - self.afternoonLowD[-1]


            if bar.resolution == self.signalResolution:
                self.bars.append(bar)

                self.timestamp.append(bar.timestamp)
                self.open.append(bar.openPrice)
                self.high.append(bar.highPrice)
                self.low.append(bar.lowPrice)
                self.close.append(bar.closePrice)
                self.volume.append(bar.volume)

            self.CalculateTA(bar)

            if self.inTradePeriod is False:
                return

            # Calculate Signal
            if self.CanCalculateExitSignal(bar):
                self.CalculateExitSignal(bar)


            if self.action is not None:
                if bar.resolution != self.signalResolution:
                    return

                if self.entryCount >= self.tradeLimit:
                    if self.session.mode == SessionMode.IB_LIVE or self.session == SessionMode.IB_DALIY_BACKTEST:
                        self.Log("sid:", self.session.config.sid, "["+str(bar.adjustedTime)+"] Reach trade limit:", self.tradeLimit)
                    return

                if self.entryHourLimitInAdjustedTime is not None:
                    if not (bar.adjustedTime > self.entryHourLimitInAdjustedTime["START"] and bar.adjustedTime < self.entryHourLimitInAdjustedTime["END"]):
                        if self.session.mode == SessionMode.IB_LIVE or self.session == SessionMode.IB_DALIY_BACKTEST:
                            self.Log("sid:", self.session.config.sid, "["+str(bar.adjustedTime)+"] Out of entry hour limit:", bar.adjustedTime, self.entryHourLimitInAdjustedTime)
                        return

                if self.session.mode == SessionMode.IB_LIVE or self.session == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("sid:", self.session.config.sid, "[" + str(bar.adjustedTime)+"]")

                self.CalculateEntrySignal(bar)

                if self.session.mode == SessionMode.IB_LIVE or self.session == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("")


    def CanCalculateExitSignal(self, bar):
        if self.config.tradeTicker not in self.session.portfolio.positions:
            return False

        if bar.resolution != self.signalResolution:
            return False

        if self.minsToExitBeforeMarketClose is not None:
            diff = utilities.mintueBetweenTwoDatetime(self.mktCloseTime, bar.timestamp, False)
            if diff <= self.minsToExitBeforeMarketClose:
                self.Exit(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, "ExitBeforeMktClose", self.baseQuantity)
                return False
        return True


    def CanCalculateExitSignalByBidAsk(self, bidAsk):
        if self.config.tradeTicker not in self.session.portfolio.positions:
            return False

        return True


    def CalculateEntrySignal(self, bar):
        count = 0
        for signal in self.entrySignals:
            if signal.CalculateSignal(bar):
                self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label()+"]: True")
                count += 1
            else:
                self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label() + "]: False")

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, signal.Label(), self.baseQuantity)


    def CalculateExitSignalByBidAsk(self, bidAsk, adjustedDate, adjustedTime):
        c = 0
        if self.session.mode == SessionMode.IB_LIVE:
            #For live sesion only use
            for signal in self.exitSignals:
                if signal.CalculateSignalByBidAsk(bidAsk):
                    self.Exit(bidAsk, adjustedDate, adjustedTime, OrderType.LIMIT, signal.Label(), self.baseQuantity)
                    return
                c += 1

    def CalculateExitSignal(self, bar):
        c = 0
        for signal in self.exitSignals:
            if signal.CalculateSignal(bar):
                self.Exit(signal.exitPrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, signal.Label(), self.baseQuantity)
                return
            c+=1

    def Entry(self, price, adjustedDate, adjustedTime, orderType, label, quantity, triggerLimit=None):
        self.entryCount += 1

        price = int(price)
        quantity = int(quantity)
        if triggerLimit is None:
            triggerLimit = int(self.config.slippage)
        else:
            triggerLimit = int(triggerLimit)

        if self.action == OrderAction.BUY:
            limitPrice = price + triggerLimit
        else:
            limitPrice = price - triggerLimit

        orderId = self.orderHandler.GetNextOrderId()
        contract = self.orderHandler.PrepareContract(self.config.tradeTicker,
                                                     self.tradeDateData["expected_expiry_month"])
        order = self.orderHandler.PrepareOrder(self.action, contract, orderId, price, limitPrice, adjustedDate, adjustedTime, orderType, label, quantity)
        order.stopLossThreshold = self.stopLoss

        self.orderHandler.PlaceOrder(orderId, contract, order, "True")
        if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
            self.Log("========== Entry:", price, adjustedDate, adjustedTime, self.entryCount, label)



    def Exit(self, price, adjustedDate, adjustedTime, orderType, label, quantity, triggerLimit=None):
        price = int(price)
        quantity = int(quantity)
        if triggerLimit is None:
            triggerLimit = self.config.slippage
        else:
            triggerLimit = int(triggerLimit)


        orderId = self.orderHandler.GetNextOrderId()
        contract = self.orderHandler.PrepareContract(self.config.tradeTicker, self.tradeDateData["expected_expiry_month"])


        if self.action == OrderAction.BUY:      #Strategy is BUY Than Exit should be SELL
            limitPrice = price - triggerLimit
            order = self.orderHandler.PrepareOrder(OrderAction.SELL, contract, orderId, price, limitPrice, adjustedDate, adjustedTime, orderType, label, quantity)
        else:
            limitPrice = price + triggerLimit
            order = self.orderHandler.PrepareOrder(OrderAction.BUY, contract, orderId, price, limitPrice, adjustedDate, adjustedTime, orderType, label, quantity)

        self.orderHandler.PlaceOrder(orderId, contract, order)
        if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
            self.Log("========== Exit:", price, orderType, label, quantity, triggerLimit)


    def UpdateContact(self):
        trade_data = self.session.dataSource.GetTickerTradeDateDataByDate(self.currentDate)
        expected_expiry_month = str(trade_data["expected_expiry_month"])
        if int(expected_expiry_month[0]) >= 8:
            year = str(1900 + int(expected_expiry_month[:2]))
        else:
            year = str(2000 + int(expected_expiry_month[:2]))

        month = str(int(expected_expiry_month[2:]))

        if self.config.tradeTicker in HKEX_FUTURE:
            self.contract = "HKFE.F." + self.config.tradeTicker + month + year
        else:
            self.Log("future_strategy.UpdateContact not develop for " + self.config.tradeTicker)


    def OnNewDay(self, bar):
        if self.rangeFilter is None:
            self.range = self.highD[-1] - self.lowD[-1]

        for ta in self.intraDayTA:
            ta.OnNewDay(bar.timestamp)

        for ta in self.interDayTA:
            ta.OnNewDay(bar.timestamp)

        for signal in self.entrySignals:
            signal.OnNewDay(bar)

        for signal in self.exitSignals:
            signal.OnNewDay(bar)

        if self.session.mode == SessionMode.IB_LIVE or self.session == SessionMode.IB_DALIY_BACKTEST:
            self.Log("OnNewDate:", bar.timestamp, self.config.startDate, self.config.endDate)

        if self.inTradePeriod is False:
            if bar.timestamp >= self.config.startDate and bar.timestamp<=self.config.endDate:
                self.inTradePeriod = True
        else:
            if bar.timestamp >= self.config.endDate:
                self.inTradePeriod = False


    def OnDayEnd(self, bar):
        for ta in self.interDayTA:
            ta.OnDayEnd()

        for ta in self.intraDayTA:
            ta.OnDayEnd()

        for signal in self.entrySignals:
            signal.OnDayEnd()

        for signal in self.exitSignals:
            signal.OnDayEnd()

    def GetAverageData(self, dataName="high", windowSize=0):
        self.windowSize = windowSize
        dataName = dataName.lower()

        if dataName == "open":
            data = self.open
        elif dataName == "high":
            data = self.high
        elif dataName == "low":
            data = self.low
        elif dataName == "close":
            data = self.close
        elif dataName == "tr":
            data = self.TR
        elif dataName == "atr":
            data = self.TR

        elif dataName == "openD":
            data = self.openD
        elif dataName == "highD":
            data = self.highD
        elif dataName == "lowD":
            data = self.lowD
        elif dataName == "closeD":
            data = self.closeD

        return cmath.Average(data, self.windowSize)


    def GetData(self, dataName="close", offset=0):
        offset = (offset * -1) - 1
        dataName = dataName.lower()

        if dataName == "open":
            return self.open[offset]
        elif dataName == "high":
            return self.high[offset]
        elif dataName == "low":
            return self.low[offset]
        elif dataName == "close":
            return self.close[offset]


        elif dataName == "openD":
            return self.openD[offset]
        elif dataName == "highD":
            return self.highD[offset]
        elif dataName == "lowD":
            return self.lowD[offset]
        elif dataName == "closeD":
            return self.closeD[offset]

        return None


    def GetTR(self):
        tr1 = self.high[-1] - self.low[-1]

        if len(self.high) == 1:
            return tr1

        tr2 = abs(self.high[-1] - self.close[-2])
        tr3 = abs(self.low[-1] - self.close[-2])

        returnVal = tr1
        if tr2 > returnVal:
            returnVal = tr2

        if tr3 > returnVal:
            returnVal = tr3

        return returnVal


    def AddIntraDayTA(self, ta):
        self.intraDayTA.append(ta)


    def AddInterDayTA(self, ta):
        self.interDayTA.append(ta)

    '''
    def CalculateInterDayTA(self):
        for ta in self.interDayTA:
            ta.UpdateData()
    '''

    def CalculateTA(self, bar):
        if self.useTR is True:
            self.TR.append(self.GetTR())

        for ta in self.interDayTA:
            ta.Calculate(bar)

        for ta in self.intraDayTA:
            ta.Calculate(bar)

        if self.rangeFilter is not None:
            self.range = self.rangeFilter[-1]


    def TAToDict(self, inputTA):
        taDict = {}
        for ta in inputTA:
            _d = ta.ToDict()
            if 'slug' in _d.keys():
                taDict[_d['slug']] = _d
            else:
                for taKey in _d:
                    taDict[taKey] = _d[taKey]

        return taDict



    def Save(self):
        import inspect, os, json
        from shutil import copyfile

        strategyClassPath = inspect.getfile(self.config.strategyClass)
        copyfile(strategyClassPath, self.config.reportDirectory + "//" + os.path.basename(strategyClassPath))
        copyfile(strategyClassPath, self.config.reportDirectory + "//strategy.txt")

        #Do inter day ta
        taDict = {}
        taList = []
        for ta in self.interDayTA:
            _d = ta.ToDict()
            _ta = {}
            _ta['ticker'] = self.config.dataTicker
            _ta['slug'] = _d['slug']
            _ta['name'] = _d['name']
            taList.append(_ta)

            jsonFolder = self.config.baseTADirectory + "interday/" + self.config.dataTicker + "/"
            utilities.createFolder(jsonFolder)

            jsonFile = jsonFolder + _d['slug'] + ".json"
            df = pd.DataFrame(
                {'date': _d['valuesTimestamp'],
                 'value': _d['values']
                 }, columns=['date', 'value'])
            df['date'] = df['date'].astype(str)
            df['value'] = df['value'].astype(float)

            self.Log("Save() jsonFile:", jsonFile)
            tryCount = 0
            lockFile = jsonFile.replace(".json", ".lock")
            isCheckLockFile = utilities.isFileExist(lockFile)

            while isCheckLockFile:
                self.Log("Lock file exist, please exit:", lockFile)
                tryCount += 1
                time.sleep(2)
                isCheckLockFile = utilities.isFileExist(lockFile)

                maxTryCount = 30
                if self.session.mode == SessionMode.IB_DALIY_BACKTEST or self.session.mode == SessionMode.IB_LIVE:
                    import random
                    time.sleep(random.randint(2,5))
                    maxTryCount = 30

                if tryCount >= maxTryCount:
                    isCheckLockFile = False
                    raise ValueError

            self.Log("Save() create lock file:", lockFile)
            with open(lockFile, 'w') as fp:
                json.dump({}, fp, indent=4)

            taDebug = False
            #taDebug = True

            if utilities.isFileExist(jsonFile):
                try:
                    previousDf = pd.read_json(jsonFile, orient='index')
                    #previousDf = pd.read_csv(csvFile, index_col="date")
                    if 'value' in previousDf.columns:
                        previousDf['date'] = previousDf.index
                        previousDf = previousDf.reset_index(drop=True)

                        previousDf['date'] = previousDf['date'].astype(str)
                        previousDf['value'] = previousDf['value'].astype(float)
                        previousDf = previousDf[['date', 'value']]

                        previousDf['value'] = previousDf['value'].round(2)
                        df['value'] = df['value'].round(2)

                    if taDebug:
                        #for debug when value not match with previous, it cannot merge
                        print(jsonFile)
                        print("previousDf")
                        print(previousDf)

                        print("df")
                        print(df)

                        forSaveDF = previousDf
                        forSaveDF.index = forSaveDF.date
                        forSaveDF.to_csv("X:\log\previousDf1.csv")
                        forSaveDF = df.drop(columns=['date'])


                        forSaveDF = df
                        forSaveDF.index = forSaveDF.date
                        forSaveDF = df.drop(columns=['date'])
                        forSaveDF.to_csv("X:\log\df.csv")

                        forSaveDF = pd.concat([previousDf, df])
                        forSaveDF['duplicated'] = forSaveDF.index.duplicated()
                        forSaveDF.to_csv("X:\log\combine.csv")

                        print(previousDf.dtypes)
                        print(df.dtypes)


                    previousDf = previousDf.dropna()
                    df = df.dropna()

                    df = pd.concat([previousDf, df]).drop_duplicates(subset=["date"])
                    if taDebug: df.to_csv("X:\log\sort_afterCombinated.csv")

                    df = df.reset_index(drop=True)
                    df = df.sort_values('date')
                except ValueError as e:
                    pass

            df.index = df.date
            df = df.drop(columns=['date'])

            if taDebug: df.to_csv("X:/log/b4Save.csv")
            df.to_json(jsonFile, orient='index')

            try:
                self.Log("Remove lock file:", lockFile)
                os.remove(lockFile)
            except:
                self.Log("Remove lock file fail:", lockFile)

        taDict = self.TAToDict(self.interDayTA)
        jsonFilename = "//interDayTA.json"


        #check TA file islock before save.

        with open(self.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(taList, fp, cls=utilities.AntJSONEncoder)

        ##########################################################################################
        ##########################################################################################

        #do intra_day_ta
        taDict = self.TAToDict(self.intraDayTA)
        intraDayTaToSave = []

        for taSlug in taDict:
            _ta = {}
            _ta['ticker'] = self.config.dataTicker
            _ta['slug'] = taDict[taSlug]['slug']
            _ta['name'] = taDict[taSlug]['name']

            if 'windowSize' in taDict[taSlug]:
                _ta['windowSize'] = taDict[taSlug]['windowSize']
            if 'offset' in taDict[taSlug]:
                _ta['offset'] = taDict[taSlug]['offset']

            _ta['resolution'] = taDict[taSlug]['resolution']
            intraDayTaToSave.append(_ta)

            for dateKey in taDict[taSlug]['valuesTimestamp']:
                folder = self.config.baseTADirectory + "intraday//" + self.config.dataTicker + "//" + taDict[taSlug]['slug'] + "_" + taDict[taSlug]['resolution']
                filename = taDict[taSlug]['slug'] + "_" + taDict[taSlug]['resolution'] + "_" + dateKey + ".json"
                utilities.createFolder(folder)
                csvPath = folder + "//" + filename

                if not utilities.isFileExist(csvPath):
                    d_to_save = {}

                    d_to_save['type'] = taDict[taSlug]['type']
                    d_to_save['name'] = taDict[taSlug]['name']
                    d_to_save['slug'] = taDict[taSlug]['slug']

                    if 'windowSize' in taDict[taSlug]:
                        d_to_save['windowSize'] = taDict[taSlug]['windowSize']
                    if 'offset' in taDict[taSlug]:
                        d_to_save['offset'] = taDict[taSlug]['offset']

                    d_to_save['resolution'] = taDict[taSlug]['resolution']
                    d_to_save['values'] = taDict[taSlug]['values'][dateKey]
                    d_to_save['valuesTimestamp'] = taDict[taSlug]['valuesTimestamp'][dateKey]

                    with open(csvPath, 'w') as fp:
                        json.dump(d_to_save, fp, cls=utilities.AntJSONEncoder)

        jsonFilename = "//intraDayTA.json"
        with open(self.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(intraDayTaToSave, fp, cls=utilities.AntJSONEncoder)
