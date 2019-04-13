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


# region Higher X Lower X comparsion
#Class: HigherX
class HigherX(EntrySignal):
    name = "Higher{X}"

    def __init__(self, strategy, x="open", xWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize

        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})


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
class LowerX(EntrySignal):
    name = "Lower{X}"

    def __init__(self, strategy, x="open", xWindowSize=0):
        super().__init__(strategy)

        self.xLabel = x
        self.xWindowSize = xWindowSize

        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})


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
class XHigherPivotPoint(EntrySignal):
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
class XLowerPivotPoint(EntrySignal):
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
class XHigherPivotPointS1(EntrySignal):
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
class XLowerPivotPointS1(EntrySignal):
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
class XHigherPivotPointR1(EntrySignal):
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
class XLowerPivotPointR1(EntrySignal):
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
class XHigherPivotPointS2(EntrySignal):
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
class XLowerPivotPointS2(EntrySignal):
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
class XHigherPivotPointR2(EntrySignal):
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
class XLowerPivotPointR2(EntrySignal):
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
class XHigherPivotPointS3(EntrySignal):
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
class XLowerPivotPointS3(EntrySignal):
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
class XHigherPivotPointR3(EntrySignal):
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
class XLowerPivotPointR3(EntrySignal):
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
class CrossUpPivotPoint(EntrySignal):
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
class CrossDownPivotPoint(EntrySignal):
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
class CrossUpPivotPointR1(EntrySignal):
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
class CrossDownPivotPointR1(EntrySignal):
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
class CrossUpPivotPointS1(EntrySignal):
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
class CrossDownPivotPointS1(EntrySignal):
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
class CrossUpPivotPointR2(EntrySignal):
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
class CrossDownPivotPointR2(EntrySignal):
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
class CrossUpPivotPointS2(EntrySignal):
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
class CrossDownPivotPointS2(EntrySignal):
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
class CrossUpPivotPointR3(EntrySignal):
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
class CrossDownPivotPointR3(EntrySignal):
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
class CrossUpPivotPointS3(EntrySignal):
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
class CrossDownPivotPointS3(EntrySignal):
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

# region KAMA related
#Class: XHigherKAMA
class XHigherKAMA(EntrySignal):
    name = "{X}HigherKAMA{WINDOWSIZE}"

    def __init__(self, strategy, x="close", windowSize=30, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1


        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName':x, 'windowSize': windowSize})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.delay] > self.kama[self.delay]:
            return True
        return False



#Class: XLowerKAMA
class XLowerKAMA(EntrySignal):
    name = "{X}LowerKAMA{WINDOWSIZE}"

    def __init__(self, strategy, x="close", windowSize=30, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import KAMA
        self.kama = self.AddTA(KAMA, {'dataName':x, 'windowSize': windowSize})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel) ).replace("{WINDOWSIZE}", str(self.windowSize) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kama.isReady:
            return False

        if self.data[self.delay] < self.kama[self.delay]:
            return True
        return False


# endregion

# region BBands related
#Class: XHigherBBandsUpper
class XHigherBBandsUpper(EntrySignal):
    name = "{X}HigherBBandsUpper{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.delay] > self.bbandsUpper[self.delay]:
            return True
        return False


#Class: XHigherBBandsMiddle
class XHigherBBandsMiddle(EntrySignal):
    name = "{X}HigherBBandsMiddle{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.delay] > self.bbandsMiddle[self.delay]:
            return True
        return False


#Class: XHigherBBandsLower
class XHigherBBandsLower(EntrySignal):
    name = "{X}HigherBBandsLower{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsLower
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsLower.isReady:
            return False

        if self.data[self.delay] > self.bbandsLower[self.delay]:
            return True
        return False



#Class: XLowerBBandsUpper
class XLowerBBandsUpper(EntrySignal):
    name = "{X}LowerBBandsUpper{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.delay] < self.bbandsUpper[self.delay]:
            return True
        return False


#Class: XLowerBBandsMiddle
class XLowerBBandsMiddle(EntrySignal):
    name = "{X}LowerBBandsMiddle{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.delay] < self.bbandsMiddle[self.delay]:
            return True
        return False


#Class: XLowerBBandsLower
class XLowerBBandsLower(EntrySignal):
    name = "{X}LowerBBandsLower{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsLower
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsLower.isReady:
            return False

        if self.data[self.delay] < self.bbandsLower[self.delay]:
            return True
        return False



class XInBBandsUpper(EntrySignal):
    name = "{X}InBBandsUpper{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsUpper, BBandsMiddle
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if self.data[self.delay] < self.bbandsUpper[self.delay] and self.data[self.delay] > self.bbandsMiddle[self.delay]:
            return True
        return False



class XInBBandsLower(EntrySignal):
    name = "{X}InBBandsLower{WINDOWSIZE}-{NBDEV}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1

        from ..ta.OverlapTA import BBandsLower, BBandsMiddle
        self.bbandsMiddle = self.AddTA(BBandsMiddle, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.bbandsMiddle.isReady:
            return False

        if self.data[self.delay] < self.bbandsMiddle[self.delay] and self.data[self.delay] > self.bbandsLower[self.delay]:
            return True
        return False


class NarrowerBBands(EntrySignal):
    name = "NarrowerBBands{WINDOWSIZE}-{NBDEV}-{COMPAREWINDOWSIZE}-{ratio}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, compareWindowSize=6, ratio=0.9, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1
        self.compareWindowSize = compareWindowSize
        self.ratio = ratio

        from ..ta.OverlapTA import BBandsLower, BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) ).replace("{COMPAREWINDOWSIZE}", str(self.compareWindowSize) ).replace("{RATIO}", str(self.ratio) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName

    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if len(self.bbandsUpper) <= (self.delay - self.compareWindowSize) * -1:
            return False

        upper1 = self.bbandsUpper[self.delay - self.compareWindowSize]
        lower1 = self.bbandsLower[self.delay - self.compareWindowSize]
        diff1 = upper1 - lower1

        upper2 = self.bbandsUpper[self.delay]
        lower2 = self.bbandsLower[self.delay]
        diff2 = upper2 - lower2

        if diff2 < diff1*self.ratio:
            return True
        return False

class WiderBBands(EntrySignal):
    name = "WiderBBands{WINDOWSIZE}-{NBDEV}-{COMPAREWINDOWSIZE}-{RATIO}"

    def __init__(self, strategy, x="close", windowSize=20, nbdev=2, compareWindowSize=6, ratio=1.1, delay=0):
        super().__init__(strategy)

        self.xLabel = x
        self.windowSize = windowSize
        self.nbdev = nbdev

        self.data = utilities.GetDataByName(strategy, x)
        self.delay = (delay * -1) - 1
        self.compareWindowSize = compareWindowSize
        self.ratio = ratio

        from ..ta.OverlapTA import BBandsLower, BBandsUpper
        self.bbandsUpper = self.AddTA(BBandsUpper, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})
        self.bbandsLower = self.AddTA(BBandsLower, {'dataName':x, 'windowSize': windowSize, 'nbdev': nbdev})


    def Label(self):
        newName = self.name.replace("{X}", str(self.xLabel)).replace("{WINDOWSIZE}", str(self.windowSize) ).replace("{NBDEV}", str(self.nbdev) ).replace("{COMPAREWINDOWSIZE}", str(self.compareWindowSize) ).replace("{RATIO}", str(self.ratio) )
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName

    def CalculateSignal(self, bar):
        if not self.bbandsUpper.isReady:
            return False

        if len(self.bbandsUpper) <= (self.delay - self.compareWindowSize) * -1:
            return False

        upper1 = self.bbandsUpper[self.delay - self.compareWindowSize]
        lower1 = self.bbandsLower[self.delay - self.compareWindowSize]
        diff1 = upper1 - lower1

        upper2 = self.bbandsUpper[self.delay]
        lower2 = self.bbandsLower[self.delay]
        diff2 = upper2 - lower2

        if diff2 > diff1*self.ratio:
            return True
        return False
# endregion

# region RSI related
#Class: MaxRSIHigherThreshold
class MaxRSIHigherThreshold(EntrySignal):
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
class MinRSIHigherThreshold(EntrySignal):
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
class MaxRSILowerThreshold(EntrySignal):
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
class MinRSILowerThreshold(EntrySignal):
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

#Class: MinRSIHigherThreshold
class MinRSIHigherThreshold(EntrySignal):
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
class MaxRSILowerThreshold(EntrySignal):
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
class MinRSILowerThreshold(EntrySignal):
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

# region MACD related
#Class: MACDSignalHigherMACD
class MACDHigherMACDSignal(EntrySignal):
    name = "MACDHigherMACDSignal"

    def __init__(self, strategy, x="close", fastWindowSize=12, slowWindowSize=26, signalWindowSize=9, delay=0):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.fastWindowSize = fastWindowSize
        self.slowWindowSize = slowWindowSize
        self.signalWindowSize = signalWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastWindowSize) + "-" + str(self.slowWindowSize) + "-" + str(
            self.signalWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.macd.isReady:
            return False

        if self.macd[self.delay] > self.macdSignalLine[self.delay]:
            return True
        return False


#Class: MACDLowerMACDSignal
class MACDLowerMACDSignal(EntrySignal):
    name = "MACDLowerMACDSignal"

    def __init__(self, strategy, x="close", fastWindowSize=12, slowWindowSize=26, signalWindowSize=9, delay=0):
        super().__init__(strategy)
        if(x!="close"): x = "closeD"

        self.xLabel = x
        self.fastWindowSize = fastWindowSize
        self.slowWindowSize = slowWindowSize
        self.signalWindowSize = signalWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastWindowSize) + "-" + str(self.slowWindowSize) + "-" + str(
            self.signalWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.macd.isReady:
            return False

        if self.macd[self.delay] < self.macdSignalLine[self.delay]:
            return True
        return False




#Class: MinRSIHigherThreshold
class MinRSIHigherThreshold(EntrySignal):
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
class MaxRSILowerThreshold(EntrySignal):
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
class MinRSILowerThreshold(EntrySignal):
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

# region Stochastic related
#Class: StochasticSlowKHigherD
class StochasticSlowKHigherD(EntrySignal):
    name = "StochasticSlowKHigherD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowKHigherD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.slowKWindowSize) + "-" + str(
            self.slowDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.dLine[self.delay]:
            return True
        return False


#Class: StochasticSlowKLowerD
class StochasticSlowKLowerD(EntrySignal):
    name = "StochasticSlowKLowerD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowKLowerD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.slowKWindowSize) + "-" + str(
            self.slowDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.dLine[self.delay]:
            return True
        return False


#Class: StochasticFastKHigherD
class StochasticFastKHigherD(EntrySignal):
    name = "StochasticFastKHigherD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastKHigherD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.dLine[self.delay]:
            return True
        return False


#Class: StochasticFastKLowerD
class StochasticFastKLowerD(EntrySignal):
    name = "StochasticFastKLowerD"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastKLowerD: only support close and closeD as data")

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.dLine[self.delay]:
            return True
        return False


#Class: StochasticRSIKHigherD
class StochasticRSIKHigherD(EntrySignal):
    name = "StochasticRSIKHigherD"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIKHigherD: only support close and closeD as data")

        self.xLabel = ""
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.rsiWindowSize) + "-" +  str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.dLine[self.delay]:
            return True
        return False


#Class: StochasticRSIKLowerD
class StochasticRSIKLowerD(EntrySignal):
    name = "StochasticRSIKLowerD"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIKLowerD: only support close and closeD as data")

        self.xLabel = ""
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.dLine[self.delay]:
            return True
        return False



#Class: StochasticSlowHigherThreshold
class StochasticSlowHigherThreshold(EntrySignal):
    name = "StochasticSlowHigherThreshold"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, threshold=80, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.slowKWindowSize) + "-" + str(
            self.slowDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.threshold and self.dLine[self.delay] > self.threshold:
            return True
        return False


#Class: StochasticSlowLowerThreshold
class StochasticSlowLowerThreshold(EntrySignal):
    name = "StochasticSlowLowerThreshold"

    def __init__(self, strategy, x="close", fastKWindowSize=5, slowKWindowSize=3, slowDWindowSize=9, threshold=20, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticSlowLowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.slowKWindowSize = slowKWindowSize
        self.slowDWindowSize = slowDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.slowKWindowSize) + "-" + str(
            self.slowDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.threshold and self.dLine[self.delay] < self.threshold:
            return True
        return False


#Class: StochasticFastHigherThreshold
class StochasticFastHigherThreshold(EntrySignal):
    name = "StochasticFastHigherThreshold"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, threshold=80, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.threshold and self.dLine[self.delay] > self.threshold:
            return True
        return False


#Class: StochasticFastLowerThreshold
class StochasticFastLowerThreshold(EntrySignal):
    name = "StochasticFastLowerThreshold"

    def __init__(self, strategy, x="close", fastKWindowSize=5, fastDWindowSize=3, threshold=20, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticFastLowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MomentumTA import StochasticFastK, StochasticFastD
        params = {
            "dataName": x,
            "fastKWindowSize": fastKWindowSize,
            "fastDWindowSize": fastDWindowSize
        }
        self.kLine = self.AddTA(StochasticFastK, params)
        self.dLine = self.AddTA(StochasticFastD, params)


    def Label(self):
        newName = self.name + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.threshold and self.dLine[self.delay] < self.threshold:
            return True
        return False


#Class: StochasticRSIHigherThreshold
class StochasticRSIHigherThreshold(EntrySignal):
    name = "StochasticRSIHigherThreshold"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, threshold=80, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSIHigherThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.rsiWindowSize) + "-" +  str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] > self.threshold and self.dLine[self.delay] > self.threshold:
            return True
        return False


#Class: StochasticRSILowerThreshold
class StochasticRSILowerThreshold(EntrySignal):
    name = "StochasticRSILowerThreshold"

    def __init__(self, strategy, x="close", rsiWindowSize=14, fastKWindowSize=5, fastDWindowSize=3, threshold=20, delay=0):
        super().__init__(strategy)
        if(x!="close" and x!="closeD"):
            raise ValueError("StochasticRSILowerThreshold: only support close and closeD as data")

        self.threshold = threshold

        self.xLabel = ""
        self.rsiWindowSize = rsiWindowSize
        self.fastKWindowSize = fastKWindowSize
        self.fastDWindowSize = fastDWindowSize
        self.delay = (delay * -1) - 1

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
        newName = self.name + "_" + str(self.rsiWindowSize) + "_" + str(self.fastKWindowSize) + "-" + str(self.fastDWindowSize) + "-" + str(self.threshold)
        if self.delay != -1:
            newName += "_delay-" + str(self.delay)
        return newName


    def CalculateSignal(self, bar):
        if not self.kLine.isReady:
            return False

        if self.kLine[self.delay] < self.threshold and self.dLine[self.delay] < self.threshold:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xOffsetTA[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MinX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MinPreviousX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.MinMax import MaxX
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xOffset=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xOffset = xOffset
        self.xOffsetForList = (xOffset * -1) - 1
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.base import OffsetTA
        from..ta.SMA import SMA
        self.xOffsetTA = self.AddTA(OffsetTA, {'dataName':x, 'offset': xOffset})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xOffset) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xOffsetTA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xOffsetTA[self.delay] < self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMin[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMin[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMin[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMin[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMin[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMin[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.base import OffsetTA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMin[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMin[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMin[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MinPreviousX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMin[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.MinMax import MaxX
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMin[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinX
        from..ta.SMA import SMA
        self.xMin = self.AddTA(MinX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMin.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMin[self.delay] < self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMaxPrevious[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.base import OffsetTA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MinPreviousX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.MinMax import MaxX
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxPreviousX
        from..ta.SMA import SMA
        self.xMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMaxPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMaxPrevious[self.delay] < self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMinPrevious[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.base import OffsetTA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MinX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.MinMax import MaxX
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MinPreviousX
        from..ta.SMA import SMA
        self.xMinPrevious = self.AddTA(MinPreviousX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMinPrevious.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMinPrevious[self.delay] < self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMax[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMax[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMax[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMax[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMax[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMax[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.base import OffsetTA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xMax[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xMax[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MaxPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xMax[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.MinMax import MinPreviousX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xMax[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xMax[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.MinMax import MaxX
        from..ta.SMA import SMA
        self.xMax = self.AddTA(MaxX, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xMax.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xMax[self.delay] < self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[self.delay] > self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xSMA[self.delay] > self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xSMA[self.delay] > self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xSMA[self.delay] > self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xSMA[self.delay] > self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xSMA[self.delay] > self.ySMA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yOffset=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yOffset = yOffset
        self.yOffsetForList = (yOffset * -1) - 1
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.base import OffsetTA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yOffsetTA = self.AddTA(OffsetTA, {'dataName':y, 'offset': yOffset})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yOffset) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yOffsetTA.isReady:
            return False

        if self.xSMA[self.delay] < self.yOffsetTA[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MinX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMin = self.AddTA(MinX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMin.isReady:
            return False

        if self.xSMA[self.delay] < self.yMin[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MaxPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMaxPrevious = self.AddTA(MaxPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMaxPrevious.isReady:
            return False

        if self.xSMA[self.delay] < self.yMaxPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MinPreviousX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMinPrevious = self.AddTA(MinPreviousX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMinPrevious.isReady:
            return False

        if self.xSMA[self.delay] < self.yMinPrevious[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        from..ta.MinMax import MaxX
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.yMax = self.AddTA(MaxX, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.yMax.isReady:
            return False

        if self.xSMA[self.delay] < self.yMax[self.delay]:
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

    def __init__(self, strategy, x="open", xWindowSize=0, y="open", yWindowSize=0, delay = 0):
        super().__init__(strategy)

        self.xLabel = x
        self.yLabel = y

        self.xWindowSize = xWindowSize
        self.yWindowSize = yWindowSize
        self.delay = (delay * -1) - 1

        from..ta.SMA import SMA
        self.xSMA = self.AddTA(SMA, {'dataName':x, 'windowSize': xWindowSize})
        self.ySMA = self.AddTA(SMA, {'dataName':y, 'windowSize': yWindowSize})


    def Label(self):
        newName = self.name.replace("{X}", self.xLabel + "(" + str(self.xWindowSize) + ")").replace("{Y}", self.yLabel + "(" + str(self.yWindowSize) + ")")
        if self.delay!=-1:
            newName += 'Delay('+str((self.delay+1)*-1)+')'
        return newName


    def CalculateSignal(self, bar):
        if not self.xSMA.isReady:
            return False

        if not self.ySMA.isReady:
            return False

        if self.xSMA[self.delay] < self.ySMA[self.delay]:
            return True

        return False

#=======================================================================
#=======================================================================
#=======================================================================
