from .. import utilities
from .base import EntrySignal
from ..order.base import OrderAction
from ..cmath import cmath



# region Time related
class FirstBarAfter(EntrySignal):
    name = "FirstBarAfter"

    def __init__(self, strategy, hour, minute, second):
        super().__init__(strategy)

        self.hour = hour
        self.minute = minute
        self.second = second

        self.time = hour * 10000 + minute * 100 + second


    def OnNewDay(self, bar):
        self.isTrigger = False


    def CalculateSignal(self, bar):
        if self.isTrigger is False:
            t = utilities.getTimeStrFromDt(bar.timestamp)
            if int(t) > int(self.time):
                self.isTrigger = True
                return True
        return False
# endregion


# region Range related
class HighLowRangeChecker(EntrySignal):
    name = "RangeChecker"

    def __init__(self, strategy, rangeThreshold):
        super().__init__(strategy, numOfDay=-1)
        self.numOfDay = numOfDay
        self.rangeThreshold = rangeThreshold


    def CalculateSignal(self, bar):
        if self.strategy.highD[self.numOfDay] - self.strategy.lowD[self.numOfDay] >= self.rangeThreshold:
            return True
        return False
# endregion


# region TA Breakout
class SimpleSMACross(EntrySignal):
    name = "SimpleSMACross"

    def __init__(self, strategy, fastWindowSize, slowWindowSize, resolution):
        from ..ta.SMA import SMA
        super().__init__(strategy)
        self.slowWindowSize = slowWindowSize
        self.fastWindowSize = fastWindowSize
        self.resolution = resolution

        self.fastSMA = SMA(self.strategy.session, fastWindowSize, resolution)
        self.slowSMA = SMA(self.strategy.session, slowWindowSize, resolution)



    def OnNewDay(self, bar):
        self.isTrigger = False


    def CalculateSignal(self, bar):
        if self.isTrigger is False:
            if self.strategy.action == OrderAction.BUY:
                if len(self.slowSMA) !=0:
                    if self.fastSMA[-1][0] > self.slowSMA[-1][0] and self.fastSMA[-2][0] < self.slowSMA[-2][0]:
                        self.isTrigger = True
                        return True
            elif self.strategy.action == OrderAction.Sell:
                if len(self.slowSMA) !=0:
                    if self.fastSMA[-1][0] < self.slowSMA[-1][0] and self.fastSMA[-2][0] > self.slowSMA[-2][0]:
                        self.isTrigger = True
                        return True
        return False

# endregion


# region Day bar related
class XHigherY(EntrySignal):
    name = "{X}Higher{Y}"
    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel+"("+str(self.xOffset)+")").replace("{Y}", self.yLabel+"("+str(self.yOffset)+")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] >= self.yOffsetTA[-1]:
            return True
        return False


class XLowerY(EntrySignal):
    name = "{X}Lower{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0, ):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel+"("+str(self.xOffset)+")").replace("{Y}", self.yLabel+"("+str(self.yOffset)+")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] <= self.yOffsetTA[-1]:
            return True
        return False


class XHigherYWithRange(EntrySignal):
    name = "{X}Higher{Y}WithRange{RANGE}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0, rangeRatio=1.0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.rangeRatio = rangeRatio

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}",
                  self.yLabel + "(" + str(self.yOffset) + ")").replace("{RANGE}", "(" + str(self.rangeRatio) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] >= self.yOffsetTA[-1] + (self.strategy.range[0] * self.rangeRatio):
            return True
        return False


class XHigherYWithoutRange(EntrySignal):
    name = "{X}Higher{Y}WithRange{RANGE}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0, rangeRatio=1.0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.rangeRatio = rangeRatio

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}",
                  self.yLabel + "(" + str(self.yOffset) + ")").replace("{RANGE}", "(" + str(self.rangeRatio) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] >= self.yOffsetTA[-1] - (self.strategy.range[0] * self.rangeRatio):
            return True
        return False


class XLowerYWithRange(EntrySignal):
    name = "{X}Lower{Y}WithRange{RANGE}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0, rangeRatio=1.0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.rangeRatio = rangeRatio

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}",
                  self.yLabel + "(" + str(self.yOffset) + ")").replace("{RANGE}", "(" + str(self.rangeRatio) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] <= self.yOffsetTA[-1] + (self.strategy.range[0] * self.rangeRatio):
            return True
        return False


class XLowerYWithoutRange(EntrySignal):
    name = "{X}Lower{Y}WithoutRange{RANGE}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yOffset=0, rangeRatio=1.0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.rangeRatio = rangeRatio

        from ..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}",
                  self.yLabel + "(" + str(self.yOffset) + ")").replace("{RANGE}", "(" + str(self.rangeRatio) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[-1] <= self.yOffsetTA[-1] - (self.strategy.range[0] * self.rangeRatio):
            return True
        return False


class XHigherMaxY(EntrySignal):
    name = "{X}HigherMax{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yMax = self.AddTA(MaxX, {"dataName":y, "windowSize": yWindowSize})



    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMax[-1]:
            return True
        return False


class XLowerMaxY(EntrySignal):
    name = "{X}LowerMax{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yMax = self.AddTA(MaxX, {"dataName":y, "windowSize": yWindowSize})

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMax[-1]:
            return True
        return False


class XHigherMinY(EntrySignal):
    name = "{X}HigherMin{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize


        from ..ta.base import OffsetTA
        from ..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yMin = self.AddTA(MinX, {"dataName":y, "windowSize": yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[-1] > self.yMin[-1]:
            return True
        return False


class XLowerMinY(EntrySignal):
    name = "{X}LowerMin{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yMin = self.AddTA(MinX, {"dataName":y, "windowSize": yWindowSize})



    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[-1] < self.yMin[-1]:
            return True
        return False


class XHigherMaxYZ(EntrySignal):
    name = "{X}HigherMax{Y}{Z}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0, z="highD", zWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize
        self.zWindowSize = zWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MaxXY
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yzMax = self.AddTA(MaxXY, {"xDataName":y, "xWindowSize": yWindowSize, "yDataName":z, "yWindowSize": zWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yzMax.isReady:
            return False

        if  self.xOffsetTA[-1] >= self.yzMax[-1]:
            return True
        return False


class XLowerMaxYZ(EntrySignal):
    name = "{X}LowerMax{Y}{Z}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0, z="highD", zWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize
        self.zWindowSize = zWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MaxXY
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yzMax = self.AddTA(MaxXY, {"xDataName":y, "xWindowSize": yWindowSize, "yDataName":z, "yWindowSize": zWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yzMax.isReady:
            return False


        if  self.xOffsetTA[-1] <= self.yzMax[-1]:
            return True
        return False


class XHigherMinYZ(EntrySignal):
    name = "{X}HigherMin{Y}{Z}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0, z="highD", zWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize
        self.zWindowSize = zWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MinXY
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yzMin = self.AddTA(MinXY, {"xDataName":y, "xWindowSize": yWindowSize, "yDataName":z, "yWindowSize": zWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yzMin.isReady:
            return False

        if  self.xOffsetTA[-1] >= self.yzMin[-1]:
            return True
        return False


class XLowerMinYZ(EntrySignal):
    name = "{X}LowerMin{Y}{Z}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0, z="highD", zWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize
        self.zWindowSize = zWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.base import OffsetTA
        from ..ta.MinMax import MinXY
        self.xOffsetTA = self.AddTA(OffsetTA, {"dataName":x, "offset": xOffset})
        self.yzMin = self.AddTA(MinXY, {"xDataName":y, "xWindowSize": yWindowSize, "yDataName":z, "yWindowSize": zWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yzMin.isReady:
            return False

        if  self.xOffsetTA[-1] <= self.yzMin[-1]:
            return True
        return False

class AverageXHigherY(EntrySignal):
    name = "Average{X}Higher{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from ..ta.SMA import SMA
        from ..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {"dataName":x, "windowSize": xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[-1] > self.yOffsetTA[-1]:
            return True
        return False


class AverageXLowerY(EntrySignal):
    name = "Average{X}Lower{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset

        from ..ta.SMA import SMA
        from ..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {"dataName":x, "windowSize": xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {"dataName":y, "offset": yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[-1] < self.yOffsetTA[-1]:
            return True
        return False


class AverageXHigherMaxY(EntrySignal):
    name = "Average{X}HigherMax{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        from ..ta.SMA import SMA
        from ..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {"dataName":x, "windowSize": xWindowSize})
        self.yMax = self.AddTA(MaxX, {"dataName":y, "windowSize": yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xSMA[-1] > self.yMax[-1]:
            return True
        return False


#below not udpated
class AverageXLowerMaxY(EntrySignal):
    name = "Average{X}LowerMax{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = cmath.Max(self.y, self.yWindowSize)
        if xVal < yVal:
            return True
        return False


class AverageXHigherMinY(EntrySignal):
    name = "Average{X}HigherMin{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = cmath.Min(self.y, self.yWindowSize)
        if xVal > yVal:
            return True
        return False


class AverageXLowerMinY(EntrySignal):
    name = "Average{X}LowerMin{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = cmath.Min(self.y, self.yWindowSize)
        if xVal < yVal:
            return True
        return False


class AverageXHigherMaxYZ(EntrySignal):
    name = "Average{X}HigherMax{Y}{Z}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0, z="highD", zOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.zOffset = zOffset

        self.yOffsetForList = (yOffset * -1) - 1
        self.zOffsetForList = (zOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)
        self.z = self.GetData(z)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if len(self.z) < self.zOffset + 1:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = self.y[self.yOffsetForList]
        if self.z[self.zOffsetForList] > yVal:
            yVal = self.z[self.zOffsetForList]
        if xVal > yVal:
            return True
        return False


class AverageXLowerMaxYZ(EntrySignal):
    name = "Average{X}LowerMax{Y}{Z}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0, z="highD", zOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.zOffset = zOffset

        self.yOffsetForList = (yOffset * -1) - 1
        self.zOffsetForList = (zOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)
        self.z = self.GetData(z)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if len(self.z) < self.zOffset + 1:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = self.y[self.yOffsetForList]
        if self.z[self.zOffsetForList] > yVal:
            yVal = self.z[self.zOffsetForList]
        if xVal < yVal:
            return True
        return False


class AverageXHigherMinYZ(EntrySignal):
    name = "Average{X}HigherMin{Y}{Z}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0, z="highD", zOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.zOffset = zOffset

        self.yOffsetForList = (yOffset * -1) - 1
        self.zOffsetForList = (zOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)
        self.z = self.GetData(z)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if len(self.z) < self.zOffset + 1:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = self.y[self.yOffsetForList]
        if self.z[self.zOffsetForList] < yVal:
            yVal = self.z[self.zOffsetForList]
        if xVal > yVal:
            return True
        return False


class AverageXLowerMinYZ(EntrySignal):
    name = "Average{X}LowerMin{Y}{Z}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yOffset=0, z="highD", zOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.zLabel = z
        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.zOffset = zOffset

        self.yOffsetForList = (yOffset * -1) - 1
        self.zOffsetForList = (zOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)
        self.z = self.GetData(z)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").\
                            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")").\
                            replace("{Z}", self.zLabel + "(" + str(self.zOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if len(self.z) < self.zOffset + 1:
            return False

        xVal = cmath.Average(self.x, self.xWindowSize)
        yVal = self.y[self.yOffsetForList]
        if self.z[self.zOffsetForList] < yVal:
            yVal = self.z[self.zOffsetForList]
        if xVal < yVal:
            return True
        return False


class XHigherAverageY(EntrySignal):
    name = "{X}HigherAverage{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xOffsetForList * -1:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        avg = cmath.Average(self.y, self.yWindowSize)
        if self.x[self.xOffsetForList] > avg:
            return True

        return False


class XLowerAverageY(EntrySignal):
    name = "{X}LowerAverage{Y}"

    def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yWindowSize = yWindowSize

        self.xOffsetForList = (xOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").\
            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")

        return newName

    def CalculateSignal(self, bar):
        if len(self.x) < self.xOffsetForList * -1:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        avg = cmath.Average(self.y, self.yWindowSize)
        if self.x[self.xOffsetForList] < avg:
            return True

        return False


class AverageXHigherAverageY(EntrySignal):
    name = "Average{X}HigherAverage{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")"). \
            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        avgX = cmath.Average(self.x, self.xWindowSize)
        avgY = cmath.Average(self.y, self.yWindowSize)
        if avgX > avgY:
            return True

        return False


class AverageXLowerAverageY(EntrySignal):
    name = "Average{X}LowerAverage{Y}"

    def __init__(self, strategy, x="high", xWindowSize=0, y="highD", yWindowSize=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")"). \
            replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xWindowSize:
            return False

        if len(self.y) < self.yWindowSize:
            return False

        avgX = cmath.Average(self.x, self.xWindowSize)
        avgY = cmath.Average(self.y, self.yWindowSize)
        if avgX < avgY:
            return True
        return False

    class AverageXLowerAverageY(EntrySignal):
        name = "Average{X}LowerAverage{Y}"

        def __init__(self, strategy, x="high", xOffset=0, y="highD", yWindowSize=0):
            super().__init__(strategy)
            self.xLabel = x
            self.yLabel = y
            self.xWindowSize = xWindowSize
            self.yWindowSize = yWindowSize

            self.x = self.GetData(x)
            self.y = self.GetData(y)

        def Label(self):
            newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")"). \
                replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
            return newName

        def CalculateSignal(self, bar):
            if len(self.x) < self.xWindowSize:
                return False

            if len(self.y) < self.yWindowSize:
                return False

            avgX = cmath.Average(self.x, self.xWindowSize)
            avgY = cmath.Average(self.y, self.yWindowSize)
            if avgX < avgY:
                return True
            return False


class XYDiffLargerRange(EntrySignal):
    name = "{X}{Y}DiffLargerRange"

    def __init__(self, strategy, x="highD", xOffset=0, y="lowD", yOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset

        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffsetForList = (yOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")"). \
            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xOffset + 1:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if self.x[self.xOffsetForList] - self.y[self.yOffsetForList] > self.strategy.range[0]:
            return True
        return False


class XYDiffSmallerRange(EntrySignal):
    name = "{X}{Y}DiffSmallRange"

    def __init__(self, strategy, x="highD", xOffset=0, y="lowD", yOffset=0):
        super().__init__(strategy)
        self.xLabel = x
        self.yLabel = y
        self.xOffset = xOffset
        self.yOffset = yOffset

        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffsetForList = (yOffset * -1) - 1

        print("need to work on intra TA!")
        self.x = self.GetData(x)
        self.y = self.GetData(y)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")"). \
            replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if len(self.x) < self.xOffset + 1:
            return False

        if len(self.y) < self.yOffset + 1:
            return False

        if self.x[self.xOffsetForList] - self.y[self.yOffsetForList] < self.strategy.range[0]:
            return True
        return False







# endregion

