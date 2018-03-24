from abc import ABCMeta
from collections import deque
from .. import utilities

class TA(object):
    __metaclass__ = ABCMeta




class WindowTA(object):
    __metaclass__ = ABCMeta

    def __init__(self, session, window_size, look_back_window_size, is_intra_day, is_save):
        self.session = session
        self.last_timestamp = None
        self.window_size = window_size
        self.look_back_window_size = look_back_window_size
        self.data_deque = deque(maxlen=self.window_size)
        self.look_back_value = deque(maxlen=self.look_back_window_size)

        self.is_save = is_save
        self.is_intra_day = is_intra_day
        if self.is_intra_day:
            self.current_date = None
            self.values = {}
            self.values_ts = {}
            self.calculated_values = {}
            self.calculated_values_ts = {}
        else:
            self.values = []
            self.values_ts = []
            self.calculated_values = []
            self.calculated_values_ts = []

    def on_new_date(self, date_ts):
        self.current_date = utilities.dt_get_date_str(date_ts)

        self.values[self.current_date] = []
        self.values_ts[self.current_date] = []
        self.calculated_values[self.current_date] = []
        self.calculated_values_ts[self.current_date] = []

