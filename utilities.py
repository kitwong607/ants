from .signal.base import Signal
import time, json, math, os, importlib, random, string
from pathlib import Path
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime, timedelta



from os import listdir
from os.path import isfile, join

import pandas as pd
import numpy as np

# region Datetime related
def getMonthList(startDate,endDate,is_return_str_list=True):
    start_date = startDate.replace(day=1)
    months = [dt for dt in rrule(MONTHLY, dtstart=start_date, until=endDate)]
    if is_return_str_list:
        monthStr_list = [m.strftime("%Y%m") for m in months]
        return monthStr_list
    return months


def clearTimeInDatetime(dtToClear):
    #print("clearTimeInDatetime: ", dtToClear, type(dtToClear))

    return dtToClear - timedelta(
                hours=dtToClear.hour,
                minutes=dtToClear.minute,
                seconds=dtToClear.second,
                microseconds=dtToClear.microsecond)


def addTimeToDatetime(dtToAdd, hour, minute, second):
    return dtToAdd + timedelta(
        hours=hour,
        minutes=minute,
        seconds=second)


def diffMonth(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def secondBetweenTwoDatetime(dt1, dt2, useAbsValue=True):
    if useAbsValue:
        if(dt1>dt2):
            return abs((dt1 - dt2).seconds)
        else:
            return abs((dt2 - dt1).seconds)

    return (dt1 - dt2).seconds


def mintueBetweenTwoDatetime(dt1, dt2, useAbsValue=True):
    if useAbsValue:
        if(dt1>dt2):
            return abs((dt1 - dt2).seconds) // 60  # in mintues
        else:
            return abs((dt2 - dt1).seconds) // 60  # in mintues

    return (dt1 - dt2).seconds // 60



def getTotalMinuteInDatetime(dt):
    return dt.hour * 60 + dt.minute


def dateParser(dateStr):
    return pd.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
# endregion


# region Convert format
def dtToTs(dt):
    return dt.timestamp()

def getDateStrFromDt(dt):
    return dt.strftime('%Y%m%d')

def getTimeStrFromDt(dt):
    return dt.strftime('%H%M%S')

def toAdjustedTime(time_int):
    if time_int<90000:
        time_int += 240000
    return time_int

def ConvertIntTimestampToDatetime(ts):
    return datetime.fromtimestamp(ts)

def ConvertAdjustedDateTimeToTimestamp(_date, _time):
    if "." in _date:
        _date = str(int(float(_date)))

    if "." in _time:
        _time = str(int(float(_time))).zfill(6)

    _isNextDate = False
    if int(float(_time)) >= 240000:
        _time = str(int(_time) - 240000).zfill(6)
        _isNextDate = True

    dt = datetime.strptime(_date + " " + _time, "%Y%m%d %H%M%S")

    if _isNextDate:
        dt += timedelta(days=1)

    return pd.Timestamp(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute, second=dt.second)
# endregion


# region Count time methods
def getCurrentDatetime():
    now = time.time()
    print("--- Process start at " + str(now) + " ---")
    return now


def calculateTimeUsed(start_time, task):
    print("--- "+str(round(time.time() - start_time, 2))+" seconds --- for " + task)
# endregion

# region File methods
def checkFileExist(filePath):
    f = Path(filePath)
    if f.is_file():
        return True
    return False

def RemoveAllFileFromDir(workingDir):
    for the_file in os.listdir(workingDir):
        file_path = os.path.join(workingDir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def createFolder(path):
    if path == "":
        return False

    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def createFile(path):
    if not isFileExist(path):
        open(path, 'a').close()
        return True
    return False


def isFileExist(path):
    if os.path.exists(path):
        return True
    return False
# endregion


# region Convert format
def dtToTs(dt):
    return dt.timestamp()

def dtGetDateStr(dt):
    return dt.strftime('%Y%m%d')

def dtGetTimeStr(dt):
    return dt.strftime('%H%M%S')

def toAdjustedTime(timeInt):
    if timeInt<90000:
        timeInt += 240000
    return timeInt
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

def LoadJson(path):
    with open(path) as json_data:
        return json.load(json_data)

    return None
#endregion


# region Create backtest report / summary methods
def PrepareBacktestReportInsertToDB(d):
    d['winRate'] = round(d['winRate'], 3)
    d['num_trade'] = round(d['num_trade'], 3)
    d['pnl'] = round(d['pnl'], 3)
    d['netPips'] = round(d['netPips'], 3)
    d['profitFactor'] = round(d['profitFactor'], 3)
    d['payoffRatio'] = round(d['payoffRatio'], 3)
    d['roci'] = round(d['roci'], 3)

    d['sharpeRatio'] = round(d['sharpeRatio'], 3)
    d['standardDeviation'] = round(d['standardDeviation'], 3)
    d['standardError'] = round(d['standardError'], 3)
    d['tharpExpectancy'] = round(d['tharpExpectancy'], 3)
    d['expectancy'] = round(d['expectancy'], 3)

    d['mdd'] = round(d['mdd'], 3)
    d['mddPct'] = round(d['mddPct'], 3)
    d['mddDaily'] = round(d['mddDaily'], 3)
    d['mddPctDaily'] = round(d['mddPctDaily'], 3)
    d['ddDuration'] = round(d['ddDuration'], 3)

    d['ddDurationDaily'] = round(d['ddDurationDaily'], 3)
    d['avg_pips_pre_contract'] = round(d['avg_pips_pre_contract'], 3)

    key_to_fillzero = ["winRate", "num_trade", "pnl", "net_pips", "profit_factor",
                   "payoffRatio", "roci", "sharpeRatio", "standardDeviation", "standard_error",
                   "tharp_expectancy", "expectancy", "mdd", "mddPct", "mddDaily",
                   "mddPct_daily", "ddDuration", "ddDuration_daily", "avg_pips_pre_contract"]

    key_to_save = ['winRate', 'num_trade', 'pnl', 'netPips', 'profitFactor', 'payoffRatio', 'roci', 'sharpeRatio', 'standardDeviation', 'standardError', 'tharpExpectancy', 'expectancy', 'mdd', 'mddPct', 'mddDaily', 'mddPctDaily', 'ddDuration', 'ddDurationDaily', 'avg_pips_pre_contract', 'report_folder_name', 'report_full_path']

    new_d = {}
    for key in d:
        if key in key_to_fillzero:
            if math.isnan(float(d[key])):
                d[key] = 0

        if key in key_to_save:
            new_d[key] = d[key]

    return new_d


def CreateFilterReport(backtestFilename):
    key_to_calculate = ["num_trade", "winRate", "pnl", "net_pips", "avg_pips_pre_contract", "profit_factor",
                        "payoffRatio", "roci", "sharpeRatio", "tharp_expectancy", "expectancy", "mdd", "mddPct",
                        "mddDaily", "mddPct_daily", "ddDuration", "ddDuration_daily"]
    optimization_values = {"num_trade": [], "winRate": [], "pnl": [], "net_pips": [], "avg_pips_pre_contract": [],
                           "profit_factor": [], "payoffRatio": [], "roci": [], "sharpeRatio": [],
                           "tharp_expectancy": [], "expectancy": [], "mdd": [], "mddPct": [], "mddDaily": [],
                           "mddPct_daily": [], "ddDuration": [], "ddDuration_daily": []}
    optimization_summary = {"num_trade": 0, "num_trade_std": 0, "num_trade_std_pct": 0, "winRate": 0,
                            "winRate_std": 0, "winRate_std_pct": 0, "pnl": 0, "pnl_std": 0, "pnl_std_pct": 0,
                            "net_pips": 0, "net_pipsSeriestd": 0, "net_pipsSeriestd_pct": 0, "avg_pips_pre_contract": 0,
                            "avg_pips_pre_contract_std": 0, "avg_pips_pre_contract_std_pct": 0, "profit_factor": 0,
                            "profit_factor_std": 0, "profit_factor_std_pct": 0, "payoffRatio": 0,
                            "payoffRatio_std": 0, "payoffRatio_std_pct": 0, "roci": 0, "roci_std": 0,
                            "roci_std_pct": 0, "sharpeRatio": 0, "sharpeRatio_std": 0, "sharpeRatio_std_pct": 0,
                            "tharp_expectancy": 0, "tharp_expectancy_std": 0, "tharp_expectancy_std_pct": 0,
                            "expectancy": 0, "expectancy_std": 0, "expectancy_std_pct": 0, "mdd": 0, "mddSeriestd": 0,
                            "mddSeriestd_pct": 0, "mddPct": 0, "mddPct_std": 0, "mddPct_std_pct": 0, "mddDaily": 0,
                            "mddDaily_std": 0, "mddDaily_std_pct": 0, "mddPct_daily": 0, "mddPct_daily_std": 0,
                            "mddPct_daily_std_pct": 0, "ddDuration": 0, "ddDuration_std": 0,
                            "ddDuration_std_pct": 0, "ddDuration_daily": 0, "ddDuration_daily_std": 0,
                            "ddDuration_daily_std_pct": 0}

    all_filter_test_summary = []

    #1 load all filters.json in backtest folder
    backtest_report_dir = SessionStaticVariable.baseReportDirectory + backtestFilename + "\\"
    filter_tests = load_json(backtest_report_dir + "filters.json")

    for filter_test in filter_tests:
        filter_test_dir = backtest_report_dir + "filtered\\" +filter_test['name'] + "\\"
        filter_test_summary = load_json(filter_test_dir + "backtestSummary.json")

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

def CreateOptimizationReport(optimization):
    result, message, backtests = db.get_backtest_by_optimization_id(optimization["id"])
    if result == "fail":
        return

    optimization_id = optimization["id"]
    result, message = db.update_optimization_status(optimization_id, "creating_optimization_report")
    if result == "fail":
        return


    key_to_calculate = ["num_trade", "winRate", "pnl", "net_pips", "avg_pips_pre_contract", "profit_factor", "payoffRatio", "roci", "sharpeRatio", "tharp_expectancy", "expectancy", "mdd", "mddPct", "mddDaily", "mddPct_daily", "ddDuration", "ddDuration_daily"]
    optimization_values = {"num_trade":[], "winRate":[], "pnl":[], "net_pips":[], "avg_pips_pre_contract":[], "profit_factor":[], "payoffRatio":[], "roci":[], "sharpeRatio":[], "tharp_expectancy":[], "expectancy":[], "mdd":[], "mddPct":[], "mddDaily":[], "mddPct_daily":[], "ddDuration":[], "ddDuration_daily":[]}
    optimization_summary = {"num_trade":0, "num_trade_std":0, "num_trade_std_pct":0, "winRate":0, "winRate_std":0, "winRate_std_pct":0, "pnl":0, "pnl_std":0, "pnl_std_pct":0, "net_pips":0, "net_pipsSeriestd":0, "net_pipsSeriestd_pct":0, "avg_pips_pre_contract":0, "avg_pips_pre_contract_std":0, "avg_pips_pre_contract_std_pct":0, "profit_factor":0, "profit_factor_std":0, "profit_factor_std_pct":0, "payoffRatio":0, "payoffRatio_std":0, "payoffRatio_std_pct":0, "roci":0, "roci_std":0, "roci_std_pct":0, "sharpeRatio":0, "sharpeRatio_std":0, "sharpeRatio_std_pct":0, "tharp_expectancy":0, "tharp_expectancy_std":0, "tharp_expectancy_std_pct":0, "expectancy":0, "expectancy_std":0, "expectancy_std_pct":0, "mdd":0, "mddSeriestd":0, "mddSeriestd_pct":0, "mddPct":0, "mddPct_std":0, "mddPct_std_pct":0, "mddDaily":0, "mddDaily_std":0, "mddDaily_std_pct":0, "mddPct_daily":0, "mddPct_daily_std":0, "mddPct_daily_std_pct":0, "ddDuration":0, "ddDuration_std":0, "ddDuration_std_pct":0, "ddDuration_daily":0, "ddDuration_daily_std":0, "ddDuration_daily_std_pct":0}

    all_backtestSummary = []

    for backtest in backtests:
        backtestSummary = {}
        backtestSummary['backtest_report_path'] = backtest['report_full_path']
        backtest_parameter = {}
        backtest_parameter_json = json.loads(backtest['strategy_parameter'])
        for key in backtest_parameter_json:
            backtest_parameter[key] = backtest_parameter_json[key]['value']
        backtestSummary['parameter'] = backtest_parameter
        backtestSummary['performance'] = backtest


        all_backtestSummary.append(backtestSummary)
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
    export_json['backtest'] = all_backtestSummary
    export_json['optimization_summary'] = optimization_summary
    first_backtestSummary = all_backtestSummary[0]

    db.update_optimization(optimization["id"], optimization_summary, all_backtestSummary[0])

    #do heatmap of parameter and pnl etc...
    for backtest in backtests:
        print(backtest)
        with open(backtest['report_full_path'] + '\\optimization.json', 'w') as fp:
            json.dump(export_json, fp, cls=AntJSONEncoder)

    result, message = db.update_optimization_status(optimization_id, "completed")


def CreateReportSummary(report_folder):
    #loop position
    with open(report_folder+"\\sessionConfig.json") as data_file:
        sessionConfig = json.load(data_file)

    with open(report_folder + "\\positions.json") as data_file:
        positions = json.load(data_file)

    with open(report_folder+"\\orders.json") as data_file:
        orders = json.load(data_file)

    positionSummary = {}
    positionSummary['winnerPosition'] = CreatePositionSummary(positions, "WIN")
    positionSummary['loserPosition'] = CreatePositionSummary(positions, "LOSS")
    positionSummary['allPosition'] = CreatePositionSummary(positions)

    _backtestSummary = CreateBacktestSummary(sessionConfig, positions, positionSummary)


    with open(report_folder + "//positionSummary.json", 'w') as fp:
        json.dump(positionSummary, fp, cls=AntJSONEncoder)

    with open(report_folder + "//backtestSummary.json", 'w') as fp:
        json.dump(_backtestSummary, fp, cls=AntJSONEncoder)

def CreateBacktestSummary(sessionConfig, positions, positionSummary):
    _backtestSummary = {}

    _backtestSummary['pnl'] = 0
    _backtestSummary['pnlSeries'] = [0]
    _backtestSummary['netPips'] = 0
    _backtestSummary['equitySeries'] = [0]
    _backtestSummary['equityDaily'] = {}
    _backtestSummary['pipsSeries'] = [0]
    _backtestSummary['pipsDaily'] = {}
    _backtestSummary['avgPipsPreContract'] = positionSummary['allPosition']['all']['avgPipsPreContract']
    _backtestSummary['winRate'] = positionSummary['allPosition']['all']['winRate']
    _backtestSummary['numTrade'] = positionSummary['allPosition']['all']['numTrade']

    # Expectancy = (Probability of Win * Average Win) – (Probability of Loss * Average Loss)
    _backtestSummary['expectancy'] = (positionSummary['allPosition']['all']['winRate'] * positionSummary['allPosition']['all'][
        'avgGain']) - (positionSummary['allPosition']['all']['lossRate'] * abs(
        positionSummary['allPosition']['all']['avgLoss']))

    _backtestSummary['tradeDate'] = []
    _backtestSummary['tradeDateTS'] = []
    for position in positions:
        if len(_backtestSummary['tradeDateTS']) == 0:
            daybackTradeDate = datetime.strptime(position['date'], '%Y%m%d') - timedelta(days=1)
            _backtestSummary['tradeDate'].append(getDateStrFromDt(daybackTradeDate))
            _backtestSummary['tradeDateTS'].append(daybackTradeDate.timestamp())

            _backtestSummary['equityDaily'][getDateStrFromDt(daybackTradeDate)] = 0
            _backtestSummary['pipsDaily'][getDateStrFromDt(daybackTradeDate)] = 0

        _backtestSummary['tradeDate'].append(position['date'])
        _backtestSummary['tradeDateTS'].append(position['dateTS'])

        if not position['date'] in _backtestSummary['equityDaily']:
            _backtestSummary['equityDaily'][position['date']] = _backtestSummary['pnl']
            _backtestSummary['pipsDaily'][position['date']] = _backtestSummary['netPips']

        _backtestSummary['pnlSeries'].append(position['pnl'])
        _backtestSummary['pnl'] += position['pnl']
        _backtestSummary['netPips'] += position['netPips']

        _backtestSummary['equitySeries'].append(_backtestSummary['pnl'])
        _backtestSummary['equityDaily'][position['date']] += position['pnl']
        _backtestSummary['pipsSeries'].append(_backtestSummary['netPips'])
        _backtestSummary['pipsDaily'][position['date']] += position['netPips']

    _backtestSummary['ddSeries'], _backtestSummary['mdd'], _backtestSummary['dd_pct'], _backtestSummary['mddPct'], \
    _backtestSummary['ddDuration'], _backtestSummary['newHighSeries'] = CalculateDrawdown(_backtestSummary['equitySeries'], sessionConfig)

    _backtestSummary['ddDaily'], _backtestSummary['mddDaily'], _backtestSummary['dd_pctDaily'], _backtestSummary['mddPctDaily'], \
    _backtestSummary['ddDurationDaily'], _backtestSummary['newHighDaily'] = CalculateDrawdown(_backtestSummary['equityDaily'], sessionConfig)

    #Payoff ratio average win / average loss
    _backtestSummary['payoffRatio'] = 0
    if(positionSummary['allPosition']['all']['grossLoss']!=0):
        _backtestSummary[
            'payoffRatio'] = positionSummary['allPosition']['all']['avgGain'] / positionSummary['allPosition']['all']['grossLoss']

    #Profit factor = (Gross Profit / Gross Loss)
    _backtestSummary['profitFactor'] = 0
    if(positionSummary['allPosition']['all']['grossLoss']!=0):
        _backtestSummary['profitFactor'] = positionSummary['allPosition']['all']['grossGain'] / abs(positionSummary['allPosition']['all']['grossLoss'])

    #recovery factor = (Gross Profit / Gross Loss)
    _backtestSummary['recoveryFactor'] = 0
    if(positionSummary['allPosition']['all']['grossLoss']!=0):
        _backtestSummary['recoveryFactor'] = positionSummary['allPosition']['all']['grossGain'] / abs(positionSummary['allPosition']['all']['grossLoss'])

    #recovery_factor = Net profit divided by Max. system drawdown
    _backtestSummary['recoveryFactor'] = 0
    if _backtestSummary['mdd']!=0:
        _backtestSummary['recoveryFactor'] = _backtestSummary['pnl'] / _backtestSummary['mdd']

    #roci = Net profit divided by Max. system drawdown
    _backtestSummary['roci'] = (_backtestSummary['pnl'] - sessionConfig['cash']) / sessionConfig['cash']

    """
    Create the Sharpe ratio for the strategy, based on a
    benchmark of zero (i.e. no risk-free rate information).

    Parameters:
    returns - A pandas Series representing period percentage returns.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """
    periods = 252
    _backtestSummary['sharpeRatio'] = 0
    if (np.std(_backtestSummary['equitySeries']) != 0):
        _backtestSummary[
            'sharpeRatio'] = np.nan_to_num(np.sqrt(periods) * (np.mean(_backtestSummary['equitySeries'])) / np.std(_backtestSummary['equitySeries']))

    pnl_s = _backtestSummary['pnlSeries'][1:]
    pnl_np = np.asarray(pnl_s)

    if len(pnl_s)==0:
        _backtestSummary['standardDeviation'] = 0
        _backtestSummary['standardError'] = 0
    else:
        std = pnl_np.std()
        _backtestSummary['standardDeviation'] = std
        _backtestSummary['standardError'] = std / math.sqrt(len(positions))

    '''
    Expectancy  = - (AW * PW + AL * PL) / AL
              = expected profit per dollar risked per trade
    where
            AW = average winning trade
            PW = probably of winning (total wins / total trades )
            AL = average losing trade
            PL = probably of losing (total losses / total trades )
    '''
    _backtestSummary['tharpExpectancy'] = 0
    if (abs(positionSummary['allPosition']['all']['avgLoss']) != 0):
        _backtestSummary['tharpExpectancy'] = ((positionSummary['allPosition']['all']['winRate'] * positionSummary['allPosition']['all']['avgGain']) + (
            positionSummary['allPosition']['all']['lossRate'] * positionSummary['allPosition']['all']['avgLoss'])) / abs(positionSummary['allPosition']['all']['avgLoss'])

    last_cash = sessionConfig['cash']
    _backtestSummary['monthlyCash'] = {}
    _backtestSummary['monthlyPnl'] = {}
    _backtestSummary['monthSeries'] = []
    for position in positions:
        _yearStr = position['date'][:4]
        _monthStr = position['date'][4:6]

        if not _yearStr in _backtestSummary['monthlyPnl']:
            _backtestSummary['monthlyCash'][_yearStr] = {}
            _backtestSummary['monthlyPnl'][_yearStr] = {}

        if not _monthStr in _backtestSummary['monthlyPnl'][_yearStr]:
            _backtestSummary['monthSeries'].append(position['date'][:6])
            _backtestSummary['monthlyCash'][_yearStr][_monthStr] = last_cash
            _backtestSummary['monthlyPnl'][_yearStr][_monthStr] = 0

        last_cash += position['pnl']
        _backtestSummary['monthlyPnl'][_yearStr][_monthStr] += position['pnl']

    _backtestSummary['monthlyReturn'] = {}
    _backtestSummary['monthlyReturnHeatmap'] = []
    x = 0
    y = 0
    x_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    y_axis = []
    lastYear = None



    for monthStr in reversed(_backtestSummary['monthSeries']):
        _yearStr = monthStr[:4]
        _monthStr = monthStr[4:]

        if lastYear is None:
            lastYear = _yearStr
            y_axis.append(lastYear)

        if lastYear != _yearStr:
            lastYear = _yearStr
            y_axis.append(lastYear)
            y += 1

        x = int(_monthStr) - 1

        if _backtestSummary['monthlyCash'][_yearStr][_monthStr] == 0:
            _backtestSummary['monthlyReturn'][monthStr] = float(0.0)
        else:
            _backtestSummary['monthlyReturn'][monthStr] = float("{0:.1f}".format(_backtestSummary['monthlyPnl'][_yearStr][_monthStr] / _backtestSummary['monthlyCash'][_yearStr][_monthStr] * 100))
        _backtestSummary['monthlyReturnHeatmap'].append([x,y,_backtestSummary['monthlyReturn'][monthStr]])
        _backtestSummary['monthlyReturnHeatmapXAxis'] = x_axis
        _backtestSummary['monthlyReturnHeatmapYAxis'] = y_axis

    return _backtestSummary


def CreatePositionSummary(positions, result_filter="ALL"):
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

    _summary['all'] = CalculatePositionSummary(_selected_position)
    _summary['long'] = CalculatePositionSummary(_selected_long_position)
    _summary['short'] = CalculatePositionSummary(_selected_short_position)

    return _summary

def CalculatePositionSummary(positions):
    _summary = {}
    _summary['numTrade'] = len(positions)
    _summary['netPips'] = 0
    _summary['pnl'] = 0
    _summary['numWinner'] = 0
    _summary['numLoser'] = 0
    _summary['grossGain'] = 0
    _summary['grossLoss'] = 0
    _summary['largestWin'] = -1
    _summary['largestLoss'] = 999999999
    _summary['commission'] = 0
    _summary['slippage'] = 0
    _summary['avgSlippage'] = 0
    _summary['numContract'] = 0

    for position in positions:
        _summary['netPips'] += position['netPips']
        _summary['pnl'] += position['pnl']
        _summary['commission'] += position['commission']
        _summary['slippage'] += position['totalSlippage']
        _summary['numContract'] += position['qty']


        #print(" _summary['netPips']",  _summary['netPips'])

        if position['result'] == "WIN":
            _summary['numWinner'] += 1
            _summary['grossGain'] += position['pnl']
            _summary['largestWin'] = max(_summary['largestWin'], position['pnl'])
        else:
            _summary['numLoser'] += 1
            _summary['grossLoss'] += position['pnl']
            _summary['largestLoss'] = min(_summary['largestLoss'], position['pnl'])

    if _summary['numTrade'] == 0:
        _summary['winRate'] = 0
        _summary['lossRate'] = 0
        _summary['avgPnl'] = 0
        _summary['avgGain'] = 0
        _summary['avgLoss'] = 0
        _summary['avgPipsPreContract'] = 0
        _summary['avgSlippage'] = 0
        _summary['avgCommission'] = 0
    else:
        _summary['winRate'] = _summary['numWinner'] / _summary['numTrade']
        _summary['lossRate'] = _summary['numLoser'] / _summary['numTrade']
        _summary['avgGain'] = _summary['grossGain'] / _summary['numTrade']
        _summary['avgLoss'] = _summary['grossLoss'] / _summary['numTrade']
        _summary['avgPnl'] = _summary['pnl'] / _summary['numTrade']
        _summary['avgPipsPreContract'] = _summary['netPips'] / _summary['numContract']
        _summary['avgSlippage'] = _summary['slippage'] / _summary['numContract']
        _summary['avgCommission'] = _summary['commission'] / _summary['numContract']

    if _summary['largestWin'] == -1:
        _summary['largestWin'] = 0

    if _summary['largestLoss'] == 999999999:
        _summary['largestLoss'] = 0

    return _summary

def CalculateDrawdown(equitySeries, sessionConfig):
    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    if (len(equitySeries) == 0):
        return equitySeries, 0.0, equitySeries, 0.0, 0, equitySeries

    watermark = 0
    durationWatermark = 0
    durationCounter = 0

    if isinstance(equitySeries, dict):
        drawdownSeries = {}
        drawdownPctSeries = {}
        newHighSeries = {}
        dateSeries = sorted(list(equitySeries.keys()))

        for dateKey in dateSeries:
            equity = equitySeries[dateKey]
            if equity > watermark:
                newHighSeries[dateKey] = equity
                watermark = equity  # markwater mark
                durationWatermark = max(durationWatermark, durationCounter)
                durationCounter = 0
            else:
                durationCounter += 1

            dd = equity - watermark
            drawdownSeries[dateKey] = dd
            drawdownPctSeries[dateKey] = abs(dd) / (watermark + sessionConfig["cash"])
        mdd = abs(min(drawdownSeries.values()))
        mddPct = max(drawdownPctSeries.values())
    else:
        drawdownSeries = []
        drawdownPctSeries = []
        newHighSeries = []

        i = 0

        for equity in equitySeries:
            if equity > watermark:
                newHighSeries.append([i+1, equity])
                watermark = equity          #markwater mark
                durationWatermark = max(durationWatermark, durationCounter)
                durationCounter = 0
            else:
                durationCounter += 1
            dd = equity - watermark
            drawdownSeries.append(dd)
            #print("sessionConfig:", sessionConfig)
            drawdownPctSeries.append(abs(dd)/(watermark + sessionConfig["cash"]))

            i += 1

        mdd = abs(min(drawdownSeries))
        mddPct = abs(max(drawdownPctSeries))

    durationWatermark = max(durationWatermark, durationCounter)
    return drawdownSeries, mdd, drawdownPctSeries, mddPct, durationWatermark, newHighSeries


def CombineWalkForwardTest(walkForwardTestId, backtests):
    db.update_walk_forward_test_status(walkForwardTestId, "combining")
    walkForwardTestReportFolder = datetime.datetime.now().strftime("walk_forward_test_%Y%m%d_")+str(walkForwardTestId).zfill(6) + "_" + backtests[0]['strategyClass']
    fromPath = SessionStaticVariable.baseReportDirectory + backtests[0]['report_folder_name']
    toPath = SessionStaticVariable.baseReportDirectory + walkForwardTestReportFolder
    copy_tree(fromPath, toPath)

    toPath += "\\"
    os.remove(toPath + "backtestSummary.json")
    os.remove(toPath + "positionSummary.json")


    orders = []
    positions = []
    endDate = None

    for backtest in backtests:
        report_folder = SessionStaticVariable.baseReportDirectory + backtest['report_folder_name'] + "\\"

        with open(report_folder + "positions.json") as data_file:
            positions += json.load(data_file)

        with open(report_folder + "orders.json") as data_file:
            orders += json.load(data_file)

        endDate = backtest['endDate']

    endDate = endDate.replace("-", "")

    i = 1;
    for position in positions:
        position['position_id'] = i
        i+=1

    i = 1;
    for order in orders:
        order['order_id'] = i
        i+=1

    os.remove(toPath + "positions.json")
    os.remove(toPath + "orders.json")

    with open(toPath + 'positions.json', 'w') as fp:
        json.dump(positions, fp, cls=AntJSONEncoder)

    with open(toPath + 'orders.json', 'w') as fp:
        json.dump(orders, fp, cls=AntJSONEncoder)


    with open(toPath + "sessionConfig.json") as data_file:
        sessionConfig = json.load(data_file)
    sessionConfig['endDate'] = endDate

    with open(toPath + 'sessionConfig.json', 'w') as fp:
        json.dump(sessionConfig, fp, cls=AntJSONEncoder, indent=4)

    create_report_summary(toPath)

    db.update_walk_forward_test_status(walkForwardTestId, "completed")
# endregion




# region Get class / class property
def GetClassFromName(moduleName, className):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(moduleName)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, className)
    return c


def GetClassNameFromSubmodule(moduleName):
    import pyclbr
    className = []
    moduleInfo = pyclbr.readmodule(moduleName)

    for item in moduleInfo.values():
        name = item.name
        targetClass = GetClassFromName(moduleName, name)

        if targetClass.IS_DISPLAY_IN_OPTION:
            className.append(item.name)

    return className


def GetClassFromSubmodule(moduleName):
    import pyclbr
    className = []
    moduleInfo = pyclbr.readmodule(moduleName)

    for item in moduleInfo.values():
        className.append(item.name)

    classes = []
    for name in className:
        classes.append(GetClassFromName(moduleName, name))

    return classes


def GetSubmoduleFromModule(submoduleName):
    skip_files = ["__init__.py", "base.py", "future_strategy.py"]
    path = os.path.dirname(ant.__file__)
    path = path + "\\" + submoduleName + "\\"

    pyFiles = []
    pyModules = []
    for f in listdir(path):
        if isfile(join(path, f)) and f not in skip_files and f[0] != "_":
            pyFiles.append(f)
            pyModules.append(f.replace(".py", ""))

    return pyFiles, pyModules

def GetStrategyClassParameter(className):
    submoduleName = "strategy"
    pyFiles, pyModules = GetSubmoduleFromModule(submoduleName)

    for m in pyModules:
        classList = GetClassNameFromSubmodule('ant.' + submoduleName + '.' + m)
        for strategyClass in classList:
            if strategyClass==className:
                strategyClass = GetClassFromSubmodule('ant.' + submoduleName + '.' + m)
                strategyClass = strategyClass[0]
                return strategyClass.OPTIMIZATION_PARAMETER
    return None

def GetSubmoduleClassName(submoduleName):
    pyFiles, pyModules = GetSubmoduleFromModule(submoduleName)

    pyClass = []
    for m in pyModules:
        pyClass = pyClass + GetClassNameFromSubmodule('ant.' + submoduleName + '.' + m)

    return pyClass

def GetSubmoduleClass(submoduleName):
    pyFiles, pyModules = GetSubmoduleFromModule(submoduleName)

    pyClass = []
    for m in pyModules:
        pyClass = pyClass + GetClassFromSubmodule('ant.' + submoduleName + '.' + m)

    return pyClass

def GetStrategyClassName():
    classesName = GetSubmoduleClassName("strategy")
    return GetSubmoduleClassName("strategy")

def GetStrategyClassNameWithMeta():
    returnDictata = []

    classesName = GetSubmoduleClassName("strategy")

    for className in classesName:
        obj = {}
        obj['className'] = className
        obj['optimizationPair'] = GetClassFromName('ant.strategy.'+className, className).OPTIMIZATION_PAIR
        obj['optimizationParameter'] = GetClassFromName('ant.strategy.'+className, className).OPTIMIZATION_PARAMETER
        obj['strategtSlug'] = GetClassFromName('ant.strategy.'+className, className).STRATEGY_SLUG
        obj['strategyName'] = GetClassFromName('ant.strategy.'+className, className).STRATEGY_NAME
        obj['version'] = GetClassFromName('ant.strategy.'+className, className).VERSION
        obj['lastUpdateDate'] = GetClassFromName('ant.strategy.'+className, className).LAST_UPDATE_DATE
        returnDictata.append(obj)

    return returnDictata

def GetWalkForwardTestClassName():
    return GetSubmoduleClassName("walk_forward")

def GetDataSourceClassName():
    return GetSubmoduleClassName("data")

def GetOrderHandlerClassName():
    return GetSubmoduleClassName("order")

def GetPortfolioClassName():
    return GetSubmoduleClassName("portfolio")

def GetFilterTestClassName():
    return GetSubmoduleClassName("filter")


def GetSubmoduleClassName(submoduleName):
    pyFiles, pyModules = GetSubmoduleFromModule(submoduleName)

    pyClass = []
    for m in pyModules:
        pyClass = pyClass + GetClassNameFromSubmodule('ant.' + submoduleName + '.' + m)


    return pyClass



def GetSubmoduleClass(submoduleName):
    pyFiles, pyModules = GetSubmoduleFromModule(submoduleName)

    pyClass = []
    for m in pyModules:
        pyClass = pyClass + GetClassFromSubmodule('ant.' + submoduleName + '.' + m)

    return pyClass

def CheckRequiredValue(keys, target_dict):
    isPass = True
    missedKey = []
    for key in keys:
        if key not in target_dict:
            isPass = False
            missedKey.append(key)

    d = {}
    if isPass:
        return True
    else:
        return CreateSocketioResponse("fail", ", ".join(missedKey) + " are missed", d)

def CreateSocketioResponse(status, description, action, data={}):
    returnDict = {}
    returnDict['status'] = status
    returnDict['description'] = description
    returnDict['action'] = action
    returnDict['data'] = data
    return returnDict
# endregion

def IsIntraDayData(dataName):
    dataName = dataName.lower()
    if dataName in ["opend", "highd", "lowd", "closed", "vold", "volumed",
                    "morningopend", "morninghighd", "morninglowd", "morningclosed", "morningvold", "morningvolumed",
                    "afternoonopend", "afternoonhighd", "afternoonlowd", "afternoonclosed", "afternoonvold", "afternoonvolumed",

                    "ranged", "uppershadowd", "lowershadowd", "bodyd",
                    "morningranged", "morninguppershadowd", "morninglowershadowd", "morningbodyd",
                    "afternoonranged", "afternoonuppershadowd", "afternoonlowershadowd", "afternoonbodyd"]:

        return False
    return True


def GetDataByName(instance, dataName):
    from .session import Session, IBLiveSession
    from .signal.base import Signal
    from .strategy.future_strategy import FutureAbstractStrategy

    strategy = None
    if issubclass(type(instance), FutureAbstractStrategy):

        strategy = instance
    elif issubclass(type(instance), Signal):
        strategy = instance.strategy
    elif issubclass(type(instance), Session):
        strategy = instance.strategy
    elif issubclass(type(instance), IBLiveSession):
        strategy = instance.strategy

    dataName = dataName.lower()

    if dataName == "tr" or dataName == "atr":
        strategy.useTR = True
        return strategy.TR
    if dataName == "open":
        return strategy.open
    elif dataName == "high":
        return strategy.high
    elif dataName == "low":
        return strategy.low
    elif dataName == "close":
        return strategy.close
    elif dataName == "vol" or dataName == "volume":
        return strategy.volume

    elif dataName == "opend":
        return strategy.openD
    elif dataName == "highd":
        return strategy.highD
    elif dataName == "lowd":
        return strategy.lowD
    elif dataName == "closed":
        return strategy.closeD
    elif dataName == "vold" or dataName == "volumed":
        return strategy.volumeD

    elif dataName == "morningopend":
        return strategy.morningOpenD
    elif dataName == "morninghighd":
        return strategy.morningHighD
    elif dataName == "morninglowd":
        return strategy.morningLowD
    elif dataName == "morningclosed":
        return strategy.morningCloseD
    elif dataName == "morningvold" or dataName == "morningvolumed":
        return strategy.morningVolumeD

    elif dataName == "afternoonopend":
        return strategy.afternoonOpenD
    elif dataName == "afternoonhighd":
        return strategy.afternoonHighD
    elif dataName == "afternoonlowd":
        return strategy.afternoonLowD
    elif dataName == "afternoonclosed":
        return strategy.afternoonCloseD
    elif dataName == "afternoonvold" or dataName == "afternoonvolumed":
        return strategy.afternoonVolumeD

    elif dataName == "ranged":
        return strategy.ranged
    elif dataName == "uppershadowd":
        return strategy.upperShadowD
    elif dataName == "lowershadowd":
        return strategy.lowerShadowD
    elif dataName == "bodyd":
        return strategy.bodyD

    elif dataName == "morningranged":
        return strategy.morningRangeD
    elif dataName == "morninguppershadowd":
        return strategy.morningUpperShadowD
    elif dataName == "morninglowershadowd":
        return strategy.morningLowerShadowD
    elif dataName == "morningbodyd":
        return strategy.morningBodyD

    elif dataName == "afternoonranged":
        return strategy.afternoonRangeD
    elif dataName == "afternoonuppershadowd":
        return strategy.afternoonUpperShadowD
    elif dataName == "afternoonlowershadowd":
        return strategy.afternoonLowerShadowD
    elif dataName == "afternoonbodyd":
        return strategy.afternoonBodyD

    return None


def GetTodayStr(todayStrHourOffset=7):
    today = datetime.today() - timedelta(hours=todayStrHourOffset)
    return today.strftime('%Y%m%d')

def GetLiveTradeDayInfo(todayStr, todayStrHourOffset=7, LogFunction = None):
    from .session import SessionStaticVariable
    #todayStrHourOffset: in case started after 0000 still using yesterday as todayStr
    #today = datetime.today() - timedelta(hours=todayStrHourOffset)
    #todayStr = today.strftime('%Y%m%d')
    #todayStrWithSperator = today.strftime('%Y-%m-%d')
    todayStrWithSperator = todayStr[0:4] + "-" + todayStr[4:6] + "-" + todayStr[6:]
    tradeDateCSVFilePath = SessionStaticVariable.baseLiveDataDirectory + "trade_date/trade_date.csv"

    isFindTradeDate = False
    with open(tradeDateCSVFilePath) as f:
        for line in f:
            line = line.replace('\n', ' ').replace('\r', '')
            cell = line.split(',')
            if cell[0] == todayStrWithSperator:
                marketAdjustedAfternoonBreakTime = cell[2]
                marketAdjustedEndTime = cell[3]
                expiryMonth = str(cell[4].replace(' ', ''))

                if LogFunction is not None:
                    LogFunction("please check how to handle the night which have no night market")
                    LogFunction("GetTradeDayInfo()", "trade date info:", todayStr, todayStrWithSperator, marketAdjustedAfternoonBreakTime, marketAdjustedEndTime, expiryMonth)
                #Log("trade date info:", todayStr, todayStrWithSperator, marketAdjustedAfternoonBreakTime, marketAdjustedEndTime, expiryMonth)

                isFindTradeDate = True

                break;
        f.close()

    if not isFindTradeDate:
        if LogFunction is not None:
            LogFunction("no trade date found:")
            LogFunction("make raise error")

    return marketAdjustedAfternoonBreakTime, marketAdjustedEndTime, expiryMonth


def GetOrderUid(sid):
    return str(sid) + "_" + "".join(random.choice(string.ascii_uppercase) for _ in range(6))



