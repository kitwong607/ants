from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ..session import SessionMode

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LONG_3_266_186_APM_5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 40, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
    }

    STRATEGY_NAME = "LONG_3_266_186_APM_5T"
    STRATEGY_SLUG = "LONG_3_266_186_APM_5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190423"
    LAST_UPDATE_TIME = "132946"

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
        #186
        signal = entry.XHigherY(self, "lowD", 2, "lowD", 3)
        #266
        signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0, 6)

        # Exit signal
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
        #self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss * 1.5)
        #self.dollarTrailingSignal = exit.DollarTrailingStop(self, self.dollarTrailing)
        self.fixedStopGain = exit.FixedStopGain(self, self.stopLoss*1.5)


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