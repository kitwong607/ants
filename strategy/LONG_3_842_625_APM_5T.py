from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ..session import SessionMode

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LONG_3_842_625_APM_5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10}
    }

    STRATEGY_NAME = "LONG_3_842_625_APM_5T"
    STRATEGY_SLUG = "LONG_3_842_625_APM_5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190524"
    LAST_UPDATE_TIME = "073538"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000, "END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]


        #Entry Signal
        #3
        signal = entry.XHigherY(self, "close", 0, "highD", 3)
        #625
        signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
        signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 4)
        #842
        signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 160)

        # Exit signal
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
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
                if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label()+"]: True")
            else:
                if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label() + "]: False")

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)
