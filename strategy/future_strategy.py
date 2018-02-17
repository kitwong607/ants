from .base import AbstractStrategy
from ..data_provider.base import DataType
from .. import utilities

MONTH_CODE = {"1": "F", "2": "G", "3": "H", "4": "J",
             "5": "K", "6": "M", "7": "N", "8": "Q",
             "9": "U", "10": "V", "11": "X", "12": "Z"}

HKEX_FUTURE = ["HSI","MHI"]

#call sequence
#1 on_new_date              -> if data is in a new day
#2 calculate_intra_day_ta   -> if data is intra day data, *it also trigger if on_new_date triggered.
#3 calculate_entry_signals  -> if data is intra day data
#4 calculate_exit_signals   -> if data is intra day data and portfolio contain position

class FutureAbstractStrategy(AbstractStrategy):
    def setup(self, session):
        self.session = session
        self.strategy_class = self.session.config.strategy_class
        self.contract = self.session.config.contract
        self.parameter = self.session.config.strategy_parameter

        self.in_period_data = False

        self._is_end_day = True
        #common
        self.all_inter_ta = []
        self.inter_day_ta = []
        self.inter_day_ta_separated = []
        self.all_intra_ta = []
        self.intra_day_ta = []
        self.intra_day_ta_separated = []

        self.invested = False
        self.invested_count = 0

        self.current_date = None
        self.previous_date = None
        self.td_close_time = None
        self.trade_date_data = None

        #filter related
        self.today_action = None

        self.contact = self.session.config.contract
        self.base_quantity = self.session.config.base_quantity

        self.current_date = self.previous_date = None
        self.p_open = None
        self.p_high = None
        self.p_low = None
        self.p_close = None
        self.p_volume = None

        self.pd_open = self.td_open = None
        self.pd_high = self.td_high = None
        self.pd_low = self.td_low = None
        self.pd_close = self.td_close = None
        self.pd_volume = self.td_volume = None

        if self.parameter is None:
            self.parameter = strategy_class.OPTIMIZATION_PARAMETER

    def calculate_tick_data(self, data):
        pass

    def calculate_bar_data(self, data):
        #1 is day end
        if data.resolution == "1D":
            #day end
            self._is_end_day = True
            self.pd_data = data
            self.on_end_date(data)
        elif (data.resolution in utilities.INTRADAY_BAR_SIZE):
            if(self._is_end_day):
                self._is_end_day = False

                self.bars = {}
                self.ticks = []

                self.previous_date = self.current_date
                self.current_date = utilities.remove_time_from_datetime(data.timestamp)
                self.invested = False
                self.invested_count = 0

                self.trade_date_date = self.session.data_provider.get_ticker_trade_date_data(self.current_date)

                close_time = self.trade_date_date["aht_close_time"]
                if close_time == 0:
                    close_time = self.trade_date_date["close_time"]
                close_time = str(close_time)
                close_time = utilities.add_time_to_datetime(self.current_date, int(close_time[0:2]), int(close_time[2:4]), int(close_time[4:]))
                self.td_close_time = close_time

                self.td_open = data.open_price
                self.td_high = data.high_price
                self.td_low = data.low_price
                self.td_close = data.close_price
                self.td_volume = data.volume

                is_new_date = True

                self.update_contact()
                self.on_new_date(data)

            if data.high_price > self.td_high: self.td_high = data.high_price
            if data.low_price < self.td_low: self.td_low = data.low_price
            self.td_close = data.close_price
            self.td_volume += data.volume

            self.last_bar = data
            self.calculate_intra_day_ta(data)

            if self.today_action is not None and self.in_period_data:
                self.calculate_entry_signals(data)

        if self.session.config.trade_ticker in self.session.portfolio.positions:
            self.calculate_exit_signals(data)

    def update_contact(self):
        trade_data = self.session.data_provider.get_ticker_trade_date_data(self.current_date)
        expected_expiry_month = str(trade_data["expected_expiry_month"])
        if int(expected_expiry_month[0]) >= 8:
            year = str(1900 + int(expected_expiry_month[:2]))
        else:
            year = str(2000 + int(expected_expiry_month[:2]))

        month = str(int(expected_expiry_month[2:]))

        if self.session.config.trade_ticker in HKEX_FUTURE:
            self.contract = "HKFE.F." + self.session.config.trade_ticker + month + year
        else:
            print("future_strategy.update_contact not develop for " + self.session.config.trade_ticker)

    def set_inverted(self):
        self.invested = True
        self.invested_count += 1

    def set_not_inverted(self):
        self.invested = False

    def ta_to_dict(self, input_ta):
        ta_d = {}
        for ta in input_ta:
            _d = ta.to_dict()

            if 'slug' in _d.keys():
                ta_d[_d['slug']] = _d
            else:
                for ta_key in _d:
                    ta_d[ta_key] = _d[ta_key]

        return ta_d


    def save(self):
        import inspect, os, json
        from shutil import copyfile

        if (self.session.config.is_sub_process and self.session.config.process_no==1) or (not self.session.config.is_sub_process):
            strategy_class_path = inspect.getfile(self.session.config.strategy_class)
            copyfile(strategy_class_path, self.session.config.report_directory + "//" + os.path.basename(strategy_class_path))
            copyfile(strategy_class_path, self.session.config.report_directory + "//strategy.txt")

        ta_d = self.ta_to_dict(self.inter_day_ta)
        json_filename = "//inter_day_ta.json"
        if self.session.config.is_sub_process:
            json_filename = "//inter_day_ta_" + str(self.session.config.process_no) + ".json"
        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(ta_d, fp, indent=4, cls=utilities.AntJSONEncoder)


        ta_d = self.ta_to_dict(self.inter_day_ta_separated)
        json_filename = "//inter_day_ta_separated.json"
        if self.session.config.is_sub_process:
            json_filename = "//inter_day_ta_separated_" + str(self.session.config.process_no) + ".json"
        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(ta_d, fp, indent=4, cls=utilities.AntJSONEncoder)

        ta_d = self.ta_to_dict(self.intra_day_ta)
        json_filename = "//intra_day_ta.json"
        if self.session.config.is_sub_process:
            json_filename = "//intra_day_ta_" + str(self.session.config.process_no) + ".json"
        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(ta_d, fp, indent=4, cls=utilities.AntJSONEncoder)

        ta_d = self.ta_to_dict(self.intra_day_ta_separated)
        json_filename = "//intra_day_ta_separated.json"
        if self.session.config.is_sub_process:
            json_filename = "//intra_day_ta_separated_" + str(self.session.config.process_no) + ".json"
        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(ta_d, fp, indent=4, cls=utilities.AntJSONEncoder)