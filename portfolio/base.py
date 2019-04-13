import json

from abc import ABCMeta
from enum import Enum
from datetime import timedelta
from ..order.base import OrderAction
from .. import utilities, static
from .position import PositionStatus
from ..session import SessionMode


class AbstractPortfolio(object):
    __metaclass__ = ABCMeta

    def __init__(self, session):
        self.session 				 = session
        self.config 				 = session.config
        self.curCash = self.initCash = session.config.cash

        self.Log = self.session.Log

        self.positions = {}
        self.closedPositions = []

        self.positionRecords = []
        self.orderRecords = []

    def CurrentPosition(self):
        if self.config.tradeTicker in self.positions:
            return self.positions[self.config.tradeTicker]
        return None

    def TransactOrder(self, order):
        if order.ticker not in self.positions:
            print("TransactOrder: Add", order.ticker, order.action)
            self.AddPosition(order)
        else:
            print("ModifyPosition: Add", order.ticker, order.action)
            self.ModifyPosition(order)

        self.RecordOrder(order)

    def ModifyPosition(self, order):
        self.positions[order.ticker].TransactOrder(order)
        print("ModifyPosition:", self.positions[order.ticker].status, self.positions[order.ticker].quantity)
        if self.positions[order.ticker].status == PositionStatus.CLOSED:
            closedPosition = self.positions.pop(order.ticker)
            self.RecordPosition(closedPosition)
            self.closedPositions.append(closedPosition)



    def RecordPosition(self, position):
        record = position.ToDict()
        record['positionId'] = len(self.positionRecords) + 1
        self.positionRecords.append(record)

    def OrderToDict(self, order):
        time_offset = timedelta(minutes=static.EXCHANGE_TIME_ZONE[order.exchange])
        d = {}

        d['orderId'] = order.orderId
        d['ticker'] = order.ticker
        d['exchange'] = order.exchange
        d['contract'] = self.ContractToDict(order.contract)
        d['price'] = order.filledPrice
        d['signalPrice'] = order.signalPrice
        if order.action == OrderAction.BUY:
            d['action'] = "BUY"
        elif order.action == OrderAction.SELL:
            d['action'] = "SELL"
        else:
            d['action'] = "None"

        d['stopLoss'] = order.stopLossThreshold
        d['quantity'] = order.totalQuantity
        d['label'] = order.label
        d['type'] = order.type
        d['status'] = order.status
        d['filledPrice'] = order.filledPrice
        d['adjustedDate'] = order.adjustedDate
        d['adjustedTime'] = order.adjustedTime
        d['date'] = utilities.getDateStrFromDt(order.filledTime)
        d['time'] = utilities.getTimeStrFromDt(order.filledTime)
        d['timestamp'] = (order.filledTime + time_offset).timestamp()
        d['commission'] = order.commission
        d['slippage'] = order.slippage

        return d

    def ContractToDict(self, contract):
        d = {}
        d['symbol'] = contract.symbol
        d['secType'] = contract.secType
        d['currency'] = contract.currency
        d['exchange'] = contract.exchange
        d['code'] = contract.code
        d['ticker'] = contract.ticker
        d['expiryMonth'] = contract.expiryMonth
        return d


    def RecordOrder(self, order):
        self.orderRecords.append(self.OrderToDict(order))


    def EntryQty(self, ticker):
        if ticker not in self.positions:
            return 0

        if self.positions[ticker].action == OrderAction.BUY:
            return self.positions[ticker].buyQty
        elif self.positions[ticker].action == OrderAction.SELL:
            return self.positions[ticker].sellQty


    def ExitQty(self, ticker):
        if ticker not in self.positions:
            return 0

        if self.positions[ticker].action == OrderAction.BUY:
            return self.positions[ticker].sellQty
        elif self.positions[ticker].action == OrderAction.SELL:
            return self.positions[ticker].buyQty


    def GetOpenPosition(self):
        return self.positions


    def GetOpenPositionByTicker(self, ticker):
        if ticker in self.positions:
            return self.positions[ticker]
        return False


    def GetLastUpdateTimestamp(self):
        return self.lastUpdateTimestamp


    def Save(self):
        #For live and daily backtest: merge previous positions and orders
        if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
            jsonFilename = "//positions.json"
            if utilities.checkFileExist(self.session.config.reportDirectory + jsonFilename):
                with open(self.session.config.reportDirectory + jsonFilename, 'r') as fp:
                    lastPositions = json.load(fp)
                for position in self.positionRecords:
                    entryDate = position['entryDate']
                    isExist = False
                    for previousPosition in lastPositions:
                        if entryDate == previousPosition['entryDate']:
                            isExist = True

                    if isExist == False:
                        lastPositions.append(position)

                self.positionRecords = lastPositions

                for i in range(0, len(self.positionRecords)):
                    self.positionRecords[i]['positionId'] = i+1

            jsonFilename = "//orders.json"
            if utilities.checkFileExist(self.session.config.reportDirectory + jsonFilename):
                with open(self.session.config.reportDirectory + jsonFilename, 'r') as fp:
                    lastOrders= json.load(fp)

                    for order in self.orderRecords:
                        adjustedDate = order['adjustedDate']
                        action = order['action']
                        isExist = False
                        for previousOrder in lastOrders:
                            if adjustedDate == previousOrder['adjustedDate'] and action == previousOrder['action']:
                                isExist = True


                        if isExist == False:
                            lastOrders.append(order)

                    self.orderRecords = lastOrders
                    for i in range(0, len(self.orderRecords)):
                        self.orderRecords[i]['orderId'] = i + 1


                #self.orderRecords = lastOrders + self.orderRecords


        jsonFilename = "//positions.json"
        with open(self.session.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(self.positionRecords, fp, cls=utilities.AntJSONEncoder)

        jsonFilename = "//orders.json"
        with open(self.session.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(self.orderRecords, fp, cls=utilities.AntJSONEncoder)