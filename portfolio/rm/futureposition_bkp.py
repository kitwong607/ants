from numpy import sign
from datetime import timedelta
import pandas as pd
from enum import IntEnum

from .base import Position
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
    def __init__(
        self, order):

        self.action = order.action
        self.ticker = order.ticker
        self.dataTicker = order.dataTicker
        self.exchange = order.exchange
        self.quantity = order.quantity
        self.commission = order.commission


        self.lastUpdateTime = order.filledTime
        self.entryTime = order.filledTime
        self.exitTime = None
        self.entryPrice = self.filledPrice
        self.entryLabel = order.label
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
            self.exitTime = order.timestamp
            self.status = PositionStatus.CLOSED

            self.pnl = ((self.avgEntryPrice - self.avgExitPrice) * self.maxNet) * self.pricePerUnit - self.commission

            if self.pnl > 0:
                self.result = PositionResult.WIN
            else:
                self.result = PositionResult.LOSS


    def TransactOrder(self, order):
        # Adjust total bought and sold
        if order.action == OrderAction.BUY:
            self.avgBotPrice = ((self.avgBotPrice * self.buyQty) + (order.filledPrice * order.quantity)) / (self.buyQty + order.quantity)
            self.buyQty += order.quantity
            self.totalBotQty += order.quantity

        elif order.action == OrderAction.SELL:
            self.avgSldPrice = ((self.avgSldPrice * self.sellQty) + (order.filledPrice * order.quantity)) / (self.sellQty + order.quantity)
            self.sellQty += order.quantity
            self.totalSldQty += order.quantity
        else:
            return

        self.commission += order.commission
        self.UpdateMaxNet(order)


    def Life(self):
        return utilities.secondBetweenTwoDatetime(self.entryTime, self.lastUpdateTime)


    def to_dict(self):
        timeOffset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[self.exchange])

        d = {}
        d['positionId'] = None
        d['date'] = utilities.dtGetDateStr(self.entryTime)
        d['dateTS'] = (self.entryTime + timeOffset).timestamp()
        d['ticker'] = self.ticker
        d['dataTicker'] = self.dataTicker
        d['action'] = self.action

        d['entryTime'] = utilities.dtGetDateStr(self.entryTime)
        d['exitTime'] = utilities.dtGetDateStr(self.exitTime)
        d['entryTimestamp'] = (self.entryTime + timeOffset).timestamp()
        d['exitTimestamp'] = (self.exitTime + timeOffset).timestamp()

        d['entryLabel'] = self.entryLabel
        d['exitLabel'] = self.exitLabel

        d['adjustedDate'] = self.adjustedDate
        d['adjustedTime'] = self.adjustedTime

        d['entryPrice'] = self.entryPrice
        d['exitPrice'] = self.exitPrice

        d['avgEntryPrice'] = self.avgEntryPrice
        d['avgExitPrice'] = self.avgExitPrice

        d['qty'] = self.maxNet
        d['pnl'] = self.pnl
        d['net_pips'] = self.pnl / self.pricePerUnit
        d['net_pips_pre_contract'] = self.pnl / self.pricePerUnit / self.maxNet

        d['commission'] = self.commission

        d['botQty'] = self.botQty
        d['sldQty'] = self.sldQty
        d['avgBotPrice'] = self.avgBotPrice
        d['avgSldPrice'] = self.avgSldPrice
        d['result'] = self.result

        return d
# endregion


# region Future Position
class FuturePosition(Position):
    def __init__(self, order):
        super.__init__(order)

        if (self.ticker == 'MHI' or self.ticker == 'MCH'):
            self.pricePerUnit = 10
        else:
            self.pricePerUnit = 50
# endregion







