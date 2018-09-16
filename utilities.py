import datetime, time, json, numpy as np, math, pandas as pd, os, importlib, calendar
from pathlib import Path
from dateutil.rrule import rrule, MONTHLY
from os import listdir
from os.path import isfile, join
import ants
from . import db
from . import session_config
from .session_config import SessionStaticVariable
from distutils.dir_util import copy_tree
from subprocess import Popen, CREATE_NEW_CONSOLE


# region Public Variable
#INTRADAY_BAR_SIZE = ["1S","2S","3S","5S","10S","12S","15S","20S","30S","1T","2T","3T","5T","8T","10T","12T","15T","20T","30T","1H","2H"]
RESOLUTION_IN_SEC = {"1S": 1, "2S": 2, "3S": 3, "5S": 5, "10S": 10, "12S": 12, "15S": 15, "20S": 30, "30S": 30,
                     "1T": 60, "2T": 120, "3T": 180, "5T": 300, "8T": 480, "10T": 600, "12T": 720, "15T": 900,
                     "20T": 1200, "30T": 1800,
                     "1H": 3600,"2H": 7200,
                     "1D": 86400}

EXCHANGE_TIME_ZONE = {"HKEX": 480}

INTRA_DATE_DATA_RESOLUTION = ["1S", "2S", "3S", "5S", "10S", "12S", "15S", "20S", "30S",
     "1T", "2T", "3T", "5T", "8T", "10T", "12T", "15T", "20T", "30T",
     "1H", "2H"]

INTRADAY_BAR_SIZE = INTRA_DATE_DATA_RESOLUTION
# endregion


# region Datetime calculation methods
# region Different
def get_months_between_two_datetime(start_date,end_date,is_return_str_list=True):
    start_date = start_date.replace(day=1)
    months = [dt for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]
    if is_return_str_list:
        month_str_list = [m.strftime("%Y%m") for m in months]
        return month_str_list
    return months

def remove_time_from_datetime(datetime_to_remove):
    time_offset = datetime.timedelta(
                hours=datetime_to_remove.hour,
                minutes=datetime_to_remove.minute,
                seconds=datetime_to_remove.second,
                microseconds=datetime_to_remove.microsecond)
    datetime_to_remove = datetime_to_remove - time_offset
    return datetime_to_remove


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def second_between_two_datetime(datetime_1, datetime_2):
    if(datetime_1>datetime_2):
        return abs((datetime_1 - datetime_2).seconds)
    else:
        return abs((datetime_2 - datetime_1).seconds)


def mintue_between_two_datetime(datetime_1, datetime_2):
    if(datetime_1>datetime_2):
        return abs((datetime_1 - datetime_2).seconds) // 60  # in mintues
    else:
        return abs((datetime_2 - datetime_1).seconds) // 60  # in mintues
# endregion


# region Calculation
def get_total_minute_from_datetime(dt):
    return dt.hour * 60 + dt.minute


def add_time_to_datetime(datetime_to_add, hour, minute, second):
    time_offset = datetime.timedelta(
        hours=hour,
        minutes=minute,
        seconds=second)
    datetime_to_add = datetime_to_add + time_offset
    return datetime_to_add


def add_months(sourcedate, months):
    months = int(months)
    if (months == 0):
        return sourcedate
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def add_months_with_last_date(sourcedate, months):
    months = int(months)
    if (months == 0):
        return sourcedate
    if (months > 0):
        months -= 1
    else:
        months += 1
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day + 31, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
# endregion


# region Comparsion
def is_new_date(current_date, input_date):
    if (current_date == None or current_date.date() != input_date.date()):
        return True
    return False


def is_time_before(marker_hour, marker_mintue, marker_second, input_hour, input_minute, input_second):
    marker_time = marker_hour*10000 + marker_mintue*100 + marker_second
    input_time = input_hour*10000 + input_minute*100 + input_second
    if input_time < marker_time:
        return True
    else:
        return False


def is_time_after(marker_hour, marker_mintue, marker_second, input_hour, input_minute, input_second):
    marker_time = marker_hour * 10000 + marker_mintue * 100 + marker_second
    input_time = input_hour * 10000 + input_minute * 100 + input_second
    if input_time > marker_time:
        return True
    else:
        return False
# endregion


# region Convert format
def dt_to_ts(dt):
    return dt.timestamp()

def dt_get_date_str(dt):
    return dt.strftime('%Y%m%d')

def dt_get_time_str(dt):
    return dt.strftime('%H%M%S')

def to_adjusted_time(time_int):
    if time_int<90000:
        time_int += 240000

    return time_int
# endregion


# endregion


# region File methods
def check_file_exist(file_path):
    my_file = Path(file_path)
    if my_file.is_file():
        return True
    return False


def create_folder(path):
    if path == "":
        return False

    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def create_file(path):
    if not is_file_exist(path):
        open(path, 'a').close()
        return True
    return False


def is_file_exist(path):
    if os.path.exists(path):
        return True
    return False
# endregion


# region Load data methods
def load_inter_day_data(_exchange, _ticker, _date, _resolution):
    _data_path = SessionStaticVariable.data_path

    if "," not in _date:
        _date_list = [_date]
    else:
        _date_list = _date.split(",")

    _date_list.sort()

    _months = []
    for _date_str in _date_list:
        _month = _date_str[:6]
        if not _month in _date_list:
            _months.append(_month)


    dfs = []
    is_first = True
    for _month in _months:
        csv_filename = _month + "_" + _ticker + "_" + _resolution + ".csv"
        csv_file_path = _data_path + _exchange + "\\csv\\" + _resolution + "\\" + csv_filename

        df = pd.DataFrame.from_csv(csv_file_path)
        if is_first:
            df['datetime_for_sort'] = df.index
        else:
            df['datetime_for_sort'] = df.index + datetime.timedelta(seconds=RESOLUTION_IN_SEC[_resolution])
        df['ticker'] = _ticker
        df['resolution'] = _resolution
        df['resolution_in_sec'] = RESOLUTION_IN_SEC[_resolution]
        dfs.append(df)

        is_first = False

    df = pd.concat(dfs)
    df = df.sort_values(["datetime_for_sort", "resolution_in_sec"])
    df = df.drop('datetime_for_sort', 1)

    start_datetime = datetime.datetime.strptime(_date_list[0], '%Y%m%d') + datetime.timedelta(hours=8)  #to 8am
    end_datetime = datetime.datetime.strptime(_date_list[-1], '%Y%m%d')  + datetime.timedelta(hours=32) #before next day 8 am
    start = df.index.searchsorted(start_datetime)
    end = df.index.searchsorted(end_datetime)

    return df.ix[start:end]


def load_month_data():
    pass
# endregion


# region Count time methods
def start_count_time_used():
    return time.time()


def stop_count_time_used(start_time, task):
    print("--- "+str(round(time.time() - start_time, 2))+" seconds --- for " + task)
# endregion


# region JSON methods
class AntJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(AntJSONEncoder, self).default(obj)

def load_json(path):
    with open(path) as json_data:
        return json.load(json_data)
#endregion


# region Create backtest report / summary methods
def prepare_backtest_report_insert_to_db(d):
    d['win_rate'] = round(d['win_rate'], 3)
    d['num_trade'] = round(d['num_trade'], 3)
    d['pnl'] = round(d['pnl'], 3)
    d['net_pips'] = round(d['net_pips'], 3)
    d['profit_factor'] = round(d['profit_factor'], 3)
    d['payoff_ratio'] = round(d['payoff_ratio'], 3)
    d['roci'] = round(d['roci'], 3)

    d['sharpe_ratio'] = round(d['sharpe_ratio'], 3)
    d['standard_deviation'] = round(d['standard_deviation'], 3)
    d['standard_error'] = round(d['standard_error'], 3)
    d['tharp_expectancy'] = round(d['tharp_expectancy'], 3)
    d['expectancy'] = round(d['expectancy'], 3)

    d['mdd'] = round(d['mdd'], 3)
    d['mdd_pct'] = round(d['mdd_pct'], 3)
    d['mdd_daily'] = round(d['mdd_daily'], 3)
    d['mdd_pct_daily'] = round(d['mdd_pct_daily'], 3)
    d['dd_duration'] = round(d['dd_duration'], 3)

    d['dd_duration_daily'] = round(d['dd_duration_daily'], 3)
    d['avg_pips_pre_contract'] = round(d['avg_pips_pre_contract'], 3)

    key_to_fillzero = ["win_rate", "num_trade", "pnl", "net_pips", "profit_factor",
                   "payoff_ratio", "roci", "sharpe_ratio", "standard_deviation", "standard_error",
                   "tharp_expectancy", "expectancy", "mdd", "mdd_pct", "mdd_daily",
                   "mdd_pct_daily", "dd_duration", "dd_duration_daily", "avg_pips_pre_contract"]

    key_to_save = ['win_rate', 'num_trade', 'pnl', 'net_pips', 'profit_factor', 'payoff_ratio', 'roci', 'sharpe_ratio', 'standard_deviation', 'standard_error', 'tharp_expectancy', 'expectancy', 'mdd', 'mdd_pct', 'mdd_daily', 'mdd_pct_daily', 'dd_duration', 'dd_duration_daily', 'avg_pips_pre_contract', 'report_folder_name', 'report_full_path']

    new_d = {}
    for key in d:
        if key in key_to_fillzero:
            if math.isnan(float(d[key])):
                d[key] = 0

        if key in key_to_save:
            new_d[key] = d[key]

    return new_d


def create_filter_report(backtest_filename):
    key_to_calculate = ["num_trade", "win_rate", "pnl", "net_pips", "avg_pips_pre_contract", "profit_factor",
                        "payoff_ratio", "roci", "sharpe_ratio", "tharp_expectancy", "expectancy", "mdd", "mdd_pct",
                        "mdd_daily", "mdd_pct_daily", "dd_duration", "dd_duration_daily"]
    optimization_values = {"num_trade": [], "win_rate": [], "pnl": [], "net_pips": [], "avg_pips_pre_contract": [],
                           "profit_factor": [], "payoff_ratio": [], "roci": [], "sharpe_ratio": [],
                           "tharp_expectancy": [], "expectancy": [], "mdd": [], "mdd_pct": [], "mdd_daily": [],
                           "mdd_pct_daily": [], "dd_duration": [], "dd_duration_daily": []}
    optimization_summary = {"num_trade": 0, "num_trade_std": 0, "num_trade_std_pct": 0, "win_rate": 0,
                            "win_rate_std": 0, "win_rate_std_pct": 0, "pnl": 0, "pnl_std": 0, "pnl_std_pct": 0,
                            "net_pips": 0, "net_pips_std": 0, "net_pips_std_pct": 0, "avg_pips_pre_contract": 0,
                            "avg_pips_pre_contract_std": 0, "avg_pips_pre_contract_std_pct": 0, "profit_factor": 0,
                            "profit_factor_std": 0, "profit_factor_std_pct": 0, "payoff_ratio": 0,
                            "payoff_ratio_std": 0, "payoff_ratio_std_pct": 0, "roci": 0, "roci_std": 0,
                            "roci_std_pct": 0, "sharpe_ratio": 0, "sharpe_ratio_std": 0, "sharpe_ratio_std_pct": 0,
                            "tharp_expectancy": 0, "tharp_expectancy_std": 0, "tharp_expectancy_std_pct": 0,
                            "expectancy": 0, "expectancy_std": 0, "expectancy_std_pct": 0, "mdd": 0, "mdd_std": 0,
                            "mdd_std_pct": 0, "mdd_pct": 0, "mdd_pct_std": 0, "mdd_pct_std_pct": 0, "mdd_daily": 0,
                            "mdd_daily_std": 0, "mdd_daily_std_pct": 0, "mdd_pct_daily": 0, "mdd_pct_daily_std": 0,
                            "mdd_pct_daily_std_pct": 0, "dd_duration": 0, "dd_duration_std": 0,
                            "dd_duration_std_pct": 0, "dd_duration_daily": 0, "dd_duration_daily_std": 0,
                            "dd_duration_daily_std_pct": 0}

    all_filter_test_summary = []

    #1 load all filters.json in backtest folder
    backtest_report_dir = SessionStaticVariable.base_report_directory + backtest_filename + "\\"
    filter_tests = load_json(backtest_report_dir + "filters.json")

    for filter_test in filter_tests:
        filter_test_dir = backtest_report_dir + "filtered\\" +filter_test['name'] + "\\"
        filter_test_summary = load_json(filter_test_dir + "backtest_summary.json")

        #filter_test = data



        reformatted_filter_test_summary = {}
        filter_parameter = {}

        filter_test_parameter = filter_test['parameter']
        for key in filter_test_parameter:
            filter_parameter[key] = filter_test_parameter[key]['value']
        reformatted_filter_test_summary['name'] = filter_test['name']
        reformatted_filter_test_summary['parameter'] = filter_parameter
        reformatted_filter_test_summary['performance'] = prepare_backtest_report_insert_to_db(filter_test_summary)
        reformatted_filter_test_summary['backtest_report_path'] = backtest_report_dir
        reformatted_filter_test_summary['report_path'] = filter_test_dir



        all_filter_test_summary.append(reformatted_filter_test_summary)
        for key in key_to_calculate:
            optimization_values[key].append(filter_test_summary[key])

    for key in optimization_values:
        optimization_summary[key] = np.mean(optimization_values[key])
        optimization_summary[key + '_std'] = np.std(optimization_values[key])
        if optimization_summary[key + '_std'] == 0 or optimization_summary[key] == 0:
            optimization_summary[key + '_std_pct']
        else:
            optimization_summary[key + '_std_pct'] = optimization_summary[key + '_std'] / optimization_summary[key]

    export_json = {}
    export_json['backtest'] = all_filter_test_summary
    export_json['optimization_summary'] = optimization_summary

    for filter_test in filter_tests:
        filter_test_dir = backtest_report_dir + "filtered\\" +filter_test['name'] + "\\"
        with open(filter_test_dir + 'optimization.json', 'w') as fp:
            json.dump(export_json, fp, cls=AntJSONEncoder)

def create_optimization_report(optimization):
    result, message, backtests = db.get_backtest_by_optimization_id(optimization["id"])
    if result == "fail":
        return

    optimization_id = optimization["id"]
    result, message = db.update_optimization_status(optimization_id, "creating_optimization_report")
    if result == "fail":
        return


    key_to_calculate = ["num_trade", "win_rate", "pnl", "net_pips", "avg_pips_pre_contract", "profit_factor", "payoff_ratio", "roci", "sharpe_ratio", "tharp_expectancy", "expectancy", "mdd", "mdd_pct", "mdd_daily", "mdd_pct_daily", "dd_duration", "dd_duration_daily"]
    optimization_values = {"num_trade":[], "win_rate":[], "pnl":[], "net_pips":[], "avg_pips_pre_contract":[], "profit_factor":[], "payoff_ratio":[], "roci":[], "sharpe_ratio":[], "tharp_expectancy":[], "expectancy":[], "mdd":[], "mdd_pct":[], "mdd_daily":[], "mdd_pct_daily":[], "dd_duration":[], "dd_duration_daily":[]}
    optimization_summary = {"num_trade":0, "num_trade_std":0, "num_trade_std_pct":0, "win_rate":0, "win_rate_std":0, "win_rate_std_pct":0, "pnl":0, "pnl_std":0, "pnl_std_pct":0, "net_pips":0, "net_pips_std":0, "net_pips_std_pct":0, "avg_pips_pre_contract":0, "avg_pips_pre_contract_std":0, "avg_pips_pre_contract_std_pct":0, "profit_factor":0, "profit_factor_std":0, "profit_factor_std_pct":0, "payoff_ratio":0, "payoff_ratio_std":0, "payoff_ratio_std_pct":0, "roci":0, "roci_std":0, "roci_std_pct":0, "sharpe_ratio":0, "sharpe_ratio_std":0, "sharpe_ratio_std_pct":0, "tharp_expectancy":0, "tharp_expectancy_std":0, "tharp_expectancy_std_pct":0, "expectancy":0, "expectancy_std":0, "expectancy_std_pct":0, "mdd":0, "mdd_std":0, "mdd_std_pct":0, "mdd_pct":0, "mdd_pct_std":0, "mdd_pct_std_pct":0, "mdd_daily":0, "mdd_daily_std":0, "mdd_daily_std_pct":0, "mdd_pct_daily":0, "mdd_pct_daily_std":0, "mdd_pct_daily_std_pct":0, "dd_duration":0, "dd_duration_std":0, "dd_duration_std_pct":0, "dd_duration_daily":0, "dd_duration_daily_std":0, "dd_duration_daily_std_pct":0}

    all_backtest_summary = []

    for backtest in backtests:
        backtest_summary = {}
        backtest_summary['backtest_report_path'] = backtest['report_full_path']
        backtest_parameter = {}
        backtest_parameter_json = json.loads(backtest['strategy_parameter'])
        for key in backtest_parameter_json:
            backtest_parameter[key] = backtest_parameter_json[key]['value']
        backtest_summary['parameter'] = backtest_parameter
        backtest_summary['performance'] = backtest


        all_backtest_summary.append(backtest_summary)
        for key in key_to_calculate:
            optimization_values[key].append(backtest[key])

    for key in optimization_values:
        optimization_summary[key] = np.mean(optimization_values[key])
        optimization_summary[key + '_std'] = np.std(optimization_values[key])
        if optimization_summary[key + '_std'] == 0 or optimization_summary[key]==0:
            optimization_summary[key + '_std_pct']
        else:
            optimization_summary[key + '_std_pct'] = optimization_summary[key + '_std'] / optimization_summary[key]

    export_json = {}
    export_json['backtest'] = all_backtest_summary
    export_json['optimization_summary'] = optimization_summary
    first_backtest_summary = all_backtest_summary[0]

    db.update_optimization(optimization["id"], optimization_summary, all_backtest_summary[0])

    #do heatmap of parameter and pnl etc...
    for backtest in backtests:
        print(backtest)
        with open(backtest['report_full_path'] + '\\optimization.json', 'w') as fp:
            json.dump(export_json, fp, cls=AntJSONEncoder)

    result, message = db.update_optimization_status(optimization_id, "completed")


def create_report_summary(report_folder):
    #loop position
    with open(report_folder+"\\session_config.json") as data_file:
        session_config = json.load(data_file)

    with open(report_folder + "\\positions.json") as data_file:
        positions = json.load(data_file)

    with open(report_folder+"\\orders.json") as data_file:
        orders = json.load(data_file)

    position_summary = {}
    position_summary['winner_position'] = create_position_summary(positions, "WIN")
    position_summary['loser_position'] = create_position_summary(positions, "LOSS")
    position_summary['all_position'] = create_position_summary(positions)

    _backtest_summary = create_backtest_summary(session_config, positions, position_summary)


    with open(report_folder + "//position_summary.json", 'w') as fp:
        json.dump(position_summary, fp, cls=AntJSONEncoder)

    with open(report_folder + "//backtest_summary.json", 'w') as fp:
        json.dump(_backtest_summary, fp, cls=AntJSONEncoder)

def create_backtest_summary(session_config, positions, position_summary):
    _backtest_summary = {}

    _backtest_summary['pnl'] = 0
    _backtest_summary['pnl_s'] = [0]
    _backtest_summary['net_pips'] = 0
    _backtest_summary['equity_s'] = [0]
    _backtest_summary['equity_daily'] = {}
    _backtest_summary['pips_s'] = [0]
    _backtest_summary['pips_daily'] = {}
    _backtest_summary['avg_pips_pre_contract'] = position_summary['all_position']['all']['avg_pips_pre_contract']
    _backtest_summary['win_rate'] = position_summary['all_position']['all']['win_rate']
    _backtest_summary['num_trade'] = position_summary['all_position']['all']['num_trade']

    # Expectancy = (Probability of Win * Average Win) – (Probability of Loss * Average Loss)
    _backtest_summary['expectancy'] = (position_summary['all_position']['all']['win_rate'] * position_summary['all_position']['all'][
        'avg_gain']) - (position_summary['all_position']['all']['loss_rate'] * abs(
        position_summary['all_position']['all']['avg_loss']))

    _backtest_summary['trade_date'] = []
    _backtest_summary['trade_date_ts'] = []
    for position in positions:
        if len(_backtest_summary['trade_date_ts']) == 0:
            dayback_trade_date = datetime.datetime.strptime(position['date'], '%Y%m%d') - datetime.timedelta(days=1)
            _backtest_summary['trade_date'].append(dt_get_date_str(dayback_trade_date))
            _backtest_summary['trade_date_ts'].append(dayback_trade_date.timestamp())

            _backtest_summary['equity_daily'][dt_get_date_str(dayback_trade_date)] = 0
            _backtest_summary['pips_daily'][dt_get_date_str(dayback_trade_date)] = 0

        _backtest_summary['trade_date'].append(position['date'])
        _backtest_summary['trade_date_ts'].append(position['date_ts'])

        if not position['date'] in _backtest_summary['equity_daily']:
            _backtest_summary['equity_daily'][position['date']] = _backtest_summary['pnl']
            _backtest_summary['pips_daily'][position['date']] = _backtest_summary['net_pips']

        _backtest_summary['pnl_s'].append(position['pnl'])
        _backtest_summary['pnl'] += position['pnl']
        _backtest_summary['net_pips'] += position['net_pips']

        _backtest_summary['equity_s'].append(_backtest_summary['pnl'])
        _backtest_summary['equity_daily'][position['date']] += position['pnl']
        _backtest_summary['pips_s'].append(_backtest_summary['net_pips'])
        _backtest_summary['pips_daily'][position['date']] += position['net_pips']

    _backtest_summary['dd_s'], _backtest_summary['mdd'], _backtest_summary['dd_pct'], _backtest_summary['mdd_pct'], \
    _backtest_summary['dd_duration'], _backtest_summary['new_high_s'] = calculate_drawdown(_backtest_summary['equity_s'], session_config)

    _backtest_summary['dd_daily'], _backtest_summary['mdd_daily'], _backtest_summary['dd_pct_daily'], _backtest_summary['mdd_pct_daily'], \
    _backtest_summary['dd_duration_daily'], _backtest_summary['new_high_daily'] = calculate_drawdown(_backtest_summary['equity_daily'], session_config)

    #Payoff ratio average win / average loss
    _backtest_summary['payoff_ratio'] = 0
    if(position_summary['all_position']['all']['gross_loss']!=0):
        _backtest_summary[
            'payoff_ratio'] = position_summary['all_position']['all']['avg_gain'] / position_summary['all_position']['all']['gross_loss']

    #Profit factor = (Gross Profit / Gross Loss)
    _backtest_summary['profit_factor'] = 0
    if(position_summary['all_position']['all']['gross_loss']!=0):
        _backtest_summary['profit_factor'] = position_summary['all_position']['all']['gross_gain'] / abs(position_summary['all_position']['all']['gross_loss'])

    #recovery factor = (Gross Profit / Gross Loss)
    _backtest_summary['recovery_factor'] = 0
    if(position_summary['all_position']['all']['gross_loss']!=0):
        _backtest_summary['recovery_factor'] = position_summary['all_position']['all']['gross_gain'] / abs(position_summary['all_position']['all']['gross_loss'])

    #recovery_factor = Net profit divided by Max. system drawdown
    _backtest_summary['recovery_factor'] = 0
    if _backtest_summary['mdd']!=0:
        _backtest_summary['recovery_factor'] = _backtest_summary['pnl'] / _backtest_summary['mdd']

    #roci = Net profit divided by Max. system drawdown
    _backtest_summary['roci'] = (_backtest_summary['pnl'] - session_config['cash']) / session_config['cash']

    """
    Create the Sharpe ratio for the strategy, based on a
    benchmark of zero (i.e. no risk-free rate information).

    Parameters:
    returns - A pandas Series representing period percentage returns.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """
    periods = 252
    _backtest_summary['sharpe_ratio'] = 0
    if (np.std(_backtest_summary['equity_s']) != 0):
        _backtest_summary[
            'sharpe_ratio'] = np.nan_to_num(np.sqrt(periods) * (np.mean(_backtest_summary['equity_s'])) / np.std(_backtest_summary['equity_s']))

    pnl_s = _backtest_summary['pnl_s'][1:]
    pnl_np = np.asarray(pnl_s)
    std = pnl_np.std()
    _backtest_summary['standard_deviation'] = std
    _backtest_summary['standard_error'] = std / math.sqrt(len(positions))


    '''
    Expectancy  = - (AW * PW + AL * PL) / AL
              = expected profit per dollar risked per trade
    where
            AW = average winning trade
            PW = probably of winning (total wins / total trades )
            AL = average losing trade
            PL = probably of losing (total losses / total trades )
    '''
    _backtest_summary['tharp_expectancy'] = 0
    if (abs(position_summary['all_position']['all']['avg_loss']) != 0):
        _backtest_summary['tharp_expectancy'] = ((position_summary['all_position']['all']['win_rate'] * position_summary['all_position']['all']['avg_gain']) + (
            position_summary['all_position']['all']['loss_rate'] * position_summary['all_position']['all']['avg_loss'])) / abs(position_summary['all_position']['all']['avg_loss'])

    last_cash = session_config['cash']
    _backtest_summary['monthly_cash'] = {}
    _backtest_summary['monthly_pnl'] = {}
    _backtest_summary['month_s'] = []
    for position in positions:
        _year_str = position['date'][:4]
        _month_str = position['date'][4:6]

        if not _year_str in _backtest_summary['monthly_pnl']:
            _backtest_summary['monthly_cash'][_year_str] = {}
            _backtest_summary['monthly_pnl'][_year_str] = {}

        if not _month_str in _backtest_summary['monthly_pnl'][_year_str]:
            _backtest_summary['month_s'].append(position['date'][:6])
            _backtest_summary['monthly_cash'][_year_str][_month_str] = last_cash
            _backtest_summary['monthly_pnl'][_year_str][_month_str] = 0

        last_cash += position['pnl']
        _backtest_summary['monthly_pnl'][_year_str][_month_str] += position['pnl']

    _backtest_summary['monthly_return'] = {}
    _backtest_summary['monthly_return_heatmap'] = []
    x = 0
    y = 0
    x_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    y_axis = []
    last_year = None
    for month_str in _backtest_summary['month_s']:
        _year_str = month_str[:4]
        _month_str = month_str[4:]

        if last_year is None:
            last_year = _year_str
            y_axis.append(last_year)

        if last_year != _year_str:
            last_year = _year_str
            y_axis.append(last_year)
            y += 1

        x = int(_month_str) - 1

        _backtest_summary['monthly_return'][month_str] = float("{0:.2f}".format(_backtest_summary['monthly_pnl'][_year_str][_month_str] / _backtest_summary['monthly_cash'][_year_str][_month_str] * 100))
        _backtest_summary['monthly_return_heatmap'].append([x,y,_backtest_summary['monthly_return'][month_str]])
        _backtest_summary['monthly_return_heatmap_x_axis'] = x_axis
        _backtest_summary['monthly_return_heatmap_y_axis'] = y_axis

    return _backtest_summary


def create_position_summary(positions, result_filter="ALL"):
    _summary = {}

    if not result_filter == "ALL":
        _selected_position = []
        for position in positions:
            if position['result'] == result_filter:
                _selected_position.append(position)
    else:
        _selected_position = positions

    _selected_long_position = []
    _selected_short_position = []
    for position in _selected_position:
        if position['action'] == "BUY":
            _selected_long_position.append(position)
        else:
            _selected_short_position.append(position)

    _summary['all'] = calculate_position_summary(_selected_position)
    _summary['long'] = calculate_position_summary(_selected_long_position)
    _summary['short'] = calculate_position_summary(_selected_short_position)

    return _summary

def calculate_position_summary(positions):
    _summary = {}
    _summary['num_trade'] = len(positions)
    _summary['net_pips'] = 0
    _summary['pnl'] = 0
    _summary['num_winner'] = 0
    _summary['num_loser'] = 0
    _summary['gross_gain'] = 0
    _summary['gross_loss'] = 0
    _summary['largest_win'] = -1
    _summary['largest_loss'] = 999999999
    _summary['commission'] = 0
    _summary['slippage'] = 0
    _summary['avg_slippage'] = 0
    _summary['num_contract'] = 0

    for position in positions:
        _summary['net_pips'] += position['net_pips']
        _summary['pnl'] += position['pnl']
        _summary['commission'] += position['commission']
        _summary['slippage'] += position['slippage']
        _summary['num_contract'] += position['max_net'] * 2
        if position['result'] == "WIN":
            _summary['num_winner'] += 1
            _summary['gross_gain'] += position['pnl']
            _summary['largest_win'] = max(_summary['largest_win'], position['pnl'])
        else:
            _summary['num_loser'] += 1
            _summary['gross_loss'] += position['pnl']
            _summary['largest_loss'] = min(_summary['largest_loss'], position['pnl'])

    if _summary['num_trade'] == 0:
        _summary['win_rate'] = 0
        _summary['loss_rate'] = 0
        _summary['avg_pnl'] = 0
        _summary['avg_gain'] = 0
        _summary['avg_loss'] = 0
        _summary['avg_pips_pre_contract'] = 0
        _summary['avg_slippage'] = 0
        _summary['avg_commission'] = 0
    else:
        _summary['win_rate'] = _summary['num_winner'] / _summary['num_trade']
        _summary['loss_rate'] = _summary['num_loser'] / _summary['num_trade']
        _summary['avg_gain'] = _summary['gross_gain'] / _summary['num_trade']
        _summary['avg_loss'] = _summary['gross_loss'] / _summary['num_trade']
        _summary['avg_pnl'] = _summary['pnl'] / _summary['num_trade']
        _summary['avg_pips_pre_contract'] = _summary['net_pips'] / _summary['num_contract']
        _summary['avg_slippage'] = _summary['slippage'] / _summary['num_contract']
        _summary['avg_commission'] = _summary['commission'] / _summary['num_contract']

    if _summary['largest_win'] == -1:
        _summary['largest_win'] = 0

    if _summary['largest_loss'] == 999999999:
        _summary['largest_loss'] = 0

    return _summary

def calculate_drawdown(equity_s, session_config):
    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    if (len(equity_s) == 0):
        return equity_s, 0.0, equity_s, 0.0, 0, equity_s

    watermark = 0
    duration_watermark = 0
    duration_counter = 0

    if isinstance(equity_s, dict):
        drawdown_s = {}
        drawdown_pct_s = {}
        new_high_s = {}
        date_s = sorted(list(equity_s.keys()))

        for date_key in date_s:
            equity = equity_s[date_key]
            if equity > watermark:
                new_high_s[date_key] = equity
                watermark = equity  # markwater mark
                duration_watermark = max(duration_watermark, duration_counter)
                duration_counter = 0
            else:
                duration_counter += 1

            dd = equity - watermark
            drawdown_s[date_key] = dd
            drawdown_pct_s[date_key] = abs(dd) / (watermark + session_config["cash"])
        mdd = abs(min(drawdown_s.values()))
        mdd_pct = max(drawdown_pct_s.values())
    else:
        drawdown_s = []
        drawdown_pct_s = []
        new_high_s = []

        i = 0

        for equity in equity_s:
            if equity > watermark:
                new_high_s.append([i+1, equity])
                watermark = equity          #markwater mark
                duration_watermark = max(duration_watermark, duration_counter)
                duration_counter = 0
            else:
                duration_counter += 1
            dd = equity - watermark
            drawdown_s.append(dd)
            drawdown_pct_s.append(abs(dd)/(watermark + session_config["cash"]))

            i += 1

        mdd = abs(min(drawdown_s))
        mdd_pct = abs(max(drawdown_pct_s))

    duration_watermark = max(duration_watermark, duration_counter)
    return drawdown_s, mdd, drawdown_pct_s, mdd_pct, duration_watermark, new_high_s


def combine_walk_forward_test(walk_forward_test_id, backtests):
    db.update_walk_forward_test_status(walk_forward_test_id, "combining")
    walk_forward_test_report_folder = datetime.datetime.now().strftime("walk_forward_test_%Y%m%d_")+str(walk_forward_test_id).zfill(6) + "_" + backtests[0]['strategy_class']
    from_path = SessionStaticVariable.base_report_directory + backtests[0]['report_folder_name']
    to_path = SessionStaticVariable.base_report_directory + walk_forward_test_report_folder
    copy_tree(from_path, to_path)

    to_path += "\\"
    os.remove(to_path + "backtest_summary.json")
    os.remove(to_path + "position_summary.json")


    orders = []
    positions = []
    end_date = None

    for backtest in backtests:
        report_folder = SessionStaticVariable.base_report_directory + backtest['report_folder_name'] + "\\"

        with open(report_folder + "positions.json") as data_file:
            positions += json.load(data_file)

        with open(report_folder + "orders.json") as data_file:
            orders += json.load(data_file)

        end_date = backtest['end_date']

    end_date = end_date.replace("-", "")

    i = 1;
    for position in positions:
        position['position_id'] = i
        i+=1

    i = 1;
    for order in orders:
        order['order_id'] = i
        i+=1

    os.remove(to_path + "positions.json")
    os.remove(to_path + "orders.json")

    with open(to_path + 'positions.json', 'w') as fp:
        json.dump(positions, fp, cls=AntJSONEncoder)

    with open(to_path + 'orders.json', 'w') as fp:
        json.dump(orders, fp, cls=AntJSONEncoder)


    with open(to_path + "session_config.json") as data_file:
        session_config = json.load(data_file)
    session_config['end_date'] = end_date

    with open(to_path + 'session_config.json', 'w') as fp:
        json.dump(session_config, fp, cls=AntJSONEncoder, indent=4)

    create_report_summary(to_path)

    db.update_walk_forward_test_status(walk_forward_test_id, "completed")
# endregion


# region Get class / class property
def get_class_from_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_class_name_from_submodule(module_name):
    import pyclbr
    class_name = []
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        class_name.append(item.name)

    return class_name


def get_class_from_submodule(module_name):
    import pyclbr
    class_name = []
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        class_name.append(item.name)

    classes = []
    for name in class_name:
        classes.append(get_class_from_name(module_name, name))

    return classes


def get_submodule_from_module(submodule_name):
    skip_files = ["__init__.py", "base.py", "future_strategy.py"]
    path = os.path.dirname(ants.__file__)
    path = path + "\\" + submodule_name + "\\"

    py_files = []
    py_modules = []
    for f in listdir(path):
        if isfile(join(path, f)) and f not in skip_files and f[0] != "_":
            py_files.append(f)
            py_modules.append(f.replace(".py", ""))

    return py_files, py_modules

def get_strategy_class_parameter(class_name):
    submodule_name = "strategy"
    py_files, py_modules = get_submodule_from_module(submodule_name)

    for m in py_modules:
        class_list = get_class_name_from_submodule('ants.' + submodule_name + '.' + m)
        for strategy_class in class_list:
            if strategy_class==class_name:
                strategy_class = get_class_from_submodule('ants.' + submodule_name + '.' + m)
                strategy_class = strategy_class[0]
                return strategy_class.OPTIMIZATION_PARAMETER
    return None

def get_submodule_class_name(submodule_name):
    py_files, py_modules = get_submodule_from_module(submodule_name)

    py_class = []
    for m in py_modules:
        py_class = py_class + get_class_name_from_submodule('ants.' + submodule_name + '.' + m)

    return py_class

def get_submodule_class(submodule_name):
    py_files, py_modules = get_submodule_from_module(submodule_name)

    py_class = []
    for m in py_modules:
        py_class = py_class + get_class_from_submodule('ants.' + submodule_name + '.' + m)

    return py_class

def get_strategy_class_name():
    classes_name = get_submodule_class_name("strategy")
    return get_submodule_class_name("strategy")

def get_strategy_class_name_with_meta():
    return_data = []

    classes_name = get_submodule_class_name("strategy")

    for class_name in classes_name:
        obj = {}
        obj['class_name'] = class_name
        obj['optimization_pair'] = get_class_from_name('ants.strategy.'+class_name, class_name).OPTIMIZATION_PAIR
        obj['optimization_parameter'] = get_class_from_name('ants.strategy.'+class_name, class_name).OPTIMIZATION_PARAMETER
        obj['strategt_slug'] = get_class_from_name('ants.strategy.'+class_name, class_name).STRATEGY_SLUG
        obj['strategy_name'] = get_class_from_name('ants.strategy.'+class_name, class_name).STRATEGY_NAME
        obj['version'] = get_class_from_name('ants.strategy.'+class_name, class_name).VERSION
        obj['last_update_date'] = get_class_from_name('ants.strategy.'+class_name, class_name).LAST_UPDATE_DATE
        return_data.append(obj)

    return return_data

def get_walk_forward_test_class_name():
    return get_submodule_class_name("walk_forward")

def get_data_provider_class_name():
    return get_submodule_class_name("data_provider")

def get_order_handler_class_name():
    return get_submodule_class_name("order_handler")

def get_portfolio_class_name():
    return get_submodule_class_name("portfolio")

def get_filter_test_classs():
    return get_submodule_class_name("filter")
# endregion


# region Math
def round(f, round):
    r_str = "{:."+str(round)+"f}"
    return float(r_str.format(float(f)))
# endregion


# region Optimization related methods
def get_optimization_parameter_combination(default_data, data):
    import itertools

    values_conbination = []
    keys = []

    for key in data:
        keys.append(key)
        temp = []
        parameter = data[key]
        parameter["min_value"] = int(parameter["min_value"])
        parameter["max_value"] = int(parameter["max_value"])
        parameter["step"] = int(parameter["step"])
        value = parameter["min_value"]
        while (value <= parameter["max_value"]):
            temp.append(value)
            value += parameter["step"]
        values_conbination.append(temp)

    values_conbination = list(itertools.product(*values_conbination))

    output_parameter = []
    for values in values_conbination:
        parameter = {}
        i = 0
        for key in keys:
            parameter[keys[i]] = {}
            parameter[keys[i]]['value'] = values[i]
            i += 1

        for default_key in default_data:
            if default_key not in parameter:
                parameter[default_key] = {}
                parameter[default_key]["value"] = default_data[default_key]["value"]

        output_parameter.append(parameter)

    return output_parameter
# endregion


# region Run external process
def run_new_py(executable, file, is_new_console=True):
    try:
        if is_new_console:
            p = Popen([executable, file], creationflags=CREATE_NEW_CONSOLE)
        else:
            p = Popen([executable, file])
        print("new py pid:", p.pid)
    except:
        print("except found on run_new_py in unilities.py")
        pass
# endregion
