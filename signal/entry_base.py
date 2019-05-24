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



#=======================================================================
#Class: XHigherY
class XHigherYWithThresold(EntrySignal):
    name = "{X}Higher{Y}WithThresold{THRESHOLD}"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, xDelay=0, yDelay=0, threshold=80):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1

        self.threshold = threshold

        from..ta.base import OffsetTA, CurrentDayOffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)
        newName = newName.replace("{THRESHOLD}", "(" + str(self.threshold) + ")")

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.yOffsetTA[self.yDelayForList] + self.threshold:
            return True

        return False

#=======================================================================

#=======================================================================
#Class: XHigherY
class XLowerYWithThresold(EntrySignal):
    name = "{X}Lower{Y}WithThresold{THRESHOLD}"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, xDelay=0, yDelay=0, threshold=80):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1

        self.threshold = threshold

        from..ta.base import OffsetTA, CurrentDayOffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)
        newName = newName.replace("{THRESHOLD}", "("+str(self.threshold) +")")

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.yOffsetTA[self.yDelayForList] + self.threshold:
            return True

        return False

#=======================================================================


# region Higher X Lower X comparsion
#Class: HigherX
class HigherX(EntrySignal):
    name = "Higher{X}"

    def __init__(self, strategy, x="open", xWindowSize=0, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})

    def Label(self):
        newName = self.name
        xLabel =   self.xLabel + "(" + str(self.xWindowSize) + ")"
        if self.xOffset != -1:
            xLabel += 'Offset('+str(self.xOffset)+')'
        newName = newName.replace("{X}", xLabel)
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if len(self.xMax) <= self.xWindowSize:
            return False

        if len(self.xMax) <= self.xWindowSize + self.xOffset + 1:
            return False

        val1 = self.xMax[self.xOffsetForList]
        val2 = self.xMax[-self.xWindowSize + self.xOffsetForList]

        if val1 > val2:
            return True
        return False

#Class: HigherX
class LowerX(EntrySignal):
    name = "Lower{X}"
    def __init__(self, strategy, x="open", xWindowSize=0, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})


    def Label(self):
        newName = self.name
        xLabel =   self.xLabel + "(" + str(self.xWindowSize) + ")"
        if self.xOffset != -1:
            xLabel += 'Offset('+str(self.xOffset)+')'
        newName = newName.replace("{X}", xLabel)
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if len(self.xMin) <= self.xWindowSize:
            return False

        if len(self.xMin) <= self.xWindowSize + self.xOffset + 1:
            return False

        val1 = self.xMin[self.xOffsetForList]
        val2 = self.xMin[-self.xWindowSize + self.xOffsetForList]
        if val1 < val2:
            return True
        return False
# endregion

# region Pivot Point related
#Class: XHigherPivotPoint
class XHigherPivotPoint(EntrySignal):
    name = "{X}HigherPivotPoint{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPoint
        self.yPivotPoint = self.AddTA(PivotPoint, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPoint
class XLowerPivotPoint(EntrySignal):
    name = "{X}LowerPivotPoint{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPoint
        self.yPivotPoint = self.AddTA(PivotPoint, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointS1
class XHigherPivotPointS1(EntrySignal):
    name = "{X}HigherPivotPointS1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS1
        self.yPivotPoint = self.AddTA(PivotPointS1, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointS1
class XLowerPivotPointS1(EntrySignal):
    name = "{X}LowerPivotPointS1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS1
        self.yPivotPoint = self.AddTA(PivotPointS1, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointR1
class XHigherPivotPointR1(EntrySignal):
    name = "{X}HigherPivotPointR1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR1
        self.yPivotPoint = self.AddTA(PivotPointR1, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointR1
class XLowerPivotPointR1(EntrySignal):
    name = "{X}LowerPivotPointR1{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR1
        self.yPivotPoint = self.AddTA(PivotPointR1, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointS2
class XHigherPivotPointS2(EntrySignal):
    name = "{X}HigherPivotPointS2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS2
        self.yPivotPoint = self.AddTA(PivotPointS2, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointS2
class XLowerPivotPointS2(EntrySignal):
    name = "{X}LowerPivotPointS2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS2
        self.yPivotPoint = self.AddTA(PivotPointS2, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointR2
class XHigherPivotPointR2(EntrySignal):
    name = "{X}HigherPivotPointR2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR2
        self.yPivotPoint = self.AddTA(PivotPointR2, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointR2
class XLowerPivotPointR2(EntrySignal):
    name = "{X}LowerPivotPointR2{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1


        from..ta.Anchor import PivotPointR2
        self.yPivotPoint = self.AddTA(PivotPointR2, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointS3
class XHigherPivotPointS3(EntrySignal):
    name = "{X}HigherPivotPointS3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS3
        self.yPivotPoint = self.AddTA(PivotPointS3, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointS3
class XLowerPivotPointS3(EntrySignal):
    name = "{X}LowerPivotPointS3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS3
        self.yPivotPoint = self.AddTA(PivotPointS3, {'dataName':x, 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XHigherPivotPointR3
class XHigherPivotPointR3(EntrySignal):
    name = "{X}HigherPivotPointR3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR3
        self.yPivotPoint = self.AddTA(PivotPointR3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)

    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] > self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: XLowerPivotPointR3
class XLowerPivotPointR3(EntrySignal):
    name = "{X}LowerPivotPointR3{Y}"

    def __init__(self, strategy, x="openD", xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = x
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR3
        self.yPivotPoint = self.AddTA(PivotPointR3, {'dataName':"", 'offset': yOffset})
        self.data = utilities.GetDataByName(strategy, x)


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", "(" + str(self.yOffset) + ")")
        return newName


    def CalculateSignal(self, bar):
        if not self.yPivotPoint.isReady:
            return False

        if self.data[self.xOffsetForList] < self.yPivotPoint[self.yOffsetForList]:
            return True
        return False

#Class: CrossUpPivotPoint
class CrossUpPivotPoint(EntrySignal):
    name = "{X}CrossUpPivotPoint"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPoint
        self.xPivotPoint = self.AddTA(PivotPoint, {'dataName':"closeD", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPoint.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPoint[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPoint[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPoint
class CrossDownPivotPoint(EntrySignal):
    name = "{X}CrossDownPivotPoint"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPoint
        self.xPivotPoint = self.AddTA(PivotPoint, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPoint.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPoint[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPoint[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointR1
class CrossUpPivotPointR1(EntrySignal):
    name = "{X}CrossUpPivotPointR1"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR1
        self.xPivotPointR1 = self.AddTA(PivotPointR1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR1.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointR1[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointR1[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointR1
class CrossDownPivotPointR1(EntrySignal):
    name = "{X}CrossDownPivotPointR1"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR1
        self.xPivotPointR1 = self.AddTA(PivotPointR1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR1.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointR1[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointR1[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointS1
class CrossUpPivotPointS1(EntrySignal):
    name = "{X}CrossUpPivotPointS1"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS1
        self.xPivotPointS1 = self.AddTA(PivotPointS1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS1.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointS1[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointS1[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointS1
class CrossDownPivotPointS1(EntrySignal):
    name = "{X}CrossDownPivotPointS1"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS1
        self.xPivotPointS1 = self.AddTA(PivotPointS1, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS1.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointS1[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointS1[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointR2
class CrossUpPivotPointR2(EntrySignal):
    name = "{X}CrossUpPivotPointR2"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR2
        self.xPivotPointR2 = self.AddTA(PivotPointR2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR2.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointR2[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointR2[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointR2
class CrossDownPivotPointR2(EntrySignal):
    name = "{X}CrossDownPivotPointR2"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR2
        self.xPivotPointR2 = self.AddTA(PivotPointR2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR2.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointR2[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointR2[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointS2
class CrossUpPivotPointS2(EntrySignal):
    name = "{X}CrossUpPivotPointS2"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS2
        self.xPivotPointS2 = self.AddTA(PivotPointS2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS2.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointS2[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointS2[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointS2
class CrossDownPivotPointS2(EntrySignal):
    name = "{X}CrossDownPivotPointS2"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS2
        self.xPivotPointS2 = self.AddTA(PivotPointS2, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS2.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointS2[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointS2[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointR3
class CrossUpPivotPointR3(EntrySignal):
    name = "{X}CrossUpPivotPointR3"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR3
        self.xPivotPointR3 = self.AddTA(PivotPointR3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR3.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointR3[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointR3[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointR3
class CrossDownPivotPointR3(EntrySignal):
    name = "{X}CrossDownPivotPointR3"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointR3
        self.xPivotPointR3 = self.AddTA(PivotPointR3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointR3.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointR3[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointR3[self.yOffsetForList]:
                return True
        return False

#Class: CrossUpPivotPointS3
class CrossUpPivotPointS3(EntrySignal):
    name = "{X}CrossUpPivotPointS3"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS3
        self.xPivotPointS3 = self.AddTA(PivotPointS3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS3.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] > self.xPivotPointS3[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] < self.xPivotPointS3[self.yOffsetForList]:
                return True
        return False

#Class: CrossDownPivotPointS3
class CrossDownPivotPointS3(EntrySignal):
    name = "{X}CrossDownPivotPointS3"

    def __init__(self, strategy, xOffset=0, yOffset=1):
        super().__init__(strategy)

        self.xLabel = ""
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        from..ta.Anchor import PivotPointS3
        self.xPivotPointS3 = self.AddTA(PivotPointS3, {'dataName':"", 'offset': xOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")")
        if self.yOffsetForList != -1:
            newName += "OFFSET(" + str(self.yOffset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.xPivotPointS3.isReady:
            return False

        if self.strategy.close[self.xOffsetForList] < self.xPivotPointS3[self.yOffsetForList]:
            if self.strategy.close[self.xOffsetForList-1] > self.xPivotPointS3[self.yOffsetForList]:
                return True
        return False
# endregion


# region KAMA related
#Class: XHigherKAMA
class XHigherKAMA(EntrySignal):
    name = "{X}HigherKAMA{WINDOWSIZE}"

    def __init__(self, strategy, x="close", xOffset=0, windowSize=30, kamaOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = (xOffset * -1) - 1
        self.xOffsetForList = (xOffset * -1) - 1
        self.kamaOffset = kamaOffset
        self.kamaOffsetForList = (kamaOffset * -1) - 1


        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName':x, 'windowSize': windowSize})


    def Label(self):
        newName = self.name
        xLabel =   self.xLabel
        if self.xOffsetForList != -1:
            xLabel +=  'Offset('+str((self.xOffset+1)*-1)+')'
        newName = newName.replace("{X}", xLabel)

        windowSizeLabel = '(' + str((self.windowSize + 1) * -1) + ')'
        if self.kamaOffsetForList != -1:
            windowSizeLabel += 'Offset(' + str((self.kamaOffset + 1) * -1) + ')'
        newName = newName.replace("{WINDOWSIZE}", windowSizeLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.xOffsetForList] > self.kama[self.kamaOffsetForList]:
            return True
        return False

#Class: XHigherKAMAY
class XHigherKAMAY(EntrySignal):
    name = "{X}HigherKAMA{Y}"

    def __init__(self, strategy, x="close", offset=0, y="closeD", windowSize = 30, kamaOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y
        self.xOffset = offset
        self.xOffsetForList = (offset * -1) - 1
        self.windowSize = windowSize
        self.kamaOffset = kamaOffset
        self.kamaOffsetForList = (kamaOffset * -1) - 1

        self.data = utilities.GetDataByName(strategy, x)



        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName':y, 'windowSize': windowSize})


    def Label(self):
        newName = self.name
        xLabel =   self.xLabel
        if self.xOffsetForList != -1:
            xLabel +=  'Offset('+str((self.xOffset+1)*-1)+')'
        newName = newName.replace("{X}", xLabel)


        yLabel = self.yLabel + "("+str(self.windowSize)+")"
        if self.kamaOffsetForList != -1:
            yLabel +=  'Offset('+str((self.kamaOffset+1)*-1)+')'
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.xOffsetForList] > self.kama[self.kamaOffsetForList]:
            return True
        return False

#Class: XLowerKAMA
class XLowerKAMA(EntrySignal):
    name = "{X}LowerKAMA{WINDOWSIZE}"

    def __init__(self, strategy, x="close", xOffset=0, windowSize=30, kamaOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = (xOffset * -1) - 1
        self.xOffsetForList = (xOffset * -1) - 1
        self.kamaOffset = kamaOffset
        self.kamaOffsetForList = (kamaOffset * -1) - 1

        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName':x, 'windowSize': windowSize})


    def Label(self):
        newName = self.name
        xLabel =   self.xLabel
        if self.xOffsetForList != -1:
            xLabel +=  'Offset('+str((self.xOffset+1)*-1)+')'
        newName = newName.replace("{X}", xLabel)

        windowSizeLabel = '(' + str((self.windowSize + 1) * -1) + ')'
        if self.kamaOffsetForList != -1:
            windowSizeLabel += 'Offset(' + str((self.kamaOffset + 1) * -1) + ')'
        newName = newName.replace("{WINDOWSIZE}", windowSizeLabel)

        return rename


    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.xOffsetForList] < self.kama[self.kamaOffsetForList]:
            return True
        return False

# Class: XLowerKAMAY
class XLowerKAMAY(EntrySignal):
    name = "{X}LowerKAMA{Y}"

    def __init__(self, strategy, x="close", offset=0, y="closeD", windowSize=30, kamaOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y
        self.xOffset = offset
        self.xOffsetForList = (offset * -1) - 1
        self.windowSize = windowSize
        self.kamaOffset = kamaOffset
        self.kamaOffsetForList = (kamaOffset * -1) - 1

        self.data = utilities.GetDataByName(strategy, x)

        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName': y, 'windowSize': windowSize})

    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffsetForList != -1:
            xLabel += 'Offset(' + str((self.xOffset + 1) * -1) + ')'
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "(" + str(self.windowSize) + ")"
        if self.kamaOffsetForList != -1:
            yLabel += 'Offset(' + str((self.kamaOffset + 1) * -1) + ')'
        newName = newName.replace("{Y}", yLabel)

        return newName

    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.xOffsetForList] < self.kama[self.kamaOffsetForList]:
            return True
        return False
# endregion


# region BBands related
#Class: XHigherBBandsUpper
class XHigherBBandsUpper(EntrySignal):
    name = "{X}HigherBBandsUpper{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.xOffsetForList] > self.bbandsUpper[self.bbOffsetForList]:
            return True
        return False

#Class: XHigherBBandsMiddle
class XHigherBBandsMiddle(EntrySignal):
    name = "{X}HigherBBandsMiddle{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.xOffsetForList] > self.bbandsMiddle[self.bbOffsetForList]:
            return True
        return False

#Class: XHigherBBandsLower
class XHigherBBandsLower(EntrySignal):
    name = "{X}HigherBBandsLower{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsLower
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)


        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsLower.isReady:
            return False

        if self.data[self.xOffsetForList] > self.bbandsLower[self.bbOffsetForList]:
            return True
        return False

#Class: XLowerBBandsUpper
class XLowerBBandsUpper(EntrySignal):
    name = "{X}LowerBBandsUpper{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.xOffsetForList] < self.bbandsUpper[self.bbOffsetForList]:
            return True
        return False

#Class: XLowerBBandsMiddle
class XLowerBBandsMiddle(EntrySignal):
    name = "{X}LowerBBandsMiddle{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.xOffsetForList] < self.bbandsMiddle[self.bbOffsetForList]:
            return True
        return False

#Class: XLowerBBandsLower
class XLowerBBandsLower(EntrySignal):
    name = "{X}LowerBBandsLower{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsLower
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsLower.isReady:
            return False

        if self.data[self.xOffsetForList] < self.bbandsLower[self.bbOffsetForList]:
            return True
        return False

#Class: XInBBandsUpper
class XInBBandsUpper(EntrySignal):
    name = "{X}InBBandsUpper{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsUpper, BBandsMiddle
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.xOffset] < self.bbandsUpper[self.bbOffsetForList] and self.data[self.xOffset] > self.bbandsMiddle[self.bbOffsetForList]:
            return True
        return False

#Class: XInBBandsLower
class XInBBandsLower(EntrySignal):
    name = "{X}InBBandsLower{BB}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, xOffset=0, bbOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        from ..ta.OverlapTA import BBandsLower, BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        if self.xOffset!=0:
            xLabel += "Offset("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.xOffsetForList] < self.bbandsMiddle[self.bbOffsetForList] and self.data[self.xOffsetForList] > self.bbandsLower[self.bbOffsetForList]:
            return True
        return False

#Class: NarrowerBBands
class NarrowerBBands(EntrySignal):
    name = "{X}NarrowerBBands{BB}-{COMPAREWINDOWSIZE}-{RATIO}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, bbOffset=0, compareWindowSize=6, ratio=1):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        self.compareWindowSize = compareWindowSize
        self.ratio = ratio

        from ..ta.OverlapTA import BBandsLower, BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)
        newName = newName.replace("{COMPAREWINDOWSIZE}", str(self.compareWindowSize))
        newName = newName.replace("{RATIO}", str(self.ratio))

        return newName

    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if len(self.bbandsUpper) <= (self.bbOffsetForList - self.compareWindowSize) * -1:
            return False

        upper1 = self.bbandsUpper[self.bbOffsetForList - self.compareWindowSize]
        lower1 = self.bbandsLower[self.bbOffsetForList - self.compareWindowSize]
        previousRange = upper1 - lower1

        upper2 = self.bbandsUpper[self.bbOffsetForList]
        lower2 = self.bbandsLower[self.bbOffsetForList]
        currentRange = upper2 - lower2

        if currentRange < previousRange*self.ratio:
            return True
        return False

#Class: WiderBBands
class WiderBBands(EntrySignal):
    name = "{X}WiderBBands{BB}-{COMPAREWINDOWSIZE}-{RATIO}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, bbOffset=0, compareWindowSize=6, ratio=1):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.bbOffset = bbOffset
        self.bbOffsetForList = (bbOffset * -1) - 1

        self.compareWindowSize = compareWindowSize
        self.ratio = ratio

        from ..ta.OverlapTA import BBandsLower, BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        bbLabel = str(self.windowSize) + "-" + str(self.nbdev)
        if self.bbOffset != 0:
            bbLabel += "Offset(" + str(self.bbOffset) + ")"
        newName = newName.replace("{BB}", bbLabel)
        newName = newName.replace("{COMPAREWINDOWSIZE}", str(self.compareWindowSize))
        newName = newName.replace("{RATIO}", str(self.ratio))

        return newName

    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if len(self.bbandsUpper) <= (self.bbOffsetForList - self.compareWindowSize) * -1:
            return False

        upper1 = self.bbandsUpper[self.bbOffsetForList - self.compareWindowSize]
        lower1 = self.bbandsLower[self.bbOffsetForList - self.compareWindowSize]
        previousRange = upper1 - lower1

        upper2 = self.bbandsUpper[self.bbOffsetForList]
        lower2 = self.bbandsLower[self.bbOffsetForList]
        currentRange = upper2 - lower2

        if currentRange > previousRange*self.ratio:
            return True
        return False
# endregion



# region RSI related
#Class: MaxRSIHigherThreshold
class MaxRSIHigherThreshold(EntrySignal):
    name = "Max{MAX}{X}RSI{RSI}HigherThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})

    def Label(self):
        newName = self.name
        newName = newName.replace("{MAX}", str(self.maxWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName

    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        if len(self.rsi) < (-self.maxWindowSize - self.rsiOffset) * -1 -1:
            return False

        val = cmath.MaxOfRange(self.rsi, -self.maxWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val > self.threshold:
            return True
        return False

#Class: MinRSIHigherThreshold
class MinRSIHigherThreshold(EntrySignal):
    name = "Min{MIN}{X}RSI{RSI}HigherThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, minWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.minWindowSize = minWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name
        newName = newName.replace("{MIN}", str(self.minWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        if len(self.rsi) < (-self.minWindowSize - self.rsiOffset) * -1 -1:
            return False

        val = cmath.MinOfRange(self.rsi, -self.minWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val > self.threshold:
            return True
        return False

#Class: MaxRSILowerThreshold
class MaxRSILowerThreshold(EntrySignal):
    name = "Max{MAX}{X}RSI{RSI}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name
        newName = newName.replace("{MAX}", str(self.maxWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False


        if len(self.rsi) < (-self.maxWindowSize - self.rsiOffset) * -1 - 1:
            return False

        val = cmath.MaxOfRange(self.rsi, -self.maxWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val < self.threshold:
            return True
        return False

#Class: MinRSIHigherThreshold
class MinRSILowerThreshold(EntrySignal):
    name = "Min{MIN}{X}RSI{RSI}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, minWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.minWindowSize = minWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name
        newName = newName.replace("{MIN}", str(self.minWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False


        if len(self.rsi) < (-self.minWindowSize - self.rsiOffset) * -1 - 1:
            return False

        val = cmath.MinOfRange(self.rsi, -self.minWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val < self.threshold:
            return True
        return False

#Class: MaxRSILowerThreshold
class MaxRSILowerThreshold(EntrySignal):
    name = "Max{MAX}{X}RSI{RSI}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, maxWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.maxWindowSize = maxWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name
        newName = newName.replace("{MAX}", str(self.maxWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        if len(self.rsi) < (-self.maxWindowSize - self.rsiOffset) * -1 - 1:
            return False

        val = cmath.MaxOfRange(self.rsi, -self.maxWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val < self.threshold:
            return True
        return False

#Class: MinRSIHigherThreshold
class MinRSILowerThreshold(EntrySignal):
    name = "Min{MIN}{X}RSI{RSI}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, rsiOffset=0, minWindowSize=14, threshold=80):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.minWindowSize = minWindowSize
        self.threshold = threshold

        self.rsiOffset = rsiOffset
        self.rsiOffsetForList = (rsiOffset * -1)

        from..ta.MomentumTA import RSI
        self.rsi = self.AddTA(RSI, {'dataName':x, 'windowSize': rsiWindowSize})


    def Label(self):
        newName = self.name
        newName = newName.replace("{MIN}", str(self.minWindowSize))

        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        rsiLabel = str(self.rsiWindowSize)
        if self.rsiOffset != 0:
            rsiLabel += "Offset(" + str(self.rsiOffset) + ")"
        newName = newName.replace("{RSI}", rsiLabel)
        newName = newName.replace("{THRESHOLD}", str(self.threshold))

        return newName


    def CalculateSignal(self, bar):
        if not self.rsi.isReady:
            return False

        if len(self.rsi) < (-self.minWindowSize - self.rsiOffset) * -1 - 1:
            return False

        val = cmath.MinOfRange(self.rsi, -self.minWindowSize - self.rsiOffset, len(self.rsi) - self.rsiOffset)
        if val < self.threshold:
            return True
        return False
# endregion


# region MACD related
#Class: MACDSignalHigherMACD
class MACDHigherMACDSignal(EntrySignal):
    name = "{X}MACDHigherMACDSignal{MACD_OFFSET}"

    def __init__(self, strategy, x="close", fastWindowSize=12, slowWindowSize=26, signalWindowSize=9, macdOffset=0):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.fastWindowSize = fastWindowSize
        self.slowWindowSize = slowWindowSize
        self.signalWindowSize = signalWindowSize
        self.macdOffset = macdOffset
        self.macdOffsetForList = (macdOffset * -1) - 1

        from..ta.MomentumTA import MACD, MACDSignalLine
        params = {
            "dataName": x,
            "fastWindowSize": fastWindowSize,
            "slowWindowSize": slowWindowSize,
            "signalWindowSize": signalWindowSize
        }
        self.macd = self.AddTA(MACD, params)
        self.macdSignalLine = self.AddTA(MACDSignalLine, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        offsetLabel = "(" + str(self.fastWindowSize) + "," + str(self.slowWindowSize) + "," + str(self.signalWindowSize) + ")"
        if self.macdOffset != 0:
            offsetLabel += "Offset("+str(self.macdOffset)+")"
        newName = newName.replace("{MACD_OFFSET}", offsetLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.macd.isReady:
            return False

        if self.macd[self.macdOffsetForList] > self.macdSignalLine[self.macdOffsetForList]:
            return True
        return False

#Class: MACDLowerMACDSignal
class MACDLowerMACDSignal(EntrySignal):
    name = "{X}MACDLowerMACDSignal{MACD_OFFSET}"
    name = "{X}MACDLowerMACDSignal"

    def __init__(self, strategy, x="close", fastWindowSize=12, slowWindowSize=26, signalWindowSize=9, macdOffset=0):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.fastWindowSize = fastWindowSize
        self.slowWindowSize = slowWindowSize
        self.signalWindowSize = signalWindowSize
        self.macdOffset = macdOffset
        self.macdOffsetForList = (macdOffset * -1) - 1

        from..ta.MomentumTA import MACD, MACDSignalLine
        params = {
            "dataName": x,
            "fastWindowSize": fastWindowSize,
            "slowWindowSize": slowWindowSize,
            "signalWindowSize": signalWindowSize
        }
        self.macd = self.AddTA(MACD, params)
        self.macdSignalLine = self.AddTA(MACDSignalLine, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        offsetLabel = "(" + str(self.fastWindowSize) + "," + str(self.slowWindowSize) + "," + str(self.signalWindowSize) + ")"
        if self.macdOffset != 0:
            offsetLabel += "Offset("+str(self.macdOffset)+")"
        newName = newName.replace("{MACD_OFFSET}", offsetLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.macd.isReady:
            return False

        if self.macd[self.macdOffsetForList] < self.macdSignalLine[self.macdOffsetForList]:
            return True
        return False
# endregion

# region Stochastic related
#Class: StochasticSlowKHigherD
class StochasticSlowKHigherD(EntrySignal):
    name = "{X}StochasticSlow{PARAMS}KHigherD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowKHigherD: only support close and closeD as data")

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticSlowK, StochasticSlowD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "slowKWindowSize": slowKWindowSize,
            "slowDWindowSize": slowDWindowSize
        }
        self.kLine = self.AddTA(StochasticSlowK, params)
        self.dLine = self.AddTA(StochasticSlowD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "("+str(self.fastKWindowSize)+","+str(self.slowKWindowSize)+","+str(self.slowDWindowSize)+")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        if self.offset != 0:
            newName += "Offset(" + str(self.offset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticSlowKLowerD
class StochasticSlowKLowerD(EntrySignal):
    name = "{X}StochasticSlow{PARAMS}KLowerD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowKLowerD: only support close and closeD as data")

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticSlowK, StochasticSlowD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "slowKWindowSize": slowKWindowSize,
            "slowDWindowSize": slowDWindowSize
        }
        self.kLine = self.AddTA(StochasticSlowK, params)
        self.dLine = self.AddTA(StochasticSlowD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "("+str(self.fastKWindowSize)+","+str(self.slowKWindowSize)+","+str(self.slowDWindowSize)+")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        if self.offset != 0:
            newName += "Offset(" + str(self.offset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return

        if self.kLine[self.offsetForList] < self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticFastKHigherD
class StochasticFastKHigherD(EntrySignal):
    name = "{X}StochasticFast{PARAMS}KHigherD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastKHigherD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "("+str(self.fastKWindowSize)+","+str(self.fastDWindowSize)+")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        if self.offset != 0:
            newName += "Offset(" + str(self.offset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticFastKLowerD
class StochasticFastKLowerD(EntrySignal):
    name = "{X}StochasticFast{PARAMS}KLowerD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastKLowerD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "("+str(self.fastKWindowSize)+","+str(self.fastDWindowSize)+")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        if self.offset != 0:
            newName += "Offset(" + str(self.offset) + ")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] < self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticRSIKHigherD
class StochasticRSIKHigherD(EntrySignal):
    name = "{X}StochasticRSI{PARAMS}KHigherD"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIKHigherD: only support close and closeD as data")

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticRSIK, StochasticRSID
        params = {
            "dataName": x,
            "rsiWindowSize": rsiWindowSize,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticRSIK, params)
        self.dLine = self.AddTA(StochasticRSID, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.rsiWindowSize) + "," + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)
        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"

        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticRSIKLowerD
class StochasticRSIKLowerD(EntrySignal):
    name = "{X}StochasticRSIK{PARAMS}LowerD"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIKLowerD: only support close and closeD as data")

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticRSIK, StochasticRSID
        params = {
            "dataName": x,
            "rsiWindowSize": rsiWindowSize,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticRSIK, params)
        self.dLine = self.AddTA(StochasticRSID, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.rsiWindowSize) + "," + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)
        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] < self.dLine[self.offsetForList]:
            return True
        return False

#Class: StochasticSlowHigherThreshold
class StochasticSlowHigherThreshold(EntrySignal):
    name = "{X}StochasticSlow{PARAMS}HigherThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, threshold=80, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticSlowK, StochasticSlowD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "slowKWindowSize": slowKWindowSize,
            "slowDWindowSize": slowDWindowSize
        }
        self.kLine = self.AddTA(StochasticSlowK, params)
        self.dLine = self.AddTA(StochasticSlowD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.fastKWindowSize) + "," + str(self.slowKWindowSize) + "," + str(self.slowDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"

        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.threshold and self.dLine[self.offsetForList] > self.threshold:
            return True
        return False

#Class: StochasticSlowLowerThreshold
class StochasticSlowLowerThreshold(EntrySignal):
    name = "{X}StochasticSlow{PARAMS}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, threshold=20, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowLowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticSlowK, StochasticSlowD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "slowKWindowSize": slowKWindowSize,
            "slowDWindowSize": slowDWindowSize
        }
        self.kLine = self.AddTA(StochasticSlowK, params)
        self.dLine = self.AddTA(StochasticSlowD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.fastKWindowSize) + "," + str(self.slowKWindowSize) + "," + str(
            self.slowDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"

        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] < self.threshold and self.dLine[self.offsetForList] < self.threshold:
            return True
        return False

#Class: StochasticFastHigherThreshold
class StochasticFastHigherThreshold(EntrySignal):
    name = "{X}StochasticFast{PARAMS}HigherThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, threshold=80, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.threshold and self.dLine[self.offsetForList] > self.threshold:
            return True
        return False

#Class: StochasticFastLowerThreshold
class StochasticFastLowerThreshold(EntrySignal):
    name = "{X}StochasticFast{PARAMS}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, threshold=20, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastLowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] < self.threshold and self.dLine[self.offsetForList] < self.threshold:
            return True
        return False

#Class: StochasticRSIHigherThreshold
class StochasticRSIHigherThreshold(EntrySignal):
    name = "{X}StochasticRSI{PARAMS}HigherThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, threshold=80, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticRSIK, StochasticRSID
        params = {
            "dataName": x,
            "rsiWindowSize": rsiWindowSize,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticRSIK, params)
        self.dLine = self.AddTA(StochasticRSID, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.rsiWindowSize) + "," + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"

        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] > self.threshold and self.dLine[self.offsetForList] > self.threshold:
            return True
        return False

#Class: StochasticRSILowerThreshold
class StochasticRSILowerThreshold(EntrySignal):
    name = "{X}StochasticRSI{PARAMS}LowerThreshold{THRESHOLD}"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, threshold=20, offset=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSILowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = x
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.offset = offset
        self.offsetForList = (offset * -1) - 1

        from..ta.MomentumTA import StochasticRSIK, StochasticRSID
        params = {
            "dataName": x,
            "rsiWindowSize": rsiWindowSize,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticRSIK, params)
        self.dLine = self.AddTA(StochasticRSID, params)


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)

        paramsLabel = "(" + str(self.rsiWindowSize) + "," + str(self.fastKWindowSize) + "," + str(self.fastDWindowSize) + ")"
        newName = newName.replace("{PARAMS}", paramsLabel)

        thresholdLabel = "("+str(self.threshold)+")"
        newName = newName.replace("{THRESHOLD}", thresholdLabel)

        if self.offset != 0:
            newName += "Offset("+str(self.offset)+")"

        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if len(self.kLine) <= self.offset:
            return False

        if self.kLine[self.offsetForList] < self.threshold and self.dLine[self.offsetForList] < self.threshold:
            return True
        return False
# endregion