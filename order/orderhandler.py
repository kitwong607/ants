from abc import ABCMeta
from ..broker.ib.IBContract import IBContract
from ..broker.ib.IBOrder import IBOrder
from ..order.base import OrderType, OrderAction
from .. import socket as antSocket
from .. import utilities
from datetime import datetime


class AbstractOrderHandler(object):
    IS_DISPLAY_IN_OPTION = False
    __metaclass__ = ABCMeta

    def __init__(self, session):
        self.session = session
        self.lastActiveDate = None
        self.filledOrder = {}
        self.unfilledOrder = {}

        self.NextOrderId = 1


    def GetNextOrderId(self):
        nextOrderId = self.NextOrderId
        self.NextOrderId += 1

        return nextOrderId

    def PrepareContract(self, tradeTicker, expiryMonth):
        if tradeTicker == "HSI":
            contract = IBContract.HSIFut(expiryMonth)
        elif tradeTicker == "MHI":
            contract = IBContract.MHIFut(expiryMonth)
        else:
            raise ValueError("Trade ticker: " + tradeTicker + " not support")

        contract.ticker = tradeTicker
        contract.expiryMonth = expiryMonth
        return contract

    def PrepareOrder(self, action, contract, orderId, signalPrice, limitPrice, adjustedDate, adjustedTime, orderType, label, quantity):
        if orderType == OrderType.MARKET:
            order = IBOrder.MarketOrder(action, quantity, signalPrice)
        elif orderType == OrderType.LIMIT:
            order = IBOrder.LimitOrder(action, quantity, signalPrice, limitPrice)
        else:
            raise ValueError("Order type: " + orderType + " not support")

        print("signalPrice:", signalPrice, "limitPrice:", limitPrice)
        print("order.signalPrice:", order.signalPrice, "order.limitPrice:", order.lmtPrice)

        #setup default variable for Order object
        order.filledTime = None
        order.adjustedDate = adjustedDate
        order.adjustedTime = adjustedTime

        order.exchange = self.session.config.exchange
        order.orderId = orderId
        order.label = label
        order.contract = contract
        order.ticker = contract.ticker
        order.type = orderType
        order.stopLossThreshold = 0
        return order


class BacktestOrderHandler(AbstractOrderHandler):
    IS_DISPLAY_IN_OPTION = True
    NAME = "BacktestOrderHandler"

    def __init__(self, session):
        super().__init__(session)


    def PlaceOrder(self, orderId, contract, order, isEntry="False"):
        if order.adjustedDate not in self.unfilledOrder:
            self.lastActiveDate = order.adjustedDate
            self.unfilledOrder[order.adjustedDate] = []
            self.filledOrder[order.adjustedDate] = []
        self.unfilledOrder[order.adjustedDate].append(order)

        #This will get from broker if in live trade
        lastClosePrice = self.session.dataSource.GetLastClose(contract.symbol)
        getLastTime = self.session.dataSource.GetLastTime(contract.symbol)
        commission = self.session.config.commission * order.totalQuantity

        if order.action == OrderAction.BUY:
            filledPirce = lastClosePrice + self.session.config.slippage
            self.FillOrder(orderId, filledPirce, getLastTime, commission)

            #self.FillOrder(order.orderId, self.session.dataSource.getLastClose(
             #   order.dataTicker) + self.session.config.slippage, filledTimestamp, self.session.config.commission * order.quantity)
        elif order.action == OrderAction.SELL:
            filledPirce = lastClosePrice - self.session.config.slippage
            self.FillOrder(orderId, filledPirce, getLastTime, commission)
        else:
            raise ValueError("Unexprected orderAction: " + order.action)

            #self.FillOrder(order.orderId, self.session.dataSource.getLastClose(
            #    order.dataTicker) - self.session.config.slippage, filledTimestamp, self.session.config.commission * order.quantity)


    def FillOrder(self, orderId, filledPrice, getLastTime, comission):
        for order in self.unfilledOrder[self.lastActiveDate]:
            if order.orderId == orderId:
                order.status = "filled"
                order.filledPrice = filledPrice
                order.filledTime = getLastTime
                order.commission = comission

                if order.action == OrderAction.BUY:
                    order.slippage = filledPrice - order.signalPrice
                elif order.action == OrderAction.SELL:
                    order.slippage = order.signalPrice - filledPrice
                else:
                    raise ValueError("Unexprected orderAction: " + order.action)


                self.filledOrder[self.lastActiveDate].append(self.unfilledOrder[self.lastActiveDate].pop(self.unfilledOrder[self.lastActiveDate].index(order)))
                self.session.portfolio.TransactOrder(order)
                break


class IBProxyServerOrderHandler(AbstractOrderHandler):
    IS_DISPLAY_IN_OPTION = True
    NAME = "IBProxyServerOrderHandler"

    def __init__(self, session):
        super().__init__(session)
        self.session = session
        self.proxyClient = session.proxyClient

        self.Log = self.session.Log


    def PlaceOrder(self, orderId, contract, order, isEntry="False"):
        self.Log("PlaceOrder 1:", order.signalPrice, order.lmtPrice)
        ######################################################################
        #Send to Proxy server to place order in IB
        data = {}
        data['uid'] = utilities.GetOrderUid(self.session.config.sid)
        data['sid'] = self.session.config.sid
        if order.action == OrderAction.BUY:
            data['action'] = "BUY"
        else:
            data['action'] = "SELL"
        data['qty'] = order.totalQuantity
        if order.type == OrderType.MARKET:
            data['limitPrice'] = int(order.signalPrice)
            data['signalPrice'] = int(order.signalPrice)
            data['triggerPrice'] = int(order.signalPrice)
        elif order.type == OrderType.LIMIT:
            data['limitPrice'] = int(order.lmtPrice)
            data['signalPrice'] = int(order.signalPrice)
            data['triggerPrice'] = int(order.signalPrice)
        else:
            raise ValueError("not support order type")
        data['expiryMonth'] = str(contract.expiryMonth)
        data['orderType'] = order.orderType
        data['ticker'] = order.ticker
        data['label'] = order.label
        data['isEntry'] = isEntry



        self.proxyClient.SendMessage(antSocket.ACTION_PLACE_ORDER, data)
        ######################################################################
        self.Log("Kit please look back here...", self.lastActiveDate)
        self.lastActiveDate = order.adjustedDate
        if order.adjustedDate not in self.unfilledOrder:
            self.lastActiveDate = order.adjustedDate
            self.unfilledOrder[order.adjustedDate] = []
            self.filledOrder[order.adjustedDate] = []
        self.unfilledOrder[order.adjustedDate].append(order)


    #this is for socket to call...
    #def FillOrder(self):

    def OnOrderPlaced(self, data):
        print("self.session.config.sessionId:", self.session.config.sessionId)
        if data["sid"] == self.session.config.sessionId:
            self.Log("self.lastActiveDate:", self.lastActiveDate)
            lastOrder = self.unfilledOrder[self.lastActiveDate][-1]
            lastOrder.orderId = data['oid']

    def OnOpenOrderEvent(self, data):
        pass

    def OnOpenOrderEndEvent(self, data):
        pass

    def OnOpenOrderUpdateEvent(self, data):
        #Check order is belong to this strategy with its order id

        for order in self.unfilledOrder[self.lastActiveDate]:
            if order.orderId == data['order_id']:
                if data['status'] == "Filled":
                    order.status = "filled"
                    order.filledPrice = data['avg_fill_price']
                    order.filledTime = datetime.fromtimestamp(int(data['filledTimestamp']))

                    self.Log("Order Filled:", order.orderId, order.filledPrice, order.filledTime)
                    self.Log(data)

                    # here have to change
                    order.commission = 0

                    if order.action == OrderAction.BUY:
                        order.slippage = order.filledPrice - order.signalPrice
                    elif order.action == OrderAction.SELL:
                        order.slippage = order.signalPrice - order.filledPrice
                    else:
                        raise ValueError("Unexprected orderAction: " + order.action)

                    self.filledOrder[self.lastActiveDate].append(self.unfilledOrder[self.lastActiveDate].pop(
                        self.unfilledOrder[self.lastActiveDate].index(order)))
                    self.session.portfolio.TransactOrder(order)


    '''
    def FillOrder(self, orderId, filledPrice, getLastTime, comission):
        for order in self.unfilledOrder[self.lastActiveDate]:
            if order.orderId == orderId:
                order.status = "filled"
                order.filledPrice = filledPrice
                order.filledTime = getLastTime
                order.commission = comission

                if order.action == OrderAction.BUY:
                    order.slippage = filledPrice - order.signalPrice
                elif order.action == OrderAction.SELL:
                    order.slippage = order.signalPrice - filledPrice
                else:
                    raise ValueError("Unexprected orderAction: " + order.action)


                self.filledOrder[self.lastActiveDate].append(self.unfilledOrder[self.lastActiveDate].pop(self.unfilledOrder[self.lastActiveDate].index(order)))
                self.session.portfolio.TransactOrder(order)
                break
    '''