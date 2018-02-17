from enum import IntEnum
from . import utilities
import json, datetime, os

class SessionMode(IntEnum):
    INTRA_DAY_SINGLE_PROCESS = 0
    INTER_DAY_SINGLE_PROCESS = 1
    INTRA_DAY_MULTI_PROCESS = 2
    INTER_DAY_MULTI_PROCESS = 3
    IB_DEMO_TRADE = 4
    IB_LIVE_TRADE = 5

class SessionConfig:
    def __init__(self, **kwargs):
        #1. read config file
        #2. assign config value

        # ---------------------------Load Config File---------------------------
        self.is_debug = False
        self.data_path = "C:\\data\\"
        self.log_directory = "C:\\log\\"
        self.api_path = "http://127.0.0.1/antXXXXXXX/XXXXXXXX/XXXXXXXX"
        self.base_report_directory = "C:\\Data\\backtest_report\\reports\\"
        # ----------------------------------------------------------------------

        # -----------------------------Mode Setting-----------------------------
        self.mode = -1
        #Mode 0 = intra day backtest (single process)
        #Mode 1 = inter day backtest (single process)
        #Mode 2 = intra day backtest (multiple process)
        #Mode 3 = inter day backtest (multiple process)
        #Mode 4 = IB demo trade
        #Mode 5 = IB live trade
        self.mode = kwargs['mode']
        # ----------------------------------------------------------------------

        # --------------------------Session ID Setting--------------------------
        if "session_id" in kwargs:
            self.session_id = kwargs['session_id']
        else:
            self.session_id = 999999

        self.is_sub_process = False
        self.num_sub_process = -1
        self.process_no = -1

        # Ask database
        # ----------------------------------------------------------------------
        self.data_start_date = kwargs['data_start_date']
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']
        self.trade_ticker = kwargs['trade_ticker']
        self.data_ticker = kwargs['data_ticker']
        self.contract = kwargs['contract']
        self.base_quantity = kwargs['base_quantity']
        self.exchange = kwargs['exchange']

        if self.mode in [ SessionMode.INTRA_DAY_SINGLE_PROCESS,
                         SessionMode.INTER_DAY_SINGLE_PROCESS,
                         SessionMode.INTRA_DAY_MULTI_PROCESS,
                         SessionMode.INTER_DAY_MULTI_PROCESS]:
            self.cash = kwargs['cash']
        elif self.mode in [SessionMode.IB_DEMO_TRADE, SessionMode.IB_LIVE_TRADE]:
            self.cash = "ask ib"
        else:
            raise Exception("Incorrect Session Mode")


        if self.mode in [ SessionMode.INTRA_DAY_SINGLE_PROCESS,
                         SessionMode.INTER_DAY_SINGLE_PROCESS,
                         SessionMode.INTRA_DAY_MULTI_PROCESS,
                         SessionMode.INTER_DAY_MULTI_PROCESS]:
            self.data_provider_class = kwargs['data_provider_class']
        elif self.mode in [SessionMode.IB_DEMO_TRADE, SessionMode.IB_LIVE_TRADE]:
            self.data_provider_class = "ask ib"
        else:
            raise Exception("Incorrect Session Mode")


        self.data_resolution = kwargs['data_resolution']
        if "1D" not in self.data_resolution:
            self.data_resolution.append("1D")

        self.strategy_class = kwargs['strategy_class']
        self.strategy_parameter = kwargs['strategy_parameter']
        self.prepare_data_period()


        self.portfolio_class = kwargs['portfolio_class']
        self.order_handler_class = kwargs['order_handler_class']


        #This is for backtest only
        self.slippage_pips = 0
        if "slippage_pips" in kwargs:
            self.slippage_pips = kwargs["slippage_pips"]

        self.commission = 0
        if "commission" in kwargs:
            self.commission = kwargs["commission"]
        # ----------------------------------------------------------------------

        self.report_folder_name = datetime.datetime.now().strftime(
                "%Y%m%d_") + str(self.session_id).zfill(6) + "_" + self.strategy_class.STRATEGY_SLUG
        self.report_directory = self.base_report_directory + self.report_folder_name


        if not os.path.exists(self.report_directory):
            os.makedirs(self.report_directory)

    def prepare_data_period(self):
        self.data_period = utilities.get_months_between_two_datetime(self.data_start_date, self.end_date)

    def save(self):
        dict_to_save = {}
        dict_to_save["session_id"] = self.session_id
        dict_to_save["mode"] = self.mode
        dict_to_save["data_start_date"] = self.data_start_date.strftime("%Y%m%d")
        dict_to_save["start_date"] = self.start_date.strftime("%Y%m%d")
        dict_to_save["end_date"] = self.end_date.strftime("%Y%m%d")
        dict_to_save["trade_ticker"] = self.trade_ticker
        dict_to_save["data_ticker"] = self.data_ticker
        dict_to_save["contract"] = self.contract
        dict_to_save["base_quantity"] = self.base_quantity
        dict_to_save["exchange"] = self.exchange

        dict_to_save["is_sub_process"] = self.is_sub_process
        dict_to_save["num_sub_process"] = self.num_sub_process
        dict_to_save["process_no"] = self.process_no

        dict_to_save["cash"] = self.cash
        dict_to_save["data_provider_class"] = self.data_provider_class.NAME
        dict_to_save["data_resolution"] = '['+ ','.join(self.data_resolution) + ']'

        dict_to_save["strategy_class"] = {}
        dict_to_save["strategy_class"]["name"] = self.strategy_class.STRATEGY_NAME
        dict_to_save["strategy_class"]["slug"] = self.strategy_class.STRATEGY_SLUG
        dict_to_save["strategy_class"]["version"] = self.strategy_class.VERSION
        dict_to_save["strategy_class"]["last_update"] = self.strategy_class.LAST_UPDATE_DATE

        dict_to_save["strategy_class"]["parameter"] = self.strategy_parameter

        dict_to_save["portfolio_class"] = self.portfolio_class.NAME
        dict_to_save["order_handler_class"] = self.order_handler_class.NAME
        dict_to_save["slippage_pips"] = self.slippage_pips
        dict_to_save["commission"] = self.commission

        config_filename = "//session_config.json"
        if self.is_sub_process:
            config_filename = "//session_config_"+str(self.process_no)+".json"

        with open(self.report_directory + config_filename, 'w') as fp:
            json.dump(dict_to_save, fp, indent=4)