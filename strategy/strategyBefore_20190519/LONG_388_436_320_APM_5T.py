from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ..session import SessionMode


from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LONG_388_436_320_APM_5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10}
    }

    STRATEGY_NAME = "LONG_388_436_320_APM_5T"
    STRATEGY_SLUG = "LONG_388_436_320_APM_5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190413"
    LAST_UPDATE_TIME = "090000"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000, "END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        #Entry signal
        #388
        signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 80)
        #436
        signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 80)
        #320
        signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
        signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 2)



        # Exit signal
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
        #self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss * 1.5)
        self.dollarTrailingSignal = exit.DollarTrailingStop(self, self.dollarTrailing)


    def CalculateEntrySignal(self, bar):
        count = 0
        label = ""
        for signal in self.entrySignals:
            if signal.CalculateSignal(bar):
                count += 1
                if label != "":
                    label += " "
                label += signal.Label()
                self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label()+"]: True")
            else:
                self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label() + "]: False")

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)
