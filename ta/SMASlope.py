from .base import TA, WindowTA
from .. import utilities
import datetime
import numpy as np, copy

###########################################################
#Please also update SMA.py and SMASlop.py
###########################################################

class SMASlope(WindowTA):
    def __init__(self, session, window_size:int, look_back_window_size=1, resolution="1T", is_intra_day = False, is_save = True):
        super().__init__(session, window_size, look_back_window_size, resolution, is_intra_day, is_save)
        self.name = "SMA(" + str(self.window_size) + ")"
        self.slug = "sma_" + str(self.window_size)

        self.all_data = []

        if self.is_intra_day:
            self.sma_values = {}
            self.calculated_sma_values = {}
        else:
            self.sma_values = []
            self.calculated_sma_values = []

    def push_data(self, data):
        self.data_deque.append(data.close_price)
        if len(self.data_deque) == self.window_size:
            self.last_timestamp = data.timestamp
            if self.is_intra_day:
                if self.current_date is None:
                    self.on_new_date(data.timestamp)

                mean = np.mean(self.data_deque)
                self.sma_values[self.current_date].append(np.mean(mean))
                if(len(self.sma_values[self.current_date])==0):
                    self.values[self.current_date].append(0)
                else:
                    self.values[self.current_date].append(self.sma_values[self.current_date][-1]-self.sma_values[self.current_date][-2])


                adjusted_ts = self.last_timestamp + datetime.timedelta(seconds=utilities.RESOLUTION_IN_SEC[self.resolution])
                self.values_ts[self.current_date].append(adjusted_ts)

                self.look_back_value.append(mean)
            else:
                mean = np.mean(self.data_deque)
                self.sma_values.append(np.mean(mean))
                if(len(self.values)==0):
                    self.values.append(0)
                else:
                    self.values.append(self.sma_values[-1]-self.sma_values[-2])
                self.values_ts.append(self.last_timestamp)
                self.look_back_value.append(mean)

    def calculate(self, data):
        if len(self.data_deque) == self.window_size:
            _temp_data_deque = list(self.data_deque)[1:]
            _temp_data_deque.append(data.close_price)
            m = float(np.mean(_temp_data_deque))
            if len(self.calculated_values) == 0:
                self.calculated_values = copy.deepcopy(self.values)
                self.calculated_values_ts = copy.deepcopy(self.values_ts)

            self.calculated_values.append(m-self.sma_values[-1])
            self.calculated_values_ts.append(data.timestamp)

            return m
        else:
            return False

    def get_look_back_value(self, idx):
        return self.look_back_value[idx]

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
        d['resolution'] = self.resolution

        d['values'] = self.values
        d['calculated_values'] = self.calculated_values
        if self.is_intra_day:
            d['values_ts'] = {}
            for date_key in self.values_ts:
                d['values_ts'][date_key] = []
                for ts in self.values_ts[date_key]:
                    print('date_key', date_key)
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