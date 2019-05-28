from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ..session import SessionMode

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class SHORT_402_248_620_APM_5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    '''
    '''

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
    }

    STRATEGY_NAME = "SHORT_402_248_620_APM_5T"
    STRATEGY_SLUG = "SHORT_402_248_620_APM_5T"
    VERSION = "97"
    LAST_UPDATE_DATE = "20190519"
    LAST_UPDATE_TIME = "132554"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.SELL
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]


        #Entry Signal
        #248
        signal = entry.XLowerMinPreviousY(self, "close", 0, "high", 24, 6, 6)
        #402
        signal = entry.HigherX(self, "high", 3, 6)
        #620
        signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
        signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 2)

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
