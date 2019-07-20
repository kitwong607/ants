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

# region TALib Pattern related
#=======================================================================
#Class: XHigherY
class XYRangeLargerThresold(EntrySignal):
    name = "{X}{Y}RangeLargerThresold{THRESHOLD}"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, threshold=80):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        self.threshold = threshold

        from..ta.base import OffsetTA, CurrentDayOffsetTA
        self.xOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        newName = newName.replace("{Y}", yLabel)
        newName = newName.replace("{THRESHOLD}", "(" + str(self.threshold) + ")")

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if abs(self.xOffsetTA[-1] - self.yOffsetTA[-1]) > self.threshold:
            return True

        return False
#=======================================================================

# endregion




#=======================================================================
#Class: XHigherY
class XYRangeLargerThresold(EntrySignal):
    name = "{X}{Y}RangeLargerThresold{THRESHOLD}"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, threshold=80):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        self.threshold = threshold

        from..ta.base import OffsetTA, CurrentDayOffsetTA
        self.xOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        newName = newName.replace("{Y}", yLabel)
        newName = newName.replace("{THRESHOLD}", "(" + str(self.threshold) + ")")

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if abs(self.xOffsetTA[-1] - self.yOffsetTA[-1]) > self.threshold:
            return True

        return False
#=======================================================================


#=======================================================================
#Class: XHigherY
class XYRangeSmallerThresold(EntrySignal):
    name = "{X}{Y}RangeSmallerThresold{THRESHOLD}"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, threshold=80):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1

        self.threshold = threshold

        from..ta.base import OffsetTA, CurrentDayOffsetTA
        self.xOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(CurrentDayOffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        newName = newName.replace("{Y}", yLabel)
        newName = newName.replace("{THRESHOLD}", "(" + str(self.threshold) + ")")

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if abs(self.xOffsetTA[-1] - self.yOffsetTA[-1]) < self.threshold:
            return True

        return False
#=======================================================================

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
            xLabel +=  'Offset('+str(self.xOffset)+')'
        newName = newName.replace("{X}", xLabel)

        windowSizeLabel = '(' + str(self.windowSize) + ')'
        if self.kamaOffsetForList != -1:
            windowSizeLabel += 'Offset(' + str(self.kamaOffset) + ')'
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
            yLabel +=  'Offset('+str(self.kamaOffset)+')'
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
            xLabel += 'Offset(' + str(self.xOffset) + ')'
        newName = newName.replace("{X}", xLabel)

        windowSizeLabel = '(' + str(self.windowSize) + ')'
        if self.kamaOffsetForList != -1:
            windowSizeLabel += 'Offset(' + str(self.kamaOffset) + ')'
        newName = newName.replace("{WINDOWSIZE}", windowSizeLabel)

        return newName


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
            xLabel += 'Offset(' + str(self.xOffset) + ')'
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "(" + str(self.windowSize) + ")"
        if self.kamaOffsetForList != -1:
            yLabel += 'Offset(' + str(self.kamaOffset) + ')'
        newName = newName.replace("{Y}", yLabel)

        return newName

    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.xOffsetForList] < self.kama[self.kamaOffsetForList]:
            return True
        return False
# endregion

# region ATR related
#Class: ATRHigherMaxPrevious
class ATRHigherMaxPrevious(EntrySignal):
    name = "{X}ATR{WINDOWS_SIZE}HigherMaxPrevious{COMPARE_WINDOWS_SIZE}"

    def __init__(self, strategy, x="close", windowSize=20, compareWindowSize=10, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.compareWindowSize = compareWindowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.VolatilityTA import ATR, MaxPreviousATR
        self.atr = self.AddTA(ATR, {'dataName':x, 'windowSize': windowSize})
        self.previousMaxATR = self.AddTA(MaxPreviousATR, {'dataName':x, 'windowSize': windowSize, 'compareWindowSize': compareWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)
        newName = newName.replace("{WINDOWS_SIZE}", "(" + str(self.windowSize) + ")")
        newName = newName.replace("{COMPARE_WINDOWS_SIZE}", "(" + str(self.compareWindowSize) + ")")
        if self.xOffset!=0:
            newName += "Offset("+str(self.xOffset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.atr.isReady:
            return False
        if not self.previousMaxATR.isReady:
            return False
        if self.atr[self.xOffsetForList] > self.previousMaxATR[self.xOffsetForList]:
            return True
        return False



#Class: ATRHigherMinPrevious
class ATRHigherMinPrevious(EntrySignal):
    name = "{X}ATR{WINDOWS_SIZE}HigherMinPrevious{COMPARE_WINDOWS_SIZE}"

    def __init__(self, strategy, x="close", windowSize=20, compareWindowSize=10, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.compareWindowSize = compareWindowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.VolatilityTA import ATR, MinPreviousATR
        self.atr = self.AddTA(ATR, {'dataName':x, 'windowSize': windowSize})
        self.previousMinATR = self.AddTA(MinPreviousATR, {'dataName':x, 'windowSize': windowSize, 'compareWindowSize': compareWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)
        newName = newName.replace("{WINDOWS_SIZE}", "(" + str(self.windowSize) + ")")
        newName = newName.replace("{COMPARE_WINDOWS_SIZE}", "(" + str(self.compareWindowSize) + ")")
        if self.xOffset!=0:
            newName += "Offset("+str(self.xOffset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.atr.isReady:
            return False
        if not self.previousMinATR.isReady:
            return False
        if self.atr[self.xOffsetForList] > self.previousMinATR[self.xOffsetForList]:
            return True
        return False




#Class: ATRLowerMaxPrevious
class ATRLowerMaxPrevious(EntrySignal):
    name = "{X}ATR{WINDOWS_SIZE}LowerMaxPrevious{COMPARE_WINDOWS_SIZE}"

    def __init__(self, strategy, x="close", windowSize=20, compareWindowSize=10, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.compareWindowSize = compareWindowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.VolatilityTA import ATR, MaxPreviousATR
        self.atr = self.AddTA(ATR, {'dataName':x, 'windowSize': windowSize})
        self.previousMaxATR = self.AddTA(MaxPreviousATR, {'dataName':x, 'windowSize': windowSize, 'compareWindowSize': compareWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)
        newName = newName.replace("{WINDOWS_SIZE}", "(" + str(self.windowSize) + ")")
        newName = newName.replace("{COMPARE_WINDOWS_SIZE}", "(" + str(self.compareWindowSize) + ")")
        if self.xOffset!=0:
            newName += "Offset("+str(self.xOffset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.atr.isReady:
            return False
        if not self.previousMaxATR.isReady:
            return False
        if self.atr[self.xOffsetForList] < self.previousMaxATR[self.xOffsetForList]:
            return True
        return False



#Class: ATRLowerMinPrevious
class ATRLowerMinPrevious(EntrySignal):
    name = "{X}ATR{WINDOWS_SIZE}LowerMinPrevious{COMPARE_WINDOWS_SIZE}"

    def __init__(self, strategy, x="close", windowSize=20, compareWindowSize=10, xOffset=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.compareWindowSize = compareWindowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1

        from ..ta.VolatilityTA import ATR, MinPreviousATR
        self.atr = self.AddTA(ATR, {'dataName':x, 'windowSize': windowSize})
        self.previousMinATR = self.AddTA(MinPreviousATR, {'dataName':x, 'windowSize': windowSize, 'compareWindowSize': compareWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel
        newName = newName.replace("{X}", xLabel)
        newName = newName.replace("{WINDOWS_SIZE}", "(" + str(self.windowSize) + ")")
        newName = newName.replace("{COMPARE_WINDOWS_SIZE}", "(" + str(self.compareWindowSize) + ")")
        if self.xOffset!=0:
            newName += "Offset("+str(self.xOffset)+")"
        return newName


    def CalculateSignal(self, bar):
        if not self.atr.isReady:
            return False
        if not self.previousMinATR.isReady:
            return False
        if self.atr[self.xOffsetForList] < self.previousMinATR[self.xOffsetForList]:
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



#=======================================================================
#=======================================================================
#Type1 entry signal list
#=======================================================================
#=======================================================================
#Class: XHigherY
class XHigherY(EntrySignal):
    name = "{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, xDelay=0, yDelay=0):
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


        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


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

        if self.xOffsetTA[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XHigherMinY
class XHigherMinY(EntrySignal):
    name = "{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XHigherMaxPreviousY
class XHigherMaxPreviousY(EntrySignal):
    name = "{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XHigherMinPreviousY
class XHigherMinPreviousY(EntrySignal):
    name = "{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XHigherMaxY
class XHigherMaxY(EntrySignal):
    name = "{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XHigherAverageY
class XHigherAverageY(EntrySignal):
    name = "{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerY
class XLowerY(EntrySignal):
    name = "{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, xDelay=0, yDelay=0):
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


        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


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

        if self.xOffsetTA[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerMinY
class XLowerMinY(EntrySignal):
    name = "{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerMaxPreviousY
class XLowerMaxPreviousY(EntrySignal):
    name = "{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerMinPreviousY
class XLowerMinPreviousY(EntrySignal):
    name = "{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerMaxY
class XLowerMaxY(EntrySignal):
    name = "{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: XLowerAverageY
class XLowerAverageY(EntrySignal):
    name = "{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "OffsetTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "OffsetTA"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xOffset)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xOffsetTA) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xOffsetTA[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherY
class MinXHigherY(EntrySignal):
    name = "Min{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Min"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMinY
class MinXHigherMinY(EntrySignal):
    name = "Min{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMaxPreviousY
class MinXHigherMaxPreviousY(EntrySignal):
    name = "Min{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMinPreviousY
class MinXHigherMinPreviousY(EntrySignal):
    name = "Min{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherMaxY
class MinXHigherMaxY(EntrySignal):
    name = "Min{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXHigherAverageY
class MinXHigherAverageY(EntrySignal):
    name = "Min{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerY
class MinXLowerY(EntrySignal):
    name = "Min{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Min"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMinY
class MinXLowerMinY(EntrySignal):
    name = "Min{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMaxPreviousY
class MinXLowerMaxPreviousY(EntrySignal):
    name = "Min{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMinPreviousY
class MinXLowerMinPreviousY(EntrySignal):
    name = "Min{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerMaxY
class MinXLowerMaxY(EntrySignal):
    name = "Min{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinXLowerAverageY
class MinXLowerAverageY(EntrySignal):
    name = "Min{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Min"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMin) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMin[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherY
class MaxPreviousXHigherY(EntrySignal):
    name = "MaxPrevious{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMinY
class MaxPreviousXHigherMinY(EntrySignal):
    name = "MaxPrevious{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMaxPreviousY
class MaxPreviousXHigherMaxPreviousY(EntrySignal):
    name = "MaxPrevious{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMinPreviousY
class MaxPreviousXHigherMinPreviousY(EntrySignal):
    name = "MaxPrevious{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherMaxY
class MaxPreviousXHigherMaxY(EntrySignal):
    name = "MaxPrevious{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXHigherAverageY
class MaxPreviousXHigherAverageY(EntrySignal):
    name = "MaxPrevious{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerY
class MaxPreviousXLowerY(EntrySignal):
    name = "MaxPrevious{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMinY
class MaxPreviousXLowerMinY(EntrySignal):
    name = "MaxPrevious{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMaxPreviousY
class MaxPreviousXLowerMaxPreviousY(EntrySignal):
    name = "MaxPrevious{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMinPreviousY
class MaxPreviousXLowerMinPreviousY(EntrySignal):
    name = "MaxPrevious{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerMaxY
class MaxPreviousXLowerMaxY(EntrySignal):
    name = "MaxPrevious{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxPreviousXLowerAverageY
class MaxPreviousXLowerAverageY(EntrySignal):
    name = "MaxPrevious{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MaxPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMaxPrevious) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMaxPrevious[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherY
class MinPreviousXHigherY(EntrySignal):
    name = "MinPrevious{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMinY
class MinPreviousXHigherMinY(EntrySignal):
    name = "MinPrevious{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMaxPreviousY
class MinPreviousXHigherMaxPreviousY(EntrySignal):
    name = "MinPrevious{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMinPreviousY
class MinPreviousXHigherMinPreviousY(EntrySignal):
    name = "MinPrevious{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherMaxY
class MinPreviousXHigherMaxY(EntrySignal):
    name = "MinPrevious{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXHigherAverageY
class MinPreviousXHigherAverageY(EntrySignal):
    name = "MinPrevious{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerY
class MinPreviousXLowerY(EntrySignal):
    name = "MinPrevious{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMinY
class MinPreviousXLowerMinY(EntrySignal):
    name = "MinPrevious{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMaxPreviousY
class MinPreviousXLowerMaxPreviousY(EntrySignal):
    name = "MinPrevious{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMinPreviousY
class MinPreviousXLowerMinPreviousY(EntrySignal):
    name = "MinPrevious{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerMaxY
class MinPreviousXLowerMaxY(EntrySignal):
    name = "MinPrevious{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MinPreviousXLowerAverageY
class MinPreviousXLowerAverageY(EntrySignal):
    name = "MinPrevious{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "MinPrevious"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMinPrevious) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMinPrevious[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherY
class MaxXHigherY(EntrySignal):
    name = "Max{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Max"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMinY
class MaxXHigherMinY(EntrySignal):
    name = "Max{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMaxPreviousY
class MaxXHigherMaxPreviousY(EntrySignal):
    name = "Max{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMinPreviousY
class MaxXHigherMinPreviousY(EntrySignal):
    name = "Max{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherMaxY
class MaxXHigherMaxY(EntrySignal):
    name = "Max{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXHigherAverageY
class MaxXHigherAverageY(EntrySignal):
    name = "Max{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerY
class MaxXLowerY(EntrySignal):
    name = "Max{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Max"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMinY
class MaxXLowerMinY(EntrySignal):
    name = "Max{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMaxPreviousY
class MaxXLowerMaxPreviousY(EntrySignal):
    name = "Max{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMinPreviousY
class MaxXLowerMinPreviousY(EntrySignal):
    name = "Max{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerMaxY
class MaxXLowerMaxY(EntrySignal):
    name = "Max{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: MaxXLowerAverageY
class MaxXLowerAverageY(EntrySignal):
    name = "Max{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Max"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xMax) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xMax[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherY
class AverageXHigherY(EntrySignal):
    name = "Average{X}Higher{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Average"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMinY
class AverageXHigherMinY(EntrySignal):
    name = "Average{X}HigherMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMaxPreviousY
class AverageXHigherMaxPreviousY(EntrySignal):
    name = "Average{X}HigherMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMinPreviousY
class AverageXHigherMinPreviousY(EntrySignal):
    name = "Average{X}HigherMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherMaxY
class AverageXHigherMaxY(EntrySignal):
    name = "Average{X}HigherMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXHigherAverageY
class AverageXHigherAverageY(EntrySignal):
    name = "Average{X}HigherAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] > self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerY
class AverageXLowerY(EntrySignal):
    name = "Average{X}Lower{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "OffsetTA"
    funcNameBefore = "Average"
    funcNameAfter = "OffsetTA"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yOffset)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yOffsetTA) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.yOffsetTA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMinY
class AverageXLowerMinY(EntrySignal):
    name = "Average{X}LowerMin{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Min"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMin) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.yMin[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMaxPreviousY
class AverageXLowerMaxPreviousY(EntrySignal):
    name = "Average{X}LowerMaxPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MaxPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMaxPrevious) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.yMaxPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMinPreviousY
class AverageXLowerMinPreviousY(EntrySignal):
    name = "Average{X}LowerMinPrevious{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "MinPrevious"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMinPrevious) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.yMinPrevious[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerMaxY
class AverageXLowerMaxY(EntrySignal):
    name = "Average{X}LowerMax{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Max"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.yMax) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.yMax[self.yDelayForList]:
            return True

        return False

#=======================================================================
#Class: AverageXLowerAverageY
class AverageXLowerAverageY(EntrySignal):
    name = "Average{X}LowerAverage{Y}"
    dataBefore = "X"
    dataAfter = "Y"
    funcTypeBefore = "WindowTA"
    funcTypeAfter = "WindowTA"
    funcNameBefore = "Average"
    funcNameAfter = "Average"

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, xDelay=0, yDelay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.xDelay = xDelay
        self.xDelayForList = (xDelay * -1) - 1

        self.yWindowSize = yWindowSize
        self.yDelay = yDelay
        self.yDelayForList = (yDelay * -1) - 1


        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name
        xLabel = self.xLabel + "("+str(self.xWindowSize)+")"
        if self.xDelay != 0:
            xLabel += "Delay(" + str(self.xDelay) + ")"
        newName = newName.replace("{X}", xLabel)

        yLabel = self.yLabel + "("+str(self.yWindowSize)+")"
        if self.yDelay != 0:
            yLabel += "Delay(" + str(self.yDelay) + ")"
        newName = newName.replace("{Y}", yLabel)

        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if len(self.xSMA) <= self.xDelay:
            return False

        if len(self.ySMA) <= self.yDelay:
            return False

        if self.xSMA[self.xDelayForList] < self.ySMA[self.yDelayForList]:
            return True

        return False

#=======================================================================
#=======================================================================
#=======================================================================
