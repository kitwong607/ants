from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal.entry import *
from ..signal.exit import *

class ShortStrategyCreator(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 61, "min": 1, "max": 184, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 95, "min": 1, "max": 184, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": -1, "min": 1, "max": 184, "step": 1},
        "rangeFilterId": {"name": "rangeFilterId", "value": 1, "min": 1, "max": 6, "step": 1}
    }

    STRATEGY_NAME = "Short Strategy Creator"
    STRATEGY_SLUG = "ShortStrategyCreator"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2018-11-04"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.SELL
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000,"END": 160000}
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
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)


    def SetupSignal(self, signalId):
        # Entry signal
        #higher or lower previous(1) day OHLC
        if signalId == 1:
            signal = XHigherY(self, "close", 0, "openD", 1)
        elif signalId == 2:
            signal = XHigherY(self, "close", 0, "highD", 1)
        elif signalId == 3:
            signal = XHigherY(self, "close", 0, "lowD", 1)
        elif signalId == 4:
            signal = XHigherY(self, "close", 0, "closeD", 1)
        elif signalId == 5:
            signal = XLowerY(self, "close", 0, "openD", 1)
        elif signalId == 6:
            signal = XLowerY(self, "close", 0, "highD", 1)
        elif signalId == 7:
            signal = XLowerY(self, "close", 0, "lowD", 1)
        elif signalId == 8:
            signal = XLowerY(self, "close", 0, "closeD", 1)

        #higher or lower previous(2) day OHLC
        elif signalId == 9:
            signal = XHigherY(self, "close", 0, "openD", 2)
        elif signalId == 10:
            signal = XHigherY(self, "close", 0, "highD", 2)
        elif signalId == 11:
            signal = XHigherY(self, "close", 0, "lowD", 2)
        elif signalId == 12:
            signal = XHigherY(self, "close", 0, "closeD", 2)
        elif signalId == 13:
            signal = XLowerY(self, "close", 0, "openD", 2)
        elif signalId == 14:
            signal = XLowerY(self, "close", 0, "highD", 2)
        elif signalId == 15:
            signal = XLowerY(self, "close", 0, "lowD", 2)
        elif signalId == 16:
            signal = XLowerY(self, "close", 0, "closeD", 2)

        #open higher or lower previous(1) bar OHLC
        elif signalId == 17:
            signal = XHigherY(self, "open", 0, "open", 1)
        elif signalId == 18:
            signal = XHigherY(self, "open", 0, "high", 1)
        elif signalId == 19:
            signal = XHigherY(self, "open", 0, "low", 1)
        elif signalId == 20:
            signal = XHigherY(self, "open", 0, "close", 1)
        elif signalId == 21:
            signal = XLowerY(self, "open", 0, "open", 1)
        elif signalId == 22:
            signal = XLowerY(self, "open", 0, "high", 1)
        elif signalId == 23:
            signal = XLowerY(self, "open", 0, "low", 1)
        elif signalId == 24:
            signal = XLowerY(self, "open", 0, "close", 1)


        #high higher or lower previous(1) bar OHLC
        elif signalId == 25:
            signal = XHigherY(self, "high", 0, "open", 1)
        elif signalId == 26:
            signal = XHigherY(self, "high", 0, "high", 1)
        elif signalId == 27:
            signal = XHigherY(self, "high", 0, "low", 1)
        elif signalId == 28:
            signal = XHigherY(self, "high", 0, "close", 1)
        elif signalId == 29:
            signal = XLowerY(self, "high", 0, "open", 1)
        elif signalId == 30:
            signal = XLowerY(self, "high", 0, "high", 1)
        elif signalId == 31:
            signal = XLowerY(self, "high", 0, "low", 1)
        elif signalId == 32:
            signal = XLowerY(self, "high", 0, "close", 1)


        #low higher or lower previous(1) bar OHLC
        elif signalId == 33:
            signal = XHigherY(self, "low", 0, "open", 1)
        elif signalId == 34:
            signal = XHigherY(self, "low", 0, "high", 1)
        elif signalId == 35:
            signal = XHigherY(self, "low", 0, "low", 1)
        elif signalId == 36:
            signal = XHigherY(self, "low", 0, "close", 1)
        elif signalId == 37:
            signal = XLowerY(self, "low", 0, "open", 1)
        elif signalId == 38:
            signal = XLowerY(self, "low", 0, "high", 1)
        elif signalId == 39:
            signal = XLowerY(self, "low", 0, "low", 1)
        elif signalId == 40:
            signal = XLowerY(self, "low", 0, "close", 1)


        #close higher or lower previous(1) bar OHLC
        elif signalId == 41:
            signal = XHigherY(self, "close", 0, "open", 1)
        elif signalId == 42:
            signal = XHigherY(self, "close", 0, "high", 1)
        elif signalId == 43:
            signal = XHigherY(self, "close", 0, "low", 1)
        elif signalId == 44:
            signal = XHigherY(self, "close", 0, "close", 1)
        elif signalId == 45:
            signal = XLowerY(self, "close", 0, "open", 1)
        elif signalId == 46:
            signal = XLowerY(self, "close", 0, "high", 1)
        elif signalId == 47:
            signal = XLowerY(self, "close", 0, "low", 1)
        elif signalId == 48:
            signal = XLowerY(self, "close", 0, "close", 1)

        #open higher or lower previous(2) bar OHLC
        elif signalId == 49:
            signal = XHigherY(self, "open", 0, "open", 2)
        elif signalId == 50:
            signal = XHigherY(self, "open", 0, "high", 2)
        elif signalId == 51:
            signal = XHigherY(self, "open", 0, "low", 2)
        elif signalId == 52:
            signal = XHigherY(self, "open", 0, "close", 2)
        elif signalId == 53:
            signal = XLowerY(self, "open", 0, "open", 2)
        elif signalId == 54:
            signal = XLowerY(self, "open", 0, "high", 2)
        elif signalId == 55:
            signal = XLowerY(self, "open", 0, "low", 2)
        elif signalId == 56:
            signal = XLowerY(self, "open", 0, "close", 2)


        #high higher or lower previous(2) bar OHLC
        elif signalId == 57:
            signal = XHigherY(self, "high", 0, "open", 2)
        elif signalId == 58:
            signal = XHigherY(self, "high", 0, "high", 2)
        elif signalId == 59:
            signal = XHigherY(self, "high", 0, "low", 2)
        elif signalId == 60:
            signal = XHigherY(self, "high", 0, "close", 2)
        elif signalId == 61:
            signal = XLowerY(self, "high", 0, "open", 2)
        elif signalId == 62:
            signal = XLowerY(self, "high", 0, "high", 2)
        elif signalId == 63:
            signal = XLowerY(self, "high", 0, "low", 2)
        elif signalId == 64:
            signal = XLowerY(self, "high", 0, "close", 2)


        #low higher or lower previous(2) bar OHLC
        elif signalId == 65:
            signal = XHigherY(self, "low", 0, "open", 2)
        elif signalId == 66:
            signal = XHigherY(self, "low", 0, "high", 2)
        elif signalId == 67:
            signal = XHigherY(self, "low", 0, "low", 2)
        elif signalId == 68:
            signal = XHigherY(self, "low", 0, "close", 2)
        elif signalId == 69:
            signal = XLowerY(self, "low", 0, "open", 2)
        elif signalId == 70:
            signal = XLowerY(self, "low", 0, "high", 2)
        elif signalId == 71:
            signal = XLowerY(self, "low", 0, "low", 2)
        elif signalId == 72:
            signal = XLowerY(self, "low", 0, "close", 2)


        #close higher or lower previous(2) bar OHLC
        elif signalId == 73:
            signal = XHigherY(self, "close", 0, "open", 2)
        elif signalId == 74:
            signal = XHigherY(self, "close", 0, "high", 2)
        elif signalId == 75:
            signal = XHigherY(self, "close", 0, "low", 2)
        elif signalId == 76:
            signal = XHigherY(self, "close", 0, "close", 2)
        elif signalId == 77:
            signal = XLowerY(self, "close", 0, "open", 2)
        elif signalId == 78:
            signal = XLowerY(self, "close", 0, "high", 2)
        elif signalId == 79:
            signal = XLowerY(self, "close", 0, "low", 2)
        elif signalId == 80:
            signal = XLowerY(self, "close", 0, "close", 2)




        #average(50) close higher or lower previous(1) bar OHLC
        elif signalId == 81:
            signal = AverageXHigherY(self, "close", 50, "openD", 1)
        elif signalId == 82:
            signal = AverageXHigherY(self, "close", 50, "highD", 1)
        elif signalId == 83:
            signal = AverageXHigherY(self, "close", 50, "lowD", 1)
        elif signalId == 84:
            signal = AverageXHigherY(self, "close", 50, "closeD", 1)
        elif signalId == 85:
            signal = AverageXLowerY(self, "close", 50, "openD", 1)
        elif signalId == 86:
            signal = AverageXLowerY(self, "close", 50, "highD", 1)
        elif signalId == 87:
            signal = AverageXLowerY(self, "close", 50, "lowD", 1)
        elif signalId == 88:
            signal = AverageXLowerY(self, "close", 50, "closeD", 1)

        #average(50) close higher or lower previous(2) bar OHLC
        elif signalId == 89:
            signal = AverageXHigherY(self, "close", 50, "openD", 2)
        elif signalId == 90:
            signal = AverageXHigherY(self, "close", 50, "highD", 2)
        elif signalId == 91:
            signal = AverageXHigherY(self, "close", 50, "lowD", 2)
        elif signalId == 92:
            signal = AverageXHigherY(self, "close", 50, "closeD", 2)
        elif signalId == 93:
            signal = AverageXLowerY(self, "close", 50, "openD", 2)
        elif signalId == 94:
            signal = AverageXLowerY(self, "close", 50, "highD", 2)
        elif signalId == 95:
            signal = AverageXLowerY(self, "close", 50, "lowD", 2)
        elif signalId == 96:
            signal = AverageXLowerY(self, "close", 50, "closeD", 2)





        #average close(50) higher and lower then Max of week OHLC
        elif signalId == 97:
            signal = AverageXHigherMaxY(self, "close", 50, "openD", 5)
        elif signalId == 98:
            signal = AverageXHigherMaxY(self, "close", 50, "highD", 5)
        elif signalId == 99:
            signal = AverageXHigherMaxY(self, "close", 50, "lowD", 5)
        elif signalId == 100:
            signal = AverageXHigherMaxY(self, "close", 50, "closeD", 5)
        elif signalId == 101:
            signal = AverageXLowerMaxY(self, "close", 50, "openD", 5)
        elif signalId == 102:
            signal = AverageXLowerMaxY(self, "close", 50, "highD", 5)
        elif signalId == 103:
            signal = AverageXLowerMaxY(self, "close", 50, "lowD", 5)
        elif signalId == 104:
            signal = AverageXLowerMaxY(self, "close", 50, "closeD", 5)


        #average close(50) higher then Max of 2 week OHLC
        elif signalId == 105:
            signal = AverageXHigherMaxY(self, "close", 50, "openD", 10)
        elif signalId == 106:
            signal = AverageXHigherMaxY(self, "close", 50, "highD", 10)
        elif signalId == 107:
            signal = AverageXHigherMaxY(self, "close", 50, "lowD", 10)
        elif signalId == 108:
            signal = AverageXHigherMaxY(self, "close", 50, "closeD", 10)
        elif signalId == 109:
            signal = AverageXLowerMaxY(self, "close", 50, "openD", 10)
        elif signalId == 110:
            signal = AverageXLowerMaxY(self, "close", 50, "highD", 10)
        elif signalId == 111:
            signal = AverageXLowerMaxY(self, "close", 50, "lowD", 10)
        elif signalId == 112:
            signal = AverageXLowerMaxY(self, "close", 50, "closeD", 10)




        #average close(50) higher and lower then Min of week OHLC
        elif signalId == 113:
            signal = AverageXHigherMinY(self, "close", 50, "openD", 5)
        elif signalId == 114:
            signal = AverageXHigherMinY(self, "close", 50, "highD", 5)
        elif signalId == 115:
            signal = AverageXHigherMinY(self, "close", 50, "lowD", 5)
        elif signalId == 116:
            signal = AverageXHigherMinY(self, "close", 50, "closeD", 5)
        elif signalId == 117:
            signal = AverageXLowerMinY(self, "close", 50, "openD", 5)
        elif signalId == 118:
            signal = AverageXLowerMinY(self, "close", 50, "highD", 5)
        elif signalId == 119:
            signal = AverageXLowerMinY(self, "close", 50, "lowD", 5)
        elif signalId == 120:
            signal = AverageXLowerMinY(self, "close", 50, "closeD", 5)


        #average close(50) higher then Min of 2 week OHLC
        elif signalId == 121:
            signal = AverageXHigherMinY(self, "close", 50, "openD", 10)
        elif signalId == 122:
            signal = AverageXHigherMinY(self, "close", 50, "highD", 10)
        elif signalId == 123:
            signal = AverageXHigherMinY(self, "close", 50, "lowD", 10)
        elif signalId == 124:
            signal = AverageXHigherMinY(self, "close", 50, "closeD", 10)
        elif signalId == 125:
            signal = AverageXLowerMinY(self, "close", 50, "openD", 10)
        elif signalId == 126:
            signal = AverageXLowerMinY(self, "close", 50, "highD", 10)
        elif signalId == 127:
            signal = AverageXLowerMinY(self, "close", 50, "lowD", 10)
        elif signalId == 128:
            signal = AverageXLowerMinY(self, "close", 50, "closeD", 10)


        #average close(30) higher and lower then average(5) day OHLC
        elif signalId == 129:
            signal = AverageXHigherAverageY(self, "close", 30, "openD", 5)
        elif signalId == 130:
            signal = AverageXHigherAverageY(self, "close", 30, "highD", 5)
        elif signalId == 131:
            signal = AverageXHigherAverageY(self, "close", 30, "lowD", 5)
        elif signalId == 132:
            signal = AverageXHigherAverageY(self, "close", 30, "closeD", 5)
        elif signalId == 133:
            signal = AverageXLowerAverageY(self, "close", 30, "openD", 5)
        elif signalId == 134:
            signal = AverageXLowerAverageY(self, "close", 30, "highD", 5)
        elif signalId == 135:
            signal = AverageXLowerAverageY(self, "close", 30, "lowD", 5)
        elif signalId == 136:
            signal = AverageXLowerAverageY(self, "close", 30, "closeD", 5)


        #average close(30) higher and lower then average(10) day OHLC
        elif signalId == 137:
            signal = AverageXHigherAverageY(self, "close", 30, "openD", 10)
        elif signalId == 138:
            signal = AverageXHigherAverageY(self, "close", 30, "highD", 10)
        elif signalId == 139:
            signal = AverageXHigherAverageY(self, "close", 30, "lowD", 10)
        elif signalId == 140:
            signal = AverageXHigherAverageY(self, "close", 30, "closeD", 10)
        elif signalId == 141:
            signal = AverageXLowerAverageY(self, "close", 30, "openD", 10)
        elif signalId == 142:
            signal = AverageXLowerAverageY(self, "close", 30, "highD", 10)
        elif signalId == 143:
            signal = AverageXLowerAverageY(self, "close", 30, "lowD", 10)
        elif signalId == 144:
            signal = AverageXLowerAverageY(self, "close", 30, "closeD", 10)


        #average bar OHLC (20) higher then average(50) bar OHLC
        elif signalId == 145:
            signal = AverageXHigherAverageY(self, "open", 20, "open", 50)
        elif signalId == 146:
            signal = AverageXHigherAverageY(self, "open", 20, "high", 50)
        elif signalId == 147:
            signal = AverageXHigherAverageY(self, "open", 20, "low", 50)
        elif signalId == 148:
            signal = AverageXHigherAverageY(self, "open", 20, "close", 50)
        elif signalId == 149:
            signal = AverageXHigherAverageY(self, "high", 20, "open", 50)
        elif signalId == 150:
            signal = AverageXHigherAverageY(self, "high", 20, "high", 50)
        elif signalId == 151:
            signal = AverageXHigherAverageY(self, "high", 20, "low", 50)
        elif signalId == 152:
            signal = AverageXHigherAverageY(self, "high", 20, "close", 50)
        elif signalId == 153:
            signal = AverageXHigherAverageY(self, "low", 20, "open", 50)
        elif signalId == 154:
            signal = AverageXHigherAverageY(self, "low", 20, "high", 50)
        elif signalId == 155:
            signal = AverageXHigherAverageY(self, "low", 20, "low", 50)
        elif signalId == 156:
            signal = AverageXHigherAverageY(self, "low", 20, "close", 50)
        elif signalId == 157:
            signal = AverageXHigherAverageY(self, "close", 20, "open", 50)
        elif signalId == 158:
            signal = AverageXHigherAverageY(self, "close", 20, "high", 50)
        elif signalId == 159:
            signal = AverageXHigherAverageY(self, "close", 20, "low", 50)
        elif signalId == 160:
            signal = AverageXHigherAverageY(self, "close", 20, "close", 50)


        #average bar OHLC (20) lower then average(50) bar OHLC
        elif signalId == 161:
            signal = AverageXLowerAverageY(self, "open", 20, "open", 50)
        elif signalId == 162:
            signal = AverageXLowerAverageY(self, "open", 20, "high", 50)
        elif signalId == 163:
            signal = AverageXLowerAverageY(self, "open", 20, "low", 50)
        elif signalId == 164:
            signal = AverageXLowerAverageY(self, "open", 20, "close", 50)
        elif signalId == 165:
            signal = AverageXLowerAverageY(self, "high", 20, "open", 50)
        elif signalId == 166:
            signal = AverageXLowerAverageY(self, "high", 20, "high", 50)
        elif signalId == 167:
            signal = AverageXLowerAverageY(self, "high", 20, "low", 50)
        elif signalId == 168:
            signal = AverageXLowerAverageY(self, "high", 20, "close", 50)
        elif signalId == 169:
            signal = AverageXLowerAverageY(self, "low", 20, "open", 50)
        elif signalId == 170:
            signal = AverageXLowerAverageY(self, "low", 20, "high", 50)
        elif signalId == 171:
            signal = AverageXLowerAverageY(self, "low", 20, "low", 50)
        elif signalId == 172:
            signal = AverageXLowerAverageY(self, "low", 20, "close", 50)
        elif signalId == 173:
            signal = AverageXLowerAverageY(self, "close", 20, "open", 50)
        elif signalId == 174:
            signal = AverageXLowerAverageY(self, "close", 20, "high", 50)
        elif signalId == 175:
            signal = AverageXLowerAverageY(self, "close", 20, "low", 50)
        elif signalId == 176:
            signal = AverageXLowerAverageY(self, "close", 20, "close", 50)


        #average(fast) atr higher lower then average(slow) atr
        elif signalId == 177:
            signal = AverageXHigherAverageY(self, "atr", 5, "art", 10)
        elif signalId == 178:
            signal = AverageXHigherAverageY(self, "atr", 10, "art", 20)
        elif signalId == 179:
            signal = AverageXHigherAverageY(self, "atr", 20, "art", 50)
        elif signalId == 180:
            signal = AverageXHigherAverageY(self, "atr", 30, "art", 70)
        elif signalId == 181:
            signal = AverageXLowerAverageY(self, "atr", 5, "art", 10)
        elif signalId == 182:
            signal = AverageXLowerAverageY(self, "atr", 10, "art", 20)
        elif signalId == 183:
            signal = AverageXLowerAverageY(self, "atr", 20, "art", 50)
        elif signalId == 184:
            signal = AverageXLowerAverageY(self, "atr", 30, "art", 70)