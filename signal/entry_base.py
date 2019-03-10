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
class LowerX(EntrySignal):
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


# endregion