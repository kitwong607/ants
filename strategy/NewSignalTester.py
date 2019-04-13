from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal.entry import *
from ..signal.exit import *

class NewSignalTester(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10}
    }

    STRATEGY_NAME = "New Signal Tester"
    STRATEGY_SLUG = "NewSignalTester"
    VERSION = "BETA"
    LAST_UPDATE_DATE = "20190101"
    LAST_UPDATE_TIME = "000000"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30
        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        # Exit signal
        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)
        self.dollarTrailingSignal = DollarTrailingStop(self, self.dollarTrailing)

        #signal = CrossUpPivotPoint(self, 1)
        #signal = CrossDownPivotPoint(self, 1)

        #signal = CrossUpPivotPointS1(self, 1)
        #signal = CrossDownPivotPointS1(self, 1)
        #signal = CrossUpPivotPointR1(self, 1)
        #signal = CrossDownPivotPointR1(self, 1)

        #signal = CrossUpPivotPointS2(self, 1)
        #signal = CrossDownPivotPointS2(self, 1)
        #signal = CrossUpPivotPointR2(self, 1)
        #signal = CrossDownPivotPointR2(self, 1)

        #signal = CrossUpPivotPointS3(self, 1)
        #signal = CrossDownPivotPointS3(self, 1)
        #signal = CrossUpPivotPointR3(self, 1)
        #signal = CrossDownPivotPointR3(self, 1)

        #signal = XHigherPivotPoint(self, "openD", 0, 1)
        #signal = XLowerPivotPoint(self, "openD", 0, 1)

        #signal = XHigherPivotPointS1(self, "openD", 0, 1)
        #signal = XLowerPivotPointS1(self, "openD", 0, 1)
        #signal = XHigherPivotPointR1(self, "openD", 0, 1)
        #signal = XLowerPivotPointR1(self, "openD", 0, 1)

        #signal = XHigherPivotPointS2(self, "openD", 0, 1)
        #signal = XLowerPivotPointS2(self, "openD", 0, 1)
        #signal = XHigherPivotPointR2(self, "openD", 0, 1)
        #signal = XLowerPivotPointR2(self, "openD", 0, 1)

        #signal = XHigherPivotPointS3(self, "openD", 0, 1)
        #signal = XLowerPivotPointS3(self, "openD", 0, 1)
        #signal = XHigherPivotPointR3(self, "openD", 0, 1)
        #signal = XLowerPivotPointR3(self, "openD", 0, 1)

        #signal = MaxRSIHigherThreshold(self, "close", 14, 14, 80)
        #signal = MinRSIHigherThreshold(self, "close", 14, 14, 80)
        #signal = MaxRSILowerThreshold(self, "close", 14, 14, 25)
        #signal = MinRSILowerThreshold(self, "close", 14, 14, 25)





    def CalculateEntrySignal(self, bar):
        count = 0
        label = ""
        for signal in self.entrySignals:
            if signal.CalculateSignal(bar):
                count += 1
                if label != "":
                    label += " "
                label += signal.Label()

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)


