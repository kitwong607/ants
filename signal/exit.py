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

    def Label(self):
        if getattr(self, "trailingStopCount", None) is None:
            return self.name
        else:
            return self.name + "(TS:" +str(self.trailingStopCount) + ")"

    def Reset(self):
        self.stopLoss = self.defaultStopLoss
        self.isTrigger = False

    def OnNewDay(self, bar):
        self.Reset()

    def CalculateSignal(self, bar):
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            if bar.lowPrice < position.entryPrice - self.stopLoss:
                self.stopLoss = self.defaultStopLoss
                return True
            return False
        elif OrderAction.SELL == position.action:
            if bar.lowPrice > position.entryPrice + self.stopLoss:
                self.stopLoss = self.defaultStopLoss
                return True
            return False

        return False
# endregion



# region trailing stop exit
class DollarTrailingStop(ExitSignal):
    name = "DollarTrailingStop"

    def __init__(self, strategy, amount):
        super().__init__(strategy)
        self.amount = amount
        self.profitWatemark = 0


    def Label(self):
        return self.name


    def OnNewDay(self, bar):
        self.profitWatemark = 0


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

            if self.profitWatemark - self.amount > currentWatermark:
                return True

        elif OrderAction.SELL == position.action:
            currentWatermark = position.entryPrice - bar.lowPrice

            if currentWatermark > self.profitWatemark:
                if currentWatermark > 0:
                    self.profitWatemark = currentWatermark

            if self.profitWatemark - self.amount > currentWatermark:
                return True

        return False


class TrailingStopWithFixedPrice(ExitSignal):
    name = "TrailingStopWithFixedPrice"

    def __init__(self, strategy, stepUpThreshold, stepUpAmount):
        super().__init__(strategy)
        self.stepUpThreshold = stepUpThreshold
        self.stepUpAmount = stepUpAmount
        self.count = 0

    def Label(self):
        return self.name


    def OnNewDay(self, bar):
        self.count = 0
        for signal in self.strategy.exitSignals:
            if signal is not self:
                if getattr(signal, "stopLoss", None) is not None:
                    signal.trailingStopCount = 0


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

    def __init__(self, strategy, stepUpThreshold, stepUpAmount, countToExit):
        super().__init__(strategy)
        self.stepUpThreshold = stepUpThreshold
        self.stepUpAmount = stepUpAmount
        self.countToExit = countToExit
        self.count = 0

    def Label(self):
        return self.name + "("+str(self.count)+")"

    def OnNewDay(self, bar):
        self.count = 0

    def CalculateSignal(self, bar):
        if self.strategy.config.tradeTicker not in self.strategy.session.portfolio.positions:
            return False

        position = self.strategy.session.portfolio.positions[self.strategy.config.tradeTicker]

        if OrderAction.BUY == position.action:
            if bar.highPrice > position.entryPrice + (self.stepUpAmount * (self.count + 1)):
                self.count += 1


        elif OrderAction.SELL == position.action:
            if bar.lowPrice < position.entryPrice - (self.stepUpThreshold * (self.count + 1)):
                self.count += 1

        if self.count == self.countToExit:
            return True

        return False


# endregion



# region Higher X Lower X comparsion
#Class: HigherX
class HigherX(ExitSignal):
    name = "Higher{X}"

    def __init__(self, strategy, x="open", xWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize

        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if len(self.xMax) <= self.xWindowSize:
            return False

        val1 = self.xMax[-1]
        val2 = self.xMax[-self.xWindowSize - 1]

        if val1 > val2:
            return True
        return False


#Class: HigherX
class LowerX(ExitSignal):
    name = "Lower{X}"

    def __init__(self, strategy, x="open", xWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize

        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if len(self.xMin) <= self.xWindowSize:
            return False

        val1 = self.xMin[-1]
        val2 = self.xMin[-self.xWindowSize - 1]
        if val1 < val2:
            return True
        return False
# endregion

# region Pivot Point related
#Class: XHigherPivotPoint
class XHigherPivotPoint(ExitSignal):
    name = "{X}HigherPivotPoint{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPoint
        self.yPivotPoint = self.AddTA(PivotPoint, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPoint
class XLowerPivotPoint(ExitSignal):
    name = "{X}LowerPivotPoint{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPoint
        self.yPivotPoint = self.AddTA(PivotPoint, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointS1
class XHigherPivotPointS1(ExitSignal):
    name = "{X}HigherPivotPointS1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS1
        self.yPivotPoint = self.AddTA(PivotPointS1, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointS1
class XLowerPivotPointS1(ExitSignal):
    name = "{X}LowerPivotPointS1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS1
        self.yPivotPoint = self.AddTA(PivotPointS1, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointR1
class XHigherPivotPointR1(ExitSignal):
    name = "{X}HigherPivotPointR1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR1
        self.yPivotPoint = self.AddTA(PivotPointR1, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointR1
class XLowerPivotPointR1(ExitSignal):
    name = "{X}LowerPivotPointR1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR1
        self.yPivotPoint = self.AddTA(PivotPointR1, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointS2
class XHigherPivotPointS2(ExitSignal):
    name = "{X}HigherPivotPointS2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS2
        self.yPivotPoint = self.AddTA(PivotPointS2, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointS2
class XLowerPivotPointS2(ExitSignal):
    name = "{X}LowerPivotPointS2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS2
        self.yPivotPoint = self.AddTA(PivotPointS2, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointR2
class XHigherPivotPointR2(ExitSignal):
    name = "{X}HigherPivotPointR2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR2
        self.yPivotPoint = self.AddTA(PivotPointR2, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointR2
class XLowerPivotPointR2(ExitSignal):
    name = "{X}LowerPivotPointR2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR2
        self.yPivotPoint = self.AddTA(PivotPointR2, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointS3
class XHigherPivotPointS3(ExitSignal):
    name = "{X}HigherPivotPointS3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS3
        self.yPivotPoint = self.AddTA(PivotPointS3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointS3
class XLowerPivotPointS3(ExitSignal):
    name = "{X}LowerPivotPointS3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointS3
        self.yPivotPoint = self.AddTA(PivotPointS3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: XHigherPivotPointR3
class XHigherPivotPointR3(ExitSignal):
    name = "{X}HigherPivotPointR3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR3
        self.yPivotPoint = self.AddTA(PivotPointR3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[-1]:
            return True
        return False

#Class: XLowerPivotPointR3
class XLowerPivotPointR3(ExitSignal):
    name = "{X}LowerPivotPointR3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset

        from..ta.Anchor import PivotPointR3
        self.yPivotPoint = self.AddTA(PivotPointR3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[-1]:
            return True
        return False

#Class: CrossUpPivotPoint
class CrossUpPivotPoint(ExitSignal):
    name = "CrossUpPivotPoint{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPoint
        self.xPivotPoint = self.AddTA(PivotPoint, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPoint.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPoint[-1]:
            if self.strategy.close[-2] < self.xPivotPoint[-1]:
                return True
        return False

#Class: CrossDownPivotPoint
class CrossDownPivotPoint(ExitSignal):
    name = "CrossDownPivotPoint{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPoint
        self.xPivotPoint = self.AddTA(PivotPoint, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPoint.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPoint[-1]:
            if self.strategy.close[-2] > self.xPivotPoint[-1]:
                return True
        return False

#Class: CrossUpPivotPointR1
class CrossUpPivotPointR1(ExitSignal):
    name = "CrossUpPivotPointR1{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR1
        self.xPivotPointR1 = self.AddTA(PivotPointR1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR1.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointR1[-1]:
            if self.strategy.close[-2] < self.xPivotPointR1[-1]:
                return True
        return False

#Class: CrossDownPivotPointR1
class CrossDownPivotPointR1(ExitSignal):
    name = "CrossDownPivotPointR1{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR1
        self.xPivotPointR1 = self.AddTA(PivotPointR1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR1.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointR1[-1]:
            if self.strategy.close[-2] > self.xPivotPointR1[-1]:
                return True
        return False

#Class: CrossUpPivotPointS1
class CrossUpPivotPointS1(ExitSignal):
    name = "CrossUpPivotPointS1{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS1
        self.xPivotPointS1 = self.AddTA(PivotPointS1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS1.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointS1[-1]:
            if self.strategy.close[-2] < self.xPivotPointS1[-1]:
                return True
        return False

#Class: CrossDownPivotPointS1
class CrossDownPivotPointS1(ExitSignal):
    name = "CrossDownPivotPointS1{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS1
        self.xPivotPointS1 = self.AddTA(PivotPointS1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS1.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointS1[-1]:
            if self.strategy.close[-2] > self.xPivotPointS1[-1]:
                return True
        return False

#Class: CrossUpPivotPointR2
class CrossUpPivotPointR2(ExitSignal):
    name = "CrossUpPivotPointR2{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR2
        self.xPivotPointR2 = self.AddTA(PivotPointR2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR2.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointR2[-1]:
            if self.strategy.close[-2] < self.xPivotPointR2[-1]:
                return True
        return False

#Class: CrossDownPivotPointR2
class CrossDownPivotPointR2(ExitSignal):
    name = "CrossDownPivotPointR2{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR2
        self.xPivotPointR2 = self.AddTA(PivotPointR2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR2.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointR2[-1]:
            if self.strategy.close[-2] > self.xPivotPointR2[-1]:
                return True
        return False

#Class: CrossUpPivotPointS2
class CrossUpPivotPointS2(ExitSignal):
    name = "CrossUpPivotPointS2{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS2
        self.xPivotPointS2 = self.AddTA(PivotPointS2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS2.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointS2[-1]:
            if self.strategy.close[-2] < self.xPivotPointS2[-1]:
                return True
        return False

#Class: CrossDownPivotPointS2
class CrossDownPivotPointS2(ExitSignal):
    name = "CrossDownPivotPointS2{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS2
        self.xPivotPointS2 = self.AddTA(PivotPointS2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS2.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointS2[-1]:
            if self.strategy.close[-2] > self.xPivotPointS2[-1]:
                return True
        return False

#Class: CrossUpPivotPointR3
class CrossUpPivotPointR3(ExitSignal):
    name = "CrossUpPivotPointR3{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR3
        self.xPivotPointR3 = self.AddTA(PivotPointR3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR3.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointR3[-1]:
            if self.strategy.close[-2] < self.xPivotPointR3[-1]:
                return True
        return False

#Class: CrossDownPivotPointR3
class CrossDownPivotPointR3(ExitSignal):
    name = "CrossDownPivotPointR3{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointR3
        self.xPivotPointR3 = self.AddTA(PivotPointR3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR3.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointR3[-1]:
            if self.strategy.close[-2] > self.xPivotPointR3[-1]:
                return True
        return False

#Class: CrossUpPivotPointS3
class CrossUpPivotPointS3(ExitSignal):
    name = "CrossUpPivotPointS3{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS3
        self.xPivotPointS3 = self.AddTA(PivotPointS3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS3.isReady:
            return False

        if self.strategy.close[-1] > self.xPivotPointS3[-1]:
            if self.strategy.close[-2] < self.xPivotPointS3[-1]:
                return True
        return False

#Class: CrossDownPivotPointS3
class CrossDownPivotPointS3(ExitSignal):
    name = "CrossDownPivotPointS3{X}"

    def __init__(self, strategy, xOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset

        from..ta.Anchor import PivotPointS3
        self.xPivotPointS3 = self.AddTA(PivotPointS3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS3.isReady:
            return False

        if self.strategy.close[-1] < self.xPivotPointS3[-1]:
            if self.strategy.close[-2] > self.xPivotPointS3[-1]:
                return True
        return False
# endregion

# region RSI related
#Class: MaxRSIHigherThreshold
class MaxRSIHigherThreshold(ExitSignal):
    name = "Max{X}RSI{Y}HigherThreshold{Z}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", "(" + str(self.maxWindowSize) + ")").replace("{Y}", "(" + str(self.rsiWindowSize) + ")").replace("{Z}", "(" + str(self.threshold) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        val = cmath.MaxOfRange(self.rsi, -self.maxWindowSize, len(self.rsi))
        if val > self.threshold:
            return True
        return False

#Class: MinRSIHigherThreshold
class MinRSIHigherThreshold(ExitSignal):
    name = "Min{X}RSI{Y}HigherThreshold{Z}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", "(" + str(self.maxWindowSize) + ")").replace("{Y}", "(" + str(self.rsiWindowSize) + ")").replace("{Z}", "(" + str(self.threshold) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        val = cmath.MinOfRange(self.rsi, -self.maxWindowSize, len(self.rsi))
        if val > self.threshold:
            return True
        return False





#Class: MaxRSILowerThreshold
class MaxRSILowerThreshold(ExitSignal):
    name = "Max{X}RSI{Y}LowerThreshold{Z}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", "(" + str(self.maxWindowSize) + ")").replace("{Y}", "(" + str(self.rsiWindowSize) + ")").replace("{Z}", "(" + str(self.threshold) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        val = cmath.MaxOfRange(self.rsi, -self.maxWindowSize, len(self.rsi))
        if val < self.threshold:
            return True
        return False




#Class: MinRSIHigherThreshold
class MinRSILowerThreshold(ExitSignal):
    name = "Min{X}RSI{Y}LowerThreshold{Z}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", "(" + str(self.maxWindowSize) + ")").replace("{Y}", "(" + str(self.rsiWindowSize) + ")").replace("{Z}", "(" + str(self.threshold) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        val = cmath.MinOfRange(self.rsi, -self.maxWindowSize, len(self.rsi))
        if val < self.threshold:
            return True
        return False


# endregion

#=======================================================================
#=======================================================================
#Type1 entry signal list
#=======================================================================
#=======================================================================
#Class: XHigherY
class XHigherY(ExitSignal):
    name = "{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: XHigherMinY
class XHigherMinY(ExitSignal):
    name = "{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: XHigherMaxPreviousY
class XHigherMaxPreviousY(ExitSignal):
    name = "{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: XHigherMinPreviousY
class XHigherMinPreviousY(ExitSignal):
    name = "{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: XHigherMaxY
class XHigherMaxY(ExitSignal):
    name = "{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: XHigherAverageY
class XHigherAverageY(ExitSignal):
    name = "{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xOffsetTA[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerY
class XLowerY(ExitSignal):
    name = "{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerMinY
class XLowerMinY(ExitSignal):
    name = "{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerMaxPreviousY
class XLowerMaxPreviousY(ExitSignal):
    name = "{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerMinPreviousY
class XLowerMinPreviousY(ExitSignal):
    name = "{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerMaxY
class XLowerMaxY(ExitSignal):
    name = "{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: XLowerAverageY
class XLowerAverageY(ExitSignal):
    name = "{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize

        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xOffsetTA[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherY
class MinXHigherY(ExitSignal):
    name = "Min{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Min"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMin[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMinY
class MinXHigherMinY(ExitSignal):
    name = "Min{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMin[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMaxPreviousY
class MinXHigherMaxPreviousY(ExitSignal):
    name = "Min{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMin[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMinPreviousY
class MinXHigherMinPreviousY(ExitSignal):
    name = "Min{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMin[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMaxY
class MinXHigherMaxY(ExitSignal):
    name = "Min{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMin[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MinXHigherAverageY
class MinXHigherAverageY(ExitSignal):
    name = "Min{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMin[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerY
class MinXLowerY(ExitSignal):
    name = "Min{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Min"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMin[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMinY
class MinXLowerMinY(ExitSignal):
    name = "Min{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMin[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMaxPreviousY
class MinXLowerMaxPreviousY(ExitSignal):
    name = "Min{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMin[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMinPreviousY
class MinXLowerMinPreviousY(ExitSignal):
    name = "Min{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMin[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMaxY
class MinXLowerMaxY(ExitSignal):
    name = "Min{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMin[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MinXLowerAverageY
class MinXLowerAverageY(ExitSignal):
    name = "Min{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMin[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherY
class MaxPreviousXHigherY(ExitSignal):
    name = "MaxPrevious{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMaxPrevious[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMinY
class MaxPreviousXHigherMinY(ExitSignal):
    name = "MaxPrevious{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMaxPrevious[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMaxPreviousY
class MaxPreviousXHigherMaxPreviousY(ExitSignal):
    name = "MaxPrevious{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMaxPrevious[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMinPreviousY
class MaxPreviousXHigherMinPreviousY(ExitSignal):
    name = "MaxPrevious{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMaxPrevious[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMaxY
class MaxPreviousXHigherMaxY(ExitSignal):
    name = "MaxPrevious{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMaxPrevious[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherAverageY
class MaxPreviousXHigherAverageY(ExitSignal):
    name = "MaxPrevious{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMaxPrevious[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerY
class MaxPreviousXLowerY(ExitSignal):
    name = "MaxPrevious{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMaxPrevious[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMinY
class MaxPreviousXLowerMinY(ExitSignal):
    name = "MaxPrevious{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMaxPrevious[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMaxPreviousY
class MaxPreviousXLowerMaxPreviousY(ExitSignal):
    name = "MaxPrevious{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMaxPrevious[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMinPreviousY
class MaxPreviousXLowerMinPreviousY(ExitSignal):
    name = "MaxPrevious{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMaxPrevious[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMaxY
class MaxPreviousXLowerMaxY(ExitSignal):
    name = "MaxPrevious{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMaxPrevious[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerAverageY
class MaxPreviousXLowerAverageY(ExitSignal):
    name = "MaxPrevious{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMaxPrevious[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherY
class MinPreviousXHigherY(ExitSignal):
    name = "MinPrevious{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMinPrevious[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMinY
class MinPreviousXHigherMinY(ExitSignal):
    name = "MinPrevious{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMinPrevious[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMaxPreviousY
class MinPreviousXHigherMaxPreviousY(ExitSignal):
    name = "MinPrevious{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMinPrevious[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMinPreviousY
class MinPreviousXHigherMinPreviousY(ExitSignal):
    name = "MinPrevious{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMinPrevious[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMaxY
class MinPreviousXHigherMaxY(ExitSignal):
    name = "MinPrevious{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMinPrevious[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherAverageY
class MinPreviousXHigherAverageY(ExitSignal):
    name = "MinPrevious{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMinPrevious[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerY
class MinPreviousXLowerY(ExitSignal):
    name = "MinPrevious{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMinPrevious[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMinY
class MinPreviousXLowerMinY(ExitSignal):
    name = "MinPrevious{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMinPrevious[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMaxPreviousY
class MinPreviousXLowerMaxPreviousY(ExitSignal):
    name = "MinPrevious{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMinPrevious[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMinPreviousY
class MinPreviousXLowerMinPreviousY(ExitSignal):
    name = "MinPrevious{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMinPrevious[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMaxY
class MinPreviousXLowerMaxY(ExitSignal):
    name = "MinPrevious{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMinPrevious[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerAverageY
class MinPreviousXLowerAverageY(ExitSignal):
    name = "MinPrevious{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMinPrevious[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherY
class MaxXHigherY(ExitSignal):
    name = "Max{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Max"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMax[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMinY
class MaxXHigherMinY(ExitSignal):
    name = "Max{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMax[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMaxPreviousY
class MaxXHigherMaxPreviousY(ExitSignal):
    name = "Max{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMax[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMinPreviousY
class MaxXHigherMinPreviousY(ExitSignal):
    name = "Max{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMax[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMaxY
class MaxXHigherMaxY(ExitSignal):
    name = "Max{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMax[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherAverageY
class MaxXHigherAverageY(ExitSignal):
    name = "Max{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMax[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerY
class MaxXLowerY(ExitSignal):
    name = "Max{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Max"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMax[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMinY
class MaxXLowerMinY(ExitSignal):
    name = "Max{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMax[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMaxPreviousY
class MaxXLowerMaxPreviousY(ExitSignal):
    name = "Max{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMax[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMinPreviousY
class MaxXLowerMinPreviousY(ExitSignal):
    name = "Max{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMax[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMaxY
class MaxXLowerMaxY(ExitSignal):
    name = "Max{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMax[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerAverageY
class MaxXLowerAverageY(ExitSignal):
    name = "Max{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMax[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherY
class AverageXHigherY(ExitSignal):
    name = "Average{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Average"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[-1] > self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMinY
class AverageXHigherMinY(ExitSignal):
    name = "Average{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xSMA[-1] > self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMaxPreviousY
class AverageXHigherMaxPreviousY(ExitSignal):
    name = "Average{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xSMA[-1] > self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMinPreviousY
class AverageXHigherMinPreviousY(ExitSignal):
    name = "Average{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xSMA[-1] > self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMaxY
class AverageXHigherMaxY(ExitSignal):
    name = "Average{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xSMA[-1] > self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherAverageY
class AverageXHigherAverageY(ExitSignal):
    name = "Average{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xSMA[-1] > self.ySMA[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerY
class AverageXLowerY(ExitSignal):
    name = "Average{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Average"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[-1] < self.yOffsetTA[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMinY
class AverageXLowerMinY(ExitSignal):
    name = "Average{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xSMA[-1] < self.yMin[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMaxPreviousY
class AverageXLowerMaxPreviousY(ExitSignal):
    name = "Average{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xSMA[-1] < self.yMaxPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMinPreviousY
class AverageXLowerMinPreviousY(ExitSignal):
    name = "Average{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xSMA[-1] < self.yMinPrevious[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMaxY
class AverageXLowerMaxY(ExitSignal):
    name = "Average{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xSMA[-1] < self.yMax[-1]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerAverageY
class AverageXLowerAverageY(ExitSignal):
    name = "Average{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xSMA[-1] < self.ySMA[-1]:
            return True

        return False

#=======================================================================
#=======================================================================
#=======================================================================