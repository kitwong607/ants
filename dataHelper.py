import datetime
import pandas as pd

from . import utilities
from .static import *
from .session import SessionStaticVariable


def LoadInterDayPriceData(exchange, ticker, date, resolution):
    _dataPath = SessionStaticVariable.dataPath

    if "," not in date:
        dateList = [date]
    else:
        dateList = date.split(",")

        dateList.sort()

    _months = []
    for dateStr in dateList:
        _month = dateStr[:6]
        if not _month in dateList:
            _months.append(_month)


    dfs = []
    isFirst = True

    tickerType = GetTickerType(ticker).lower()
    for _month in _months:
        csvFilename = _month + "_" + ticker + "_" + resolution + ".csv"
        csvFilePath = _dataPath + tickerType + "/" + exchange + "/csv/" + resolution + "/" + csvFilename
        df = pd.DataFrame.from_csv(csvFilePath)

        if isFirst:
            df['datetime_for_sort'] = df.index
        else:
            df['datetime_for_sort'] = df.index + datetime.timedelta(seconds=RESOLUTION_IN_SEC[resolution])
        df['ticker'] = ticker
        df['resolution'] = resolution
        df['resolution_in_sec'] = RESOLUTION_IN_SEC[resolution]
        dfs.append(df)

        isFirst = False

    df = pd.concat(dfs)
    df = df.sort_values(["datetime_for_sort", "resolution_in_sec"])
    df = df.drop('datetime_for_sort', 1)

    startDatetime = datetime.datetime.strptime(dateList[0], '%Y%m%d') + datetime.timedelta(hours=8)  #to 8am
    endDatetime = datetime.datetime.strptime(dateList[-1], '%Y%m%d')  + datetime.timedelta(hours=32) #before next day 8 am
    start = df.index.searchsorted(startDatetime)
    end = df.index.searchsorted(endDatetime)

    return df.ix[start:end]




'''
def load_inter_day_data(exchange, ticker, date, resolution):
    _data_path = SessionStaticVariable.dataPath

    if "," not in date:
        date_list = [date]
    else:
        date_list = date.split(",")

    date_list.sort()

    _months = []
    for date_str in date_list:
        _month = date_str[:6]
        if not _month in date_list:
            _months.append(_month)


    dfs = []
    is_first = True
    for _month in _months:
        csv_filename = _month + "_" + ticker + "_" + resolution + ".csv"
        csv_file_path = _data_path + exchange + "\\csv\\" + resolution + "\\" + csv_filename

        df = pd.DataFrame.from_csv(csv_file_path)
        if is_first:
            df['datetime_for_sort'] = df.index
        else:
            df['datetime_for_sort'] = df.index + datetime.timedelta(seconds=RESOLUTION_IN_SEC[resolution])
        df['ticker'] = ticker
        df['resolution'] = resolution
        df['resolution_in_sec'] = RESOLUTION_IN_SEC[resolution]
        dfs.append(df)

        is_first = False

    df = pd.concat(dfs)
    df = df.sort_values(["datetime_for_sort", "resolution_in_sec"])
    df = df.drop('datetime_for_sort', 1)

    startdatetime = datetime.datetime.strptime(date_list[0], '%Y%m%d') + datetime.timedelta(hours=8)  #to 8am
    enddatetime = datetime.datetime.strptime(date_list[-1], '%Y%m%d')  + datetime.timedelta(hours=32) #before next day 8 am
    start = df.index.searchsorted(startdatetime)
    end = df.index.searchsorted(enddatetime)

    return df.ix[start:end]
    
    '''
