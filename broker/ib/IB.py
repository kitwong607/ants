import sys
import argparse
import datetime
import collections
import inspect

import logging
import time
import os.path
import traceback



from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import *
from ibapi.order_condition import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import *

from ibapi.account_summary_tags import *

from . import Static
from .IBContract import IBContract
from .IBOrder import IBOrder
from .IBAvailableAlgoParams import IBAvailableAlgoParams
from .IBScannerSubscription import IBScannerSubscription
from .IBFaAllocation import IBFaAllocation

from ...session import SessionStaticVariable

def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)


def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)
    return fn2

def printinstance(inst:Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))



class Activity(Object):
    def __init__(self, reqMsgId, ansMsgId, ansEndMsgId, reqId):
        self.reqMsdId = reqMsgId
        self.ansMsgId = ansMsgId
        self.ansEndMsgId = ansEndMsgId
        self.reqId = reqId


class RequestMgr(Object):
    def __init__(self):
        # I will keep this simple even if slower for now: only one list of
        # requests finding will be done by linear search
        self.requests = []

    def addReq(self, req):
        self.requests.append(req)

    def receivedMsg(self, msg):
        pass


# ! [socket_declare]
class IBAPIClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        # ! [socket_declare]

        # how many times a method is called to see test coverage
        self.clntMeth2callCount = collections.defaultdict(int)
        self.clntMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nReq = collections.defaultdict(int)
        self.setupDetectReqId()

    def countReqId(self, methName, fn):
        def countReqId_(*args, **kwargs):
            self.clntMeth2callCount[methName] += 1
            idx = self.clntMeth2reqIdIdx[methName]
            if idx >= 0:
                sign = -1 if 'cancel' in methName else 1
                self.reqId2nReq[sign * args[idx]] += 1
            return fn(*args, **kwargs)

        return countReqId_

    def setupDetectReqId(self):
        methods = inspect.getmembers(EClient, inspect.isfunction)
        for (methName, meth) in methods:
            if methName != "send_msg":
                # don't screw up the nice automated logging in the send_msg()
                self.clntMeth2callCount[methName] = 0
                # logging.debug("meth %s", name)
                sig = inspect.signature(meth)
                for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                    (paramName, param) = pnameNparam
                    if paramName == "reqId":
                        self.clntMeth2reqIdIdx[methName] = idx

                setattr(IBAPIClient, methName, self.countReqId(methName, meth))

                # print("IBAPIClient.clntMeth2reqIdIdx", self.clntMeth2reqIdIdx)


# ! [ewrapperimpl]
class IBAPIWrapper(wrapper.EWrapper):
    # ! [ewrapperimpl]
    def __init__(self):
        wrapper.EWrapper.__init__(self)

        self.wrapMeth2callCount = collections.defaultdict(int)
        self.wrapMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nAns = collections.defaultdict(int)
        self.setupDetectWrapperReqId()

    # TODO: see how to factor this out !!

    def countWrapReqId(self, methName, fn):
        def countWrapReqId_(*args, **kwargs):
            self.wrapMeth2callCount[methName] += 1
            idx = self.wrapMeth2reqIdIdx[methName]
            if idx >= 0:
                self.reqId2nAns[args[idx]] += 1
            return fn(*args, **kwargs)

        return countWrapReqId_


    def setupDetectWrapperReqId(self):
        methods = inspect.getmembers(wrapper.EWrapper, inspect.isfunction)
        for (methName, meth) in methods:
            self.wrapMeth2callCount[methName] = 0
            # logging.debug("meth %s", name)
            sig = inspect.signature(meth)
            for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                (paramName, param) = pnameNparam
                # we want to count the errors as 'error' not 'answer'
                if 'error' not in methName and paramName == "reqId":
                    self.wrapMeth2reqIdIdx[methName] = idx

            setattr(IBAPIWrapper, methName, self.countWrapReqId(methName, meth))

            # print("IBAPIClient.wrapMeth2reqIdIdx", self.wrapMeth2reqIdIdx)


# this is here for documentation generation
"""
#! [ereader]
        #this code is in Client::connect() so it's automatically done, no need
        # for user to do it
        self.reader = reader.EReader(self.conn, self.msg_queue)
        self.reader.start()   # start thread

#! [ereader]
"""


# ! [socket_init]
class IB(IBAPIWrapper, IBAPIClient):
    def __init__(self, IBEventHandler):
        IBAPIWrapper.__init__(self)
        IBAPIClient.__init__(self, wrapper=self)
        # ! [socket_init]
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.simplePlaceOid = None

        self.account_info = {}
        self.IBEventHandler = IBEventHandler

    def convert_order_state_to_dict(self, orderState):
        d = {}
        d['status'] = orderState.status
        d['initMarginBefore'] = orderState.initMarginBefore
        d['maintMarginBefore'] = orderState.maintMarginBefore
        d['equityWithLoanBefore'] = orderState.equityWithLoanBefore
        d['initMarginChange'] = orderState.initMarginChange
        d['maintMarginChange'] = orderState.maintMarginChange
        d['equityWithLoanChange'] = orderState.equityWithLoanChange
        d['initMarginAfter'] = orderState.initMarginAfter
        d['maintMarginAfter'] = orderState.maintMarginAfter
        d['equityWithLoanAfter'] = orderState.equityWithLoanAfter

        d['commission'] = orderState.commission
        d['minCommission'] = orderState.minCommission
        d['maxCommission'] = orderState.maxCommission
        d['commissionCurrency'] = orderState.commissionCurrency
        d['warningText'] = orderState.warningText


        return d

    def convert_order_to_dict(self, order):
        d = {}
        d['orderId'] = order.orderId
        d['clientId'] = order.clientId
        d['permId'] = order.permId

        d['orderType'] = order.orderType
        d['action'] = order.action
        d['totalQuantity'] = order.totalQuantity

        d['lmtPrice'] = order.lmtPrice


        return d

    def convert_contract_to_dict(self, contract):
        d = {}
        d['conId'] = contract.conId
        d['symbol'] = contract.symbol
        d['secType'] = contract.secType
        d['lastTradeDateOrContractMonth'] = contract.lastTradeDateOrContractMonth
        d['strike'] = contract.strike
        d['right'] = contract.right
        d['multiplier'] = contract.multiplier
        d['exchange'] = contract.exchange
        d['primaryExchange'] = contract.primaryExchange
        d['currency'] = contract.currency
        d['localSymbol'] = contract.localSymbol
        d['tradingClass'] = contract.tradingClass
        d['includeExpired'] = contract.includeExpired
        d['secIdType'] = contract.secIdType
        d['secId'] = contract.secId
        return d

    def requestAccountUpdateMulti(self, account=None):
        if account == self.account:
            return

        if account is None:
            return
        else:
            req_id = int(account.replace("U", "").replace("D", ""))
            self.reqAccountUpdatesMulti(req_id, account, "", False)


    def dispatchEvent(self, event, data):
        try:
            if self.IBEventHandler is not None:
                self.IBEventHandler(event, data)
        except:
            traceback.print_exc()
            pass
        finally:
            #todo do log here?
            pass


    def dumpTestCoverageSituation(self):
        for clntMeth in sorted(self.clntMeth2callCount.keys()):
            logging.debug("ClntMeth: %-30s %6d" % (clntMeth,
                                                   self.clntMeth2callCount[clntMeth]))

        for wrapMeth in sorted(self.wrapMeth2callCount.keys()):
            logging.debug("WrapMeth: %-30s %6d" % (wrapMeth,
                                                   self.wrapMeth2callCount[wrapMeth]))


    def dumpReqAnsErrSituation(self):
        logging.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
        for reqId in sorted(self.reqId2nReq.keys()):
            nReq = self.reqId2nReq.get(reqId, 0)
            nAns = self.reqId2nAns.get(reqId, 0)
            nErr = self.reqId2nErr.get(reqId, 0)
            logging.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))

    @iswrapper
    # ! [connectack]
    def connectAck(self):
        if self.async:
            self.startApi()
    # ! [connectack]

    @iswrapper
    # ! [connectack]
    def connectAck(self):
        if self.async:
            self.startApi()
    # ! [connectack]

    @iswrapper
    # ! [nextvalidid]
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)

        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # ! [nextvalidid]

    def start(self):
        if self.started:
            print("IB.start()... already start")
            return

        self.started = True

        self.dispatchEvent(Static.APIStartEvent, {"status":Static.SuccessStatus})
        self.reqManagedAccts()

    def subscribeMktData(self):
        '''
        client.reqTickByTickData(19001, IBContract.MHIFut(), "Last", 0, false);
        client.reqTickByTickData(19002, IBContract.MHIFut(), "AllLast", 0, false);
        client.reqTickByTickData(19003, IBContract.MHIFut(), "BidAsk", 0, true);
        '''
        pass


    #todo test how its work
    def keyboardInterrupt(self):
        self.nKeybInt += 1
        if self.nKeybInt == 1:
            self.stop()
        else:
            print("Finishing test")
            self.done = True


    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1

        return oid


    @iswrapper
    # ! [error]
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        self.dispatchEvent(Static.APIErrorEvent, {"reqId":reqId, "errorCode":errorCode, "errorString":errorString})
        #print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

    # ! [error] self.reqId2nErr[reqId] += 1


    @iswrapper
    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)
        self.dispatchEvent(Static.WinEvent, {"text": text, "lastError": lastError})
        #ws.ib_win_error(text, lastError)


    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType,
              "@", contract.exchange, ":", order.action, order.orderType,
              order.totalQuantity, orderState.status)


        contractDict = self.convert_contract_to_dict(contract)
        orderDict = self.convert_order_to_dict(order)
        orderStateDict  = self.convert_order_state_to_dict(orderState)

        self.dispatchEvent(Static.OpenOrderEvent, {"order_id": orderId, "contract": contractDict, "order": orderDict, "order_state": orderStateDict})

        # ! [openorder]

        order.contract = contract
        self.permId2ord[order.permId] = order


    @iswrapper
    # ! [openorderend]
    def openOrderEnd(self):
        super().openOrderEnd()
        # ! [openorderend]
        self.dispatchEvent(Static.OpenOrderEndEvent, {})
        logging.debug("Received %d openOrders", len(self.permId2ord))


    @iswrapper
    # ! [orderstatus]
    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):

        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

        '''
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled,
              ", Remaining: ", remaining, ", AvgFillPrice: ", avgFillPrice,
              ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ",
              lastFillPrice, ", ClientId: ", clientId, ", WhyHeld: ",
              whyHeld, ", MktCapPrice: ", mktCapPrice)
        '''

        self.dispatchEvent(Static.OrderStatusEvent, {"order_id": orderId, "status": status, "filled": filled, "remaining": remaining,
                                   "avg_fill_price": avgFillPrice, "perm_id": permId, "parent_id": parentId,
                                   "last_fill_price": lastFillPrice, "client_id": clientId, "why_held": whyHeld, "mkt_cap_price": mktCapPrice})


    # ! [orderstatus]


    @iswrapper
    # ! [managedaccounts]
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        self.account = accountsList.split(",")[0]
        self.accountsList = []
        for account in accountsList.split(","):
            if account != "":
                self.accountsList.append(account)

        self.dispatchEvent(Static.ManagedAccountsEvent, {"accounts": self.accountsList})

        print("subscribe account update")
        self.reqAccountUpdates(True, self.account)

        print("subscribe account update multi")
        for account in self.accountsList:
            self.requestAccountUpdateMulti(account)

        print("subscribe open order")
        self.reqOpenOrders()



    @iswrapper
    # ! [accountsummary]
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        '''
        print("Acct Summary. ReqId:", reqId, "Acct:", account,
              "Tag: ", tag, "Value:", value, "Currency:", currency)
        '''

        self.dispatchEvent(Static.ManagedSummaryEvent, {"req_id":reqId, "account":account, "tag":tag, "value":value, "currency":currency})
    # ! [accountsummary]


    @iswrapper
    # ! [accountsummaryend]
    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        #print("AccountSummaryEnd. Req Id: ", reqId)

        self.dispatchEvent(Static.ManagedSummaryEndEvent, {"req_id": reqId})
    # ! [accountsummaryend]


    @iswrapper
    # ! [updateaccountvalue]
    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):
        super().updateAccountValue(key, val, currency, accountName)


        if accountName not in self.account_info:
            self.account_info[accountName] = {}

        if currency not in self.account_info[accountName]:
            self.account_info[accountName][currency] = {}

        self.account_info[accountName][currency][key] = val

        self.dispatchEvent(Static.AccountUpdateEvent, {"key":key, "val":val, "currency":currency, "account": accountName})
    # ! [updateaccountvalue]


    @iswrapper
    # ! [updateportfolio]
    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", contract.symbol, "", contract.secType, "@",
              contract.exchange, "Position:", position, "MarketPrice:", marketPrice,
              "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL,
              "AccountName:", accountName)

        data = {
                    "ticker": contract.symbol,
                    "sec_type": contract.secType,
                    "exchange": contract.exchange,
                    "contract": contract.localSymbol,
                    "position": position,
                    "market_price": marketPrice,
                    "market_value": marketValue,
                    "average_cost": averageCost,
                    "unrealized_pnl": unrealizedPNL,
                    "realized_pnl": realizedPNL,
                    "account": accountName
                }
        self.dispatchEvent(Static.PortfolioUpdateEvent, data)

    # ! [updateportfolio]


    @iswrapper
    # ! [updateaccounttime]
    def updateAccountTime(self, timestamp: str):
        super().updateAccountTime(timestamp)
        self.dispatchEvent(Static.AccountUpdateTimeEvent, {"time": timestamp})
    # ! [updateaccounttime]


    @iswrapper
    # ! [accountdownloadend]
    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        self.dispatchEvent(Static.AccountDownloadEndEvent, {"account": accountName})

    # ! [accountdownloadend]


    @iswrapper
    # ! [position]
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

        self.dispatchEvent(Static.PositionEvent, {"account": account, "contract": contract, Static.PositionEvent: position, "avg_cost": avgCost})

    # ! [position]


    @iswrapper
    # ! [positionend]
    def positionEnd(self):
        super().positionEnd()
        #print("PositionEnd")

        self.dispatchEvent(Static.PositionEndEvent, {})
    # ! [positionend]


    @iswrapper
    # ! [positionmulti]
    def positionMulti(self, reqId: int, account: str, modelCode: str,
                      contract: Contract, position: float, avgCost: float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)
        print("Position Multi. Request:", reqId, "Account:", account,
              "ModelCode:", modelCode, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency, ",Position:",
              position, "AvgCost:", avgCost)

        self.dispatchEvent(Static.PositionMultiEvent, {"req_id": reqId, "account": account, "model_code": modelCode, "contract": contract, Static.PositionEvent: position, "avg_cost": avgCost})
    # ! [positionmulti]


    @iswrapper
    # ! [positionmultiend]
    def positionMultiEnd(self, reqId: int):
        super().positionMultiEnd(reqId)
        print("Position Multi End. Request:", reqId)

        self.dispatchEvent(Static.PositionMultiEndEventEvent, {})
    # ! [positionmultiend]


    @iswrapper
    # ! [accountupdatemulti]
    def accountUpdateMulti(self, reqId: int, accountName: str, modelCode: str,
                           key: str, val: str, currency: str):
        super().accountUpdateMulti(reqId, accountName, modelCode, key, val,
                                   currency)

        if accountName not in self.account_info:
            self.account_info[accountName] = {}

        if currency not in self.account_info[accountName]:
            self.account_info[accountName][currency] = {}

        self.account_info[accountName][currency][key] = val

        self.dispatchEvent(Static.AccountUpdateMultiEvent, {"req_id": reqId, "account": accountName, "model_code": modelCode, "key": key, "val": val, "currency": currency})

    # ! [accountupdatemulti]


    @iswrapper
    # ! [accountupdatemultiend]
    def accountUpdateMultiEnd(self, reqId: int):
        super().accountUpdateMultiEnd(reqId)
        print("Account Update Multi End. Request:", reqId)

        self.dispatchEvent(Static.AccountUpdateMultiEndEvent, {"req_id": reqId})
    # ! [accountupdatemultiend]


    @iswrapper
    # ! [familyCodes]
    def familyCodes(self, familyCodes: ListOfFamilyCode):
        super().familyCodes(familyCodes)
        print("Family Codes:")
        for familyCode in familyCodes:
            print("Account ID: %s, Family Code Str: %s" % (
                familyCode.accountID, familyCode.familyCodeStr))
            self.dispatchEvent(Static.FamilyCodesEvent,
                       {"account_id": familyCode.accountID, "family_code":familyCode.familyCodeStr})

    # ! [familyCodes]

    @iswrapper
    # ! [tickbytickbidask]
    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: int, askSize: int, attribs: TickAttrib):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, attribs)

        '''
        time_str = datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S")
        print("BidAsk. Req Id: ", reqId,
              " Time: ", time_str,
              " BidPrice: ", bidPrice, " AskPrice: ", askPrice, " BidSize: ", bidSize,
              " AskSize: ", askSize, end='')
        '''

        self.dispatchEvent(Static.TickByTickBidAskEvent,
                   {"req_id": reqId, "ticker_id": reqId, "bid_price": bidPrice, "ask_price": askPrice,
                   "bid_size": bidSize, "ask_size": askSize,
                   "time":time})

        '''
        if attribs.bidPastLow:
            print(" bidPastLow", end='')
        if attribs.askPastHigh:
            print(" askPastHigh", end='')
        '''

    # ! [tickbytickbidask]

    def marketDataType_req(self):
        # ! [reqmarketdatatype]
        # Switch to live (1) frozen (2) delayed (3) delayed frozen (4).
        self.reqMarketDataType(MarketDataTypeEnum.REALTIME)
        # ! [reqmarketdatatype]

    @iswrapper
    # ! [marketdatatype]
    def marketDataType(self, reqId: TickerId, marketDataType: int):
        super().marketDataType(reqId, marketDataType)
        print("MarketDataType. ", reqId, "Type:", marketDataType)

        self.dispatchEvent(Static.MarketDataTypeEvent, {"req_id": reqId, "ticker_id": reqId, "market_data_type": marketDataType})

    # ! [marketdatatype]


    @iswrapper
    # ! [tickprice]
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        '''
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:",
              price, "CanAutoExecute:", attrib.canAutoExecute,
              "PastLimit", attrib.pastLimit)
        '''


        self.dispatchEvent(Static.TickPriceEvent, {"req_id": reqId, "ticker_id": reqId, "tick_type": tickType, "price": price, "tick_attrib": attrib})
    # ! [tickprice]


    @iswrapper
    # ! [ticksize]
    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)

        '''
        print("Tick Size. Ticker Id:", reqId, "tickType:", tickType, "Size:", size)
        '''
        self.dispatchEvent(Static.TickSizeEvent, {"req_id": reqId, "ticker_id": reqId, "size": size, "tick_type": tickType})
    # ! [ticksize]


    @iswrapper
    # ! [tickgeneric]
    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        '''
        print("Tick Generic. Ticker Id:", reqId, "tickType:", tickType, "Value:", value)
        '''

        #self.dispatchEvent("tick_generic", {"req_id": reqId, "ticker_id": reqId, "value": value, "tick_type": tickType})
    # ! [tickgeneric]


    @iswrapper
    # ! [tickstring]
    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        super().tickString(reqId, tickType, value)
        '''
        print("Tick string. Ticker Id:", reqId, "Type:", tickType, "Value:", value)
        '''

        self.dispatchEvent(Static.TickStringEvent, {"req_id": reqId, "ticker_id": reqId, "value": value, "tick_type": tickType})
    # ! [tickstring]


    @iswrapper
    # ! [ticksnapshotend]
    def tickSnapshotEnd(self, reqId: int):
        super().tickSnapshotEnd(reqId)
        print("TickSnapshotEnd:", reqId)

        self.dispatchEvent(Static.TickSnapshotEndEvent, {"req_id": reqId})
    # ! [ticksnapshotend]


    @iswrapper
    # ! [updatemktdepth]
    def updateMktDepth(self, reqId: TickerId, position: int, operation: int,
                       side: int, price: float, size: int):
        super().updateMktDepth(reqId, position, operation, side, price, size)
        print("UpdateMarketDepth. ", reqId, "Position:", position, "Operation:",
              operation, "Side:", side, "Price:", price, "Size", size)

        self.dispatchEvent(Static.UpdateMktDepthEvent, {"req_id": reqId, "ticker_id": reqId, Static.PositionEvent: position, "operation": operation,
                                        "side": side, "price": price, "size": size})
    # ! [updatemktdepth]


    @iswrapper
    # ! [updatemktdepthl2]
    def updateMktDepthL2(self, reqId: TickerId, position: int, marketMaker: str,
                         operation: int, side: int, price: float, size: int):
        super().updateMktDepthL2(reqId, position, marketMaker, operation, side,
                                 price, size)
        print("UpdateMarketDepthL2. ", reqId, "Position:", position, "Operation:",
              operation, "Side:", side, "Price:", price, "Size", size)

        self.dispatchEvent(Static.UpdateMktDepthL2Event,
                   {"req_id": reqId, "ticker_id": reqId, Static.PositionEvent: position, "market_maker": marketMaker,
                    "operation": operation, "side": side, "price": price, "size": size})

    # ! [updatemktdepthl2]


    @printWhenExecuting
    def historicalDataRequests_req(self):
        # Requesting historical data
        # ! [reqHeadTimeStamp]
        self.reqHeadTimeStamp(4103, ContractSamples.USStockAtSmart(), "TRADES", 0, 1)
        # ! [reqHeadTimeStamp]

        time.sleep(1)

        # ! [cancelHeadTimestamp]
        self.cancelHeadTimeStamp(4103)
        # ! [cancelHeadTimestamp]

        # ! [reqhistoricaldata]
        queryTime = (datetime.datetime.today() -
                     datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(4101, ContractSamples.USStockAtSmart(), queryTime,
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        self.reqHistoricalData(4001, ContractSamples.EurGbpFx(), queryTime,
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        self.reqHistoricalData(4002, ContractSamples.EuropeanStock(), queryTime,
                               "10 D", "1 min", "TRADES", 1, 1, False, [])
        # ! [reqhistoricaldata]

        # ! [reqHistogramData]
        self.reqHistogramData(4104, ContractSamples.USStock(), False, "3 days")
        # ! [reqHistogramData]
        time.sleep(2)
        # ! [cancelHistogramData]
        self.cancelHistogramData(4104)
        # ! [cancelHistogramData]


    @printWhenExecuting
    def historicalDataRequests_cancel(self):
        # Canceling historical data requests
        self.cancelHistoricalData(4101)
        self.cancelHistoricalData(4001)
        self.cancelHistoricalData(4002)

    @iswrapper
    # ! [headTimestamp]
    def headTimestamp(self, reqId:int, headTimestamp:str):
        print("HeadTimestamp: ", reqId, " ", headTimestamp)
        self.dispatchEvent(Static.HeadTimestampEvent, {"req_id": reqId, "head_timestamp": headTimestamp})
    # ! [headTimestamp]

    @iswrapper
    # ! [histogramData]
    def histogramData(self, reqId:int, items:HistogramDataList):
        print("HistogramData: ", reqId, " ", items)
        self.dispatchEvent(Static.HistogramDataEvent, {"req_id": reqId, "histogram_data_list": items})
    # ! [histogramData]

    @iswrapper
    # ! [historicaldata]
    def historicalData(self, reqId:int, bar: BarData):
        '''
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)
        '''

        self.dispatchEvent(Static.HistoricalDataEvent, {"req_id": reqId, "bar": bar})
    # ! [historicaldata]

    @iswrapper
    # ! [historicaldataend]
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        '''
        print("HistoricalDataEnd ", reqId, "from", start, "to", end)
        '''
        self.dispatchEvent(Static.HistoricalDataEndEvent, {"req_id": reqId, "start": start, "end": end})
    # ! [historicaldataend]

    @iswrapper
    #! [historicalDataUpdate]
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)
        self.dispatchEvent(Static.HistoricalDataUpdateEvent, {"req_id": reqId, "bar": bar})
    #! [historicalDataUpdate]


    @printWhenExecuting
    def miscelaneous_req(self):
        # Request TWS' current time ***/
        self.reqCurrentTime()
        # Setting TWS logging level  ***/
        self.setServerLogLevel(1)


    @iswrapper
    # ! [displaygrouplist]
    def displayGroupList(self, reqId: int, groups: str):
        super().displayGroupList(reqId, groups)
        print("DisplayGroupList. Request: ", reqId, "Groups", groups)

    # ! [displaygrouplist]


    @iswrapper
    # ! [displaygroupupdated]
    def displayGroupUpdated(self, reqId: int, contractInfo: str):
        super().displayGroupUpdated(reqId, contractInfo)
        print("displayGroupUpdated. Request:", reqId, "ContractInfo:", contractInfo)

    # ! [displaygroupupdated]



    def orderOperations_cancel(self):
        if self.simplePlaceOid is not None:
            # ! [cancelorder]
            self.cancelOrder(self.simplePlaceOid)
            # ! [cancelorder]

    @iswrapper
    # ! [execdetails]
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency,
              execution.execId, execution.orderId, execution.shares)

    # ! [execdetails]


    @iswrapper
    # ! [execdetailsend]
    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ", reqId)

    # ! [execdetailsend]


    @iswrapper
    # ! [commissionreport]
    def commissionReport(self, commissionReport: CommissionReport):
        super().commissionReport(commissionReport)
        print("CommissionReport. ", commissionReport.execId, commissionReport.commission,
              commissionReport.currency, commissionReport.realizedPNL)
        # ! [commissionreport]