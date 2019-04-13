import os, pandas as pd, datetime, numpy as np, time

from .. import utilities

from .. import static
from .base import AbstractBarDataSource
from .datamodel import DataType, OHLC, TickData

class IBProxyServerDataSource(AbstractBarDataSource):
    IS_DISPLAY_IN_OPTION = False
    NAME = "IBProxyServerDataSource"

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.config = self.session.config

        self.inPeriodData = False
        self.currentCsvFileIdx = 0
        self.tradeDate = None
        self.liveTradeDate = None

        self.historicalDf = False
        self.liveDataDf = False

        self.isReady = False

        if not "1D" in self.config.dataResolution:
            self.config.dataResolution.append("1D")

        self.backtestCSVFile = []
        self.liveCSVFile = []
        self.backfillDf = []

        self.PrepareBacktestData()


    def PrepareBacktestData(self):
        dataFolderPath = self.config.dataPath + self.config.productType + "/" + self.config.exchange

        #Load trade date data in backtest data folder
        if self.tradeDate is None:
            csvFilePath = dataFolderPath + "/csv/trade_date/trade_date.csv"
            if utilities.checkFileExist(csvFilePath):
                #print(CSVOHLCDataSource.NAME, "load trade date")
                self.tradeDate = pd.read_csv(csvFilePath, index_col=0, parse_dates=True, date_parser=pd.core.tools.datetimes.to_datetime)
            else:
                raise OSError('CSV file not exist: ' + csvFilePath)

        # Prepare backtest data csv file list to load

        for dataPeriod in self.config.dataPeriod:
            for resolution in self.config.dataResolution:
                csvFilename = dataPeriod + "_" + self.config.dataTicker + "_" + resolution + ".csv"
                csvFilePath = dataFolderPath + "/csv/" + resolution + "/" + csvFilename
                if utilities.checkFileExist(csvFilePath):
                    self.backtestCSVFile.append({"filePath": csvFilePath, "resolution": resolution})
                else:
                    self.session.Log("CSV file not found:", csvFilePath)
                    self.liveCSVFile.append({"month": dataPeriod, "filePath": csvFilePath, "resolution": resolution})

        self.LoadBacktestData()

    def LoadBarCsvFile(self,filePath, resolution, isFirst=False):
        df = pd.read_csv(filePath, index_col=0, parse_dates=True,
                         date_parser=pd.core.tools.datetimes.to_datetime)
        df['datetime'] = df.index

        if 'adjusted_time' not in df.columns:
            raise OSError('CSV file format error, adjusted_time not found:' + csvFilePath)
        if resolution not in static.INTRA_DATE_DATA_RESOLUTION:
            df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

            df['hour'] = "33"
            df['minute'] = "00"
            df['second'] = "00"

            df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
            df['adjusted_time'] = df['adjusted_time'].astype(int)
        else:
            df['hour'] = df['hour'].astype(str).str.zfill(2)
            df['minute'] = df['minute'].astype(str).str.zfill(2)
            df['second'] = df['second'].astype(str).str.zfill(2)

        if isFirst:
            df['datetime_for_sort'] = df.index
        else:
            df['datetime_for_sort'] = df.index + datetime.timedelta(
                seconds=static.RESOLUTION_IN_SEC[resolution])

        df['ticker'] = self.config.dataTicker
        df['resolution'] = resolution
        df['resolution_in_sec'] = static.RESOLUTION_IN_SEC[resolution]

        return df

    def MergeOHLCData(self, dfs):
        if len(dfs) == 0:
            return False

        df = pd.concat(dfs)

        # to made different resolution sort in correct order
        # 1T 09:15:00
        df['adjusted_time'] = df['adjusted_time'] + df['resolution_in_sec']

        df = df.sort_values(["adjusted_date", "adjusted_time", "resolution_in_sec"])
        if 'datetime_for_sort' in df:
            df = df.drop('datetime_for_sort', 1)
        df = df[
            ['open', 'high', 'low', 'close', 'volume', 'ticker', 'resolution', 'resolution_in_sec', 'adjusted_date',
             'adjusted_time']]

        return df

    def LoadBacktestData(self):
        print("========== Start LoadBacktestData ==========")
        isFirst = True
        dfs = []
        if len(self.backtestCSVFile)>0:
            for obj in self.backtestCSVFile:
                csvFilePath = obj['filePath']
                resolution = obj['resolution']
                self.session.Log("LoadBarCsvFile:", csvFilePath)
                df = self.LoadBarCsvFile(csvFilePath, resolution, isFirst)
                '''
                df = pd.read_csv(csvFilePath, index_col=0, parse_dates=True,
                                 date_parser=pd.core.tools.datetimes.to_datetime)
                df['datetime'] = df.index

                if 'adjusted_time' not in df.columns:
                    raise OSError('CSV file format error, adjusted_time not found:' + csvFilePath)
                if resolution not in static.INTRA_DATE_DATA_RESOLUTION:
                    df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                    df['hour'] = "33"
                    df['minute'] = "00"
                    df['second'] = "00"

                    df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                    df['adjusted_time'] = df['adjusted_time'].astype(int)
                else:
                    df['hour'] = df['hour'].astype(str).str.zfill(2)
                    df['minute'] = df['minute'].astype(str).str.zfill(2)
                    df['second'] = df['second'].astype(str).str.zfill(2)

                if isFirst:
                    df['datetime_for_sort'] = df.index
                else:
                    df['datetime_for_sort'] = df.index + datetime.timedelta(
                        seconds=static.RESOLUTION_IN_SEC[resolution])

                df['ticker'] = self.config.dataTicker
                df['resolution'] = resolution
                df['resolution_in_sec'] = static.RESOLUTION_IN_SEC[resolution]
                '''
                isFirst = False
                dfs.append(df)
            self.historicalDf = self.MergeOHLCData(dfs)

        print("========== End LoadBacktestData ==========")
        self.LoadLiveData()

    def LoadLiveData(self):
        print("========== Start LoadLiveData ==========")
        firstDateInLiveData = None
        for liveDataToLoad in self.liveCSVFile:
            if firstDateInLiveData is None:
                firstDateInLiveData = liveDataToLoad['month'] + "01"
                break

        firstDateInLiveData = datetime.datetime.fromtimestamp(time.mktime(time.strptime(firstDateInLiveData, "%Y%m%d")))
        dataFolderPath = self.config.dataPath + self.config.productType + "/IB/Live/"

        if self.liveTradeDate is None:
            csvFilePath = dataFolderPath + "trade_date/trade_date.csv"
            if utilities.checkFileExist(csvFilePath):
                #print(CSVOHLCDataSource.NAME, "load trade date")
                self.liveTradeDate = pd.read_csv(csvFilePath, index_col=0, parse_dates=True, date_parser=pd.core.tools.datetimes.to_datetime)
            else:
                raise OSError('CSV file not exist: ' + csvFilePath)

        df = self.liveTradeDate.loc[((self.liveTradeDate.index>=firstDateInLiveData) & (self.liveTradeDate.index<self.config.startDate))]


        self.tradeDate = pd.concat([self.tradeDate, self.liveTradeDate])
        self.tradeDate['target_date'] = self.tradeDate.index
        self.tradeDate = self.tradeDate.reset_index()
        self.tradeDate = self.tradeDate.drop_duplicates(subset='target_date', keep='first').set_index('target_date')


        dfs = []
        for date in df.index.tolist():
            dateStr = date.strftime("%Y%m%d")
            for resolution in self.config.dataResolution:
                csvFilename = dateStr + "_" + self.config.dataTicker + "_" + resolution + ".csv"
                csvFilePath = dataFolderPath + resolution + "/" + csvFilename
                if utilities.checkFileExist(csvFilePath):
                    print(date, csvFilePath)
                    dfs.append(self.LoadBarCsvFile(csvFilePath, resolution))
                else:
                    print("remove this if else statment for live trade current for debug")

        self.liveDataDf = self.MergeOHLCData(dfs)
        if type(self.liveDataDf) == bool and self.liveDataDf == False:
            self.backfillDf = self.historicalDf
        else:
            self.backfillDf = self.MergeOHLCData([self.historicalDf, self.liveDataDf])
        print("========== End LoadLiveData ==========")


    def FeedBackfillData(self):
        print("========== Start FeedBackfillData ==========")
        for row in self.backfillDf.itertuples():
            barData = OHLC(row)

            self.StoreData(barData)
            self.session.OnHistoricalData(barData)
        print("========== End FeedBackfillData ==========")
        self.isReady = True

    def OnBidAsk(self, data):
        if self.config.dataTicker == data['ticker'] and str(self.config.expiryMonth) == str(data['expiryMonth']):
            ticker = data['ticker']
            timestamp = utilities.ConvertAdjustedDateTimeToTimestamp(str(data['adjustedDate']), str(data['adjustedTime']))
            bid = int(data['bidPrice'])
            ask = int(data['askPrice'])
            adjustedDate = int(data['adjustedDate'])
            adjustedTime = int(data['adjustedTime'])
            tick = TickData(ticker, timestamp, bid, ask, adjustedDate, adjustedTime)
            self.StoreData(tick)
            self.session.OnData(tick)

            #print("OnBidAsk:", adjustedDate, adjustedTime, ticker, bid, ask)


    def OnTickData(self, data):
        if self.config.dataTicker == data['ticker'] and str(self.config.expiryMonth) == str(data['expiryMonth']):
            ticker = data['ticker']
            timestamp = utilities.ConvertAdjustedDateTimeToTimestamp(str(data['adjustedDate']),
                                                                     str(data['adjustedTime']))
            bid = int(data['price'])
            ask = int(data['price'])
            adjustedDate = int(data['adjustedDate'])
            adjustedTime = int(data['adjustedTime'])
            tick = TickData(ticker, timestamp, bid, ask, adjustedDate, adjustedTime)
            self.StoreData(tick)
            self.session.OnData(tick)

            #print("OnTickData: ", adjustedDate, adjustedTime, ticker, bid, ask)


    def OnOHLCData(self, data):
        if data['resolution'] not in self.session.config.dataResolution:
            return

        if self.config.dataTicker == data['ticker']:
            timestamp = utilities.ConvertAdjustedDateTimeToTimestamp(data['adjustedDate'], data['adjustedTime'])
            openPrice = int(data['open'])
            highPrice = int(data['high'])
            lowPrice = int(data['low'])
            closePrice = int(data['close'])
            vol = int(data['qty'])
            ticker = data['ticker']
            resolution = data['resolution']
            resolutionInSec = int(data['resolution_in_sec'])
            adjustedDate = int(data['adjustedDate'])
            adjustedTime = int(data['adjustedTime'])
            barData = OHLC((timestamp, openPrice, highPrice, lowPrice, closePrice, vol, ticker, resolution, resolutionInSec, adjustedDate, adjustedTime))

            #print("barData:   ", timestamp, openPrice, highPrice, lowPrice, closePrice, vol, ticker, resolution, resolutionInSec, adjustedDate, adjustedTime)

            self.StoreData(barData)
            self.session.OnData(barData)

            #print("OnOHLCData:", adjustedDate, adjustedTime, ticker, resolution, resolutionInSec, openPrice, highPrice, lowPrice, closePrice, vol)




    def GetTickerTradeDateDataByDate(self, timestamp):
        #return self.trade_date_dict[str(timestamp.date())]
        return self.tradeDate.loc[timestamp].to_dict()