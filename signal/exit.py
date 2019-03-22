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
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bidAsk < self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                return True

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice + self.stopLoss

            if bidAsk > self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                return True

        return False

    def CalculateSignal(self, bar):
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            self.exitPrice = position.entryPrice - self.stopLoss

            if bar.lowPrice < self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                return True
            return False

        elif OrderAction.SELL == position.action:
            self.exitPrice = position.entryPrice + self.stopLoss

            if bar.highPrice > self.exitPrice:
                self.stopLoss = self.defaultStopLoss
                return True

        return False
# endregion


# region trailing stop exit
class DollarTrailingStop(ExitSignal):
    name = "DollarTrailingStop"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.amount = amount
        self.profitWatemark = 0
        self.exitPrice = None


    def Label(self):
        return self.name


    def Reset(self):
        self.profitWatemark = 0
        self.exitPrice = None


    def OnNewDay(self, bar):
        self.Reset()


    def CalculateSignalByBidAsk(self, bidAsk):
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
                return True

        elif OrderAction.SELL == position.action:
            currentWatermark = position.entryPrice - bidAsk

            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice - self.profitWatemark + self.amount
            if bidAsk > self.exitPrice:
                return True

        return False


    def CalculateSignal(self, bar):
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
                return True

        elif OrderAction.SELL == position.action:
            currentWatermark = position.entryPrice - bar.lowPrice

            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            self.exitPrice = position.entryPrice - self.profitWatemark + self.amount
            if bar.highPrice > self.exitPrice:
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


        pass


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


    def Label(self):
        return self.name + "("+str(self.count)+")"


    def Reset(self):
        self.count = 0
        self.exitPrice = None


    def OnNewDay(self, bar):
        self.Reset()


    def CalculateSignalByBidAsk(self, bidAsk):
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
            return True

        return False


# endregion