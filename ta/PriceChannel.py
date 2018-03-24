from .base import TA, WindowTA
import numpy as np, copy
from collections import deque

class PriceChannel(WindowTA):
    def __init__(self, session, window_size, is_intra_day = False, is_save = True):
        super().__init__(session, window_size, is_intra_day, is_save)
        self.name = "PriceChannel(" + str(self.window_size) + ")"
        self.slug = "price_channel_" + str(self.window_size)

        self.open_price_deque = deque(maxlen=self.window_size)
        self.high_price_deque = deque(maxlen=self.window_size)
        self.low_price_deque = deque(maxlen=self.window_size)
        self.close_price_deque = deque(maxlen=self.window_size)

    def push_data(self, data):
        self.data_deque.append(data.close_price)
        self.open_price_deque.append(data.open_price)
        self.high_price_deque.append(data.high_price)
        self.low_price_deque.append(data.low_price)
        self.close_price_deque.append(data.close_price)


        if len(self.data_deque) == self.window_size:
            self.last_timestamp = data.timestamp
            if self.is_intra_day:
                if self.current_date is None:
                    self.on_new_date(data.timestamp)

                self.values[self.current_date].append({"max": np.max(self.high_price_deque), "min": np.min(self.low_price_deque)})
                self.values_ts[self.current_date].append(self.last_timestamp)
            else:
                self.values.append({"max":np.max(self.high_price), "min": np.min(self.low_price)})
                self.values_ts.append(self.last_timestamp)


    def get_low(self, _from=None, _to=None):
        if _from is None and _to is None:
            return np.min(self.low_price_deque)

        if _form is None:
            return np.min(self.low_price_deque[:_to])

        if _to is None:
            return np.min(self.low_price_deque[_from:])

        return np.min(self.low_price_deque[_from:_to])

    def get_high(self, _from=None, _to=None):
        if _from is None and _to is None:
            return np.max(self.high_price_deque)

        if _form is None:
            return np.max(self.high_price_deque[:_to])

        if _to is None:
            return np.max(self.high_price_deque[_from:])

        return np.max(self.high_price_deque[_from:_to])


    def get_high_idx(self):
        return self.high_price_deque.index(np.max(self.high_price_deque))


    def get_low_idx(self):
        return self.low_price_deque.index(np.min(self.low_price_deque))


    def print(self):
        print(self.data_deque)
        print(self.values)

    def calculate(self, data):
        return

    def to_dict(self):
        if not self.is_save:
            return

        from .. import utilities
        from datetime import timedelta
        time_offset = timedelta(minutes=utilities.EXCHANGE_TIME_ZONE[self.session.config.exchange])

        d = {}
        d['name'] = self.name
        d['slug'] = self.slug
        d['window_size'] = self.window_size

        d['values'] = self.values
        d['calculated_values'] = self.calculated_values

        if self.is_intra_day:
            d['values_ts'] = {}
            for date_key in self.values_ts:
                d['values_ts'][date_key] = []
                for ts in self.values_ts[date_key]:
                    d['values_ts'][date_key].append((ts + time_offset).timestamp())

            d['calculated_values_ts'] = {}
            for date_key in self.calculated_values_ts:
                d['calculated_values_ts'][date_key] = []
                for ts in self.calculated_values_ts[date_key]:
                    d['calculated_values_ts'][date_key].append((ts + time_offset).timestamp())
        else:
            d['values_ts'] = []
            for ts in self.values_ts:
                d['values_ts'].append((ts + time_offset).timestamp())

            d['calculated_values_ts'] = []
            for ts in self.calculated_values_ts:
                d['calculated_values_ts'].append((ts + time_offset).timestamp())

        return d