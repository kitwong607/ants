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
        "stopLoss": {"name": "stopLoss", "value": 60, "min": 60, "max": 120, "step": 10 },
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
        #signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 20)

        #signal = entry.XHigherY(self, "close", 0, "highD", 1)
        #signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 80)

        #signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 200)
        #signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, -80)
        #signal = entry.XYRangeLargerThresold(self, "highD", 0, "lowD", 0, 200)
        #signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 150)
        #signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 250)

        '''
        signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 0)
        signal = entry.XHigherKAMA(self, "openD", 0, 30)
        #signal = entry.XHigherY(self, "openD", 0, "closeD", 1)
        #signal = entry.XHigherY(self, "close", 0, "openD", 0)
        signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 300)
        '''

        #signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 0)
        #signal = entry.ATRHigherMaxPrevious(self, "close", 14, 7, 0)
        #signal = entry.XHigherKAMA(self, "close", 0, 12)
        #signal = entry.XLowerKAMA(self, "openD", 0, 9)
        #signal = entry.XHigherKAMA(self, "openD", 0, 30)
        #signal = entry.XHigherY(self, "afternoonCloseD", 1, "openD", 1)
        #signal = entry.XHigherY(self, "athCloseD", 1, "afternoonCloseD", 1)
        # signal = entry.XLowerY(self, "close", 0, "openD", 0)
        #signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 200)
        #signal = entry.XYRangeLargerThresold(self, "highD", 2, "lowD", 2, 300)
        #signal = entry.XYRangeLargerThresold(self, "highD", 3, "lowD", 3, 300)

        '''
        self.action = OrderAction.SELL
        signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 12, 0)
        signal = entry.XLowerKAMA(self, "openD", 0, 30)
        signal = entry.XHigherY(self, "openD", 0, "closeD", 1)
        '''
        #signal = entry.XHigherKAMA(self, "openD", 0, 20)
        '''
        signal = entry.XLowerYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 100)
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, -100)
        signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -100)
        '''
        '''
        signal = entry.XLowerYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 150)
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, -50)
        signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -50)
        '''

        '''
        signal = entry.XLowerYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 200)
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 0)
        signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, 0)
        '''
        #signal = entry.XLowerYWithThresold(self, "openD", 0, "afternoonCloseD", 1, 0, 0, 200)
        #signal = entry.XLowerYWithThresold(self, "openD", 0, "afternoonCloseD", 1, 0, 0, 0)
        #signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, 0)

        '''
        signal = entry.XLowerYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 100)
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 0)
        signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, 0)
        '''

        '''
        signal = entry.XLowerYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 300)
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 100)
        signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, 100)
        '''
        '''
        signal = entry.XHigherYWithThresold(self, "afternoonCloseD", 1, "openD", 0, 0, 0, 200)
        '''

        #Open Higher than yesterday afternoon close 100pips
        #signal = entry.XLowerYWithThresold(self, "openD", 0, "afternoonCloseD", 1, 0, 0, 100)
        #signal = entry.XHigherYWithThresold(self, "openD", 0, "afternoonCloseD", 1, 0, 0, 100)
        #signal = entry.XHigherY(self, "openD", 0, "afternoonCloseD", 1)
        #signal = entry.XLowerYWithThresold(self, "openD", 0, "afternoonCloseD", 1, 0, 0, -200)
        #signal = entry.XHigherY(self, "openD", 0, "afternoonCloseD", 1)
        #signal = entry.XHigherY(self, "close", 0, "openD", 0)
        #signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -100)
        #signal = entry.XHigherYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -200)
        #signal = entry.XHigherKAMA(self, "close", 0, 6)
        #signal = entry.XHigherMaxPreviousY(self, "close", 0, "close", 6)


        size = 4 * 2
        signal = entry.XHigherY(self, "close", int(size/2), "close", int(size))

        signal = entry.XLowerY(self, "close", int(size/4), "close", int(size/2))
        signal = entry.XHigherY(self, "close", int(size/4), "close", int(size))

        signal = entry.XHigherY(self, "close", 0, "close", int(size/2))
        #signal = entry.XLowerKAMAY(self, "openD", 0, "closeD", 10)
        signal = entry.XHigherKAMAY(self, "openD", 0, "closeD", 10)


        #signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -50)
        #signal = entry.XLowerY(self, "lowD", 0, "openD", 0)

        #Make new low after open
        #signal = entry.XLowerY(self, "lowD", 0, "openD", 0)
        #signal = entry.XLowerYWithThresold(self, "lowD", 0, "openD", 0, 0, 0, -200)
        #signal = entry.XHigherMaxPreviousY(self, "close", 0, "close", 12)

        #trend filter
        #signal = entry.XHigherKAMAY(self, "openD", 0, "closeD", 40)
        #signal = entry.XLowerKAMA(self, "closeD", 1, 10)
        #signal = entry.XHigherKAMA(self, "closeD", 1, 40)

        #signal = entry.XHigherKAMA(self, "openD", 0, 20)

        #signal = entry.XHigherY(self, "openD", 0, "afternoonCloseD", 1)
        #signal = entry.XHigherY(self, "afternoonCloseD", 1, "athCloseD", 1)
        #signal = entry.XHigherMaxPreviousY(self, "close", 6, "close", 3)
        #signal = entry.XYRangeSmallerThresold(self, "highD", 0, "lowD", 0, 200)
        #signal = entry.XLowerMaxPreviousY(self, "close", 0, "high", 120, 0)
        #signal = entry.XHigherY(self, "openD", 0, "closeD", 1)

        #signal = exit.ATRHigherMinPrevious(self, "close", 14, 10)

        '''
        self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss)
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
        self.dollarTrailingSignal = exit.DollarTrailingStop(self, self.dollarTrailing)
        self.fixedStopGain = exit.FixedStopGain(self, self.stopLoss * 3)
        self.dayRangeTouch = exit.DayRangeTouch(self, 400)
        '''

        #self.atrLowerMinPrevious = exit.ATRLowerMinPrevious(self, "close", 12, 6)
        #self.dayRangeTouch = exit.DayRangeTouch(self, 500)
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

        if count == len(self.entrySignals):
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)

