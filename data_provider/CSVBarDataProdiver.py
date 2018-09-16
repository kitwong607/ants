import os, pandas as pd, datetime, numpy as np

from .. import utilities
from ..functions import ant_time
from .base import AbstractBarDataProdiver, DataType, BarData

class CSVBarDataProdiver(AbstractBarDataProdiver):
    NAME = "CSVBarDataProdiver"


    def __init__(self, session):
        super().__init__()

        self.session = session
        self.config = self.session.config

        self.in_period_data = False
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

                '''
                print(self.trade_date)
                self.trade_date['date'] = self.trade_date.index
                month = self.trade_date['date'].dt.month.astype(str).str.zfill(2)
                day = self.trade_date['date'].dt.day.astype(str).str.zfill(2)
                year = self.trade_date['date'].dt.year.astype(str).str.zfill(4)
                self.trade_date['trade_date'] = year + "-" + month + "-" + day
                self.trade_date.index = self.trade_date['trade_date']
                self.trade_date_dict = self.trade_date.to_dict('index')
                self.trade_date.index = self.trade_date['date']
                #print(test)
                #quit()
                '''
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

                    month = df['datetime'].dt.month.astype(str).str.zfill(2)
                    day   = df['datetime'].dt.day.astype(str).str.zfill(2)
                    year  = df['datetime'].dt.year.astype(str).str.zfill(4)
                    df['adjusted_date'] = year + month + day
                    #df['adjusted_date'] = df.apply(lambda x: x['datetime_for_sort'].strftime('%Y%m%d'), axis=1)
                    df['adjusted_date'] = df['adjusted_date'].astype(int)

                    df['hour'] = df['datetime'].dt.hour
                    df['hour'] = df['hour'].astype(str).str.zfill(2)

                    df['minute'] = df['datetime'].dt.minute
                    df['minute'] = df['minute'].astype(str)

                    df['second'] = df['datetime'].dt.second
                    df['second'] = df['second'].astype(str).str.zfill(2)

                    if resolution not in utilities.INTRA_DATE_DATA_RESOLUTION:
                        df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                        df['hour'] = "33"
                        df['minute'] = "00"
                        df['second'] = "00"

                    df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                    df['adjusted_time'] = df['adjusted_time'].astype(int)
                else:
                    if resolution not in utilities.INTRA_DATE_DATA_RESOLUTION:
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
                    df['datetime_for_sort'] = df.index + datetime.timedelta(seconds = utilities.RESOLUTION_IN_SEC[resolution])


                df['ticker'] = self.config.data_ticker
                df['resolution'] = resolution
                df['resolution_in_sec'] = utilities.RESOLUTION_IN_SEC[resolution]


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


        if self.current_csv_file_idx == 0:
            start = df.index.searchsorted(self.config.start_date)
            self.data_df = df.ix[start:].itertuples()
        elif self.current_csv_file_idx == len(self.config.data_period) - 1:
            end = df.index.searchsorted(self.config.end_date)
            self.data_df = df.ix[:end].itertuples()

        self.data_df = df.itertuples()
        self.current_csv_file_idx += 1


    def streaming(self):
        #loop data monthly
        for row in self.data_df:
            bar_data = BarData(row)

            if not self.in_period_data:
                if bar_data.timestamp >= self.config.start_date:
                    self.in_period_data = True
                    self.session.on_in_period_data()


            self._store_data(bar_data)
            self.session.on_data(bar_data)

        #load another month after looping
        if self.current_csv_file_idx != len(self.config.data_period):
            start_time = datetime.datetime.now()

            self._load_ticker_csv_file()

            time_elapsed = datetime.datetime.now() - start_time
            print('Time elapsed for load data (hh:mm:ss.ms) {}'.format(time_elapsed))


            self.streaming()
            return

        #exit is no data to loop
        self.session.on_complete()


    def get_ticker_trade_date_data(self, timestamp):
        #return self.trade_date_dict[str(timestamp.date())]
        return self.trade_date.loc[timestamp].to_dict()