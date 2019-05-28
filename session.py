import queue, copy,datetime, calendar, multiprocessing

from dateutil.relativedelta import relativedelta

import sys, traceback
from enum import IntEnum
import json, os

from datetime import datetime, timedelta

from .data.csvdatasource import CSVOHLCDataSource
from .data.datamodel import DataType



# region Class: SessionMode
class SessionMode(IntEnum):
    SYNC_BACKTEST = 0
    ASYNC_BACKTEST = 1
    IB_LIVE = 2
    IB_DALIY_BACKTEST = 3
# endregion


# region Class: SessionStaticVariable
class SessionStaticVariable:
    # region socket port related
    IB_WS_SERVER_PORT = 8000
    IB_WS_SERVER_PORT_DEBUG = 8001

    IB_JSON_SERVER_PORT = 8090
    IB_JSON_SERVER_PORT_DEBUG = 8091


    IB_GATEWAY_PORT = 8100
    IB_GATEWAY_IP = "127.0.0.1"
    IB_CONTROLLER_PORT = 8101
    IB_BACKTEST_CONTROLLER_PORT = 8102

    IB_CLIENT_ID = 0
    IB_CLIENT_ID_DAILY_HISTORICAL = 90
    IB_CLIENT_ID_DEBUG = 99

    HKEX_LIVE_WS_SERVER_PORT = 8200

    HSI_MKT_DATA_REQ_ID = 1001
    MHI_MKT_DATA_REQ_ID = 1002
    # endregion


    # region IB Account setting
    IB_HKEX_BUY_ACCOUNT = "U8618806"
    IB_HKEX_SELL_ACCOUNT = "U8633399"

    IB_COMMISSION = {"MHI":13, "HSI":50}
    # endregion


    # region Directory, file location, python path
    dataPath = "X:/"
    #dataPath = "C:/tmp/"
    logDirectory = "X:/log/"
    logDirectory = "C:/log/" #"X:/log/"
    api_path = "http://127.0.0.1/antXXXXXXX/XXXXXXXX/XXXXXXXX"

    baseReportDirectory = "Y:/ReportData/BacktestReport/Reports/"
    baseTADirectory = "Y:/ReportData/BacktestReport/TA/"

    #baseLiveReportDirectory = "Y:/ReportData/LiveReport/Reports/"
    #baseLiveTADirectory = "Y:/ReportData/LiveReport/TA/"
    baseLiveReportDirectory = "C:/tmp/ReportData/LiveReport/Reports/"
    baseLiveTADirectory = "C:/tmp/ReportData/LiveReport/TA/"



    baseLiveBacktestReportDirectory = "C:/tmp/ReportData/LiveBacktestReport/Reports/"
    baseLiveBacktestTADirectory = "C:/tmp/ReportData/LiveBacktestReport/TA/"
    baseLiveBacktestReportDirectory = "Y:/ReportData/LiveBacktestReport/Reports/"
    baseLiveBacktestTADirectory = "Y:/ReportData/LiveBacktestReport/TA/"

    base_filter_directory = "Y:/ReportData/BacktestReport/Filter/"

    #base_live_data_directory = "X:/index/ib/Live/"
    baseDataDirectory = "X:/index/hkex/csv/"
    baseLiveDataDirectory = "X:/index/ib/"
    #baseLiveDataDirectory = "C:/tmp/index/IB/Live/"

    baseLiveStrategyRotationDirectory = "Y:/ReportData/LiveReport/StrategyRotation/"


    base_live_filter_directory = "Y:/ReportData/LiveReport/Filter/"

    pythonw_path = 'C:/Anaconda3/pythonw.exe'
    python_path = "C:/Anaconda3/python.exe"

    antScriptDirectory = "D:/PythonScript/AntBotScripts/AntsScript"


    HKEXTradingHour = [
        {
            "date": "0000-00-00"
        },
        #Period 1
        {
            "date": "2011-03-07",
            "morning": {"open": 94500, "close": 123000},
            "afternoon": {"open": 143000, "close": 161500}
        },
        #Period 2
        {
            "date": "2012-03-05",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 133000, "close": 161500}
        },
        #Period 3
        # MHI have on market later the HSI so we take MHI time here, so night market start date not same as HKEX start
        {
            "date": "2014-01-06",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 130000, "close": 161500}
        },
        #Period 4
        {
            "date": "2014-11-03",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 130000, "close": 161500},
            "ath": {"open": 170000, "close": 230000}
        },
        #Period 5
        {
            "date": "2016-07-25",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 130000, "close": 161500},
            "ath": {"open": 170000, "close": 234500}
        },
        #Period 6
        {
            "date": "2017-11-06",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 130000, "close": 163000},
            "ath": {"open": 171500, "close": 234500}
        },
        #Period 7
        {
            "date": "present",
            "morning": {"open": 91500, "close": 120000},
            "afternoon": {"open": 130000, "close": 163000},
            "ath": {"open": 171500, "close": 250000}
        }
    ]
    # endregion




    @staticmethod
    def GetHistoricalPriceDataPath(ticker, exchange):
        from . import dataHelper

        path = SessionStaticVariable.dataPath

        #if str(ticker)
        #if str(ticker).upper() == "MHI" or str(ticker).lower() == "HSI":
        path += dataHelper.GetTickerType(str(ticker).lower()).lower() + '/'
        path += str(exchange).lower() + "/csv/"
        return path

# endregion


# region Class: SessionConfig
class SessionConfig:
    def __init__(self, **kwargs):
        from . import utilities


        # region Directory path, file path related
        self.isDebug = False
        self.productType = "index"
        self.dataPath = SessionStaticVariable.dataPath
        self.logDirectory = SessionStaticVariable.logDirectory
        self.apiPath = SessionStaticVariable.api_path

        self.baseReportDirectory = SessionStaticVariable.baseReportDirectory
        self.baseTADirectory = SessionStaticVariable.baseTADirectory
        # endregion

        self.Log = kwargs["logFunction"] if "logFunction" in kwargs else print


        # region Session setting
        self.mode = kwargs["mode"] if "mode" in kwargs else SessionMode.SYNC_BACKTEST
        self.sid = kwargs["sid"] if "sid" in kwargs else -1

        if self.mode == SessionMode.IB_LIVE:
            self.baseReportDirectory = SessionStaticVariable.baseLiveReportDirectory
            self.baseTADirectory = SessionStaticVariable.baseLiveTADirectory

        elif self.mode == SessionMode.IB_DALIY_BACKTEST:
            self.baseReportDirectory = SessionStaticVariable.baseLiveBacktestReportDirectory
            self.baseTADirectory = SessionStaticVariable.baseLiveBacktestTADirectory

        self.sessionId = kwargs["sessionId"] if "sessionId" in kwargs else 999999
        self.numReferenceDay = kwargs["numReferenceDay"] if "numReferenceDay" in kwargs else 31
        self.startDate = kwargs["startDate"] if "startDate" in kwargs else datetime(2014, 1, 1, 1, 0, 0)
        self.endDate = kwargs["endDate"] if "endDate" in kwargs else datetime(2014, 12, 31, 1, 0, 0)
        self.dataPeriod = utilities.getMonthList(self.startDate - timedelta(days=self.numReferenceDay), self.endDate)

        self.productType = kwargs["productType"] if "productType" in kwargs else "index"
        self.tradeTicker = kwargs["tradeTicker"] if "tradeTicker" in kwargs else "MHI"
        self.dataTicker = kwargs["dataTicker"] if "dataTicker" in kwargs else "MHI"

        self.expiryMonth = kwargs["expiryMonth"] if "expiryMonth" in kwargs else "201705"
        self.contract = kwargs["contract"] if "contract" in kwargs else "MHIF17"
        self.baseQuantity = kwargs["baseQuantity"] if "baseQuantity" in kwargs else 1
        self.exchange = kwargs["exchange"] if "exchange" in kwargs else "HKFE"

        self.cash = kwargs["cash"] if "cash" in kwargs else 40000

        self.signalResolution = kwargs["signalResolution"] if "signalResolution" in kwargs else "1T"
        self.dataResolution = kwargs["dataResolution"] if "dataResolution" in kwargs else ["1T","1D"]
        if "1D" not in self.dataResolution:
            self.dataResolution.append("1D")

        self.dataSourceClass = kwargs["dataSourceClass"] if "dataSourceClass" in kwargs else CSVOHLCDataSource
        self.strategyClass = kwargs["strategyClass"] if "strategyClass" in kwargs else None
        self.strategyParameter = kwargs["strategyParameter"] if "strategyParameter" in kwargs else None

        self.portfolioClass = kwargs["portfolioClass"] if "portfolioClass" in kwargs else None
        self.orderHandlerClass = kwargs["orderHandlerClass"] if "orderHandlerClass" in kwargs else None

        self.slippage = kwargs["slippage"] if "slippage" in kwargs else 3
        self.commission = kwargs["commission"] if "commission" in kwargs else 17

        if self.signalResolution in self.strategyClass.STRATEGY_SLUG:
            self.reportFolderName = datetime.now().strftime(
                "%Y%m%d_") + str(self.sessionId).zfill(
                6) + "_" + self.strategyClass.STRATEGY_SLUG
        else:
            self.reportFolderName = datetime.now().strftime(
            "%Y%m%d_") + str(self.sessionId).zfill(6) + "_" + self.strategyClass.STRATEGY_SLUG + "_" + self.signalResolution
        self.reportDirectory = self.baseReportDirectory + self.reportFolderName

        self.Log("self.reportDirectory:", self.reportDirectory)
        try:
            if not os.path.exists(self.reportDirectory):
                os.makedirs(self.reportDirectory)
        except:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info

        # endregion
    def SetReportFolderDate(self, dateStr, cat=""):
        try:
            import shutil
            shutil.rmtree(self.reportDirectory)
            if "_" not in str(dateStr):
                dateStr += "_"

            if self.signalResolution in self.strategyClass.STRATEGY_SLUG:
                self.reportFolderName = str(dateStr) + str(self.sessionId).zfill(
                    6) + "_" + self.strategyClass.STRATEGY_SLUG
            else:
                self.reportFolderName = str(dateStr) + str(self.sessionId).zfill(
                    6) + "_" + self.strategyClass.STRATEGY_SLUG + "_" + self.signalResolution

            if cat != "":
                self.reportFolderName += "_" + cat

            self.reportDirectory = self.baseReportDirectory + self.reportFolderName

            self.Log("self.reportDirectory:", self.reportDirectory)
            if not os.path.exists(self.reportDirectory):
                os.makedirs(self.reportDirectory)
        except:
            traceback.print_exc()
            pass


    def SetReportFolderForLive(self):
        try:
            import shutil
            shutil.rmtree(self.reportDirectory)
            self.reportFolderName = str(self.sessionId).zfill(
                6) + "_" + self.strategyClass.STRATEGY_SLUG

            self.reportDirectory = self.baseReportDirectory + self.reportFolderName

            if not os.path.exists(self.reportDirectory):
                os.makedirs(self.reportDirectory)
        except:
            pass

    def Save(self):
        #Load previous session config and update end date only if file exist
        if self.mode == SessionMode.IB_LIVE or self.mode == SessionMode.IB_DALIY_BACKTEST:
            from pathlib import Path
            configFilename = "/sessionConfig.json"
            csvFile = Path(self.reportDirectory + configFilename)
            if csvFile.is_file():
                with open(self.reportDirectory + configFilename) as fp:
                    dictToSave = json.load(fp)

                dictToSave["endDate"] = self.endDate.strftime("%Y%m%d")
                with open(self.reportDirectory + configFilename, 'w') as fp:
                    json.dump(dictToSave, fp, indent=4)

                return


        dictToSave = {}
        dictToSave["sessionId"] = self.sessionId
        dictToSave["mode"] = self.mode
        dictToSave["numReferenceDay"] = self.numReferenceDay
        dictToSave["startDate"] = self.startDate.strftime("%Y%m%d")
        dictToSave["endDate"] = self.endDate.strftime("%Y%m%d")
        dictToSave["tradeTicker"] = self.tradeTicker
        dictToSave["dataTicker"] = self.dataTicker
        dictToSave["contract"] = self.contract
        dictToSave["baseQuantity"] = self.baseQuantity
        dictToSave["exchange"] = self.exchange

        dictToSave["cash"] = self.cash
        dictToSave["dataSourceClass"] = self.dataSourceClass.NAME
        dictToSave["dataResolution"] = '['+ ','.join(self.dataResolution) + ']'
        dictToSave["signalResolution"] = self.signalResolution

        dictToSave["strategyClass"] = {}
        dictToSave["strategyClass"]["name"] = self.strategyClass.STRATEGY_NAME
        dictToSave["strategyClass"]["slug"] = self.strategyClass.STRATEGY_SLUG
        dictToSave["strategyClass"]["version"] = self.strategyClass.VERSION
        dictToSave["strategyClass"]["lastUpdate"] = self.strategyClass.LAST_UPDATE_DATE
        dictToSave["strategyClass"]["parameter"] = self.strategyParameter

        dictToSave["portfolioClass"] = self.portfolioClass.NAME
        dictToSave["orderHandlerClass"] = self.orderHandlerClass.NAME

        dictToSave["slippage"] = self.slippage
        dictToSave["commission"] = self.commission

        configFilename = "/sessionConfig.json"

        with open(self.reportDirectory + configFilename, 'w') as fp:
            json.dump(dictToSave, fp, indent=4)
# endregion


# region Class: Session (Backtest)
class Session(object):
    def __init__(self, config):
        self.config = config
        self.Log = self.config.Log

        self.dataQueue = queue.Queue()
        self.dataSource = self.config.dataSourceClass(self)
        self.portfolio = self.config.portfolioClass(self)
        self.orderHandler = self.config.orderHandlerClass(self)
        self.mode = config.mode

        self.strategy = self.config.strategyClass()
        self.strategy.Setup(self)


    def Run(self):
        self.dataSource.StartStreaming()


    def OnData(self, data):
        if data.type == DataType.OHLC:
            self.strategy.CalculateBar(data)
        else:
            raise NotImplemented("Unsupported event.type '%s'" % data.type)


    def OnComplete(self):
        from . import utilities

        self.Log("Saving config")
        self.config.Save()

        self.Log("Saving portfolio")
        self.portfolio.Save()

        self.Log("Saving strategy")
        self.strategy.Save()

        self.Log("saving creating summary report:", self.config.reportFolderName)
        utilities.CreateReportSummary(self.config.reportDirectory)


    def NextValidOrderId(self):
        self.order_id += 1
        return self.order_id
    # endregion


class IBLiveSession(object):
    def __init__(self, config, proxyClient):
        self.proxyClient = proxyClient
        self.mode = SessionMode.IB_LIVE

        self.config = config
        self.config.SetReportFolderForLive()
        self.Log = self.config.Log

        self.dataQueue = queue.Queue()

        self.dataSource = self.config.dataSourceClass(self)
        self.portfolio = self.config.portfolioClass(self)
        self.orderHandler = self.config.orderHandlerClass(self)

        self.strategy = self.config.strategyClass()
        self.strategy.Setup(self)


    def Run(self):
        self.dataSource.FeedBackfillData()


    def OnHistoricalData(self, data):
        self.PushDataToStrategy(data)


    def OnData(self, data):
        if self.dataSource.isReady:
            self.PushDataToStrategy(data)


    def PushDataToStrategy(self, data):
        if data.type == DataType.OHLC:
            self.strategy.CalculateBar(data)
        elif data.type == DataType.TICK:
            self.strategy.CalculateTick(data)
        else:
            raise NotImplemented("Unsupported event.type '%s'" % data.type)


    def OnComplete(self):
        from . import utilities

        self.Log("Saving config")
        #This will overweite the json
        self.config.Save()

        self.Log("Saving portfolio")
        self.portfolio.Save()

        self.Log("Saving strategy")
        # This will overweite the json
        self.strategy.Save()

        #This will be update base one new positions.json data
        self.Log("saving creating summary report:", self.config.reportFolderName)
        utilities.CreateReportSummary(self.config.reportDirectory)


    def NextValidOrderId(self):
        self.order_id += 1
        return self.order_id
    # endregion