from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class DebugSignalTester(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    NUM_SIGNAL = 253
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1}
    }

    STRATEGY_NAME = "Debug Signal Tester"
    STRATEGY_SLUG = "DebugSignalTester"
    VERSION = "97"
    LAST_UPDATE_DATE = "20190207"
    LAST_UPDATE_TIME = "153230"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        fastWindowSize = 5
        slowWindowSize = 3
        signalWindowSize = 3
        #signal = entry.StochasticSlowKHigherD(self, "close", fastWindowSize, slowWindowSize, signalWindowSize)
        #signal = entry.StochasticSlowHigherThreshold(self, "close", fastWindowSize, fastWindowSize, slowWindowSize, 80)
        #signal = entry.XLowerKAMA(self, "close", 10)
        #signal = entry.StochasticRSIKLowerD(self, "close", 14, fastWindowSize, slowWindowSize)
        #signal = entry.XInBBandsUpper(self, "close", 20, 2)
        #signal = entry.WiderBBands(self, "close", 20, 2, 6, 1.5)
        #signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
        #signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 4)
        #signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 6, 20, 6)
        signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 20)


        self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss)
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
        self.dollarTrailingSignal = exit.DollarTrailingStop(self, self.dollarTrailing)
        self.fixedStopGain = exit.FixedStopGain(self, self.stopLoss * 3)
        self.dayRangeTouch = exit.DayRangeTouch(self, 400)




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

