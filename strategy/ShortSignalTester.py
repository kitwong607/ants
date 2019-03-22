from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class ShortSignalTester(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    NUM_SIGNAL = 342

    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1}
    }

    STRATEGY_NAME = "Short Signal Tester"
    STRATEGY_SLUG = "ShortSignalTester"
    VERSION = "97"
    LAST_UPDATE_DATE = "20190216"
    LAST_UPDATE_TIME = "100000"

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


    # 1 Breakout previous day high
    # 2 Breakout previous day low
    # 3 Breakout previous day open
    # 4 Breakout previous day close

    # 5 Breakout previous intra day price channel high
    # 6 Breakout previous intra day price channel low

    # 7 Daily higher open
    # 8 Daily lower open
    # 9 Daily higher high
    # 10 Daily lower high
    # 11 Daily higher low
    # 12 Daily lower low
    # 13 Daily higher close
    # 14 Daily lower close

    # 15 Intra day higher high
    # 16 Intra day lower high
    # 17 Intra day higher low
    # 18 Intra day lower low

    # 19 Open higher lower pivot point
    # 20 close cross pivot point
    # 21 higher or lower pivot point
    # 22 RSI related

    # 23 Intra day SMA related

    def SetupSignal(self, signalId):
        # <editor-fold desc="# 1 Breakout previous high">
        if signalId == 1:
            signal = entry.XHigherY(self, "close", 0, "highD", 1)
        elif signalId == 2:
            signal = entry.XHigherY(self, "close", 0, "highD", 2)
        elif signalId == 3:
            signal = entry.XHigherY(self, "close", 0, "highD", 3)
        elif signalId == 4:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 5)
        elif signalId == 5:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 10)
        elif signalId == 6:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 15)
        elif signalId == 7:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 20)
        # </editor-fold>


        # <editor-fold desc="# 24 Breakout previous high with delay">
        elif signalId == 6:
            signal = entry.XHigherY(self, "close", 15, "highD", 1)
        elif signalId == 7:
            signal = entry.XHigherY(self, "close", 30, "highD", 1)
        elif signalId == 8:
            signal = entry.XHigherY(self, "close", 60, "highD", 1)
        elif signalId == 9:
            signal = entry.XHigherY(self, "close", 90, "highD", 1)

        elif signalId == 10:
            signal = entry.XHigherY(self, "close", 15, "highD", 2)
        elif signalId == 11:
            signal = entry.XHigherY(self, "close", 30, "highD", 2)
        elif signalId == 12:
            signal = entry.XHigherY(self, "close", 60, "highD", 2)
        elif signalId == 13:
            signal = entry.XHigherY(self, "close", 90, "highD", 2)

        elif signalId == 14:
            signal = entry.XHigherY(self, "close", 15, "highD", 3)
        elif signalId == 15:
            signal = entry.XHigherY(self, "close", 30, "highD", 3)
        elif signalId == 16:
            signal = entry.XHigherY(self, "close", 60, "highD", 3)
        elif signalId == 17:
            signal = entry.XHigherY(self, "close", 90, "highD", 3)



        elif signalId == 18:
            signal = entry.XLowerY(self, "close", 15, "highD", 1)
        elif signalId == 19:
            signal = entry.XLowerY(self, "close", 30, "highD", 1)
        elif signalId == 20:
            signal = entry.XLowerY(self, "close", 60, "highD", 1)
        elif signalId == 21:
            signal = entry.XLowerY(self, "close", 90, "highD", 1)

        elif signalId == 22:
            signal = entry.XLowerY(self, "close", 15, "highD", 2)
        elif signalId == 23:
            signal = entry.XLowerY(self, "close", 30, "highD", 2)
        elif signalId == 24:
            signal = entry.XLowerY(self, "close", 60, "highD", 2)
        elif signalId == 25:
            signal = entry.XLowerY(self, "close", 90, "highD", 2)

        elif signalId == 26:
            signal = entry.XLowerY(self, "close", 15, "highD", 3)
        elif signalId == 27:
            signal = entry.XLowerY(self, "close", 30, "highD", 3)
        elif signalId == 28:
            signal = entry.XLowerY(self, "close", 60, "highD", 3)
        elif signalId == 29:
            signal = entry.XLowerY(self, "close", 90, "highD", 3)
        # </editor-fold>

        # <editor-fold desc="# 2 Breakout previous low">
        elif signalId == 8:
            signal = entry.XLowerY(self, "close", 0, "lowD", 1)
        elif signalId == 9:
            signal = entry.XLowerY(self, "close", 0, "lowD", 2)
        elif signalId == 10:
            signal = entry.XLowerY(self, "close", 0, "lowD", 3)
        elif signalId == 11:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "lowD", 5)
        elif signalId == 12:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "lowD", 10)
        elif signalId == 13:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "lowD", 15)
        elif signalId == 14:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "lowD", 20)
        # </editor-fold>


        # <editor-fold desc="# 3 Breakout previous open">
        elif signalId == 15:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
        elif signalId == 16:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
        elif signalId == 17:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
        elif signalId == 18:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
        elif signalId == 19:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 10)
        elif signalId == 20:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 15)
        elif signalId == 21:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 20)

        elif signalId == 22:
            signal = entry.XLowerY(self, "close", 0, "openD", 1)
        elif signalId == 23:
            signal = entry.XLowerY(self, "close", 0, "openD", 2)
        elif signalId == 24:
            signal = entry.XLowerY(self, "close", 0, "openD", 3)
        elif signalId == 25:
            signal = entry.XLowerMinY(self, "close", 0, "openD", 5)
        elif signalId == 26:
            signal = entry.XLowerMinY(self, "close", 0, "openD", 10)
        elif signalId == 27:
            signal = entry.XLowerMinY(self, "close", 0, "openD", 15)
        elif signalId == 28:
            signal = entry.XLowerMinY(self, "close", 0, "openD", 20)
        # </editor-fold>


        # <editor-fold desc="# 4 Breakout previous close">
        elif signalId == 29:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
        elif signalId == 30:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
        elif signalId == 31:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
        elif signalId == 32:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
        elif signalId == 33:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 10)
        elif signalId == 34:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 15)
        elif signalId == 35:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 20)

        elif signalId == 36:
            signal = entry.XLowerY(self, "close", 0, "closeD", 1)
        elif signalId == 37:
            signal = entry.XLowerY(self, "close", 0, "closeD", 2)
        elif signalId == 38:
            signal = entry.XLowerY(self, "close", 0, "closeD", 3)
        elif signalId == 39:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "closeD", 5)
        elif signalId == 40:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "closeD", 10)
        elif signalId == 41:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "closeD", 15)
        elif signalId == 42:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "closeD", 20)
        # </editor-fold>


        # <editor-fold desc="# 5 Breakout previous intra day price channel high">
        elif signalId == 43:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10)
        elif signalId == 44:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20)
        elif signalId == 45:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30)
        elif signalId == 46:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
        elif signalId == 47:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90)
        elif signalId == 48:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120)
        elif signalId == 49:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 150)
        # </editor-fold>


        # <editor-fold desc="# 6 Breakout previous intra day price channel low">
        elif signalId == 50:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10)
        elif signalId == 51:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20)
        elif signalId == 52:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30)
        elif signalId == 53:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60)
        elif signalId == 54:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90)
        elif signalId == 55:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120)
        elif signalId == 56:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150)
        # </editor-fold>


        # <editor-fold desc="# 7 Daily higher open">
        elif signalId == 57:
            signal = entry.XHigherY(self, "openD", 1, "openD", 2)
        elif signalId == 58:
            signal = entry.XHigherY(self, "openD", 2, "openD", 3)
        elif signalId == 59:
            signal = entry.XHigherY(self, "openD", 3, "openD", 4)
        elif signalId == 60:
            signal = entry.XHigherY(self, "openD", 4, "openD", 5)
        elif signalId == 61:
            signal = entry.HigherX(self, "openD", 2)
        elif signalId == 62:
            signal = entry.HigherX(self, "openD", 3)
        elif signalId == 63:
            signal = entry.HigherX(self, "openD", 4)
        elif signalId == 64:
            signal = entry.HigherX(self, "openD", 5)
        # </editor-fold>


        # <editor-fold desc="# 8 Daily lower open">
        elif signalId == 65:
            signal = entry.XLowerY(self, "openD", 1, "openD", 2)
        elif signalId == 66:
            signal = entry.XLowerY(self, "openD", 2, "openD", 3)
        elif signalId == 67:
            signal = entry.XLowerY(self, "openD", 3, "openD", 4)
        elif signalId == 68:
            signal = entry.XLowerY(self, "openD", 4, "openD", 5)
        elif signalId == 69:
            signal = entry.LowerX(self, "openD", 2)
        elif signalId == 70:
            signal = entry.LowerX(self, "openD", 3)
        elif signalId == 71:
            signal = entry.LowerX(self, "openD", 4)
        elif signalId == 72:
            signal = entry.LowerX(self, "openD", 5)
        # </editor-fold>


        # <editor-fold desc="# 9 Daily higher high">
        elif signalId == 73:
            signal = entry.XHigherY(self, "highD", 1, "highD", 2)
        elif signalId == 74:
            signal = entry.XHigherY(self, "highD", 2, "highD", 3)
        elif signalId == 75:
            signal = entry.XHigherY(self, "highD", 3, "highD", 4)
        elif signalId == 76:
            signal = entry.XHigherY(self, "highD", 4, "highD", 5)
        elif signalId == 77:
            signal = entry.HigherX(self, "highD", 2)
        elif signalId == 78:
            signal = entry.HigherX(self, "highD", 3)
        elif signalId == 79:
            signal = entry.HigherX(self, "highD", 4)
        elif signalId == 80:
            signal = entry.HigherX(self, "highD", 5)
        # </editor-fold>


        # <editor-fold desc="# 10 Daily lower high">
        elif signalId == 81:
            signal = entry.XLowerY(self, "highD", 1, "highD", 2)
        elif signalId == 82:
            signal = entry.XLowerY(self, "highD", 2, "highD", 3)
        elif signalId == 83:
            signal = entry.XLowerY(self, "highD", 3, "highD", 4)
        elif signalId == 84:
            signal = entry.XLowerY(self, "highD", 4, "highD", 5)
        elif signalId == 85:
            signal = entry.LowerX(self, "highD", 2)
        elif signalId == 86:
            signal = entry.LowerX(self, "highD", 3)
        elif signalId == 87:
            signal = entry.LowerX(self, "highD", 4)
        elif signalId == 88:
            signal = entry.LowerX(self, "highD", 5)
        # </editor-fold>


        # <editor-fold desc="# 11 Daily higher low">
        elif signalId == 89:
            signal = entry.XHigherY(self, "lowD", 1, "lowD", 2)
        elif signalId == 90:
            signal = entry.XHigherY(self, "lowD", 2, "lowD", 3)
        elif signalId == 91:
            signal = entry.XHigherY(self, "lowD", 3, "lowD", 4)
        elif signalId == 92:
            signal = entry.XHigherY(self, "lowD", 4, "lowD", 5)
        elif signalId == 93:
            signal = entry.HigherX(self, "lowD", 2)
        elif signalId == 94:
            signal = entry.HigherX(self, "lowD", 3)
        elif signalId == 95:
            signal = entry.HigherX(self, "lowD", 4)
        elif signalId == 96:
            signal = entry.HigherX(self, "lowD", 5)
        # </editor-fold>


        # <editor-fold desc="# 12 Daily lower low">
        elif signalId == 97:
            signal = entry.XLowerY(self, "lowD", 1, "lowD", 2)
        elif signalId == 98:
            signal = entry.XLowerY(self, "lowD", 2, "lowD", 3)
        elif signalId == 99:
            signal = entry.XLowerY(self, "lowD", 3, "lowD", 4)
        elif signalId == 100:
            signal = entry.XLowerY(self, "lowD", 4, "lowD", 5)
        elif signalId == 101:
            signal = entry.LowerX(self, "lowD", 2)
        elif signalId == 102:
            signal = entry.LowerX(self, "lowD", 3)
        elif signalId == 103:
            signal = entry.LowerX(self, "lowD", 4)
        elif signalId == 104:
            signal = entry.LowerX(self, "lowD", 5)
        # </editor-fold>


        # <editor-fold desc="# 13 Daily higher close">
        elif signalId == 105:
            signal = entry.XHigherY(self, "closeD", 1, "closeD", 2)
        elif signalId == 106:
            signal = entry.XHigherY(self, "closeD", 2, "closeD", 3)
        elif signalId == 107:
            signal = entry.XHigherY(self, "closeD", 3, "closeD", 4)
        elif signalId == 108:
            signal = entry.XHigherY(self, "closeD", 4, "closeD", 5)
        elif signalId == 109:
            signal = entry.HigherX(self, "closeD", 2)
        elif signalId == 110:
            signal = entry.HigherX(self, "closeD", 3)
        elif signalId == 111:
            signal = entry.HigherX(self, "closeD", 4)
        elif signalId == 112:
            signal = entry.HigherX(self, "closeD", 5)
        # </editor-fold>


        # <editor-fold desc="# 14 Daily lower close">
        elif signalId == 113:
            signal = entry.XLowerY(self, "closeD", 1, "closeD", 2)
        elif signalId == 114:
            signal = entry.XLowerY(self, "closeD", 2, "closeD", 3)
        elif signalId == 115:
            signal = entry.XLowerY(self, "closeD", 3, "closeD", 4)
        elif signalId == 116:
            signal = entry.XLowerY(self, "closeD", 4, "closeD", 5)
        elif signalId == 117:
            signal = entry.LowerX(self, "closeD", 2)
        elif signalId == 118:
            signal = entry.LowerX(self, "closeD", 3)
        elif signalId == 119:
            signal = entry.LowerX(self, "closeD", 4)
        elif signalId == 120:
            signal = entry.LowerX(self, "closeD", 5)
        # </editor-fold>


        # <editor-fold desc="# 15 Intra day higher high">
        elif signalId == 121:
            signal = entry.HigherX(self, "high", 5)
        elif signalId == 122:
            signal = entry.HigherX(self, "high", 10)
        elif signalId == 123:
            signal = entry.HigherX(self, "high", 15)
        elif signalId == 124:
            signal = entry.HigherX(self, "high", 20)
        elif signalId == 125:
            signal = entry.HigherX(self, "high", 30)
        elif signalId == 126:
            signal = entry.HigherX(self, "high", 40)
        elif signalId == 127:
            signal = entry.HigherX(self, "high", 50)
        elif signalId == 128:
            signal = entry.HigherX(self, "high", 60)
        # </editor-fold>


        # <editor-fold desc="# 16 Intra day lower high">
        elif signalId == 129:
            signal = entry.LowerX(self, "high", 5)
        elif signalId == 130:
            signal = entry.LowerX(self, "high", 10)
        elif signalId == 131:
            signal = entry.LowerX(self, "high", 15)
        elif signalId == 132:
            signal = entry.LowerX(self, "high", 20)
        elif signalId == 133:
            signal = entry.LowerX(self, "high", 30)
        elif signalId == 134:
            signal = entry.LowerX(self, "high", 40)
        elif signalId == 135:
            signal = entry.LowerX(self, "high", 50)
        elif signalId == 136:
            signal = entry.LowerX(self, "high", 60)
        # </editor-fold>


        # <editor-fold desc="# 17 Intra day higher low">
        elif signalId == 137:
            signal = entry.HigherX(self, "low", 5)
        elif signalId == 138:
            signal = entry.HigherX(self, "low", 10)
        elif signalId == 139:
            signal = entry.HigherX(self, "low", 15)
        elif signalId == 140:
            signal = entry.HigherX(self, "low", 20)
        elif signalId == 141:
            signal = entry.HigherX(self, "low", 30)
        elif signalId == 142:
            signal = entry.HigherX(self, "low", 40)
        elif signalId == 143:
            signal = entry.HigherX(self, "low", 50)
        elif signalId == 144:
            signal = entry.HigherX(self, "low", 60)
        # </editor-fold>


        # <editor-fold desc="# 18 Intra day lower low">
        elif signalId == 145:
            signal = entry.LowerX(self, "low", 5)
        elif signalId == 146:
            signal = entry.LowerX(self, "low", 10)
        elif signalId == 147:
            signal = entry.LowerX(self, "low", 15)
        elif signalId == 148:
            signal = entry.LowerX(self, "low", 20)
        elif signalId == 149:
            signal = entry.LowerX(self, "low", 30)
        elif signalId == 150:
            signal = entry.LowerX(self, "low", 40)
        elif signalId == 151:
            signal = entry.LowerX(self, "low", 50)
        elif signalId == 152:
            signal = entry.LowerX(self, "low", 60)
        # </editor-fold>



        # <editor-fold desc="# 19 Open higher lower pivot point">
        elif signalId == 153:
            signal = entry.XHigherPivotPoint(self, "openD", 0, 1)
        elif signalId == 154:
            signal = entry.XLowerPivotPoint(self, "openD", 0, 1)
        elif signalId == 155:
            signal = entry.XHigherPivotPointS1(self, "openD", 0, 1)
        elif signalId == 156:
            signal = entry.XLowerPivotPointS1(self, "openD", 0, 1)
        elif signalId == 157:
            signal = entry.XHigherPivotPointR1(self, "openD", 0, 1)
        elif signalId == 158:
            signal = entry.XLowerPivotPointR1(self, "openD", 0, 1)
        elif signalId == 159:
            signal = entry.XHigherPivotPointS2(self, "openD", 0, 1)
        elif signalId == 160:
            signal = entry.XLowerPivotPointS2(self, "openD", 0, 1)
        elif signalId == 161:
            signal = entry.XHigherPivotPointR2(self, "openD", 0, 1)
        elif signalId == 162:
            signal = entry.XLowerPivotPointR2(self, "openD", 0, 1)
        elif signalId == 163:
            signal = entry.XHigherPivotPointS3(self, "openD", 0, 1)
        elif signalId == 164:
            signal = entry.XLowerPivotPointS3(self, "openD", 0, 1)
        elif signalId == 165:
            signal = entry.XHigherPivotPointR3(self, "openD", 0, 1)
        elif signalId == 166:
            signal = entry.XLowerPivotPointR3(self, "openD", 0, 1)
        # </editor-fold>

        # <editor-fold desc="# 20 close cross pivot point">
        elif signalId == 167:
            signal = entry.CrossUpPivotPoint(self, 1)
        elif signalId == 168:
            signal = entry.CrossDownPivotPoint(self, 1)
        elif signalId == 169:
            signal = entry.CrossUpPivotPointS1(self, 1)
        elif signalId == 170:
            signal = entry.CrossDownPivotPointS1(self, 1)
        elif signalId == 171:
            signal = entry.CrossUpPivotPointR1(self, 1)
        elif signalId == 172:
            signal = entry.CrossDownPivotPointR1(self, 1)
        elif signalId == 173:
            signal = entry.CrossUpPivotPointS2(self, 1)
        elif signalId == 174:
            signal = entry.CrossDownPivotPointS2(self, 1)
        elif signalId == 175:
            signal = entry.CrossUpPivotPointR2(self, 1)
        elif signalId == 176:
            signal = entry.CrossDownPivotPointR2(self, 1)
        elif signalId == 177:
            signal = entry.CrossUpPivotPointS3(self, 1)
        elif signalId == 178:
            signal = entry.CrossDownPivotPointS3(self, 1)
        elif signalId == 179:
            signal = entry.CrossUpPivotPointR3(self, 1)
        elif signalId == 180:
            signal = entry.CrossDownPivotPointR3(self, 1)
        # </editor-fold>

        # <editor-fold desc="# 21 higher or lower pivot point">
        elif signalId == 181:
            signal = entry.XHigherPivotPoint(self, "close", 0, 1)
        elif signalId == 182:
            signal = entry.XLowerPivotPoint(self, "close", 0, 1)
        elif signalId == 183:
            signal = entry.XHigherPivotPointS1(self, "close", 0, 1)
        elif signalId == 184:
            signal = entry.XLowerPivotPointS1(self, "close", 0, 1)
        elif signalId == 185:
            signal = entry.XHigherPivotPointR1(self, "close", 0, 1)
        elif signalId == 186:
            signal = entry.XLowerPivotPointR1(self, "close", 0, 1)
        elif signalId == 187:
            signal = entry.XHigherPivotPointS2(self, "close", 0, 1)
        elif signalId == 188:
            signal = entry.XLowerPivotPointS2(self, "close", 0, 1)
        elif signalId == 189:
            signal = entry.XHigherPivotPointR2(self, "close", 0, 1)
        elif signalId == 190:
            signal = entry.XLowerPivotPointR2(self, "close", 0, 1)
        elif signalId == 191:
            signal = entry.XHigherPivotPointS3(self, "close", 0, 1)
        elif signalId == 192:
            signal = entry.XLowerPivotPointS3(self, "close", 0, 1)
        elif signalId == 193:
            signal = entry.XHigherPivotPointR3(self, "close", 0, 1)
        elif signalId == 194:
            signal = entry.XLowerPivotPointR3(self, "close", 0, 1)
        # </editor-fold>


        # <editor-fold desc="# 22 RSI related">
        elif signalId == 195:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 2, 80)
        elif signalId == 196:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 2, 20)
        elif signalId == 197:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 5, 80)
        elif signalId == 198:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 5, 20)
        elif signalId == 199:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 10, 80)
        elif signalId == 200:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 10, 20)
        elif signalId == 201:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 15, 80)
        elif signalId == 202:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 15, 20)
        elif signalId == 203:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 20, 80)
        elif signalId == 204:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 20, 20)
        elif signalId == 205:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 30, 80)
        elif signalId == 206:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 30, 20)
        # </editor-fold>


        # <editor-fold desc="# 23 Intra day SMA related">
        elif signalId == 207:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
        elif signalId == 208:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
        elif signalId == 209:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
        elif signalId == 210:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 60)
        elif signalId == 211:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 90)
        elif signalId == 212:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 120)

        elif signalId == 213:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 10)
        elif signalId == 214:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 20)
        elif signalId == 215:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 40)
        elif signalId == 216:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 60)
        elif signalId == 217:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 90)
        elif signalId == 218:
            signal = entry.XLowerAverageY(self, "close", 0, "close", 120)

        elif signalId == 219:
            signal = entry.AverageXHigherAverageY(self, "close", 10, "open", 10)
        elif signalId == 220:
            signal = entry.AverageXHigherAverageY(self, "close", 20, "open", 20)
        elif signalId == 221:
            signal = entry.AverageXHigherAverageY(self, "close", 40, "open", 40)
        elif signalId == 222:
            signal = entry.AverageXHigherAverageY(self, "close", 60, "open", 60)
        elif signalId == 223:
            signal = entry.AverageXHigherAverageY(self, "close", 90, "open", 90)
        elif signalId == 224:
            signal = entry.AverageXHigherAverageY(self, "close", 120, "open", 120)

        elif signalId == 225:
            signal = entry.AverageXLowerAverageY(self, "close", 10, "open", 10)
        elif signalId == 226:
            signal = entry.AverageXLowerAverageY(self, "close", 20, "open", 20)
        elif signalId == 227:
            signal = entry.AverageXLowerAverageY(self, "close", 40, "open", 40)
        elif signalId == 228:
            signal = entry.AverageXLowerAverageY(self, "close", 60, "open", 60)
        elif signalId == 229:
            signal = entry.AverageXLowerAverageY(self, "close", 90, "open", 90)
        elif signalId == 230:
            signal = entry.AverageXLowerAverageY(self, "close", 120, "open", 120)
        # </editor-fold>





        # <editor-fold desc="# 24 Breakout previous high with delay">
        elif signalId == 231:
            signal = entry.XHigherY(self, "close", 15, "highD", 1)
        elif signalId == 232:
            signal = entry.XHigherY(self, "close", 30, "highD", 1)
        elif signalId == 233:
            signal = entry.XHigherY(self, "close", 60, "highD", 1)
        elif signalId == 234:
            signal = entry.XHigherY(self, "close", 90, "highD", 1)

        elif signalId == 235:
            signal = entry.XHigherY(self, "close", 15, "highD", 2)
        elif signalId == 236:
            signal = entry.XHigherY(self, "close", 30, "highD", 2)
        elif signalId == 237:
            signal = entry.XHigherY(self, "close", 60, "highD", 2)
        elif signalId == 238:
            signal = entry.XHigherY(self, "close", 90, "highD", 2)

        elif signalId == 239:
            signal = entry.XHigherY(self, "close", 15, "highD", 3)
        elif signalId == 240:
            signal = entry.XHigherY(self, "close", 30, "highD", 3)
        elif signalId == 241:
            signal = entry.XHigherY(self, "close", 60, "highD", 3)
        elif signalId == 242:
            signal = entry.XHigherY(self, "close", 90, "highD", 3)



        elif signalId == 243:
            signal = entry.XLowerY(self, "close", 15, "highD", 1)
        elif signalId == 244:
            signal = entry.XLowerY(self, "close", 30, "highD", 1)
        elif signalId == 245:
            signal = entry.XLowerY(self, "close", 60, "highD", 1)
        elif signalId == 246:
            signal = entry.XLowerY(self, "close", 90, "highD", 1)

        elif signalId == 247:
            signal = entry.XLowerY(self, "close", 15, "highD", 2)
        elif signalId == 248:
            signal = entry.XLowerY(self, "close", 30, "highD", 2)
        elif signalId == 249:
            signal = entry.XLowerY(self, "close", 60, "highD", 2)
        elif signalId == 250:
            signal = entry.XLowerY(self, "close", 90, "highD", 2)

        elif signalId == 251:
            signal = entry.XLowerY(self, "close", 15, "highD", 3)
        elif signalId == 252:
            signal = entry.XLowerY(self, "close", 30, "highD", 3)
        elif signalId == 253:
            signal = entry.XLowerY(self, "close", 60, "highD", 3)
        elif signalId == 254:
            signal = entry.XLowerY(self, "close", 90, "highD", 3)
        # </editor-fold>

        # <editor-fold desc="# 25 Breakout previous low with delay">
        elif signalId == 255:
            signal = entry.XHigherY(self, "close", 15, "lowD", 1)
        elif signalId == 256:
            signal = entry.XHigherY(self, "close", 30, "lowD", 1)
        elif signalId == 257:
            signal = entry.XHigherY(self, "close", 60, "lowD", 1)
        elif signalId == 258:
            signal = entry.XHigherY(self, "close", 90, "lowD", 1)


        elif signalId == 259:
            signal = entry.XHigherY(self, "close", 15, "lowD", 2)
        elif signalId == 260:
            signal = entry.XHigherY(self, "close", 30, "lowD", 2)
        elif signalId == 261:
            signal = entry.XHigherY(self, "close", 60, "lowD", 2)
        elif signalId == 262:
            signal = entry.XHigherY(self, "close", 90, "lowD", 2)


        elif signalId == 263:
            signal = entry.XHigherY(self, "close", 15, "lowD", 3)
        elif signalId == 264:
            signal = entry.XHigherY(self, "close", 30, "lowD", 3)
        elif signalId == 265:
            signal = entry.XHigherY(self, "close", 60, "lowD", 3)
        elif signalId == 266:
            signal = entry.XHigherY(self, "close", 90, "lowD", 3)
        # </editor-fold>

        # <editor-fold desc="# 26 Breakout previous open with delay">
        elif signalId == 267:
            signal = entry.XHigherY(self, "close", 10, "openD", 1)
        elif signalId == 268:
            signal = entry.XHigherY(self, "close", 30, "openD", 1)
        elif signalId == 269:
            signal = entry.XHigherY(self, "close", 60, "openD", 1)
        elif signalId == 270:
            signal = entry.XHigherY(self, "close", 90, "openD", 1)

        elif signalId == 271:
            signal = entry.XHigherY(self, "close", 10, "openD", 2)
        elif signalId == 272:
            signal = entry.XHigherY(self, "close", 30, "openD", 2)
        elif signalId == 273:
            signal = entry.XHigherY(self, "close", 60, "openD", 2)
        elif signalId == 274:
            signal = entry.XHigherY(self, "close", 90, "openD", 2)

        elif signalId == 275:
            signal = entry.XHigherY(self, "close", 10, "openD", 3)
        elif signalId == 276:
            signal = entry.XHigherY(self, "close", 30, "openD", 3)
        elif signalId == 277:
            signal = entry.XHigherY(self, "close", 60, "openD", 3)
        elif signalId == 278:
            signal = entry.XHigherY(self, "close", 90, "openD", 3)

        elif signalId == 279:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 5)
        elif signalId == 280:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 5)
        elif signalId == 281:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 5)
        elif signalId == 282:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 5)

        elif signalId == 283:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 10)
        elif signalId == 284:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 10)
        elif signalId == 285:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 10)
        elif signalId == 286:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 10)

        elif signalId == 287:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 15)
        elif signalId == 288:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 15)
        elif signalId == 289:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 15)
        elif signalId == 290:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 15)
        # </editor-fold>

        # <editor-fold desc="# 28 Breakout previous intra day price channel high with delay">
        elif signalId == 291:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 15)
        elif signalId == 292:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 30)
        elif signalId == 293:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 45)
        elif signalId == 294:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 60)

        elif signalId == 295:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 15)
        elif signalId == 296:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 30)
        elif signalId == 297:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 45)
        elif signalId == 298:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 60)

        elif signalId == 299:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 15)
        elif signalId == 300:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 30)
        elif signalId == 301:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 45)
        elif signalId == 302:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 60)

        elif signalId == 303:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 15)
        elif signalId == 304:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 30)
        elif signalId == 305:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 45)
        elif signalId == 306:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 60)

        elif signalId == 307:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 15)
        elif signalId == 308:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 30)
        elif signalId == 309:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 45)
        elif signalId == 310:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 60)

        elif signalId == 311:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 15)
        elif signalId == 312:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 30)
        elif signalId == 313:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 45)
        elif signalId == 314:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 60)
        # </editor-fold>

        # <editor-fold desc="# 29 Breakout previous intra day price channel low with delay">
        elif signalId == 315:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 15)
        elif signalId == 316:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 30)
        elif signalId == 317:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 60)
        elif signalId == 318:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 90)

        elif signalId == 319:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 15)
        elif signalId == 320:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 3)
        elif signalId == 321:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 60)
        elif signalId == 322:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 90)

        elif signalId == 323:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 15)
        elif signalId == 324:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 30)
        elif signalId == 325:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 60)
        elif signalId == 326:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 90)

        elif signalId == 327:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 15)
        elif signalId == 328:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 30)
        elif signalId == 329:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 60)
        elif signalId == 330:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 90)

        elif signalId == 331:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 15)
        elif signalId == 332:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 30)
        elif signalId == 333:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 60)
        elif signalId == 334:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 90)

        elif signalId == 335:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 15)
        elif signalId == 336:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 30)
        elif signalId == 337:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 60)
        elif signalId == 338:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 90)

        elif signalId == 339:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 15)
        elif signalId == 340:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 30)
        elif signalId == 341:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 60)
        elif signalId == 342:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 90)
        # </editor-fold>