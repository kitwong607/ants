from .. import utilities
from .base import ExitSignal
from ..order.base import OrderAction
from ..cmath import cmath


# region Stop loss exit
class StopLossWithFixedPrice(ExitSignal):
    name = "StopLossWithFixedPrice"

    def __init__(self, strategy, stopLoss):
        super().__init__(strategy)
        self.stopLoss = self.defaultStopLoss = stopLoss
        self.exitPrice = None
        self.isTrigger = False



    def Label(self):
        if getattr(self, "trailingStopCount", None) is None:
            return self.name
        else:
            return self.name + "(TS:" +str(self.trailingStopCount) + ")"

    def Reset(self):
        self.stopLoss = self.defaultStopLoss
        self.isTrigger = False
        self.exitPrice = None

    def OnNewDay(self, bar):
        self.Reset()

    def CalculateSignalByBidAsk(self, bidAsk):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bidAsk < self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                self.isTrigger = True
                return True

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice + self.stopLoss

            if bidAsk > self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                self.isTrigger = True
                return True

        return False

    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bar.lowPrice < self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                self.isTrigger = True
                return True
            return False

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice + self.stopLoss

            if bar.highPrice > self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                self.isTrigger = True
                return True

        return False
# endregion

# region FixedStopGain
class FixedStopGain(ExitSignal):
    name = "FixedStopGain"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.amount = amount
        self.exitPrice = None


    def Label(self):
        return self.name + "_" + str(self.amount)


    def OnNewDay(self, bar):
        self.isTrigger = False
        self.isTriggerBreakeven = False
        self.exitPrice = None



    def CalculateSignalByBidAsk(self, bidAsk):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice + self.amount

            if bidAsk > self.exitPrice:
                self.isTrigger = True
                return True

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bidAsk < self.exitPrice:
                self.isTrigger = True
                return True

        return False


    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]


        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice + self.amount

            if bar.closePrice > self.exitPrice:
                self.isTrigger = True
                return True

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bar.closePrice < self.exitPrice:
                self.isTrigger = True
                return True
        return False

# region DayRangeTouch
class DayRangeTouch(ExitSignal):
    name = "DayRangeTouch"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.amount = amount


    def Label(self):
        return self.name + "_" + str(self.amount)


    def OnNewDay(self, bar):
        self.isTrigger = False
        self.isTriggerBreakeven = False
        self.profitWatemark = 0


    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        if self.strategy.highD[-1] - self.strategy.lowD[-1] > self.amount:
            self.isTrigger = True
            return True

        return False

# region breakeven
class BreakevenAfterTouchThreshold(ExitSignal):
    name = "BreakevenAfterTouchThreshold"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.isTriggerBreakeven = False
        self.amount = amount


    def Label(self):
        return self.name + "_" + str(self.amount)


    def OnNewDay(self, bar):
        self.isTrigger = False
        self.isTriggerBreakeven = False
        self.profitWatemark = 0


    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]
        if self.isTriggerBreakeven == False:
            if OrderAction.BUY == position.action:
                currentWatermark = bar.highPrice - position.entryPrice
                if currentWatermark > self.amount:
                    self.isTriggerBreakeven = True

            elif OrderAction.SELL == position.action:
                currentWatermark = position.entryPrice - bar.lowPrice
                if currentWatermark > self.amount:
                    self.isTriggerBreakeven = True
        else:
            if OrderAction.BUY == position.action:
                currentWatermark = bar.lowPrice - position.entryPrice

            elif OrderAction.SELL == position.action:
                currentWatermark = position.entryPrice - bar.highPrice

            if currentWatermark < 0:
                self.isTrigger = True
                return True


        return False

# region trailing stop exit
class DollarTrailingStop(ExitSignal):
    name = "DollarTrailingStop"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.amount = amount
        self.profitWatemark = 0
        self.exitPrice = None
        self.isTrigger = False


    def Label(self):
        return self.name + "_" + str(self.amount)


    def Reset(self):
        self.profitWatemark = 0
        self.exitPrice = None
        self.isTrigger = False


    def OnNewDay(self, bar):
        self.Reset()


    def CalculateSignalByBidAsk(self, bidAsk):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if getattr(position, "trailingStopCount", None) is None:
            position.trailingStopCount = 0

        if OrderAction.BUY == position.action:
            currentWatermark = bidAsk - position.entryPrice
            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice + self.profitWatemark - self.amount
            if bidAsk < self.exitPrice:
                self.isTrigger = True
                return True

        elif OrderAction.SELL == position.action:
            currentWatermark = position.entryPrice - bidAsk

            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice - self.profitWatemark + self.amount
            if bidAsk > self.exitPrice:
                self.isTrigger = True
                return True

        return False


    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if getattr(position, "trailingStopCount", None) is None:
            position.trailingStopCount = 0

        if OrderAction.BUY == position.action:
            currentWatermark = bar.highPrice - position.entryPrice
            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice + self.profitWatemark - self.amount
            if bar.lowPrice < self.exitPrice:
                self.isTrigger = True
                return True

        elif OrderAction.SELL == position.action:
            currentWatermark = position.entryPrice - bar.lowPrice

            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice - self.profitWatemark + self.amount
            if bar.highPrice > self.exitPrice:
                self.isTrigger = True
                return True

        return False


#This Class will update all ExitSignal when it hit stepup amount
class TrailingStopWithFixedPrice(ExitSignal):
    name = "TrailingStopWithFixedPrice"

    def __init__(self, strategy, stepUpThreshold, stepUpAmount):
        super().__init__(strategy)
        self.stepUpThreshold = stepUpThreshold
        self.stepUpAmount = stepUpAmount
        self.count = 0
        self.exitPrice = None
        self.isTrigger = False

    def Label(self):
        return self.name


    def Reset(self):
        self.count = 0
        self.exitPrice = None
        for signal in self.strategy.exitSignals:
            if signal is not self:
                if getattr(signal, "stopLoss", None) is not None:
                    signal.trailingStopCount = 0


    def OnNewDay(self, bar):
        self.Reset()


    def CalculateSignalByBidAsk(self, bidAsk):
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if getattr(position, "trailingStopCount", None) is None:
            position.trailingStopCount = 0

        if OrderAction.BUY == position.action:

            if bidAsk > position.entryPrice + (self.stepUpAmount * (position.trailingStopCount + 1)):
                position.trailingStopCount += 1
                for signal in self.strategy.exitSignals:
                    if signal is not self:
                        if getattr(signal, "stopLoss", None) is not None:
                            signal.stopLoss -= self.stepUpAmount
                            self.count = signal.trailingStopCount = position.trailingStopCount


        elif OrderAction.SELL == position.action:
            if bidAsk < position.entryPrice - (self.stepUpThreshold * (position.trailingStopCount + 1)):
                position.trailingStopCount += 1
                for signal in self.strategy.exitSignals:
                    if signal is not self:
                        if getattr(signal, "stopLoss", None) is not None:
                            signal.stopLoss -= self.stepUpAmount
                            self.count = signal.trailingStopCount = position.trailingStopCount

        return False


    def CalculateSignal(self, bar):
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if getattr(position, "trailingStopCount", None) is None:
            position.trailingStopCount = 0

        if OrderAction.BUY == position.action:

            if bar.highPrice > position.entryPrice + (self.stepUpAmount * (position.trailingStopCount + 1)):
                position.trailingStopCount += 1
                for signal in self.strategy.exitSignals:
                    if signal is not self:
                        if getattr(signal, "stopLoss", None) is not None:
                            signal.stopLoss -= self.stepUpAmount
                            self.count = signal.trailingStopCount = position.trailingStopCount


        elif OrderAction.SELL == position.action:
            if bar.lowPrice < position.entryPrice - (self.stepUpThreshold * (position.trailingStopCount + 1)):
                position.trailingStopCount += 1
                for signal in self.strategy.exitSignals:
                    if signal is not self:
                        if getattr(signal, "stopLoss", None) is not None:
                            signal.stopLoss -= self.stepUpAmount
                            self.count = signal.trailingStopCount = position.trailingStopCount

        return False


class TrailingStopCountExit(ExitSignal):
    name = "TrailingStopCount"

    def __init__(self, strategy, stepUpThreshold, stepUpAmount, countToExit=1):
        super().__init__(strategy)
        self.stepUpThreshold = stepUpThreshold
        self.stepUpAmount = stepUpAmount
        self.countToExit = countToExit
        self.count = 0
        self.exitPrice = None
        self.isTrigger = False


    def Label(self):
        return self.name + "("+str(self.count)+")"


    def Reset(self):
        self.count = 0
        self.isTrigger = False
        self.isTrigger = False
        self.exitPrice = None


    def OnNewDay(self, bar):
        self.Reset()


    def CalculateSignalByBidAsk(self, bidAsk):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False
        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = threshold = position.entryPrice + (self.stepUpAmount * self.count) + self.stepUpThreshold
            if bidAsk > threshold:
                self.count += 1

        elif OrderAction.SELL == position.action:
            self.exitPrice = threshold = position.entryPrice - (self.stepUpAmount * self.count) - self.stepUpThreshold

            if bidAsk < threshold:
                self.count += 1

        if self.count == self.countToExit:
            return True

        return False


    def CalculateSignal(self, bar):
        if self.isTrigger:
            return False

        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = threshold = position.entryPrice + (self.stepUpAmount * self.count) + self.stepUpThreshold
            if bar.highPrice > threshold:
                self.count += 1

        elif OrderAction.SELL == position.action:
            self.exitPrice = threshold = position.entryPrice - (self.stepUpAmount * self.count) - self.stepUpThreshold

            if bar.lowPrice < threshold:
                self.count += 1

        if self.count == self.countToExit:
            self.isTrigger = True
            return True

        return False


# endregion