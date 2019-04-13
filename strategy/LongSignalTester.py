from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LongSignalTester(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    NUM_SIGNAL = 253
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},

        "entryPeriod": {"name": "entryLimit", "value": 0, "min": 0, "max": 2, "step": 1}
    }

    STRATEGY_NAME = "Long Signal Tester"
    STRATEGY_SLUG = "LongSignalTester"
    VERSION = "97"
    LAST_UPDATE_DATE = "20190207"
    LAST_UPDATE_TIME = "153230"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        if self.parameter["entryPeriod"]["value"] == 0:     #Full Day
            self.entryHourLimitInAdjustedTime = {"START": 100000,"END": 160000}
        elif self.parameter["entryPeriod"]["value"] == 1:   #AM
            self.entryHourLimitInAdjustedTime = {"START": 100000, "END": 120000}
        elif self.parameter["entryPeriod"]["value"] == 2:   #PM
            self.entryHourLimitInAdjustedTime = {"START": 130000, "END": 160000}

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
        self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss * 1.5)
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
    # 24 Breakout previous high with delay

    # 2 Breakout previous day low
    # 25 Breakout previous low with delay

    # 3 Breakout previous day open
    # 26 Breakout previous open with delay

    # 4 Breakout previous day close
    # 27 Breakout previous close with delay

    # 5 Breakout previous intra day price channel high
    # 30 Breakout previous intra day price channel high with delay

    # 6 Breakout previous intra day price channel low
    # 29 Breakout previous intra day price channel low with delay

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
            signal = entry.XHigherY(self, "close", 0, "highD", 4)
        elif signalId == 5:
            signal = entry.XHigherY(self, "close", 0, "highD", 5)
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
        elif signalId == 30:
            signal = entry.XHigherY(self, "close", 0, "lowD", 1)
        elif signalId == 31:
            signal = entry.XHigherY(self, "close", 0, "lowD", 2)
        elif signalId == 32:
            signal = entry.XHigherY(self, "close", 0, "lowD", 3)
        elif signalId == 33:
            signal = entry.XHigherY(self, "close", 0, "lowD", 4)
        elif signalId == 34:
            signal = entry.XHigherY(self, "close", 0, "lowD", 5)
        # </editor-fold>

        # <editor-fold desc="# 25 Breakout previous low with delay">
        elif signalId == 35:
            signal = entry.XHigherY(self, "close", 15, "lowD", 1)
        elif signalId == 36:
            signal = entry.XHigherY(self, "close", 30, "lowD", 1)
        elif signalId == 37:
            signal = entry.XHigherY(self, "close", 60, "lowD", 1)
        elif signalId == 38:
            signal = entry.XHigherY(self, "close", 90, "lowD", 1)


        elif signalId == 39:
            signal = entry.XHigherY(self, "close", 15, "lowD", 2)
        elif signalId == 40:
            signal = entry.XHigherY(self, "close", 30, "lowD", 2)
        elif signalId == 41:
            signal = entry.XHigherY(self, "close", 60, "lowD", 2)
        elif signalId == 42:
            signal = entry.XHigherY(self, "close", 90, "lowD", 2)


        elif signalId == 43:
            signal = entry.XHigherY(self, "close", 15, "lowD", 3)
        elif signalId == 44:
            signal = entry.XHigherY(self, "close", 30, "lowD", 3)
        elif signalId == 45:
            signal = entry.XHigherY(self, "close", 60, "lowD", 3)
        elif signalId == 46:
            signal = entry.XHigherY(self, "close", 90, "lowD", 3)
        # </editor-fold>


        # <editor-fold desc="# 3 Breakout previous open">
        elif signalId == 47:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
        elif signalId == 48:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
        elif signalId == 49:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
        elif signalId == 50:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
        elif signalId == 51:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 10)
        elif signalId == 52:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 15)
        # </editor-fold>

        # <editor-fold desc="# 26 Breakout previous open with delay">
        elif signalId == 53:
            signal = entry.XHigherY(self, "close", 10, "openD", 1)
        elif signalId == 54:
            signal = entry.XHigherY(self, "close", 30, "openD", 1)
        elif signalId == 55:
            signal = entry.XHigherY(self, "close", 60, "openD", 1)
        elif signalId == 56:
            signal = entry.XHigherY(self, "close", 90, "openD", 1)

        elif signalId == 57:
            signal = entry.XHigherY(self, "close", 10, "openD", 2)
        elif signalId == 58:
            signal = entry.XHigherY(self, "close", 30, "openD", 2)
        elif signalId == 59:
            signal = entry.XHigherY(self, "close", 60, "openD", 2)
        elif signalId == 60:
            signal = entry.XHigherY(self, "close", 90, "openD", 2)

        elif signalId == 61:
            signal = entry.XHigherY(self, "close", 10, "openD", 3)
        elif signalId == 62:
            signal = entry.XHigherY(self, "close", 30, "openD", 3)
        elif signalId == 63:
            signal = entry.XHigherY(self, "close", 60, "openD", 3)
        elif signalId == 64:
            signal = entry.XHigherY(self, "close", 90, "openD", 3)

        elif signalId == 65:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 5)
        elif signalId == 66:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 5)
        elif signalId == 67:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 5)
        elif signalId == 68:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 5)

        elif signalId == 69:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 10)
        elif signalId == 70:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 10)
        elif signalId == 71:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 10)
        elif signalId == 72:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 10)

        elif signalId == 73:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "openD", 15)
        elif signalId == 74:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "openD", 15)
        elif signalId == 75:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "openD", 15)
        elif signalId == 76:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "openD", 15)
        # </editor-fold>


        # <editor-fold desc="# 4 Breakout previous close">
        elif signalId == 77:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
        elif signalId == 78:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
        elif signalId == 79:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
        elif signalId == 80:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
        elif signalId == 81:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 10)
        elif signalId == 82:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 15)
        # </editor-fold>

        # <editor-fold desc="# 27 Breakout previous close with delay">
        elif signalId == 83:
            signal = entry.XHigherY(self, "close", 10, "closeD", 1)
        elif signalId == 84:
            signal = entry.XHigherY(self, "close", 30, "closeD", 1)
        elif signalId == 85:
            signal = entry.XHigherY(self, "close", 60, "closeD", 1)
        elif signalId == 86:
            signal = entry.XHigherY(self, "close", 90, "closeD", 1)

        elif signalId == 87:
            signal = entry.XHigherY(self, "close", 10, "closeD", 2)
        elif signalId == 88:
            signal = entry.XHigherY(self, "close", 30, "closeD", 2)
        elif signalId == 89:
            signal = entry.XHigherY(self, "close", 60, "closeD", 2)
        elif signalId == 90:
            signal = entry.XHigherY(self, "close", 90, "closeD", 2)

        elif signalId == 91:
            signal = entry.XHigherY(self, "close", 10, "closeD", 3)
        elif signalId == 92:
            signal = entry.XHigherY(self, "close", 30, "closeD", 3)
        elif signalId == 93:
            signal = entry.XHigherY(self, "close", 60, "closeD", 3)
        elif signalId == 94:
            signal = entry.XHigherY(self, "close", 90, "closeD", 3)

        elif signalId == 95:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "closeD", 5)
        elif signalId == 96:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "closeD", 5)
        elif signalId == 97:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "closeD", 5)
        elif signalId == 98:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "closeD", 5)

        elif signalId == 99:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "closeD", 10)
        elif signalId == 100:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "closeD", 10)
        elif signalId == 101:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "closeD", 10)
        elif signalId == 102:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "closeD", 10)

        elif signalId == 103:
            signal = entry.XHigherMaxPreviousY(self, "close", 10, "closeD", 15)
        elif signalId == 104:
            signal = entry.XHigherMaxPreviousY(self, "close", 30, "closeD", 15)
        elif signalId == 105:
            signal = entry.XHigherMaxPreviousY(self, "close", 60, "closeD", 15)
        elif signalId == 106:
            signal = entry.XHigherMaxPreviousY(self, "close", 90, "closeD", 15)
        # </editor-fold>


        # <editor-fold desc="# 5 Breakout previous intra day price channel high">
        elif signalId == 107:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10)
        elif signalId == 108:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20)
        elif signalId == 109:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30)
        elif signalId == 110:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
        elif signalId == 111:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90)
        elif signalId == 112:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120)
        elif signalId == 113:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 150)
        # </editor-fold>

        # <editor-fold desc="# 28 Breakout previous intra day price channel high with delay">
        elif signalId == 114:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 15)
        elif signalId == 115:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 30)
        elif signalId == 116:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 45)
        elif signalId == 117:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 10, 60)

        elif signalId == 118:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 15)
        elif signalId == 119:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 30)
        elif signalId == 120:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 45)
        elif signalId == 121:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 20, 60)

        elif signalId == 122:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 15)
        elif signalId == 123:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 30)
        elif signalId == 124:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 45)
        elif signalId == 125:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 30, 60)

        elif signalId == 126:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 15)
        elif signalId == 127:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 30)
        elif signalId == 128:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 45)
        elif signalId == 129:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 60)

        elif signalId == 130:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 15)
        elif signalId == 131:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 30)
        elif signalId == 132:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 45)
        elif signalId == 133:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 90, 60)

        elif signalId == 134:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 15)
        elif signalId == 135:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 30)
        elif signalId == 136:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 45)
        elif signalId == 137:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 120, 60)
        # </editor-fold>


        # <editor-fold desc="# 6 Breakout previous intra day price channel low">
        elif signalId == 138:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10)
        elif signalId == 139:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20)
        elif signalId == 140:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30)
        elif signalId == 141:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60)
        elif signalId == 142:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90)
        elif signalId == 143:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120)
        elif signalId == 144:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150)
        # </editor-fold>

        # <editor-fold desc="# 29 Breakout previous intra day price channel low with delay">
        elif signalId == 145:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 15)
        elif signalId == 146:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 30)
        elif signalId == 147:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 60)
        elif signalId == 148:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 10, 90)

        elif signalId == 149:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 15)
        elif signalId == 150:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 3)
        elif signalId == 151:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 60)
        elif signalId == 152:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 20, 90)

        elif signalId == 153:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 15)
        elif signalId == 154:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 30)
        elif signalId == 155:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 60)
        elif signalId == 156:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 30, 90)

        elif signalId == 157:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 15)
        elif signalId == 158:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 30)
        elif signalId == 159:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 60)
        elif signalId == 160:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 60, 90)

        elif signalId == 161:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 15)
        elif signalId == 162:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 30)
        elif signalId == 163:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 60)
        elif signalId == 164:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 90, 90)

        elif signalId == 165:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 15)
        elif signalId == 166:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 30)
        elif signalId == 167:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 60)
        elif signalId == 168:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 120, 90)

        elif signalId == 169:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 15)
        elif signalId == 170:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 30)
        elif signalId == 171:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 60)
        elif signalId == 172:
            signal = entry.XLowerMinPreviousY(self, "close", 0, "low", 150, 90)
        # </editor-fold>


        # <editor-fold desc="# 7 Daily higher open">
        elif signalId == 173:
            signal = entry.XHigherY(self, "openD", 1, "openD", 2)
        elif signalId == 174:
            signal = entry.XHigherY(self, "openD", 2, "openD", 3)
        elif signalId == 175:
            signal = entry.XHigherY(self, "openD", 3, "openD", 4)
        elif signalId == 176:
            signal = entry.XHigherY(self, "openD", 4, "openD", 5)
        elif signalId == 177:
            signal = entry.HigherX(self, "openD", 2)
        elif signalId == 178:
            signal = entry.HigherX(self, "openD", 3)
        # </editor-fold>

        # <editor-fold desc="# 8 Daily lower open">
        # </editor-fold>


        # <editor-fold desc="# 9 Daily higher high">
        elif signalId == 179:
            signal = entry.XHigherY(self, "highD", 1, "highD", 2)
        elif signalId == 180:
            signal = entry.XHigherY(self, "highD", 2, "highD", 3)
        elif signalId == 181:
            signal = entry.XHigherY(self, "highD", 3, "highD", 4)
        elif signalId == 182:
            signal = entry.XHigherY(self, "highD", 4, "highD", 5)
        elif signalId == 183:
            signal = entry.HigherX(self, "highD", 2)
        elif signalId == 184:
            signal = entry.HigherX(self, "highD", 3)
        # </editor-fold>


        # <editor-fold desc="# 10 Daily lower high">
        # </editor-fold>


        # <editor-fold desc="# 11 Daily higher low">
        elif signalId == 185:
            signal = entry.XHigherY(self, "lowD", 1, "lowD", 2)
        elif signalId == 186:
            signal = entry.XHigherY(self, "lowD", 2, "lowD", 3)
        elif signalId == 187:
            signal = entry.XHigherY(self, "lowD", 3, "lowD", 4)
        elif signalId == 188:
            signal = entry.XHigherY(self, "lowD", 4, "lowD", 5)
        elif signalId == 189:
            signal = entry.HigherX(self, "lowD", 2)
        elif signalId == 190:
            signal = entry.HigherX(self, "lowD", 3)
        elif signalId == 191:
            signal = entry.HigherX(self, "lowD", 4)
        # </editor-fold>


        # <editor-fold desc="# 12 Daily lower low">
        # </editor-fold>


        # <editor-fold desc="# 13 Daily higher close">
        elif signalId == 192:
            signal = entry.XHigherY(self, "closeD", 3, "closeD", 4)
        elif signalId == 193:
            signal = entry.XHigherY(self, "closeD", 4, "closeD", 5)
        elif signalId == 194:
            signal = entry.HigherX(self, "closeD", 2)
        elif signalId == 195:
            signal = entry.HigherX(self, "closeD", 3)
        # </editor-fold>


        # <editor-fold desc="# 14 Daily lower close">
        # </editor-fold>


        # <editor-fold desc="# 15 Intra day higher high">
        elif signalId == 196:
            signal = entry.HigherX(self, "high", 5)
        elif signalId == 197:
            signal = entry.HigherX(self, "high", 10)
        elif signalId == 198:
            signal = entry.HigherX(self, "high", 15)
        elif signalId == 199:
            signal = entry.HigherX(self, "high", 20)
        elif signalId == 200:
            signal = entry.HigherX(self, "high", 30)
        elif signalId == 201:
            signal = entry.HigherX(self, "high", 40)
        elif signalId == 202:
            signal = entry.HigherX(self, "high", 50)
        elif signalId == 203:
            signal = entry.HigherX(self, "high", 60)
        # </editor-fold>


        # <editor-fold desc="# 16 Intra day lower high">
        # </editor-fold>


        # <editor-fold desc="# 17 Intra day higher low">
        elif signalId == 204:
            signal = entry.HigherX(self, "low", 5)
        elif signalId == 205:
            signal = entry.HigherX(self, "low", 10)
        elif signalId == 206:
            signal = entry.HigherX(self, "low", 15)
        elif signalId == 207:
            signal = entry.HigherX(self, "low", 20)
        elif signalId == 208:
            signal = entry.HigherX(self, "low", 30)
        elif signalId == 209:
            signal = entry.HigherX(self, "low", 40)
        elif signalId == 210:
            signal = entry.HigherX(self, "low", 50)
        elif signalId == 211:
            signal = entry.HigherX(self, "low", 60)
        # </editor-fold>


        # <editor-fold desc="# 18 Intra day lower low">
        # </editor-fold>



        # <editor-fold desc="# 19 Open higher lower pivot point">
        elif signalId == 212:
            signal = entry.XHigherPivotPoint(self, "openD", 0, 1)
        elif signalId == 213:
            signal = entry.XLowerPivotPoint(self, "openD", 0, 1)
        elif signalId == 214:
            signal = entry.XHigherPivotPointS1(self, "openD", 0, 1)
        elif signalId == 215:
            signal = entry.XLowerPivotPointS1(self, "openD", 0, 1)
        elif signalId == 216:
            signal = entry.XHigherPivotPointR1(self, "openD", 0, 1)
        elif signalId == 217:
            signal = entry.XLowerPivotPointR1(self, "openD", 0, 1)
        elif signalId == 218:
            signal = entry.XHigherPivotPointS2(self, "openD", 0, 1)
        elif signalId == 219:
            signal = entry.XLowerPivotPointS2(self, "openD", 0, 1)
        elif signalId == 220:
            signal = entry.XHigherPivotPointR2(self, "openD", 0, 1)
        elif signalId == 221:
            signal = entry.XLowerPivotPointR2(self, "openD", 0, 1)
        elif signalId == 222:
            signal = entry.XHigherPivotPointS3(self, "openD", 0, 1)
        elif signalId == 223:
            signal = entry.XLowerPivotPointS3(self, "openD", 0, 1)
        elif signalId == 224:
            signal = entry.XHigherPivotPointR3(self, "openD", 0, 1)
        elif signalId == 225:
            signal = entry.XLowerPivotPointR3(self, "openD", 0, 1)
        # </editor-fold>

        # <editor-fold desc="# 20 close cross pivot point">
        # </editor-fold>

        # <editor-fold desc="# 21 higher or lower pivot point">
        elif signalId == 226:
            signal = entry.XHigherPivotPoint(self, "close", 0, 1)
        elif signalId == 227:
            signal = entry.XLowerPivotPoint(self, "close", 0, 1)
        elif signalId == 228:
            signal = entry.XHigherPivotPointS1(self, "close", 0, 1)
        elif signalId == 229:
            signal = entry.XLowerPivotPointS1(self, "close", 0, 1)
        elif signalId == 230:
            signal = entry.XHigherPivotPointR1(self, "close", 0, 1)
        elif signalId == 231:
            signal = entry.XLowerPivotPointR1(self, "close", 0, 1)
        # </editor-fold>


        # <editor-fold desc="# 22 RSI related">
        elif signalId == 232:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 2, 80)
        elif signalId == 233:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 2, 20)
        elif signalId == 234:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 5, 80)
        elif signalId == 235:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 5, 20)
        # </editor-fold>


        # <editor-fold desc="# 23 Intra day SMA related">
        elif signalId == 236:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
        elif signalId == 237:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
        elif signalId == 238:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
        elif signalId == 239:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 60)
        elif signalId == 240:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 90)
        elif signalId == 241:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 120)
        elif signalId == 242:
            signal = entry.AverageXHigherAverageY(self, "close", 10, "open", 10)
        elif signalId == 243:
            signal = entry.AverageXHigherAverageY(self, "close", 20, "open", 20)
        elif signalId == 244:
            signal = entry.AverageXHigherAverageY(self, "close", 40, "open", 40)
        elif signalId == 245:
            signal = entry.AverageXHigherAverageY(self, "close", 60, "open", 60)
        elif signalId == 246:
            signal = entry.AverageXHigherAverageY(self, "close", 90, "open", 90)
        elif signalId == 247:
            signal = entry.AverageXHigherAverageY(self, "close", 120, "open", 120)

        elif signalId == 248:
            signal = entry.AverageXLowerAverageY(self, "close", 10, "open", 10)
        elif signalId == 249:
            signal = entry.AverageXLowerAverageY(self, "close", 20, "open", 20)
        elif signalId == 250:
            signal = entry.AverageXLowerAverageY(self, "close", 40, "open", 40)
        elif signalId == 251:
            signal = entry.AverageXLowerAverageY(self, "close", 60, "open", 60)
        elif signalId == 252:
            signal = entry.AverageXLowerAverageY(self, "close", 90, "open", 90)
        elif signalId == 253:
            signal = entry.AverageXLowerAverageY(self, "close", 120, "open", 120)
        # </editor-fold>