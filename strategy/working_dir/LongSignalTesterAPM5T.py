from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LongSignalTesterAPM5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    SELECTED_SIGNAL = [
                        # 1 Breakout previous day high
                        1, 2, 3, 4, 5,

                        # 24 Breakout previous high with delay
                        7, 8, 10,
                       11, 12,     14, 15, 16, 17, 18, 19, 20,
                       21,         24, 25,

                        # 2 Breakout previous day low
                                                           30,
                       31, 32, 33, 34,

                        # 25 Breakout previous low with delay
                                       35, 36, 37, 38, 39, 40,
                       41, 42, 43, 44, 45, 46,

                        # 3 Breakout previous day open
                                               47, 48, 49, 50,
                       51, 52,


                        # 26 Breakout previous open with delay
                               53, 54, 55, 56, 57, 58, 59, 60,
                       61, 62, 63, 64, 65,

                        # 4 Breakout previous day close
                                               77, 78, 79, 80,
                       81, 82,

                        # 27 Breakout previous day close with delay
                               83, 84, 85, 86, 87, 88, 89, 90,
                       91, 92, 93, 94, 95, 96, 97,     99,
                       101,      103,

                        # 5 Breakout previous intra day price channel high
                                                     107, 108, 109, 110,
                       111, 112, 113,

                        # 28 Breakout previous intra day price channel high with delay
                                      114, 115, 116, 117, 118, 119, 120,
                       121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
                       131, 132, 133, 134, 135, 136, 137,

                        # 6 Breakout previous intra day price channel low

                        # 29 Breakout previous intra day price channel low with delay
                                           145, 146, 147, 148, 149, 150,
                       151, 152, 153, 154, 155, 156, 157, 158, 159,

                        # 7 Daily higher open
                                 173, 174, 175, 176, 177, 178,

                        # 8 Daily lower open

                        # 9 Daily higher high
                                                               179, 180,
                       181, 182, 183, 184,

                        # 10 Daily lower high

                        # 11 Daily higher low
                                           185, 186, 187, 188, 189, 190,
                       191,

                        # 12 Daily lower low

                        # 13 Daily higher close
                            192, 193, 194, 195,

                        # 14 Daily lower close

                        # 15 Intra day higher high
                                                196, 197, 198, 199, 200,
                       201, 202, 203,

                        # 16 Intra day lower high

                        # 17 Intra day higher low
                                      204, 205, 206, 207, 208, 209, 210,
                       211,

                        # 18 Intra day lower low

                        # 19 Open higher lower pivot point
                            212,      214,      216, 217, 218,
                       221, 222,      224, 225,

                        # 20 close cross pivot point

                        # 21 higher or lower pivot point
                                                226,      228,      230,
                       231,

                        # 22 RSI related
                                 233, 234,

                        # 23 Intra day SMA related
                                                236, 237, 238, 239, 240,
                       241, 242, 243, 244, 245, 246, 247, 248,

                        # 30 Close Higher Morning OHLC
                        254, 255, 256, 257,

                        # 31 Close Higher Morning OHLC with delay
                        258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273,

                        # 32 Lower Morning OHLC
                        274, 275, 276, 277,

                        # 33 Lower Morning OHLC with delay
                        278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293,

                        # 34 Intra day MACD cross
                        294, 295, 296,

                        # 35 Intra day MACD cross with delay
                        297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311,

                        # 36 Inter day MACD cross
                        312, 313, 314,

                        # 37 Intra day Stochastic cross
                        315, 316, 317, 318,

                        # 38 Intra day Stochastic cross with delay
                        319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334,

                        # 39 Inter day Stochastic cross
                        335, 336, 337, 338,

                        # 40 Intra day Stochastic Fast cross
                        339, 340, 341, 342,

                        # 41 Intra day Stochastic Fast cross with delay
                        343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358,

                        # 42 Inter day Stochastic Fast cross
                        359, 360, 361, 362,

                        # 43 Intra day Stochastic Relative Strength Index cross
                        363, 364, 365, 366,

                        # 44 Intra day Stochastic Relative Strength Index cross with delay
                        367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382,

                        # 45 Inter day Stochastic Relative Strength Index cross
                        383, 384, 385, 386,

                        # 46 Intra day Stochastic Higher than threshold
                        387, 388, 389, 390,

                        # 47 Intra day Stochastic Higher than threshold with delay
                        391, 392, 393, 394, 395, 396,

                        # 48 Inter day Stochastic Higher than threshold with delay
                        397, 398,

                        # 49 Intra day Stochastic Lower than threshold
                        399, 400, 401, 402,

                        # 50 Intra day Stochastic Lower than threshold with delay
                        403, 404, 405, 406, 407, 408,

                        # 51 Inter day Stochastic Lower than threshold with delay
                        409, 410,

                        # 52 Intra day Stochastic fast Higher than threshold
                        411, 412, 413, 414,

                        # 53 Intra day Stochastic fast Higher than threshold with delay
                        415, 416, 417, 418, 419, 420,

                        # 54 Inter day Stochastic fast Higher than threshold with delay
                        421, 422,

                        # 55 Intra day Stochastic fast Lower than threshold
                        423, 424, 425, 426,

                        # 56 Intra day Stochastic fast Lower than threshold with delay
                        427, 428, 429, 430, 431, 432,

                        # 57 Inter day Stochastic fast Lower than threshold with delay
                        433, 434,

                        # 58 Intra day Stochastic RSI Higher than threshold
                        435, 436, 437, 438,

                        # 59 Intra day Stochastic RSI Higher than threshold with delay
                        439, 440, 441, 442, 443, 444,

                        # 60 Inter day Stochastic RSI Higher than threshold with delay
                        445, 446,

                        # 61 Intra day Stochastic RSI Lower than threshold
                        447, 448, 449, 450,

                        # 62 Intra day Stochastic RSI Lower than threshold with delay
                        451, 452, 453, 454, 455, 456,

                        # 63 Inter day Stochastic RSI Lower than threshold with delay
                        457, 458,

                        # 64 Intra day Higher KAMA
                        459, 460, 461,

                        # 65 Intra day Higher KAMA with delay
                        462, 463, 464, 465, 466, 467, 468, 469, 470,

                        # 66 Inter day Higher KAMA
                        471, 472, 473, 474, 475,

                        # 67 Intra day Higher BBANDS
                        476, 477, 478,

                        # 68 Intra day Higher BBANDS with delay
                        479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490,

                        # 69 Inter day Higher BBANDS
                        491, 492, 493,

                        # 70 Inter day BBANDS width change
                        494, 495
                                    ]
    NUM_SIGNAL = len(SELECTED_SIGNAL)
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": -1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_4": {"name": "signalId_4", "value": -1, "min": 1, "max": NUM_SIGNAL, "step": 1},
    }

    STRATEGY_NAME = "Long Signal Tester APM 5T"
    STRATEGY_SLUG = "LongSignalTesterAPM5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190410"
    LAST_UPDATE_TIME = "133000"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000, "END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        signalNo1 = self.parameter["signalId_1"]["value"]
        signalNo2 = self.parameter["signalId_2"]["value"]
        signalNo3 = self.parameter["signalId_3"]["value"]
        signalNo4 = self.parameter["signalId_4"]["value"]

        self.SetupSignal(signalNo1)
        if signalNo2 != -1:
            self.SetupSignal(signalNo2)
            if signalNo3 != -1:
                self.SetupSignal(signalNo3)
                if signalNo4 != -1:
                    self.SetupSignal(signalNo4)

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

        if count == len(self.entrySignals):
            self.Entry(bar, OrderType.MARKET, label, self.baseQuantity)


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

    # 30 Close Higher Morning OHLC
    # 31 Close Higher Morning OHLC with delay
    # 32 Lower Morning OHLC
    # 33 Lower Morning OHLC with delay

    # 34 Intra day MACD cross
    # 35 Intra day MACD cross with delay
    # 36 Inter day MACD cross

    # 37 Intra day Stochastic cross
    # 38 Intra day Stochastic cross with delay
    # 39 Inter day Stochastic cross

    # 40 Intra day Stochastic Fast cross
    # 41 Intra day Stochastic Fast cross with delay
    # 42 Inter day Stochastic Fast cross

    # 43 Intra day Stochastic Relative Strength Index cross
    # 44 Intra day Stochastic Relative Strength Index cross with delay
    # 45 Inter day Stochastic Relative Strength Index cross

    # 46 Intra day Stochastic Higher than threshold

    # 47 Intra day Stochastic Higher than threshold with delay

    # 48 Inter day Stochastic Higher than threshold with delay

    # 49 Intra day Stochastic Lower than threshold

    # 50 Intra day Stochastic Lower than threshold with delay

    # 51 Inter day Stochastic Lower than threshold with delay

    # 52 Intra day Stochastic fast Higher than threshold

    # 53 Intra day Stochastic fast Higher than threshold with delay

    # 54 Inter day Stochastic fast Higher than threshold with delay

    # 55 Intra day Stochastic fast Lower than threshold

    # 56 Intra day Stochastic fast Lower than threshold with delay

    # 57 Inter day Stochastic fast Lower than threshold with delay

    # 58 Intra day Stochastic RSI Higher than threshold

    # 59 Intra day Stochastic RSI Higher than threshold with delay

    # 60 Inter day Stochastic RSI Higher than threshold with delay

    # 61 Intra day Stochastic RSI Lower than threshold

    # 62 Intra day Stochastic RSI Lower than threshold with delay

    # 63 Inter day Stochastic RSI Lower than threshold with delay

    # 64 Intra day Higher KAMA

    # 65 Intra day Higher KAMA with delay

    # 66 Inter day Higher KAMA

    # 67 Intra day Higher BBANDS

    # 68 Intra day Higher BBANDS with delay

    # 69 Inter day Higher BBANDS

    # 70 Inter day BBANDS width change

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

        # <editor-fold desc="# 14 Daily lower close">f
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

        # <editor-fold desc="# 30 Close Higher Morning OHLC">
        elif signalId == 254:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0)
        elif signalId == 255:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0)
        elif signalId == 256:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0)
        elif signalId == 257:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0)
        # </editor-fold>

        # <editor-fold desc="# 31 Close Higher Morning OHLC with delay">
        elif signalId == 258:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0, 2)
        elif signalId == 259:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0, 2)
        elif signalId == 260:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0, 2)
        elif signalId == 261:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0, 2)

        elif signalId == 262:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0, 4)
        elif signalId == 263:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0, 4)
        elif signalId == 264:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0, 4)
        elif signalId == 265:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0, 4)

        elif signalId == 266:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0, 6)
        elif signalId == 267:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0, 6)
        elif signalId == 268:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0, 6)
        elif signalId == 269:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0, 6)

        elif signalId == 270:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0, 8)
        elif signalId == 271:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0, 8)
        elif signalId == 272:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0, 8)
        elif signalId == 273:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0, 8)
        # </editor-fold>

        # <editor-fold desc="# 32 Lower Morning OHLC">
        elif signalId == 274:
            signal = entry.XLowerY(self, "close", 0, "morningOpenD", 0)
        elif signalId == 275:
            signal = entry.XLowerY(self, "close", 0, "morningHighD", 0)
        elif signalId == 276:
            signal = entry.XLowerY(self, "close", 0, "morningLowD", 0)
        elif signalId == 277:
            signal = entry.XLowerY(self, "close", 0, "morningCloseD", 0)
        # </editor-fold>

        # <editor-fold desc="# 33 Lower Morning OHLC with delay">
        elif signalId == 278:
            signal = entry.XLowerY(self, "close", 0, "morningOpenD", 0, 2)
        elif signalId == 279:
            signal = entry.XLowerY(self, "close", 0, "morningHighD", 0, 2)
        elif signalId == 280:
            signal = entry.XLowerY(self, "close", 0, "morningLowD", 0, 2)
        elif signalId == 281:
            signal = entry.XLowerY(self, "close", 0, "morningCloseD", 0, 2)

        elif signalId == 282:
            signal = entry.XLowerY(self, "close", 0, "morningOpenD", 0, 4)
        elif signalId == 283:
            signal = entry.XLowerY(self, "close", 0, "morningHighD", 0, 4)
        elif signalId == 284:
            signal = entry.XLowerY(self, "close", 0, "morningLowD", 0, 4)
        elif signalId == 285:
            signal = entry.XLowerY(self, "close", 0, "morningCloseD", 0, 4)

        elif signalId == 286:
            signal = entry.XLowerY(self, "close", 0, "morningOpenD", 0, 6)
        elif signalId == 287:
            signal = entry.XLowerY(self, "close", 0, "morningHighD", 0, 6)
        elif signalId == 288:
            signal = entry.XLowerY(self, "close", 0, "morningLowD", 0, 6)
        elif signalId == 289:
            signal = entry.XLowerY(self, "close", 0, "morningCloseD", 0, 6)

        elif signalId == 290:
            signal = entry.XLowerY(self, "close", 0, "morningOpenD", 0, 8)
        elif signalId == 291:
            signal = entry.XLowerY(self, "close", 0, "morningHighD", 0, 8)
        elif signalId == 292:
            signal = entry.XLowerY(self, "close", 0, "morningLowD", 0, 8)
        elif signalId == 293:
            signal = entry.XLowerY(self, "close", 0, "morningCloseD", 0, 8)
        # </editor-fold>

        # <editor-fold desc="# 34 Intra day MACD cross">
        elif signalId == 294:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4)
        elif signalId == 295:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9)
        elif signalId == 296:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14)
        # </editor-fold>

        # <editor-fold desc="# 35 Intra day MACD cross with delay">
        elif signalId == 297:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 2)
        elif signalId == 298:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 2)
        elif signalId == 299:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 2)


        elif signalId == 300:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 4)
        elif signalId == 301:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 4)
        elif signalId == 302:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 4)


        elif signalId == 303:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 6)
        elif signalId == 304:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 6)
        elif signalId == 305:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 6)


        elif signalId == 306:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 8)
        elif signalId == 307:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 8)
        elif signalId == 308:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 8)


        elif signalId == 309:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 10)
        elif signalId == 310:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 10)
        elif signalId == 311:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 10)
        # </editor-fold>

        # <editor-fold desc="# 36 Inter day MACD cross">
        elif signalId == 312:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 6, 13, 4, 1)
        elif signalId == 313:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 12, 26, 9, 1)
        elif signalId == 314:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 18, 39, 14, 1)
        # </editor-fold>

        # <editor-fold desc="# 37 Intra day Stochastic cross">
        elif signalId == 315:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
        elif signalId == 316:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
        elif signalId == 317:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
        elif signalId == 318:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
        # </editor-fold>

        # <editor-fold desc="# 38 Intra day Stochastic cross with delay">
        elif signalId == 319:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 2)
        elif signalId == 320:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 2)
        elif signalId == 321:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 2)
        elif signalId == 322:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 2)


        elif signalId == 323:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 4)
        elif signalId == 324:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 4)
        elif signalId == 325:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 4)
        elif signalId == 326:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 4)


        elif signalId == 327:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 6)
        elif signalId == 328:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 6)
        elif signalId == 329:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 6)
        elif signalId == 330:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 6)


        elif signalId == 331:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 8)
        elif signalId == 332:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 8)
        elif signalId == 333:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 8)
        elif signalId == 334:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 8)
        # </editor-fold>

        # <editor-fold desc="# 39 Inter day Stochastic cross">
        elif signalId == 335:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 1)
        elif signalId == 336:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 1)
        elif signalId == 337:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 1)
        elif signalId == 338:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 1)
        # </editor-fold>

        # <editor-fold desc="# 40 Intra day Stochastic Fast cross">
        elif signalId == 339:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
        elif signalId == 340:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
        elif signalId == 341:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
        elif signalId == 342:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
        # </editor-fold>

        # <editor-fold desc="# 41 Intra day Stochastic Fast cross with delay">
        elif signalId == 343:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3 )
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 2)
        elif signalId == 344:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 2)
        elif signalId == 345:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 2)
        elif signalId == 346:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 2)

        elif signalId == 347:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 4)
        elif signalId == 348:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 4)
        elif signalId == 349:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 4)
        elif signalId == 350:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 4)

        elif signalId == 351:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 6)
        elif signalId == 352:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 6)
        elif signalId == 353:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 6)
        elif signalId == 354:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 6)

        elif signalId == 355:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 8)
        elif signalId == 356:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 8)
        elif signalId == 357:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 8)
        elif signalId == 358:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 8)
        # </editor-fold>

        # <editor-fold desc="# 42 Inter day Stochastic Fast cross">
        elif signalId == 359:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 1)
        elif signalId == 360:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 1)
        elif signalId == 361:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 1)
        elif signalId == 362:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 1)
        # </editor-fold>

        # <editor-fold desc="# 43 Intra day Stochastic Relative Strength Index cross">
        elif signalId == 363:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
        elif signalId == 364:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
        elif signalId == 365:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
        elif signalId == 366:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
        # </editor-fold>

        # <editor-fold desc="# 44 Intra day Stochastic Relative Strength Index cross with delay">
        elif signalId == 367:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3, 2)
        elif signalId == 368:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 2)
        elif signalId == 369:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6, 2)
        elif signalId == 370:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 2)


        elif signalId == 371:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3, 4)
        elif signalId == 372:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 4)
        elif signalId == 373:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6, 4)
        elif signalId == 374:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 4)


        elif signalId == 375:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3, 6)
        elif signalId == 376:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 6)
        elif signalId == 377:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6, 6)
        elif signalId == 378:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 6)


        elif signalId == 379:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3, 8)
        elif signalId == 380:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 8)
        elif signalId == 381:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6, 8)
        elif signalId == 382:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 8)
        # </editor-fold>

        # <editor-fold desc="# 45 Inter day Stochastic Relative Strength Index cross">
        elif signalId == 383:
            signal = entry.StochasticRSIKHigherD(self, "closeD", 14, 5, 3)
        elif signalId == 384:
            signal = entry.StochasticRSIKLowerD(self, "closeD", 14, 5, 3)
        elif signalId == 385:
            signal = entry.StochasticRSIKHigherD(self, "closeD", 14, 10, 6)
        elif signalId == 386:
            signal = entry.StochasticRSIKLowerD(self, "closeD", 14, 10, 6)
        # </editor-fold>

        # <editor-fold desc="# 46 Intra day Stochastic Higher than threshold">
        elif signalId == 387:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 80)
        elif signalId == 388:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 80)
        elif signalId == 389:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20)
        elif signalId == 390:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 47 Intra day Stochastic Higher than threshold with delay">
        elif signalId == 391:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 80, 2)
        elif signalId == 392:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 80, 2)
        elif signalId == 393:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20, 4)
        elif signalId == 394:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20, 4)
        elif signalId == 395:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20, 6)
        elif signalId == 396:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 48 Inter day Stochastic Higher than threshold">
        elif signalId == 397:
            signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 20)
        elif signalId == 398:
            signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 49 Intra day Stochastic Lower than threshold">
        elif signalId == 399:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 80)
        elif signalId == 400:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 80)
        elif signalId == 401:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20)
        elif signalId == 402:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 50 Intra day Stochastic Lower than threshold with delay">
        elif signalId == 403:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 80, 2)
        elif signalId == 404:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 80, 2)
        elif signalId == 405:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20, 4)
        elif signalId == 406:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20, 4)
        elif signalId == 407:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20, 6)
        elif signalId == 408:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 51 Inter day Stochastic Lower than threshold">
        elif signalId == 409:
            signal = entry.StochasticSlowLowerThreshold(self, "closeD", 5, 3, 3, 20)
        elif signalId == 410:
            signal = entry.StochasticSlowLowerThreshold(self, "closeD", 5, 3, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 52 Intra day Stochastic fast Higher than threshold">
        elif signalId == 411:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 80)
        elif signalId == 412:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 80)
        elif signalId == 413:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20)
        elif signalId == 414:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 53 Intra day Stochastic fast Higher than threshold with delay">
        elif signalId == 415:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 80, 2)
        elif signalId == 416:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 80, 2)
        elif signalId == 417:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20, 4)
        elif signalId == 418:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20, 4)
        elif signalId == 419:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20, 6)
        elif signalId == 420:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 54 Inter day Stochastic fast Higher than threshold">
        elif signalId == 421:
            signal = entry.StochasticFastHigherThreshold(self, "closeD", 5, 3, 20)
        elif signalId == 422:
            signal = entry.StochasticFastHigherThreshold(self, "closeD", 5, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 55 Intra day Stochastic fast Lower than threshold">
        elif signalId == 423:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 80)
        elif signalId == 424:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 80)
        elif signalId == 425:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20)
        elif signalId == 426:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 56 Intra day Stochastic fast Lower than threshold with delay">
        elif signalId == 427:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 80, 2)
        elif signalId == 428:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 80, 2)
        elif signalId == 429:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20, 4)
        elif signalId == 430:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20, 4)
        elif signalId == 431:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20, 6)
        elif signalId == 432:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 57 Inter day Stochastic fast Lower than threshold">
        elif signalId == 433:
            signal = entry.StochasticFastLowerThreshold(self, "closeD", 5, 3, 20)
        elif signalId == 434:
            signal = entry.StochasticFastLowerThreshold(self, "closeD", 5, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 58 Intra day Stochastic RSI Higher than threshold">
        elif signalId == 435:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 80)
        elif signalId == 436:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 80)
        elif signalId == 437:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20)
        elif signalId == 438:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 59 Intra day Stochastic RSI Higher than threshold with delay">
        elif signalId == 439:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 80, 2)
        elif signalId == 440:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 80, 2)
        elif signalId == 441:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20, 4)
        elif signalId == 442:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20, 4)
        elif signalId == 443:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20, 6)
        elif signalId == 444:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 60 Inter day Stochastic RSI Higher than threshold">
        elif signalId == 445:
            signal = entry.StochasticRSIHigherThreshold(self, "closeD", 14, 5, 3, 20)
        elif signalId == 446:
            signal = entry.StochasticRSIHigherThreshold(self, "closeD", 14, 5, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 61 Intra day Stochastic RSI Lower than threshold">
        elif signalId == 447:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 80)
        elif signalId == 448:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 80)
        elif signalId == 449:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20)
        elif signalId == 450:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 62 Intra day Stochastic RSI Lower than threshold with delay">
        elif signalId == 451:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 80, 2)
        elif signalId == 452:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 80, 2)
        elif signalId == 453:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20, 4)
        elif signalId == 454:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20, 4)
        elif signalId == 455:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20, 6)
        elif signalId == 456:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 63 Inter day Stochastic RSI Lower than threshold">
        elif signalId == 457:
            signal = entry.StochasticRSILowerThreshold(self, "closeD", 14, 5, 3, 20)
        elif signalId == 458:
            signal = entry.StochasticRSILowerThreshold(self, "closeD", 14, 5, 3, 80)
        # </editor-fold>

        # <editor-fold desc="# 64 Intra day Higher KAMA">
        elif signalId == 459:
            signal = entry.XHigherKAMA(self, "close", 10)
        elif signalId == 460:
            signal = entry.XHigherKAMA(self, "close", 20)
        elif signalId == 461:
            signal = entry.XHigherKAMA(self, "close", 30)
        # </editor-fold>

        # <editor-fold desc="# 65 Intra day Higher KAMA with delay">
        elif signalId == 462:
            signal = entry.XHigherKAMA(self, "close", 10, 2)
        elif signalId == 463:
            signal = entry.XHigherKAMA(self, "close", 10, 4)
        elif signalId == 464:
            signal = entry.XHigherKAMA(self, "close", 10, 6)
        elif signalId == 465:
            signal = entry.XHigherKAMA(self, "close", 20, 2)
        elif signalId == 466:
            signal = entry.XHigherKAMA(self, "close", 20, 4)
        elif signalId == 467:
            signal = entry.XHigherKAMA(self, "close", 20, 6)
        elif signalId == 468:
            signal = entry.XHigherKAMA(self, "close", 30, 2)
        elif signalId == 469:
            signal = entry.XHigherKAMA(self, "close", 30, 4)
        elif signalId == 470:
            signal = entry.XHigherKAMA(self, "close", 30, 6)
        # </editor-fold>

        # <editor-fold desc="# 66 Inter day Higher KAMA">
        elif signalId == 471:
            signal = entry.XHigherKAMA(self, "closeD", 10)
        elif signalId == 472:
            signal = entry.XHigherKAMA(self, "closeD", 15)
        elif signalId == 473:
            signal = entry.XHigherKAMA(self, "closeD", 20)
        elif signalId == 474:
            signal = entry.XHigherKAMA(self, "closeD", 30)
        elif signalId == 475:
            signal = entry.XHigherKAMA(self, "closeD", 60)
        # </editor-fold>

        # <editor-fold desc="# 67 Intra day Higher BBANDS">
        elif signalId == 476:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
        elif signalId == 477:
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
        elif signalId == 478:
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
        # </editor-fold>

        # <editor-fold desc="# 68 Intra day Higher BBANDS with delay">
        elif signalId == 479:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 2)
        elif signalId == 480:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 4)
        elif signalId == 481:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 6)
        elif signalId == 482:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 8)

        elif signalId == 483:
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 2)
        elif signalId == 484:
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 4)
        elif signalId == 485:
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 6)
        elif signalId == 486:
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 8)

        elif signalId == 487:
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 2)
        elif signalId == 488:
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 4)
        elif signalId == 489:
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 6)
        elif signalId == 490:
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 8)
        # </editor-fold>

        # <editor-fold desc="# 69 Inter day Higher BBANDS">
        elif signalId == 491:
            signal = entry.XHigherBBandsUpper(self, "closeD", 20, 2)
        elif signalId == 492:
            signal = entry.XHigherBBandsMiddle(self, "closeD", 20, 2)
        elif signalId == 493:
            signal = entry.XHigherBBandsLower(self, "closeD", 20, 2)
        # </editor-fold>

        # <editor-fold desc="# 70 Inter day BBANDS width change">
        elif signalId == 491:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 6, 0.5)
        elif signalId == 492:
            signal = entry.WiderBBands(self, "close", 20, 2, 6, 1.5)
        # </editor-fold>