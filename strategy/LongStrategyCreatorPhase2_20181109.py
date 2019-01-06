from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal.entry import *
from ..signal.exit import *

class LongStrategyCreatorPhase2_20181109(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 2, "min": 1, "max": 9, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 9, "min": 1, "max": 9, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": -1, "min": 1, "max": 9, "step": 1}
    }

    STRATEGY_NAME = "LongStrategyCreatorPhase2_20181109"
    STRATEGY_SLUG = "LongStrategyCreatorPhase2_20181109"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2018-11-09"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.tradingAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        signalNo1 = self.parameter["signalId_1"]["value"]
        signalNo2 = self.parameter["signalId_2"]["value"]
        signalNo3 = self.parameter["signalId_3"]["value"]

        self.SetupSignal(signalNo1)

        if signalNo2 != -1:
            self.SetupSignal(signalNo2)
            if signalNo3 != -1:
                self.SetupSignal(signalNo3)

        # Exit signal
        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)
        self.dollarTrailingSignal = DollarTrailingStop(self, self.dollarTrailing)


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
            self.Entry(bar, OrderType.MARKET, label, self.baseQuantity)


    def SetupSignal(self, signalId):
        # Entry signal
        #higher or lower previous(1) day OHLC
        if signalId == 1:
            signal = XHigherY(self, "close", 0, "highD", 1)
        if signalId == 2:
            signal = XHigherY(self, "close", 0, "closeD", 1)

        #higher or lower previous(2) day OHLC
        elif signalId == 3:
            signal = XHigherY(self, "close", 0, "openD", 2)
        elif signalId == 4:
            signal = XHigherY(self, "close", 0, "highD", 2)

        #average(50) close higher or lower previous(1) bar OHLC
        elif signalId == 5:
            signal = AverageXHigherY(self, "close", 50, "closeD", 1)


        #average(50) close higher or lower previous(2) bar OHLC
        elif signalId == 6:
            signal = AverageXHigherY(self, "close", 50, "highD", 2)

        #average close(50) higher and lower then Max of week OHLC
        elif signalId == 7:
            signal = AverageXHigherMaxY(self, "close", 50, "openD", 5)
        elif signalId == 8:
            signal = AverageXHigherMaxY(self, "close", 50, "closeD", 5)