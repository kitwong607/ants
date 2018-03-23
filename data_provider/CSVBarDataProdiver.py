import os, pandas as pd, datetime, numpy as np

from .. import utilities
from ..functions import ant_time
from .base import AbstractBarDataProdiver, DataType, BarData

class CSVBarDataProdiver(AbstractBarDataProdiver):
    NAME = "CSVBarDataProdiver"
    INTRA_DATE_DATA_RESOLUTION = ["1S", "2S", "3S", "5S", "10S", "12S", "15S", "20S", "30S",
     "1T", "2T", "3T", "5T", "8T", "10T", "12T", "15T", "20T", "30T",
     "1H", "2H"]


    def __init__(self, session):
        super().__init__()

        self.in_period_data = False
        self.session = session
        self.config = self.session.config
        self.current_csv_file_idx = 0
        self.trade_date = None

        if not "1D" in self.config.data_resolution:
            self.config.data_resolution.append("1D")

        self._load_ticker_csv_file()

    def _load_ticker_csv_file(self):
        if self.trade_date is None:
            csv_file_path = self.config.data_path + self.config.exchange + "\\csv\\trade_date\\trade_date.csv"
            if utilities.check_file_exist(csv_file_path):
                self.trade_date = pd.DataFrame.from_csv(csv_file_path)
                #self.trade_date = self.trade_date.to_dict(orient ="index")
            else:
                raise OSError('CSV file not exist: ' + csv_file_path)

        is_first = True
        dfs = []
        for resolution in self.config.data_resolution:
            csv_filename = self.config.data_period[self.current_csv_file_idx] + "_" + self.config.data_ticker + "_" + resolution + ".csv"
            csv_file_path = self.config.data_path + self.config.exchange + "\\csv\\" + resolution + "\\" + csv_filename


            if utilities.check_file_exist(csv_file_path):
                df = pd.DataFrame.from_csv(csv_file_path)
                df['datetime'] = df.index

                if 'adjusted_time' not in df.columns:
                    df['datetime_for_sort'] = df['datetime']
                    df['adjusted_date'] = df.apply(lambda x: x['datetime_for_sort'].strftime('%Y%m%d'), axis=1)
                    df['adjusted_date'] = df['adjusted_date'].astype(int)

                    df['hour'] = df['datetime'].dt.hour
                    df['hour'] = df['hour'].astype(str)
                    df['hour'] = df['hour'].str.zfill(2)

                    df['minute'] = df['datetime'].dt.minute
                    df['minute'] = df['minute'].astype(str)
                    df['minute'] = df['minute'].str.zfill(2)

                    df['second'] = df['datetime'].dt.second
                    df['second'] = df['second'].astype(str)
                    df['second'] = df['second'].str.zfill(2)

                    if resolution not in CSVBarDataProdiver.INTRA_DATE_DATA_RESOLUTION:
                        df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                        df['hour'] = "33"
                        df['minute'] = "00"
                        df['second'] = "00"

                    df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                    df['adjusted_time'] = df['adjusted_time'].astype(int)
                else:
                    if resolution not in CSVBarDataProdiver.INTRA_DATE_DATA_RESOLUTION:
                        df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                        df['hour'] = "33"
                        df['minute'] = "00"
                        df['second'] = "00"

                        df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                        df['adjusted_time'] = df['adjusted_time'].astype(int)
                    else:
                        df['hour'] = df['hour'].astype(str)
                        df['hour'] = df['hour'].str.zfill(2)
                        df['minute'] = df['minute'].astype(str)
                        df['minute'] = df['minute'].str.zfill(2)
                        df['second'] = df['second'].astype(str)
                        df['second'] = df['second'].str.zfill(2)

                if is_first:
                    df['datetime_for_sort'] = df.index
                else:
                    df['datetime_for_sort'] = df.index + datetime.timedelta(seconds = utilities.RESOLUTION_IN_SEC[resolution])
                df['ticker'] = self.config.data_ticker
                df['resolution'] = resolution
                df['resolution_in_sec'] = utilities.RESOLUTION_IN_SEC[resolution]
                dfs.append(df)
            is_first = False


        df = pd.concat(dfs)
        df = df.sort_values(["adjusted_date","adjusted_time","resolution_in_sec"])
        df = df.drop('datetime_for_sort', 1)
        df = df[['open','high','low','close','volume','ticker','resolution','resolution_in_sec','adjusted_date','adjusted_time']]

        df.to_csv(self.config.data_period[self.current_csv_file_idx] + "_" + self.config.data_ticker + ".csv")

        if self.current_csv_file_idx == 0:
            if self.config.start_date is not None:
                start = df.index.searchsorted(self.config.start_date)
                self.data_df = df.ix[start:].itertuples()
        elif self.current_csv_file_idx == len(self.config.data_period) - 1:
            end = df.index.searchsorted(self.config.end_date)
            self.data_df = df.ix[:end].itertuples()

        self.data_df = df.itertuples()
        self.current_csv_file_idx += 1


    def _create_data(self, row):
        #'open', 'high', 'low', 'close', 'volume', 'ticker', 'resolution', 'resolution_in_sec', 'adjusted_date', 'adjest_time'
        dt, open_price, high_price, low_price, close_price, vol, ticker, resolution, resolution_in_sec, adjusted_date, adjest_time = row
        bar_data = BarData(
            ticker, resolution, dt,
            open_price, high_price, low_price, close_price, vol, adjusted_date, adjest_time
        )
        return bar_data

    def streaming(self):
        #loop data monthly
        for row in self.data_df:
            bar_data = self._create_data(row)

            if not self.in_period_data:
                if bar_data.timestamp >= self.config.start_date:
                    self.in_period_data = True
                    self.session.on_in_period_data()

            self._store_data(bar_data)
            self.session.on_data(bar_data)

        #load another month after looping
        if self.current_csv_file_idx != len(self.config.data_period):
            self._load_ticker_csv_file()
            self.streaming()
            return

        #exit is no data to loop
        self.session.on_complete()

    def get_ticker_trade_date_data(self, timestamp):
        return self.trade_date.loc[timestamp].to_dict()