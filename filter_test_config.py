from . import utilities
from .session_config import SessionStaticVariable
import json, datetime, os
from dateutil.relativedelta import relativedelta

class FilterTestConfig:
    def __init__(self, **kwargs):
        #1. read config file
        #2. assign config value

        # ---------------------------Load Config File---------------------------
        self.data_path = SessionStaticVariable.data_path
        self.log_directory = SessionStaticVariable.log_directory
        self.api_path = SessionStaticVariable.api_path
        self.base_report_directory = SessionStaticVariable.base_report_directory
        self.base_ta_directory = SessionStaticVariable.base_ta_directory
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        self.filter_test_name = None
        self.backtest_name = kwargs['backtest_name']
        self.filter_class = kwargs['filter_class']
        self.filter = self.filter_class.NAME
        self.filter_parameter = None
        self.filter_list = None
        self.filter_resolution = self.filter_class.RESOLUTION
        self.backtest_report_dir = SessionStaticVariable.base_report_directory + self.backtest_name + "\\"

        self.filter_result = None

        session_config = utilities.load_json(self.backtest_report_dir + "session_config.json")
        positions = utilities.load_json(self.backtest_report_dir + "positions.json")

        self.start_date = session_config['start_date']
        self.end_date = session_config['end_date']
        self.data_ticker = session_config['data_ticker']
        self.exchange = session_config['exchange']

        dfs = []
        first_data_date = datetime.datetime.strptime("20021101", '%Y%m%d')
        self.start_date = datetime.datetime.strptime(self.start_date, '%Y%m%d')
        self.end_date = datetime.datetime.strptime(self.end_date, '%Y%m%d')
        day_back_start_date = self.start_date - relativedelta(years=1)

        if (day_back_start_date < first_data_date):
            self.start_date = first_data_date
        else:
            self.start_date = day_back_start_date

        self.data_period = utilities.get_months_between_two_datetime(self.start_date, self.end_date)


    def save(self):
        dict_to_save = {}
        dict_to_save["backtest_name"] = self.backtest_name
        dict_to_save["start_date"] = self.start_date.strftime("%Y%m%d")
        dict_to_save["end_date"] = self.end_date.strftime("%Y%m%d")
        dict_to_save["data_ticker"] = self.data_ticker
        dict_to_save["exchange"] = self.exchange

        dict_to_save["filter_class"] = {}
        dict_to_save["filter_class"]["name"] = self.filter_class.NAME
        dict_to_save["filter_class"]["parameter"] = self.filter_parameter
        dict_to_save["filter_class"]["resolution"] = '['+ ','.join(self.filter_resolution) + ']'

        dict_to_save["filter_result"] = self.filter_result

        config_filename = "\\filter_test_config.json"
        with open(self.backtest_report_dir + "filtered\\" + self.filter_test_name + config_filename, 'w') as fp:
            json.dump(dict_to_save, fp, indent=4)