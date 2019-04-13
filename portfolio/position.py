from numpy import sign
from datetime import timedelta
import pandas as pd
from enum import IntEnum

from .. import utilities, static
from ..order.base import OrderAction

from numpy import sign


# region Class: PositionStatus
class PositionStatus(IntEnum):
    OPEN = 0
    CLOSED = 1
# endregion


# region Class: PositionResult
class PositionResult(IntEnum):
    WIN = 0
    LOSS = 1
# endregion


# region Class: Position
class Position(object):
    def __init__(self, order):

        self.action = order.action
        self.ticker = order.ticker
        self.exchange = order.exchange
        self.quantity = order.totalQuantity
        self.commission = order.commission


        self.lastUpdateTime = order.filledTime
        self.entryTime = order.filledTime
        self.exitTime = None

        self.entryPrice = order.filledPrice

        self.entryLabel = order.label
        self.exitLabel = ""

        self.pricePerUnit = 1
        self.orders = [order]

        self.pnl = 0
        self.maxNet = 0
        self.buyQty = 0
        self.sellQty = 0
        self.avgBotPrice = 0
        self.avgSldPrice = 0
        self.totalBotQty = 0
        self.totalSldQty = 0
        if self.action == OrderAction.BUY:
            self.maxNet = self.quantity
            self.buyQty = self.quantity
            self.totalBotQty = self.quantity
            self.avgBotPrice = self.entryPrice
        else:
            self.maxNet = self.quantity * -1
            self.sellQty = self.quantity
            self.totalSldQty = self.quantity
            self.avgSldPrice = self.entryPrice


        self.entryAdjustedDate = order.adjustedDate
        self.entryAdjustedTime = order.adjustedTime
        self.status = PositionStatus.OPEN

        self.totalSlippage = order.slippage


    def Update(self, bar):
        self.lastUpdateTime = bar.timestamp


    def UpdateMaxNet(self, order):
        if self.action == OrderAction.BUY:
            self.maxNet = max(self.maxNet, self.buyQty)
            self.avgEntryPrice = self.avgBotPrice
            self.avgExitPrice = self.avgSldPrice

        elif self.action == OrderAction.SELL:
            self.maxNet = max(self.maxNet, self.sellQty) * -1
            self.avgEntryPrice = self.avgSldPrice
            self.avgExitPrice = self.avgBotPrice
        else:
            return

        self.net = self.buyQty - self.sellQty
        self.quantity = self.net


        if self.quantity == 0:
            self.exitLabel = order.label
            self.exitTime = order.filledTime
            self.exitAdjustedDate = order.adjustedDate
            self.exitAdjustedTime = order.adjustedTime
            self.status = PositionStatus.CLOSED

            self.pnl = 0
            if self.action == OrderAction.BUY:
                self.pnl = (
                           (self.avgExitPrice - self.avgEntryPrice) * self.maxNet) * self.pricePerUnit - self.commission
            elif self.action == OrderAction.SELL:
                self.pnl = (
                           (self.avgEntryPrice - self.avgExitPrice) * self.maxNet * -1) * self.pricePerUnit - self.commission
            else:
                raise ValueError('Incorrect action type')



            if self.pnl > 0:
                self.result = PositionResult.WIN
            else:
                self.result = PositionResult.LOSS


    def TransactOrder(self, order):
        # Adjust total bought and sold
        if order.action == OrderAction.BUY:
            self.avgBotPrice = ((self.avgBotPrice * self.buyQty) + (order.filledPrice * order.totalQuantity)) / (self.buyQty + order.totalQuantity)
            self.buyQty += order.totalQuantity
            self.totalBotQty += order.totalQuantity

        elif order.action == OrderAction.SELL:
            self.avgSldPrice = ((self.avgSldPrice * self.sellQty) + (order.filledPrice * order.totalQuantity)) / (self.sellQty + order.totalQuantity)
            self.sellQty += order.totalQuantity
            self.totalSldQty += order.totalQuantity
        else:
            return
        self.totalSlippage += order.slippage
        self.commission += order.commission
        self.UpdateMaxNet(order)


    def Life(self):
        return utilities.secondBetweenTwoDatetime(self.entryTime, self.lastUpdateTime)


    def ToDict(self):
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.exchange])

        d = {}
        d['positionId'] = None
        d['date'] = utilities.dtGetDateStr(self.entryTime)
        d['dateTS'] = (self.entryTime + timeOffset).timestamp()
        d['ticker'] = self.ticker


        if self.action == OrderAction.BUY:
            d['action'] = "BUY"
        elif self.action == OrderAction.SELL:
            d['action'] = "SELL"


        d['entryTime'] = utilities.dtGetTimeStr(self.entryTime)
        d['exitTime'] = utilities.dtGetTimeStr(self.exitTime)
        d['entryDate'] = utilities.dtGetDateStr(self.entryTime)
        d['exitDate'] = utilities.dtGetDateStr(self.exitTime)
        d['entryTimestamp'] = (self.entryTime + timeOffset).timestamp()
        d['exitTimestamp'] = (self.exitTime + timeOffset).timestamp()

        d['entryLabel'] = self.entryLabel
        d['exitLabel'] = self.exitLabel

        d['entryAdjustedDate'] = self.entryAdjustedDate
        d['entryAdjustedTime'] = self.entryAdjustedTime
        d['exitAdjustedDate'] = self.exitAdjustedDate
        d['exitAdjustedTime'] = self.exitAdjustedTime

        d['avgEntryPrice'] = self.avgEntryPrice
        d['avgExitPrice'] = self.avgExitPrice

        d['qty'] = self.maxNet
        d['pnl'] = self.pnl
        d['netPips'] = self.pnl / self.pricePerUnit
        d['netPipsPreContract'] = self.pnl / self.pricePerUnit / self.maxNet

        d['totalSlippage'] = self.totalSlippage
        d['commission'] = self.commission

        d['buyQty'] = self.buyQty
        d['sellQty'] = self.sellQty
        d['avgBotPrice'] = self.avgBotPrice
        d['avgSldPrice'] = self.avgSldPrice

        if self.result == PositionResult.WIN:
            d['result'] = "WIN"
        else:
            d['result'] = "LOSS"

        return d
# endregion


# region Future Position
class FuturePosition(Position):
    IS_DISPLAY_IN_OPTION = False

    def __init__(self, order):
        super().__init__(order)

        if (self.ticker == 'MHI' or self.ticker == 'MCH'):
            self.pricePerUnit = 10
        else:
            self.pricePerUnit = 50
# endregion
