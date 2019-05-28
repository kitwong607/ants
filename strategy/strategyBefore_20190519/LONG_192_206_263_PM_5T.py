from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ants.session import SessionMode

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LONG_192_206_263_PM_5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
    }

    STRATEGY_NAME = "LONG_192_206_263_PM_5T"
    STRATEGY_SLUG = "LONG_192_206_263_PM_5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190422"
    LAST_UPDATE_TIME = "072525"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 123000, "END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]


        #Entry Signal
        #192
        signal = entry.XHigherY(self, "closeD", 3, "closeD", 4)
        #206
        signal = entry.HigherX(self, "low", 15)
        #263
        signal = entry.XHigherY(self, "close", 0, "morningHighD", 0, 4)
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
                if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label()+"]: True")
                elif self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
                    self.Log("Entry signal["+str(self.session.config.sid)+"-"+signal.Label() + "]: False")

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)
