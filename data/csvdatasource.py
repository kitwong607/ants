import os, pandas as pd, datetime, numpy as np

from .. import utilities

from .. import static
from .base import AbstractBarDataSource
from .datamodel import DataType, OHLC

class CSVOHLCDataSource(AbstractBarDataSource):
    IS_DISPLAY_IN_OPTION = True
    NAME = "CSVOHLCDataSource"

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.config = self.session.config

        self.inPeriodData = False
        self.currentCsvFileIdx = 0
        self.tradeDate = None

        if not "1D" in self.config.dataResolution:
            self.config.dataResolution.append("1D")

        self.LoadCsvFile()


    def LoadCsvFile(self):
        if self.tradeDate is None:
            csvFilePath = self.config.dataPath + self.config.exchange + "\\csv\\trade_date\\trade_date.csv"
            if utilities.checkFileExist(csvFilePath):
                #print(CSVOHLCDataSource.NAME, "load trade date")
                self.tradeDate = pd.read_csv(csvFilePath, index_col=0, parse_dates=True, date_parser=pd.core.tools.datetimes.to_datetime)

            else:
                raise OSError('CSV file not exist: ' + csvFilePath)



        is_first = True
        dfs = []
        for resolution in self.config.dataResolution:
            csvFilename = self.config.dataPeriod[self.currentCsvFileIdx] + "_" + self.config.dataTicker + "_" + resolution + ".csv"
            csvFilePath = self.config.dataPath + self.config.exchange + "\\csv\\" + resolution + "\\" + csvFilename

            if utilities.checkFileExist(csvFilePath):
                #print(CSVOHLCDataSource.NAME, "load csv:", resolution, self.config.exchange, self.config.dataTicker)
                df = pd.read_csv(csvFilePath, index_col=0, parse_dates=True, date_parser=pd.core.tools.datetimes.to_datetime)
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


                if is_first:
                    df['datetime_for_sort'] = df.index
                else:
                    df['datetime_for_sort'] = df.index + datetime.timedelta(seconds = static.RESOLUTION_IN_SEC[resolution])


                df['ticker'] = self.config.dataTicker
                df['resolution'] = resolution
                df['resolution_in_sec'] = static.RESOLUTION_IN_SEC[resolution]


                dfs.append(df)
            is_first = False


        #concat multiple resolution df into single one for looping
        df = pd.concat(dfs)


        #to made different resolution sort in correct order
        #1T 09:15:00
        df['adjusted_time'] = df['adjusted_time'] + df['resolution_in_sec']


        df = df.sort_values(["adjusted_date","adjusted_time","resolution_in_sec"])
        df = df.drop('datetime_for_sort', 1)
        df = df[['open','high','low','close','volume','ticker','resolution','resolution_in_sec','adjusted_date','adjusted_time']]

        self.dataDf = df.itertuples()
        self.currentCsvFileIdx += 1


    def StartStreaming(self):
        #loop data monthly
        for row in self.dataDf:
            barData = OHLC(row)

            if self.inPeriodData:
                if barData.timestamp >= self.config.endDate:
                    self.inPeriodData = False
            else:
                if barData.timestamp >= self.config.startDate:
                    self.inPeriodData = True


            self.StoreData(barData)
            self.session.OnData(barData)

        #load another month after looping
        if self.currentCsvFileIdx != len(self.config.dataPeriod):
            self.LoadCsvFile()
            self.StartStreaming()
            return

        #exit is no data to loop
        self.session.OnComplete()


    def GetTickerTradeDateDataByDate(self, timestamp):
        #return self.trade_date_dict[str(timestamp.date())]
        return self.tradeDate.loc[timestamp].to_dict()