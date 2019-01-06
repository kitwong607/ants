from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
#from ..ta import SMA

from ..ta.Range import *
from ..signal.entry import *
from ..signal.exit import StopLossWithFixedPrice

class StrategyCreator(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []


    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 100, "min": 100, "max": 100, "step": 10 },
        "trailingDollar": {"name": "trailingDollar", "value": 200, "min": 200, "max": 200, "step": 10 },
        "rangeId": {"name": "rangeId", "value": 0, "min": 0, "max": 5, "step": 1 },
        "signalId": {"name": "signalId", "value": 200, "min": 200, "max": 200, "step": 1 }
    }

    STRATEGY_NAME = "Strategy Creator"
    STRATEGY_SLUG = "strategyCreator"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2018-10-27"


    def __init__(self):
        pass


    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.tradingAdjustedTime = {"START": 100000,"END": 160000}
        self.minsToExitBeforeMarketClose = 30


        self.rangeFunction_1 = PreviousDayHighLowRange(session, -2)
        self.rangeFunction_2 = MinPreviousDayHighLowRange(session, [-2, -3])
        self.rangeFunction_3 = PreviousDayHighLowRange(session, -2, 0.5)
        self.rangeFunction_4 = PreviousDayHighLowRange(session, -3, 0.5)
        self.rangeFunction_5 = MaxPreviousCandlestickBodyAndShadow(session, -2)
        self.rangeFunction_6 = PreviousDayHighLowRange(session, -2, 0.2)

        self.rangeFunctions = [self.rangeFunction_1, self.rangeFunction_2, self.rangeFunction_3, self.rangeFunction_4,
                               self.rangeFunction_5, self.rangeFunction_6]

        self.longSignal_1  = XHigherY(self, "close", 0, "highD", 1)
        self.longSignal_2  = XHigherY(self, "close", 0, "highD", 2)
        self.longSignal_3  = XLowerY(self, "close", 0, "lowD", 1)
        self.longSignal_4  = XHigherY(self, "close", 0, "lowD", 2)
        self.longSignal_5  = XHigherY(self, "close", 0, "openD", 0)
        self.longSignal_6  = XHigherYWithRange(self, "close", 0, "openD", 0, 0.5)
        self.longSignal_7  = XHigherY(self, "close", 0, "close", 1)
        self.longSignal_8  = XHigherMaxYZ(self, "close", 0, "closeD", 1, "highD", 2)
        self.longSignal_9  = AverageXHigherY(self, "low", 3, "highD", 1)
        self.longSignal_10 = XHigherAverageY(self, "openD", 0, "high", 200)

        self.longSignal_11 = AverageXHigherAverageY(self, "low", 2, "high", 50)
        self.longSignal_12 = AverageXHigherAverageY(self, "low", 20, "close", 50)
        self.longSignal_13 = XHigherY(self, "low", 0, "high", 1)
        self.longSignal_14 = XHigherY(self, "lowD", 0, "closeD", 2)

        self.longSignal_15 = AverageXHigherMaxYZ(self, "high", 40, "closeD", 1, "openD", 1)
        self.longSignal_16 = AverageXHigherY(self, "high", 50, "highD", 1)
        self.longSignal_17 = AverageXLowerY(self, "low", 50, "lowD", 1)
        self.longSignal_18 =
        self.longSignal_19 =
        self.longSignal_20 = XLowerMinY(self, "low", 0, "low", 100)
        self.longSignal_21 = XHigherY(self, "high", 0, "high", 1)
        self.longSignal_22 = XLowerY(self, "low", 0, "low", 1)
        self.longSignal_23 = XHigherY(self, "close", 0, "open", 0)
        self.longSignal_24 = XHigherY(self, "high", 0, "highD", 0)
        self.longSignal_25 = XHigherMaxY(self, "high", 0, "highD", 5)
        self.longSignal_26 = XHigherMaxY(self, "high", 0, "high", 100)
        self.longSignal_27 = XYDiffLargerRange(self, "highD", 0, "lowD", 0)

        '''
        #15 average(high,40) > maxlist(closed(1),opend(1));

        #18 minlist(closed(1),opend(1)) < average(low,100) - averagetruerange(100);
        #19 high > opend(0) + rng/3 + averagetruerange(50)*4;



        #28 highd(0) - lowd(0) > rng
        '''

        #self.longSignal_1  = HigherPreviousDayHigh(self, -2)
        #self.longSignal_2  = HigherPreviousDayHigh(self, -3)
        #self.longSignal_3  = LowerPreviousDayLow(self, -2)
        #self.longSignal_4  = LowerPreviousDayLow(self, -3)

        #self.longSignal_5  = HigherPreviousDayOpen(self, -1)
        #self.longSignal_6  = HigherPreviousDayOpenWithRangeLimit(self, -1, 0.5)
        #self.longSignal_7  = HigherPreviousDayClose(self, -1)
        #self.longSignal_8  = HigherPreviousCloseAndHigh(self, -2, -3)

        #self.longSignal_9  = AverageXHigherPreviousDayY(self, "low", "high", 3, -2)
        #self.longSignal_10 = PreviousDayXHigherAverageY(self, "open", "high", -1, 200)
        #self.longSignal_11 = AverageXHigherAverageY(self, "low", "high", 2, 50)
        #self.longSignal_12 = AverageXHigherAverageY(self, "low", "clsoe", 20, 50)
        #self.longSignal_13 = XHigherLastBarY(self, "low", "high", -2)
        #self.longSignal_14 = PreviousDayXHigherPreviousDayY(self, "low", "close", -1, -3)

        self.longSignal_15 =
        self.longSignal_16 = AverageXHigherPreviousDayY(self, "high", "high", 50, -2)
        self.longSignal_17 = AverageXLowerPreviousDayY(self, "low", "low", 50, -2)
        self.longSignal_18 =
        self.longSignal_19 =
        self.longSignal_20 =
        self.longSignal_21 = XHigherLastBarY(self, "high", "high", -2)
        self.longSignal_22 =
        self.longSignal_23 = XHigherLastBarY(self, "close", "open", -1)
        self.longSignal_24 =
        self.longSignal_25 =
        self.longSignal_26 =
        self.longSignal_27 =
        self.longSignal_28 =




        self.entrySignal = FirstBarAfter(self, 11, 0, 0)
        self.stopLossSignal = StopLossWithFixedPrice(self, self.stopLoss)


    def CalculateEntrySignal(self, bar):
        self.range = self.rangeFunctions[self.parameter["rangeId"]["value"]][-1]


        if self.entrySignal.CalculateSignal(bar):
            label = 'long entry (sl:' + str(self.stopLoss) + ')'
            self.Entry(bar, OrderType.MARKET, label, self.baseQuantity)


    def CalculateExitSignal(self, bar):
        if self.stopLossSignal.CalculateSignal(bar):
            label = 'stopLoss'
            self.Exit(bar, OrderType.MARKET, label, self.baseQuantity)