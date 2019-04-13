from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
#from ..ta import SMA

from ..signal.entry import FirstBarAfter
from ..signal.exit import StopLossWithFixedPrice

class SimpleDebugStrategy(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []


    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 60, "min": 60, "max": 120, "step": 10 }
    }

    STRATEGY_NAME = "Basic Strategy For Debug"
    STRATEGY_SLUG = "basicStrategyForDebug"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2018-09-28"


    def __init__(self):
        pass



    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.tradingAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.entrySignal = FirstBarAfter(self, 11, 0, 0)
        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)


    def CalculateEntrySignal(self, bar):
        if self.entrySignal.CalculateSignal(bar):
            label = 'long entry (sl:' + str(self.stopLoss) + ')'
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)


    def CalculateExitSignal(self, bar):
        if self.stopLossSignal.CalculateSignal(bar):
            label = 'stopLoss'
            self.Exit(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)