from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal.entry import *
from ..signal.exit import *

class AverageHighBreakDayHigh(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "slowSMA": {"name": "slowSMA", "value": 3, "min": 3, "max": 6, "step": 1},
        "fastSMA": {"name": "fastSMA", "value": 8, "min": 8, "max": 14, "step": 2},
        "entrySignal": {"name": "entrySignal", "value": 1, "min": 1, "max": 25, "step": 1}
    }

    STRATEGY_NAME = "Average High Break Day High"
    STRATEGY_SLUG = "AverageHighBreakDayHigh"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2018-10-18"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        #self.action = OrderAction.SELL
        self.tradeLimit = 1
        self.tradingAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        #self.rangeFilter = self.rangeFunction_6 = PreviousDayHighLowRange(session, 1, 0.2)


        # Entry signal
        if self.parameter["entrySignal"]["value"] == 1:
            self.longSignal_1 = XHigherY(self, "close", 0, "highD", 1)

        elif self.parameter["entrySignal"]["value"] == 2:
            self.longSignal_2  = XHigherY(self, "close", 0, "highD", 2)

        elif self.parameter["entrySignal"]["value"] == 3:
            self.longSignal_3  = XLowerY(self, "close", 0, "lowD", 1)

        elif self.parameter["entrySignal"]["value"] == 4:
            self.longSignal_4  = XLowerY(self, "close", 0, "lowD", 2)

        elif self.parameter["entrySignal"]["value"] == 5:
            self.longSignal_5  = XHigherY(self, "close", 0, "openD", 0)

        elif self.parameter["entrySignal"]["value"] == 6:
            self.rangeFilter = self.rangeFunction_6 = PreviousDayHighLowRange(session, 1, 0.5)
            self.longSignal_6 = XHigherYWithRange(self, "close", 0, "openD", 0, 0.5)

        elif self.parameter["entrySignal"]["value"] == 7:
            self.longSignal_7  = XHigherY(self, "close", 0, "close", 1)

        elif self.parameter["entrySignal"]["value"] == 8:
            self.longSignal_8  = XHigherMaxYZ(self, "close", 0, "closeD", 1, "highD", 2)

        elif self.parameter["entrySignal"]["value"] == 9:
            self.longSignal_9  = AverageXHigherY(self, "low", 3, "highD", 1)

        elif self.parameter["entrySignal"]["value"] == 10:
            self.longSignal_10 = XHigherAverageY(self, "openD", 0, "high", 200)

        elif self.parameter["entrySignal"]["value"] == 11:
            self.longSignal_11 = AverageXHigherAverageY(self, "low", 2, "high", 50)

        elif self.parameter["entrySignal"]["value"] == 12:
            self.longSignal_12 = AverageXHigherAverageY(self, "low", 20, "close", 50)

        elif self.parameter["entrySignal"]["value"] == 13:
            self.longSignal_13 = XHigherY(self, "low", 0, "high", 1)

        elif self.parameter["entrySignal"]["value"] == 14:
            self.longSignal_14 = XHigherY(self, "lowD", 0, "closeD", 2)

        elif self.parameter["entrySignal"]["value"] == 15:
            self.longSignal_15 = AverageXHigherMaxYZ(self, "high", 40, "closeD", 1, "openD", 1)

        elif self.parameter["entrySignal"]["value"] == 16:
            self.longSignal_16 = AverageXHigherY(self, "high", 50, "highD", 1)

        elif self.parameter["entrySignal"]["value"] == 17:
            self.longSignal_17 = AverageXLowerY(self, "low", 50, "lowD", 1)

        elif self.parameter["entrySignal"]["value"] == 18:
            self.longSignal_20 = XLowerMinY(self, "low", 0, "low", 100)

        elif self.parameter["entrySignal"]["value"] == 19:
            self.longSignal_21 = XHigherY(self, "high", 0, "high", 1)

        elif self.parameter["entrySignal"]["value"] == 20:
            self.longSignal_22 = XLowerY(self, "low", 0, "low", 1)

        elif self.parameter["entrySignal"]["value"] == 21:
            self.longSignal_23 = XHigherY(self, "close", 0, "open", 0)

        elif self.parameter["entrySignal"]["value"] == 22:
            self.longSignal_24 = XHigherY(self, "high", 0, "highD", 0)

        elif self.parameter["entrySignal"]["value"] == 23:
            self.longSignal_25 = XHigherMaxY(self, "high", 0, "highD", 5)

        elif self.parameter["entrySignal"]["value"] == 24:
            self.longSignal_26 = XHigherMaxY(self, "high", 0, "high", 100)

        elif self.parameter["entrySignal"]["value"] == 25:
            self.rangeFilter = self.rangeFunction_6 = PreviousDayHighLowRange(session, 1, 0.5)
            self.longSignal_27 = XYDiffLargerRange(self, "highD", 0, "lowD", 0)


        #self.longSignal_1  = XHigherY(self, "close", 0, "highD", 1)
        #self.longSignal_2  = XHigherY(self, "close", 0, "highD", 2)
        #self.longSignal_3  = XLowerY(self, "close", 0, "lowD", 1)
        #self.longSignal_4  = XHigherY(self, "close", 0, "lowD", 2)
        #self.longSignal_5  = XHigherY(self, "close", 0, "openD", 0)


        #self.longSignal_6  = XHigherYWithRange(self, "close", 0, "openD", 0, 0.5)
        # 6  close > opend(0) + rng/2;

        #self.longSignal_7  = XHigherY(self, "close", 0, "close", 1)
        #self.longSignal_8  = XHigherMaxYZ(self, "close", 0, "closeD", 1, "highD", 2)
        #self.longSignal_9  = AverageXHigherY(self, "low", 3, "highD", 1)
        #self.longSignal_10 = XHigherAverageY(self, "openD", 0, "high", 200)

        #self.longSignal_11 = AverageXHigherAverageY(self, "low", 2, "high", 50)
        #self.longSignal_12 = AverageXHigherAverageY(self, "low", 20, "close", 50)
        #self.longSignal_13 = XHigherY(self, "low", 0, "high", 1)
        #self.longSignal_14 = XHigherY(self, "lowD", 0, "closeD", 2)
        #self.longSignal_15 = AverageXHigherMaxYZ(self, "high", 40, "closeD", 1, "openD", 1)

        #self.longSignal_16 = AverageXHigherY(self, "high", 50, "highD", 1)
        #self.longSignal_17 = AverageXLowerY(self, "low", 50, "lowD", 1)

        #self.longSignal_18 = MinXYLowerAverageXMinusATR(self, "closeD", 1, "openD", 1, "low", 100, 100)
        #self.longSignal_19 = XHigherYWithRangeAndATR(self, "high", 0, "openD", 0, 0.34, 50, 4.0)

        # 18 minlist(closed(1),opend(1)) < average(low,100) - averagetruerange(100);
        # 19 high > opend(0) + rng/3 + averagetruerange(50)*4;

        #self.longSignal_20 = XLowerMinY(self, "low", 0, "low", 100)
        #self.longSignal_21 = XHigherY(self, "high", 0, "high", 1)
        #self.longSignal_22 = XLowerY(self, "low", 0, "low", 1)
        #self.longSignal_23 = XHigherY(self, "close", 0, "open", 0)
        #self.longSignal_24 = XHigherY(self, "high", 0, "highD", 0)
        #self.longSignal_25 = XHigherMaxY(self, "high", 0, "highD", 5)
        #self.longSignal_26 = XHigherMaxY(self, "high", 0, "high", 100)
        #self.longSignal_27 = XYDiffLargerRange(self, "highD", 0, "lowD", 0)


        # Exit signal
        #self.trailingStopSignal = TrailingStopWithFixedPrice(self, 100, 45)
        #self.trailingStopCountExitSignal = TrailingStopCountExit(self, 100, 45, 3)

        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)
        self.dollarTrailingSignal = DollarTrailingStop(self, self.dollarTrailing)
