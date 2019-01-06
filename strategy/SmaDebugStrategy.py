from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities


from ..signal.entry import *
from ..signal.exit import *

class SmaDebugStrategy(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "slowSMA": {"name": "slowSMA", "value": 3, "min": 3, "max": 6, "step": 1},
        "fastSMA": {"name": "fastSMA", "value": 8, "min": 8, "max": 14, "step": 2}
    }

    STRATEGY_NAME = "SMA Strategy For Debug"
    STRATEGY_SLUG = "smaStrategyForDebug"
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



        # Entry signal
        #self.simpleSMACrossSignal = SimpleSMACross(self, self.parameter["slowSMA"]["value"], self.parameter["fastSMA"]["value"], "1T")
        #self.breakPreviousHigh = BreakPreviousHigh(self, -2)
        #self.upBreakPreviousClose = UpBreakPreviousClose(self, -2)
        #self.upBreakPreviousOpen = UpBreakPreviousOpen(self, -2)
        #self.downBreakPreviousOpen = DownBreakPreviousOpen(self, -2)
        #self.rangeChecker = RangeChecker(self, 300)
        self.averageLowHigherAverageClose = AverageLowHigherAverageClose(self, 20, 50)
        #self.averageLowLowerAverageClose = AverageLowLowerAverageClose(self, 20, 50)


        # Exit signal
        #self.trailingStopSignal = TrailingStopWithFixedPrice(self, 100, 45)
        #self.trailingStopCountExitSignal = TrailingStopCountExit(self, 100, 45, 3)

        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)
        #self.dollarTrailingSignal = DollarTrailingStop(self, self.dollarTrailing)
