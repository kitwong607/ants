import pymysql.cursors, json, traceback, datetime, sys, itertools, math, copy, requests
from . import utilities, static

NOT_SET = "not_set"
CONFIG_HOST = "localhost"
CONFIG_USER = "ants_admin"
CONFIG_PASSWORD = "SlamDunk21"
CONFIG_DB = "ants"


# region DB connect function
def ConnectToMySQL():
    connection = pymysql.connect(host=CONFIG_HOST,
                                 user=CONFIG_USER,
                                 password=CONFIG_PASSWORD,
                                 db=CONFIG_DB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def DisconnectToMySQL(connection):
    connection.close()
# endregion

############################################################################

# region Data format convert
def MySQLTimeToString(dt):
    if dt is None:
        return "0000-00-00 00:00:00"
    return dt.strftime('%Y-%m-%d %H:%M:%S')
# endregion

############################################################################

# region Option related
def GetOption(option_key):
    try:
        value = NOT_SET
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `sys_option` WHERE `option_key`=%s LIMIT 1"
            cursor.execute(sql, (option_key))
            connection.commit()
            result = cursor.fetchone()
            if result is None:
                value = "not_set"
            else:
                value = result['option_value']

        return value
    except:
        traceback.print_exc()
        return NOT_SET
    finally:
        DisconnectToMySQL(connection)


def UpdateOption(optionKey, optionValue):
    try:
        value = NOT_SET
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `sys_option` WHERE `option_key`=%s"
            cursor.execute(sql, (optionKey))
            connection.commit()
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO `sys_option` (`option_key`, `option_value`) VALUES(%s, %s)"
                cursor.execute(sql, (optionKey,optionValue))
                connection.commit()
                result = cursor.fetchone()
            else:
                sql = "UPDATE `sys_option` SET `option_value`=%s WHERE `option_key`=%s"
                cursor.execute(sql, (optionValue, optionKey))
                connection.commit()
                result = cursor.fetchone()

        return True
    except:
        traceback.print_exc()
        return False
    finally:
        DisconnectToMySQL(connection)
# endregion

############################################################################

# region Backtest related
# region Get Method
def GetFinalBacktestByWalkforwardTest(wftId):
    try:
        value = NOT_SET
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `backtest_report` WHERE `walk_forward_test_id`=%s AND `is_final_walk_forward_backtest`=%s ORDER BY `start_date` ASC"
            cursor.execute(sql, (wftId, 'yes'))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value.append(row)

        return value
    except:
        traceback.print_exc()
        return NOT_SET
    finally:
        DisconnectToMySQL(connection)

def GetBacktestByOptimizationId(optimizationId):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `backtest_report` WHERE `optimization_id`=%s  ORDER BY `created_time`, `id`"
            cursor.execute(sql, (optimization_id))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value.append(row)

        return value
    except:
        traceback.print_exc()
        return value

    finally:
        DisconnectToMySQL(connection)

def GetBacktestById(backtestId, table="backtest_report"):
    try:
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `"+table+"` WHERE `id`=%s  LIMIT 1"
            cursor.execute(sql, (backtestId))
            connection.commit()
            result = cursor.fetchone()

        return result
    except:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)

def GetBacktest(status="running"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            if status=="all":
                sql = "SELECT * FROM `backtest_report` ORDER BY `created_time`"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM `backtest_report` WHERE `status`=%s  ORDER BY `created_time`"
                cursor.execute(sql, (status))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])

                    value.append(row)

        return value
    except:
        traceback.print_exc()
        return value
    finally:
        DisconnectToMySQL(connection)

def GetBacktestStatusSummary(result):
    value = {}
    value['num_backtest'] = 0
    value['num_completed'] = 0
    value['num_error'] = 0
    value['num_running'] = 0
    value['num_pending'] = 0
    value['num_delete'] = 0

    if result is not None:
        for row in result:
            value["num_" + row['status']] += row['num_rows']
            value['num_backtest'] += row['num_rows']

    return value

def GetBacktestWithPagination(pageSize, pageNo):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()

            value = GetBacktestStatusSummary(result)
            value['page_size'] = pageSize
            value['page_no'] = pageNo
            value['num_pages'] = int(math.ceil(value['num_backtest'] / pageSize))

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, ((pageNo - 1) * pageSize, pageSize))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['backtest'].append(row)

        return value
    except:
        print(traceback.print_exc())
        return NOT_SET
    finally:
        DisconnectToMySQL(connection)


def GetBacktestWithOptimizationId(optimizationId, pageSize, pageNo):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id` = %s GROUP BY `status`"
            cursor.execute(sql, (optimizationId))
            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            value = GetBacktestStatusSummary(result)
            value['page_size'] = pageSize
            value['page_no'] = pageNo
            value['num_pages'] = int(math.ceil(value['num_backtest'] / pageSize))

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` WHERE `optimization_id` = %s ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, (optimizationId, (pageNo - 1) * pageSize, pageSize))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['backtest'].append(row)

        return value
    except:
        print(traceback.print_exc())
        return []
    finally:
        DisconnectToMySQL(connection)


def GetBacktestWithWalkForwardTestId(wftId):
    try:
        connection = ConnectToMySQL()
        value = []
        yes = "yes"

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `walk_forward_test_id` = %s AND `is_final_walk_forward_backtest`=%s GROUP BY `status`"
            cursor.execute(sql, (wftId, yes))
            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            value = GetBacktestStatusSummary(result)

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` WHERE `walk_forward_test_id` = %s AND `is_final_walk_forward_backtest`=%s ORDER BY `id`"
            cursor.execute(sql, (wftId, yes))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['backtest'].append(row)

        return value
    except:
        print(traceback.print_exc())
        return []

    finally:
        DisconnectToMySQL(connection)
# endregion


# region Update method
def UpdateBacktestReport(config):
    try:
        with open(config.report_directory + '\\backtest_summary.json') as jsonData:
            d = json.load(jsonData)
            d['report_folder_name'] = config.report_folder_name
            d['report_full_path'] = config.report_directory

            connection = ConnectToMySQL()
            value = []

            d = utilities.PrepareBacktestReportInsertToDB(d)

            with connection.cursor() as cursor:
                sql = "UPDATE `backtest_report` SET `win_rate`=%s, `num_trade`=%s, `pnl`=%s, `net_pips`=%s, `profit_factor`=%s, `payoff_ratio`=%s, `roci`=%s, `sharpe_ratio`=%s, `standard_deviation`=%s, `standard_error`=%s, `tharp_expectancy`=%s, `expectancy`=%s, `mdd`=%s, `mdd_pct`=%s, `mdd_daily`=%s, `mdd_pct_daily`=%s, `dd_duration`=%s, `dd_duration_daily`=%s, `avg_pips_pre_contract`=%s, `report_folder_name`=%s, `report_full_path`=%s, `modified_time`=NOW() WHERE `id`=%s"
                cursor.execute(sql, (d['win_rate'], d['num_trade'], d['pnl'], d['net_pips'], d['profit_factor'], d['payoff_ratio'], d['roci'],
                                     d['sharpe_ratio'], d['standard_deviation'], d['standard_error'], d['tharp_expectancy'], d['expectancy'],
                                     d['mdd'], d['mdd_pct'], d['mdd_daily'], d['mdd_pct_daily'], d['dd_duration'],
                                     d['dd_duration_daily'], d['avg_pips_pre_contract'], d['report_folder_name'], d['report_full_path'], config.session_id))

                connection.commit()

            return True

        return False

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)


def UpdateBacktestStartTime(backtestId, table="backtest_report"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `"+table+"` SET `backtest_start_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (backtestId))
            connection.commit()

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)


def UpdateBacktestEndTime(backtestId, table="backtest_report"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `"+table+"` SET `backtest_end_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (backtestId))
            connection.commit()

            result = GetBacktestById(backtestId, table)
            if result == NOT_SET: return False

            if (backtest is not None) and (result == "success"):
                secDiff = (backtest['backtest_end_time'] - backtest['backtest_start_time']).total_seconds()
                secDiff = str(datetime.timedelta(seconds=int(secDiff)))

                sql = "UPDATE `" + table + "` SET `backtest_used_time`=%s WHERE `id`=%s"
                cursor.execute(sql, (secDiff, backtestId))
                connection.commit()

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)



def UpdateBacktestStatus(backtestId, status, errorMsg=""):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            result = GetBacktestById(backtestId)
            if result == NOT_SET: return False

            backtest = result
            optimizationId = backtest['optimization_id']


            sql = "UPDATE `backtest_report` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, errorMsg, backtestId))
            connection.commit()



            if status == "running":
                UpdateBacktestStartTime(backtestId)

                if optimizationId != 0:
                    sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id`=%s GROUP BY `status`"
                    cursor.execute(sql, (optimizationId))
                    connection.commit()

                    result = cursor.fetchall()
                    value = GetBacktestStatusSummary(result)
                    if value['num_backtest'] == value['num_running'] + value['num_pending'] and value['num_running']==1:
                        UpdateOptimizationStatus(optimizationId, "running")



            elif status == "completed":
                UpdateBacktestEndTime(backtestId)

                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtestId))
                connection.commit()
                backtest = cursor.fetchone()
                isDBError = False

                if backtest is not None:
                    #check current backtest is a optimization
                    if optimizationId != 0:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (optimizationId))
                        connection.commit()

                        result = cursor.fetchall()
                        value = GetBacktestStatusSummary(result)

                        if value['num_backtest'] == value['num_completed']:
                            UpdateOptimizationStatus(optimizationId, "backtest_complete")

                    if backtest['is_final_walk_forward_backtest'] == 'yes':
                        sql = "SELECT * FROM `backtest_report` WHERE `walk_forward_test_id`=%s and  `is_final_walk_forward_backtest`=%s ORDER BY `id` ASC"
                        cursor.execute(sql, (backtest['walk_forward_test_id'], 'yes'))
                        connection.commit()

                        rows = cursor.fetchall()

                        is_completed = True
                        for row in  rows:
                            if row['status'] != "completed":
                                is_completed = False
                                break

                        if is_completed:
                            UpdateWalkForwardTestStatus(backtest['walk_forward_test_id'], 'backtest_complete')



            elif status=="error":
                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                result = cursor.fetchone()

                if optimizationId != 0:
                    UpdateOptimizationStatus(optimizationId, "error")

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion


# region Create method
def AddBacktest(data):
    try:
        connection = ConnectToMySQL()
        value = []

        strategyClass = utilities.GetClassFromName('ants.strategy.'+data['strategy'], data['strategy'])
        data["strategy_name"] = strategyClass.STRATEGY_NAME
        data["strategy_slug"] = strategyClass.STRATEGY_SLUG
        data["last_update"] = strategyClass.VERSION
        data["version"] = strategyClass.LAST_UPDATE_DATE

        data["backtest_mode_no"] = int(data["backtest_mode"])
        if data["backtest_mode_no"] == 0:
            data["backtest_mode"] = "Intra day single process"
        elif data["backtest_mode_no"] == 1:
            data["backtest_mode"] = "Inter day single process"
        elif data["backtest_mode_no"] == 2:
            data["backtest_mode"] = "Intra day multi process"
        elif data["backtest_mode_no"] == 3:
            data["backtest_mode"] = "Inter day multi process"
        else:
            data["backtest_mode"] = "not handle in db.py"

        with connection.cursor() as cursor:
            if "optimization_id" not in data:
                data["optimization_id"] = 0

            if "walk_forward_test_id" not in data:
                data["walk_forward_test_id"] = 0

            if "is_final_walk_forward_backtest" not in data:
                data["is_final_walk_forward_backtest"] = 'no'

            if "remark" not in data:
                data["remark"] = ""

            sql = "INSERT INTO `backtest_report` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategyClass`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `StrategyParameter`, `optimization_id`, `walk_forward_test_id`,`is_final_walk_forward_backtest`,`remark`,`created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
            cursor.execute(sql, (
            data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"],
            data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"],
            data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"],
            data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"],
            data["strategy_slug"], data["last_update"], data["version"], data["parameter"], data["optimization_id"],
            data["walk_forward_test_id"], data["is_final_walk_forward_backtest"], data["remark"]))

            #25
            connection.commit()
            result = cursor.fetchone()

            return True

        return False

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

def CreateBacktestJobFromOptimization():

    optimizations = GetOptimization("pending")
    if optimizations == NOT_SET: return False


    for job in jobs:
        StrategyParameter_str = job['strategy_parameter']
        StrategyParameter = json.loads(StrategyParameter_str)
        strategyClass = utilities.GetClassFromName('ants.strategy.' + job['strategy_class'], job['strategy_class'])
        optimization_parameter = strategyClass.OPTIMIZATION_PARAMETER

        keys = []
        values = []
        for key, parameter in optimization_parameter.items():
            print(parameter)
            keys.append(key)
            value = []
            if key in StrategyParameter:
                print(key)
                for i in range(parameter['min_value'], parameter['max_value']+1, parameter['step']):
                    value.append(i)
            else:
                value.append(parameter['value'])
            values.append(value)

        data = {}
        data["backtest_mode"] = int(job["backtest_mode_no"])
        data["data_start_date"] = job['data_start_date']
        data["start_date"] = job['start_date']
        data["end_date"] = job['end_date']
        data["data_ticker"] = job['data_ticker']
        data["trade_ticker"] = job['trade_ticker']
        data["exchange"] = job['exchange']
        data["cash"] = job['cash']
        data["base_quantity"] = job['base_quantity']
        data["commission"] = job['commission']
        data["slippage_pips"] = job['slippage_pips']
        data["data_resolution"] = job['data_resolution']
        data["portfolio"] = job['portfolio_class']
        data["order_handler"] = job['order_handler_class']
        data["data_provider"] = job['data_provider_class']
        data["strategy"] = job['strategy_class']
        data["strategy_name"] = job['strategy_name']
        data["strategy_slug"] = job['strategy_slug']
        data["last_update"] = job['last_update']
        data["version"] = job['version']
        data["contract"] = job['contract']
        data["optimization_id"] = job['id']
        for combination in itertools.product(*values):
            parameter = {}
            i = 0
            for key in keys:
                parameter[key] = combination[i]

            data["parameter"] = json.dumps(parameter)

            result, msg = addBacktest(data)
# endregion


# endregion

############################################################################

# region Optimization related
# region Get method
def GetOptimizationwithWalkForwardTestId(wftId):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
            cursor.execute(sql, wftId)
            connection.commit()
            result = cursor.fetchall()

            value = {}
            value['num_optimization'] = 0
            value['num_error'] = 0
            value['num_running'] = 0
            value['num_pending'] = 0
            value['num_delete'] = 0
            value['num_completed'] = 0
            value['num_backtest_complete'] = 0

            value['optimization'] = []

            if result is not None:
                for row in result:
                    if "num_"+row['status'] not in value:
                        value["num_"+row['status']] = 0
                    value["num_"+row['status']] += row['num_rows']
                    value['num_optimization'] += row['num_rows']

            sql = "SELECT * FROM `optimization` WHERE `walk_forward_test_id`=%s ORDER BY `id` DESC, `created_time` DESC"
            cursor.execute(sql, wftId)
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['optimization'].append(row)

        return value
    except:
        print(traceback.print_exc())
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetOptimizationWithPagination(pageSize, pageNo):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            value = {}
            value['num_optimization'] = 0
            value['num_error'] = 0
            value['num_running'] = 0
            value['num_pending'] = 0
            value['num_delete'] = 0
            value['num_completed'] = 0
            value['num_backtest_complete'] = 0

            value['optimization'] = []

            if result is not None:
                for row in result:
                    if "num_"+row['status'] not in value:
                        value["num_"+row['status']] = 0
                    value["num_"+row['status']] += row['num_rows']
                    value['num_optimization'] += row['num_rows']

            value['page_size'] = pageSize
            value['page_no'] = pageNo
            value['num_pages'] = int(math.ceil(value['num_optimization'] / pageSize))

            sql = "SELECT * FROM `optimization` ORDER BY `id` DESC, `created_time` DESC LIMIT %s, %s"
            cursor.execute(sql, ((pageNo-1)*pageSize, pageSize))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['optimization'].append(row)

        return value
    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)


def GetOptimizationById(optimizationId):
    try:
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            sql = "SELECT * FROM `optimization` WHERE `id`=%s  ORDER BY `created_time` DESC"
            cursor.execute(sql, (optimizationId))
            connection.commit()
            result = cursor.fetchone()
            isDBError = False

            if result is not None:
                result['backtest_start_time'] = MySQLTimeToString(result['backtest_start_time'])
                result['backtest_end_time'] = MySQLTimeToString(result['backtest_end_time'])
                result['created_time'] = MySQLTimeToString(result['created_time'])
                result['modified_time'] = MySQLTimeToString(result['modified_time'])

        return result
    except:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetOptimization(status="running"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            if status=="all":
                sql = "SELECT * FROM `optimization` ORDER BY `created_time` DESC"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM `optimization` WHERE `status`=%s  ORDER BY `created_time` DESC"
                cursor.execute(sql, (status))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value.append(row)

        return value

    except:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetOptimizationStatusSummary(result):
    value = {}
    value['num_optimization'] = 0
    value['num_completed'] = 0
    value['num_error'] = 0
    value['num_running'] = 0
    value['num_pending'] = 0
    value['num_delete'] = 0

    if result is not None:
        for row in result:
            if "num_"+row['status'] not in value:
                value["num_" + row['status']] = 0
            value["num_" + row['status']] += row['num_rows']
            value['num_optimization'] += row['num_rows']
    return value
# endregion


# region Update method
def UpdateOptimization(optimizationId:int, optimizationSummary, firstBacktestReport):
    try:
        isDBError = True
        isSuccess = True
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `optimization` SET `report_full_path`=%s, `report_folder_name`=%s, `num_trade`=%s, `num_trade_std`=%s, `num_trade_std_pct`=%s, `win_rate`=%s, `win_rate_std`=%s, `win_rate_std_pct`=%s, `pnl`=%s, `pnl_std`=%s, `pnl_std_pct`=%s, `net_pips`=%s, `net_pips_std`=%s, `net_pips_std_pct`=%s, `avg_pips_pre_contract`=%s, `avg_pips_pre_contract_std`=%s, `avg_pips_pre_contract_std_pct`=%s, `profit_factor`=%s, `profit_factor_std`=%s, `profit_factor_std_pct`=%s, `payoff_ratio`=%s, `payoff_ratio_std`=%s, `payoff_ratio_std_pct`=%s, `roci`=%s, `roci_std`=%s, `roci_std_pct`=%s, `sharpe_ratio`=%s, `sharpe_ratio_std`=%s, `sharpe_ratio_std_pct`=%s, `tharp_expectancy`=%s, `tharp_expectancy_std`=%s, `tharp_expectancy_std_pct`=%s, `expectancy`=%s, `expectancy_std`=%s, `expectancy_std_pct`=%s, `mdd`=%s, `mdd_std`=%s, `mdd_std_pct`=%s, `mdd_pct`=%s, `mdd_pct_std`=%s, `mdd_pct_std_pct`=%s, `mdd_daily`=%s, `mdd_daily_std`=%s, `mdd_daily_std_pct`=%s, `mdd_pct_daily`=%s, `mdd_pct_daily_std`=%s, `mdd_pct_daily_std_pct`=%s, `dd_duration`=%s, `dd_duration_std`=%s, `dd_duration_std_pct`=%s, `dd_duration_daily`=%s, `dd_duration_daily_std`=%s, `dd_duration_daily_std_pct`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (   firstBacktestReport['performance']['report_full_path'],
                                    firstBacktestReport['performance']['report_folder_name'],
                                    "{0:.8f}".format(float(optimizationSummary['num_trade'])),
                                    "{0:.8f}".format(float(optimizationSummary['num_trade_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['num_trade_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['win_rate'])),
                                    "{0:.8f}".format(float(optimizationSummary['win_rate_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['win_rate_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['pnl'])),
                                    "{0:.8f}".format(float(optimizationSummary['pnl_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['pnl_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['net_pips'])),
                                    "{0:.8f}".format(float(optimizationSummary['net_pips_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['net_pips_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['avg_pips_pre_contract'])),
                                    "{0:.8f}".format(float(optimizationSummary['avg_pips_pre_contract_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['avg_pips_pre_contract_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['profit_factor'])),
                                    "{0:.8f}".format(float(optimizationSummary['profit_factor_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['profit_factor_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['payoff_ratio'])),
                                    "{0:.8f}".format(float(optimizationSummary['payoff_ratio_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['payoff_ratio_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['roci'])),
                                    "{0:.8f}".format(float(optimizationSummary['roci_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['roci_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['sharpe_ratio'])),
                                    "{0:.8f}".format(float(optimizationSummary['sharpe_ratio_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['sharpe_ratio_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['tharp_expectancy'])),
                                    "{0:.8f}".format(float(optimizationSummary['tharp_expectancy_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['tharp_expectancy_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['expectancy'])),
                                    "{0:.8f}".format(float(optimizationSummary['expectancy_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['expectancy_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_daily'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_daily_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_daily_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct_daily'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct_daily_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['mdd_pct_daily_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration_std_pct'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration_daily'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration_daily_std'])),
                                    "{0:.8f}".format(float(optimizationSummary['dd_duration_daily_std_pct'])),
                                    optimizationId))
            connection.commit()
        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)


def UpdateOptimizationStatus(optimizationId, status, errorMsg=""):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `optimization` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, errorMsg, optimizationId))
            connection.commit()

            if status == "running":
                UpdateBacktestStartTime(optimizationId, 'optimization')

                result = GetBacktestById(optimizationId, 'optimization')

                if result == NOT_SET: return False

                if (optimization is not None) and (result == "success"):
                    wftId = optimization['walk_forward_test_id']

                    if wftId != 0 or wftId is not None:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (wftId))
                        connection.commit()


                        result = cursor.fetchall()
                        value = GetOptimizationStatusSummary(result)
                        if value['num_optimization'] == value['num_running'] + value['num_pending'] and value['num_running']==1:
                            UpdateWalkForwardTestStatus(wftId, "running")


            elif status=="backtest_complete":
                UpdateBacktestEndTime(optimizationId, 'optimization')

            elif status == "completed":
                wftId = 0
                result = GetOptimizationById(optimizationId)

                if result == NOT_SET: return False

                if (optimization is not None) and (result == "success"):
                    wftId = optimization['walk_forward_test_id']

                if result is not None:
                    #check current optimization is a walk forward test
                    if wftId != 0:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (wftId))
                        connection.commit()

                        result = cursor.fetchall()
                        value = GetOptimizationStatusSummary(result)

                        if value['num_optimization'] == value['num_completed']:
                            UpdateWalkForwardTestStatus(wftId, "optimization_complete")
                else:
                    print("result is none")

            elif status=="error":
                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                result = cursor.fetchone()

                if optimizationId != 0:
                    UpdateOptimizationStatus(optimizationId, "error")


        return True
    except e:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion


# region Create method
def AddOptimization(data):
    try:
        connection = ConnectToMySQL()
        value = []

        strategyClass = utilities.GetClassFromName('ants.strategy.'+data['strategy'], data['strategy'])
        data["strategy_name"] = strategyClass.STRATEGY_NAME
        data["strategy_slug"] = strategyClass.STRATEGY_SLUG
        data["last_update"] = strategyClass.VERSION
        data["version"] = strategyClass.LAST_UPDATE_DATE

        # ToDo mark as filter backtest
        StrategyParameter = strategyClass.OPTIMIZATION_PARAMETER

        data["backtest_mode_no"] = int(data["backtest_mode"])
        if data["backtest_mode_no"] == 0:
            data["backtest_mode"] = "Intra day single process"
        elif data["backtest_mode_no"] == 1:
            data["backtest_mode"] = "Inter day single process"
        elif data["backtest_mode_no"] == 2:
            data["backtest_mode"] = "Intra day multi process"
        elif data["backtest_mode_no"] == 3:
            data["backtest_mode"] = "Inter day multi process"
        else:
            data["backtest_mode"] = "not handle in db.py"

        with connection.cursor() as cursor:
            if "walk_forward_test_id" not in data:
                data["walk_forward_test_id"] = 0

            if "remark" not in data:
                data["remark"] = 0

            sql = "INSERT INTO `optimization` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategyClass`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `StrategyParameter`, `walk_forward_test_id`, `remark`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
            cursor.execute(sql, (
            data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"],
            data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"],
            data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"],
            data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"],
            data["strategy_slug"], data["last_update"], data["version"], data["parameter"], data["walk_forward_test_id"], data["remark"]))

            connection.commit()
            result = cursor.fetchone()
            isDBError = False

            optimizationId = cursor.lastrowid
            optimize_parameter = json.loads(data['parameter'])

            StrategyParameter_combination = utilities.get_optimization_parameter_combination(StrategyParameter, optimize_parameter)
            #add backtest job here
            for parameter in StrategyParameter_combination:
                newData = copy.deepcopy(data)
                newData["backtest_mode"] = data["backtest_mode_no"]
                newData["parameter"] = json.dumps(parameter)
                newData["optimization_id"] = optimizationId
                addBacktest(newData)

        return True

    except e:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

# endregion


# endregion

############################################################################

# region Walk forward test
def AddWalkForwardTest(data):
    try:
        connection = ConnectToMySQL()
        value = []

        strategyClass = utilities.GetClassFromName('ants.strategy.'+data['strategy'], data['strategy'])
        data["strategy_name"] = strategyClass.STRATEGY_NAME
        data["strategy_slug"] = strategyClass.STRATEGY_SLUG
        data["last_update"] = strategyClass.VERSION
        data["version"] = strategyClass.LAST_UPDATE_DATE

        if "remark" not in data:
            data["remark"] = ""
        StrategyParameter = strategyClass.OPTIMIZATION_PARAMETER

        data["backtest_mode_no"] = int(data["backtest_mode"])

        #1 add walk forward test
        with connection.cursor() as cursor:
            sql = "INSERT INTO `walk_forward_test` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategyClass`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `remark`,  `walk_forward_test`, `no_of_month`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
            cursor.execute(sql, (data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"], data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"], data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"], data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"], data["strategy_slug"], data["last_update"], data["version"], data["remark"], data["walk_forward_test"], data["no_of_month"]))
            connection.commit()
            result = cursor.fetchone()
            isDBError = False

            data['walk_forward_test_id'] = cursor.lastrowid


            #add optimization
            optimization_pair = strategyClass.OPTIMIZATION_PAIR
            optimization_parameter = strategyClass.OPTIMIZATION_PARAMETER
            optimization_pair_for_checking = list(itertools.chain.from_iterable(optimization_pair))

            allParameterExistInPair = True

            for key in optimization_parameter:
                if key not in optimization_pair_for_checking:
                    allParameterExistInPair = False

            if not allParameterExistInPair:
                return "fail", "error found on add walk forward test, optimization pair and optimization parameter not match"

            dataStartDateDt = datetime.datetime.strptime(data['data_start_date'], "%Y-%m-%d").date()
            startDateDt = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            endDateDt = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d").date()

            monthDiff = abs(utilities.diffMonth(dataStartDateDt, startDateDt))
            totalNoOfMonth = abs(utilities.diff_month(startDateDt, endDateDt)) + 1

            optimizationIdBatch = []

            for i in range(0, totalNoOfMonth):
                optimization_id_single_batch = []
                next_startDateDt = utilities.add_months(startDateDt, i)

                # for optimization
                newStartDateDt = utilities.add_months(next_startDateDt, int(data['no_of_month'])*-1)
                newDataStartDateDt = utilities.add_months(newStartDateDt, -monthDiff)
                newEndDateDt = utilities.add_months_with_last_date(newStartDateDt, int(data['no_of_month']))

                newBacktestStartDate = next_startDateDt
                newBacktestDataStartDate = utilities.add_months(newBacktestStartDate, -monthDiff)
                newBacktestEndDateDt = utilities.add_months_with_last_date(newBacktestStartDate, 1)

                for pair in optimization_pair:
                    newOptimizeParameter = {}
                    for key in pair:
                        newOptimizeParameter[key] = optimization_parameter[key]

                    newData = copy.deepcopy(data)
                    newData['data_start_date'] = newDataStartDateDt.strftime("%Y-%m-%d")
                    newData['start_date'] = newStartDateDt.strftime("%Y-%m-%d")
                    newData['end_date'] = newEndDateDt.strftime("%Y-%m-%d")
                    newData['parameter'] = json.dumps(newOptimizeParameter)

                    optimization_id = add_optimization(newData, False)
                    optimization_id_single_batch.append(optimization_id)
                    # add optimization here
                    print("add optimization:", optimization_id)
                optimizationIdBatch.append(optimization_id_single_batch)

            optimizationIdBatch = json.dumps(optimizationIdBatch)

            print("optimizationIdBatch", optimizationIdBatch)
            print("optimizationIdBatch", type(optimizationIdBatch))
            print("data['walk_forward_test_id']", data['walk_forward_test_id'])

            sql = "UPDATE `walk_forward_test` SET `optimization_batch`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (optimizationIdBatch, data['walk_forward_test_id']))
            connection.commit()
            result = cursor.fetchone()

        return True

    except e:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)

def GetWalkForwardTestStatusSummary(result):
    value = {}
    value['num_walk_forward_test'] = 0
    value['num_completed'] = 0
    value['num_error'] = 0
    value['num_running'] = 0
    value['num_pending'] = 0
    value['num_delete'] = 0
    value['num_backtest_complete'] = 0
    value['num_creating_final_backtest'] = 0
    value['num_optimization_complete'] = 0
    value['num_delete'] = 0

    if result is not None:
        for row in result:
            if "num_"+row['status'] not in value:
                value["num_" + row['status']] = 0
            value["num_" + row['status']] += row['num_rows']
            value['num_walk_forward_test'] += row['num_rows']

    return value


def UpdateWalkForwardTestStatus(walkForwardTestId, status, errorMsg=""):
    try:
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            sql = "UPDATE `walk_forward_test` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, errorMsg, walkForwardTestId))
            connection.commit()

            if status == "running":
                UpdateBacktestStartTime(walkForwardTestId, 'walk_forward_test')

            elif status=="optimization_complete":
                UpdateBacktestEndTime(walkForwardTestId, 'walk_forward_test')

            elif status == "completed":
                pass

            elif status=="error":
                pass

        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)


def GetWalkForwardTest(status="running"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            if status=="all":
                sql = "SELECT * FROM `walk_forward_Test` ORDER BY `created_time` DESC"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM `walk_forward_Test` WHERE `status`=%s  ORDER BY `created_time` DESC"
                cursor.execute(sql, (status))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value.append(row)

        return value

    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)

def GetWalkForwardTestWithPagination(pageSize, pageNo):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `walk_forward_test` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            value = get_walk_forward_test_status_summary(result)
            value['page_size'] = pageSize
            value['page_no'] = pageNo
            value['num_pages'] = int(math.ceil(value['num_walk_forward_test'] / pageSize))

            value['walk_forward_test'] = []

            sql = "SELECT * FROM `walk_forward_test` ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, ((pageNo-1)*pageSize, pageSize))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = MySQLTimeToString(row['backtest_start_time'])
                    row['backtest_end_time'] = MySQLTimeToString(row['backtest_end_time'])
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['walk_forward_test'].append(row)

        return value
    except:
        print(traceback.print_exc())
    finally:
        DisconnectToMySQL(connection)

# endregion

############################################################################

# region Strategy related
def ReformatTimestrInStrategy(strategyRecord):
    if strategyRecord['created_time'] is None:
        strategyRecord['created_time'] = "0000-00-00 00:00:00"
    else:
        strategyRecord['created_time'] = strategyRecord['created_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategyRecord['modified_time'] is None:
        strategyRecord['modified_time'] = "0000-00-00 00:00:00"
    else:
        strategyRecord['modified_time'] = strategyRecord['modified_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategyRecord['last_handshake_time'] is None:
        strategyRecord['last_handshake_time'] = "0000-00-00 00:00:00"
    else:
        strategyRecord['last_handshake_time'] = strategyRecord['last_handshake_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategyRecord['online_time'] is None:
        strategyRecord['online_time'] = "0000-00-00 00:00:00"
    else:
        strategyRecord['online_time'] = strategyRecord['online_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategyRecord['offline_time'] is None:
        strategyRecord['offline_time'] = "0000-00-00 00:00:00"
    else:
        strategyRecord['offline_time'] = strategyRecord['offline_time'].strftime('%Y-%m-%d %H:%M:%S')

    return strategyRecord


############################################################################

# region Create method
def AddStrategy(data):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "INSERT INTO `strategy` (`name`, `slug`, `filename`, `class_name`, `data_ticker`, `trade_ticker`, `data_resolution`, `contract`, `exchange`, `sec_type`, `action`, `base_qty`, `parameter`, `description`, `version`, `parent_id`, `status`, `created_time`, `modified_time`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
            cursor.execute(sql, (data['name'], data['slug'], data['filename'], data['class_name'], data['data_ticker'], data['trade_ticker'], data['data_resolution'], data['contract'], data['exchange'], data['sec_type'], data['action'], data['base_qty'], data['parameter'], data['description'], data['version'], data['parent_id'], data['status']))
            connection.commit()
            result = cursor.fetchone()

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion

############################################################################

# region Update method
def UpdateStrategy(data):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `strategy` SET `name`=%s, `slug`=%s, `filename`=%s, `class_name`=%s, `data_ticker`=%s, `trade_ticker`=%s, `data_resolution`=%s, `contract`=%s, `exchange`=%s, `sec_type`=%s, `action`=%s, `base_qty`=%s, `parameter`=%s, `description`=%s, `version`=%s, `parent_id`=%s, `status`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (data['name'], data['slug'], data['filename'], data['class_name'], data['data_ticker'], data['trade_ticker'], data['data_resolution'], data['contract'], data['exchange'], data['sec_type'], data['action'], data['base_qty'], data['parameter'], data['description'], data['version'], data['parent_id'], data['status'], data['strategy_id']))
            connection.commit()
            result = cursor.fetchone()

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion

############################################################################

# region Delete method
def Deletestrategy(strategyId):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `strategy` SET `status`='delete' WHERE `id`=%s"
            cursor.execute(sql, (strategyId))
            connection.commit()
            result = cursor.fetchone()

        return True

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion

############################################################################

# region Get method
def GetStrategy(status=None, strategyId=None, parentId=None):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            if status is None and strategyId is None and parentId is not None:
                # search by parent_id
                if parent_id == -1:
                    parent_id = ""
                sql = "SELECT * FROM `strategy` WHERE `parent_id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (parentId))
            elif status is None and parent_id is None and strategyId is not None:
                # search by strategyId
                sql = "SELECT * FROM `strategy` WHERE `id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (strategyId))
            elif strategyId is None and parent_id is None and status is not None:
                # search by status
                sql = "SELECT * FROM `strategy` WHERE `status`=%s ORDER BY `created_time`"
                cursor.execute(sql, (status))
            else:
                sql = "SELECT * FROM `strategy` WHERE NOT `status`='delete' ORDER BY `created_time`"
                cursor.execute(sql)

            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    value.append(reformat_timestr_in_strategy(row))

        return value

    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)


def GetStrategyById(strategyId):
    try:
        connection = ConnectToMySQL()
        value = {}

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `id`=%s ORDER BY `id` ASC"
            cursor.execute(sql, (strategyId))

            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    value = reformat_timestr_in_strategy(row)

        return value
    except e:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetStrategyTo_dailyBacktest(status=None):
    try:
        connection = ConnectToMySQL()
        value = []
        online = "online"
        offline = "offline"

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `status`=%s or `status`=%s ORDER BY `id` ASC"
            cursor.execute(sql, (online, offline))

            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            if result is not None:
                for row in result:
                    value.append(reformat_timestr_in_strategy(row))

        return value
    except e:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetAvailableStrategyEquity(status, date):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `status`=%s ORDER BY `created_time`"
            cursor.execute(sql, (status))

            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')

                    sql = "SELECT * FROM `strategy_equity` WHERE `strategy_id`=%s AND `equity_type`=%s AND `date`=%s ORDER BY `date` ASC"
                    if status == "online":
                        cursor.execute(sql, (row['id'], "live", date))
                    elif status == "offline":
                        cursor.execute(sql, (row['id'], "backtest", date))

                    connection.commit()
                    equity_result = cursor.fetchall()

                    for equity_row in equity_result:
                        equity_row['created_time'] = equity_row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                        equity_row['modified_time'] = equity_row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')
                        row["equity"] = equity_row
                value.append(row)

        return value
    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)


def GetSingleStrategyEquity(strategyId):
    try:
        connection = ConnectToMySQL()
        value = {}

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy_equity` WHERE `strategy_id`=%s ORDER BY `date` ASC"
            cursor.execute(sql, (strategyId))

            connection.commit()
            result = cursor.fetchall()

            liveEquity = []
            backtestEquity = []

            if result is not None:
                for row in result:

                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')

                    if row['equity_type'] == "live":
                        liveEquity.append(row)
                    else:
                        backtestEquity.append(row)

            value['live_equity'] = liveEquity
            value['backtest_equity'] = backtestEquity

        return value

    except:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)


def GetNextStrategyToOnline(exchange):
    try:
        connection = ConnectToMySQL()
        value = {}

        with connection.cursor() as cursor:
            status = "online"
            ws_status = "offline"
            sql = "SELECT * FROM `strategy` WHERE `exchange`=%s AND `status`=%s AND `ws_status`=%s ORDER BY `id` ASC LIMIT 1"
            cursor.execute(sql, (exchange, status, ws_status))

            connection.commit()
            result = cursor.fetchall()

            strategies = []

            if result is not None:
                for row in result:
                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')
                    if row['last_handshake_time'] is None:
                        row['last_handshake_time'] = "0000-00-00 00:00:00"
                    else:
                        row['last_handshake_time'] = row['last_handshake_time'].strftime('%Y-%m-%d %H:%M:%S')


                    if row['online_time'] is None:
                        row['online_time'] = "0000-00-00 00:00:00"
                    else:
                        row['online_time'] = row['online_time'].strftime('%Y-%m-%d %H:%M:%S')


                    if row['offline_time'] is None:
                        row['offline_time'] = "0000-00-00 00:00:00"
                    else:
                        row['offline_time'] = row['offline_time'].strftime('%Y-%m-%d %H:%M:%S')


                    strategies.append(row)
            value['strategy'] = strategies

        return value
    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)

# endregion
# endregion

############################################################################

# region Filter test

# region Create method
def AddFilterTest(filterClass, backtestName, remark=""):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "INSERT INTO `filter_test` (`filter_class`, `backtest_name`, `status`, `remark`, `created_time`, `modified_time`) VALUES (%s,%s,%s,%s,NOW(),NOW())"
            cursor.execute(sql, (filterClass, backtestName, "pending", remark))
            connection.commit()
            result = cursor.fetchone()

            return cursor.lastrowid

    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion


# region Update method
def UpdateFilterTestStatus(filterTestId, status, errorMsg=""):
        try:
            connection = ConnectToMySQL()
            value = []

            with connection.cursor() as cursor:
                sql = "UPDATE `filter_test` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
                cursor.execute(sql, (status, errorMsg, filterTestId))
                connection.commit()

            return True

        except:
            traceback.print_exc()
            return False

        finally:
            DisconnectToMySQL(connection)


# endregion


# region Get method
def GetFilterTest(status="running"):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            if status=="all":
                sql = "SELECT * FROM `filter_test` ORDER BY `id` DESC, `created_time` DESC"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM `filter_test` WHERE `status`=%s  ORDER BY `id` DESC, `created_time` DESC"
                cursor.execute(sql, (status))
            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value.append(row)

        return value

    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)


def GetFilterTestWithPagination(pageSize, pageNo):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `filter_test` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()

            value = {}
            value['num_filter_test'] = 0
            value['num_complete'] = 0
            value['num_error'] = 0
            value['num_running'] = 0
            value['num_pending'] = 0
            value['num_delete'] = 0
            value['num_completed'] = 0

            value['filter_test'] = []

            if result is not None:
                for row in result:
                    if "num_"+row['status'] not in value:
                        value["num_"+row['status']] = 0
                    value["num_"+row['status']] += row['num_rows']
                    value['num_filter_test'] += row['num_rows']

            value['page_size'] = pageSize
            value['page_no'] = pageNo
            value['num_pages'] = int(math.ceil(value['num_filter_test'] / pageSize))

            sql = "SELECT * FROM `filter_test` ORDER BY `created_time` DESC LIMIT %s, %s"
            cursor.execute(sql, ((pageNo-1)*pageSize, pageSize))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    value['filter_test'].append(row)

        return value
    except:
        print(traceback.print_exc())
        return []

    finally:
        DisconnectToMySQL(connection)

# endregion

# endregion

############################################################################

# region Service related
def GetServer():
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `services` ORDER BY `id` ASC"
            cursor.execute(sql)

            connection.commit()
            result = cursor.fetchall()

            if result is not None:
                for row in result:
                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')
                    value.append(row)

        return value
    except:
        print(traceback.print_exc())
        return []

    finally:
        DisconnectToMySQL(connection)
# endregion

############################################################################

# region Live Order related

# region Add method
def AddOrder(order, tradeType="backtest"):
    try:
        connection = ConnectToMySQL()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `trade_orders` ( `oid`, `sid`, `client_id`, `trade_type`," \
                                                "`exchange`, `ticker`, `contract`, `action`," \
                                                " `qty`, `order_type`, `trigger_price`, `label`, " \
                                                "`account`, `status`, `adjusted_date`, `adjusted_time`, " \
                                                "`created_time`, `modified_time`) " \
                                                "VALUES (%s,%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "NOW(), NOW())"

            order['trade_type'] = tradeType
            cursor.execute(sql, (order['oid'], order['sid'], order['clientId'], order['tradeType'],
                                 order['exchange'],order['ticker'],order['contract'], order['action'],
                                 order['qty'], order['orderType'],order['triggerPrice'],order['label'],
                                 order['account'], order['status'], order['adjustedDate'],order['adjustedTime']))
            connection.commit()
            result = cursor.fetchone()

            filterTestId = cursor.lastrowid
            return filterTestId
    except:
        traceback.print_exc()
        return NOT_SET

    finally:
        DisconnectToMySQL(connection)

# endregion


# region Get method
def GetLiveOrderByDate(date_str):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `live_orders` WHERE `adjusted_date`=%s ORDER BY `oid` DESC"
            cursor.execute(sql, (date_str))
            connection.commit()
            result = cursor.fetchall()
            isDBError = False

            if result is not None:
                for row in result:
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    row['filled_time'] = MySQLTimeToString(row['filled_time'])
                    value.append(row)

        return value

    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)

def GetOrderById(oid, permId):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `trade_orders` WHERE `oid`=%s AND `perm_id`=%s LIMIT 1"
            cursor.execute(sql, (oid, permId))
            connection.commit()
            result = cursor.fetchall()


            if result is not None:
                for row in result:
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    row['filled_time'] = MySQLTimeToString(row['filled_time'])
                    value.append(row)

        return value

    except:
        traceback.print_exc()
        return []

    finally:
        DisconnectToMySQL(connection)


# endregion


# region Update method
def UpdateLiveOrderStatus(orderId, sid, status):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `status`=%s, `modified_time`=NOW() WHERE `oid`=%s AND `sid`=%s"
            cursor.execute(sql, (status, orderId, sid))
            connection.commit()

        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

def UpdateLiveOrderColumn(orderId, sid, column, value):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `"+column+"`=%s, `modified_time`=NOW() WHERE `oid`=%s AND `sid`=%s"
            cursor.execute(sql, (value, orderId, sid))
            connection.commit()

        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

def UpdateOrderCommission(orderId, commission):
    try:
        connection = ConnectToMySQL()

        with connection.cursor() as cursor:
            sql = "UPDATE `trade_orders` SET `commission`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (commission, orderId))
            connection.commit()
        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

'''
#if no problem will remove this
def UpdateLiveOrderWithOrderStatus(orderId, permId, status):
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `status`=%s, `perm_id`=%s, `modified_time`=NOW() WHERE `oid`=%s"
            cursor.execute(sql, (status, perm_id, order_id))
            connection.commit()

        return value

    except:
        traceback.print_exc()
        return []
    finally:
        DisconnectToMySQL(connection)
'''
#old update_live_order_from_open_order
'''
def update_live_order_from_open_order(order_id, perm_id, status):
    try:
        isDBError = True
        isSuccess = True
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `status`=%s, `perm_id`=%s, `modified_time`=NOW() WHERE `oid`=%s"
            cursor.execute(sql, (status, perm_id, order_id))
            connection.commit()
            isDBError = False

        if isDBError:
            isSuccess = False

    except:
        traceback.print_exc()
        isSuccess = False

    finally:
        DisconnectToMySQL(connection)

        if isSuccess:
            return "success", "update live order status success"
        else:
            return "fail", "error found update live order status"
'''



#def UpdateOrderWithOrderStatus(orderId, permId, status, filled, avgFillPrice):
def UpdateOrderWithOrderStatus(orderStatus):
    try:
        connection = ConnectToMySQL()
        value = []
        #db.data['order_id'], data['perm_id'], data['status'], data['filled'], data['avg_fill_price'])

        with connection.cursor() as cursor:
            orderId = orderStatus['order_id']
            permId = orderStatus['perm_id']
            status = orderStatus['status']

            if status =="Filled":
                orders = GetOrderById(orderId, permId)

                if len(orders) > 0:
                    order = orders[0]

                    #Skip update order status if order already filled
                    if order['status'] == "Filled":
                        return False

                    filled = orderStatus['filled']
                    avgFillPrice = orderStatus['avg_fill_price']

                    if order['action'] == "BUY":
                        slippage = avgFillPrice - order['trigger_price']
                    else:
                        slippage = order['trigger_price'] - avgFillPrice

                    print("Update Order:", orderId, slippage)
                    sql = "UPDATE `trade_orders` SET `perm_id`=%s, `status`=%s, `filled_qty`=%s, `filled_price`=%s, `slippage`=%s, `modified_time`=NOW(), `filled_time`=NOW() WHERE `oid`=%s"
                    cursor.execute(sql, (permId, status, filled, avgFillPrice, slippage, orderId))
                    connection.commit()

                    UpdatePositionFromFilledOrder(orderStatus)

            else:
                sql = "UPDATE `trade_orders` SET `perm_id`=%s, `status`=%s, `modified_time`=NOW() WHERE `oid`=%s"
                cursor.execute(sql, (permId, status, orderId))
                connection.commit()

        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)
# endregion

# endregion



# region Position related
# region Add method
#def UpdatePositionFromFilledOrder(orderId, permId, status):
def UpdatePositionFromFilledOrder(orderStatus):
    status = orderStatus['status']
    if status != "Filled": return
    try:
        connection = ConnectToMySQL()
        value = []

        with connection.cursor() as cursor:
            # 1 Selected order with same permId and orderId
            # 2 Select position
            # 3 Create a new position if no position exist else update it

            # 1 Selected order with same permId and orderId
            orderId = orderStatus['order_id']
            permId = orderStatus['perm_id']
            orders = GetOrderById(orderId, permId)
            if len(orders)==0: return False

            #1 Check with position table which has created position
            order = orders[0]
            sql = "SELECT * FROM `trade_positions` WHERE `sid`=%s AND `entry_date`=%s LIMIT 1"
            cursor.execute(sql, (order['sid'], order['adjusted_date']))
            connection.commit()
            result = cursor.fetchall()

            positions = []
            if result is not None:
                for row in result:
                    row['created_time'] = MySQLTimeToString(row['created_time'])
                    row['modified_time'] = MySQLTimeToString(row['modified_time'])
                    positions.append(row)

            if len(positions)==0:
                #Condition: No position created today
                #Action: Create a new position with filled order
                status = "Open"

                sql = "INSERT INTO `trade_positions` (`sid`, `account`, `client_id`, `trade_type`, `exchange`, " \
                                                        "`ticker`, `contract`, `action`, `entry_oid`, `entry_date`, " \
                                                        "`entry_time`, `entry_label`, `entry_price`, `entry_qty`, `qty`, " \
                                                        "`commission`, `slippage`, `status`, `created_time`, `modified_time`)" \
                                                        " VALUES( %s, %s, %s, %s, %s," \
                                                                " %s, %s, %s, %s, %s," \
                                                                " %s, %s, %s, %s, %s," \
                                                                " %s, %s, %s, Now(),Now())"
                cursor.execute(sql, (order['sid'], order['account'], order['client_id'], order['trade_type'], order['exchange'],
                                     order['ticker'], order['contract'], order['action'], order['oid'], order['adjusted_date'],
                                     order['adjusted_time'], order['label'], order['filled_price'], order['qty'], order['qty'],
                                     order['commission'], order['slippage'], status))
                connection.commit()
                result = cursor.fetchone()
                pass

            else:
                # Condition: Today position created
                # Action: Update it
                status = "Closed"
                position = positions[0]

                # Do not update if status is closed
                if position['status'] == status:
                    return False

                slippage = int(order['slippage']) + int(position['slippage'])
                commission = int(position['commission']) + int(order['commission'])

                if position['action'] == 'BUY':
                    pnl = int(order['filled_price']) - int(position['entry_price'])
                else:
                    pnl = int(position['entry_price']) - int(order['filled_price'])
                pnl *= static.CONTRACT_MULTIPLY[position['ticker']]
                pnl -= commission

                result = "LOSS"
                if pnl > 0:
                    result = "WIN"

                sql = "UPDATE `trade_positions` SET `exit_oid`=%s, `exit_date`=%s, `exit_time`=%s, `exit_label`=%s, " \
                                                "`exit_price`=%s, `exit_qty`=%s, `commission`=%s, `pnl`=%s, " \
                                                "`result`=%s, `slippage`=%s, `status`=%s, " \
                                                "`modified_time`=NOW() WHERE `id`=%s"

                cursor.execute(sql, (order['oid'], order['adjusted_date'], order['adjusted_time'], order['label'],
                                     order['filled_price'], order['qty'], commission, pnl,
                                     result, slippage, status,
                                     position['id']))

                connection.commit()

        return True
    except:
        traceback.print_exc()
        return False

    finally:
        DisconnectToMySQL(connection)

# endregion

# endregion
############################################################################




