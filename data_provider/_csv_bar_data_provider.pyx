import os, pandas as pd

from .. import utilities
from ..functions import ant_time
from ..events.data_event import BarEvent

from .base import AbstractBarDataFeeder

cdef class CSVBarDataFeeder(AbstractBarDataFeeder):
    def __init__(self, config):
        super().__init__()
        self.current_csv_file_idx = 0
        self.config = config
        self.session = self.config.session
        self.events_queue = self.session.events_queue
        self.tickers = self.config.tickers

        self.tickers_data = {}
        self.tickers_price = {}

        self.data_resolution = self.config.data_resolution

        self.start_date = self.config.start_date
        self.end_date = self.config.end_date
        self.config.data_period = utilities.get_months_between_two_datetime(self.start_date,self.end_date);

        self.config.continue_session = True

        self._subscribe_ticker()

    def _load_ticker_csv_file(self):
        csv_filename = self.config.data_period[
                            self.current_csv_file_idx]+"_"+self.config.data_ticker+"_"+self.config.data_resolution+".csv"
        csv_file_path = self.config.data_path + self.config.exchange + "\\csv\\" + self.config.data_resolution + "\\" + csv_filename

        print("load csv file:",csv_file_path)
        if utilities.check_file_exist(csv_file_path):
            df = pd.DataFrame.from_csv(csv_file_path)
            df['ticker'] = self.config.data_ticker
            df['resolution'] = self.config.data_resolution

            self.tickers_data[self.config.data_ticker] = df

            if self.current_csv_file_idx == 0:
                if self.start_date is not None:
                    start = df.index.searchsorted(self.start_date)
                    self.bar_stream = df.ix[start:].itertuples()
            elif self.current_csv_file_idx == len(self.config.data_period) - 1:
                end = df.index.searchsorted(self.end_date)
                self.bar_stream = df.ix[:end].itertuples()
            else:
                self.bar_stream = df.itertuples()
            self.current_csv_file_idx += 1
        else:
            raise OSError ('CSV file not exist: ' + csv_file_path)

    def _subscribe_ticker(self):
        self._load_ticker_csv_file()
        self.tickers_price[self.config.data_ticker] = {}

    def _create_event(self, row):
        dt, open_price, high_price, low_price, close_price, vol, ticker, resolution = row

        open_price = open_price
        high_price = high_price
        low_price = low_price

        bar_event = BarEvent(
            ticker, resolution, dt,
            open_price, high_price, low_price, close_price, vol
        )
        return bar_event

    def _store_event(self, event):
        super()._store_event(event)
        self.tickers_price[event.ticker]['open'] = event.open_price
        self.tickers_price[event.ticker]['high'] = event.high_price
        self.tickers_price[event.ticker]['low'] = event.low_price
        self.tickers_price[event.ticker]['close'] = event.close_price
        self.tickers_price[event.ticker]['volume'] = event.volume
        self.tickers_price[event.ticker]['type'] = event.type
        self.tickers_price[event.ticker]['ticker'] = event.ticker
        self.tickers_price[event.ticker]['resolution'] = event.resolution

    def stream_next(self):
        try:
            row = next(self.bar_stream)
            dt, open_price, high_price, low_price, close_price, vol, ticker, resolution = row
        except StopIteration:
            if self.current_csv_file_idx != len(self.config.data_period):
                self._load_ticker_csv_file()
                self.stream_next()
            else:
                self.config.continue_session = False
            return

        bar_event = self._create_event(row)
        self._store_event(bar_event)
        self.events_queue.put(bar_event)