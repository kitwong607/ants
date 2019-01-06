import pymysql.cursors, json, traceback, datetime, sys, itertools, math, copy
from ants import utilities


# region DB connect function
def connect_to_mysql():
    connection = pymysql.connect(host='localhost',
                                 user='ants_admin',
                                 password='SlamDunk21',
                                 db='ants',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def disconnect_to_mysql(connection):
    connection.close()
# endregion


# region Data format convert
def mysql_time_to_string(dt):
    if dt is None:
        return "0000-00-00 00:00:00"
    return dt.strftime('%Y-%m-%d %H:%M:%S')
# endregion


# region Option related
# moved to php
def get_option(option_key, return_value_only=False):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()

        with connection.cursor() as cursor:

            sql = "SELECT * FROM `sys_option` WHERE `option_key`=%s LIMIT 1"
            cursor.execute(sql, (option_key))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False
            if result is None:
                value = "not_set"
            else:
                value = result['option_value']

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            if return_value_only:
                return value
            else:
                return "success", "option updated", value
        else:
            if return_value_only:
                return "fail"
            else:
                return "fail", "error found on option update.", value

def update_option(option_key, option_value):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()

        with connection.cursor() as cursor:

            sql = "SELECT * FROM `sys_option` WHERE `option_key`=%s"
            cursor.execute(sql, (option_key))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False
            if result is None:
                sql = "INSERT INTO `sys_option` (`option_key`, `option_value`) VALUES(%s, %s)"
                cursor.execute(sql, (option_key,option_value))
                connection.commit()
                result = cursor.fetchone()
            else:
                sql = "UPDATE `sys_option` SET `option_value`=%s WHERE `option_key`=%s"
                cursor.execute(sql, (option_value, option_key))
                connection.commit()
                result = cursor.fetchone()

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "option updated"
        else:
            return "fail", "error found on option update."
# endregion


# region Backtest related
# region Get Method
def get_final_backtest_by_walk_forward_test(walk_forward_test_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `backtest_report` WHERE `walk_forward_test_id`=%s AND `is_final_walk_forward_backtest`=%s ORDER BY `start_date` ASC"
            cursor.execute(sql, (walk_forward_test_id, 'yes'))
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest by optimization_id success", value
        else:
            return "fail", "error found on get backtest by optimization_id.", "not_set"


def get_backtest_by_optimization_id(optimization_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `backtest_report` WHERE `optimization_id`=%s  ORDER BY `created_time`, `id`"
            cursor.execute(sql, (optimization_id))
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest by optimization_id success", value
        else:
            return "fail", "error found on get backtest by optimization_id.", "not_set"


def get_backtest_by_id(backtest_id, table="backtest_report"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `"+table+"` WHERE `id`=%s  LIMIT 1"
            cursor.execute(sql, (backtest_id))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest", result
        else:
            return "fail", "error found on get backtest.", "not_set"


def get_backtest(status="running"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
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
            is_db_error = False

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])

                    value.append(row)


        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest", value
        else:
            return "fail", "error found on get backtest.", "not_set"

def get_backtest_status_summary(result):
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

def get_backtest_with_pagination(page_size, page_no):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            value = get_backtest_status_summary(result)
            value['page_size'] = page_size
            value['page_no'] = page_no
            value['num_pages'] = int(math.ceil(value['num_backtest'] / page_size))

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, ((page_no - 1) * page_size, page_size))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['backtest'].append(row)

        if is_db_error:
            is_success = False
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest with pagination", value
        else:
            return "fail", "error found on get backtest with pagination", "not_set"

def get_backtest_with_optimization_id(optimization_id, page_size, page_no):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id` = %s GROUP BY `status`"
            cursor.execute(sql, (optimization_id))
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            value = get_backtest_status_summary(result)
            value['page_size'] = page_size
            value['page_no'] = page_no
            value['num_pages'] = int(math.ceil(value['num_backtest'] / page_size))

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` WHERE `optimization_id` = %s ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, (optimization_id, (page_no - 1) * page_size, page_size))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['backtest'].append(row)

        if is_db_error:
            is_success = False
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest with optimization id", value
        else:
            return "fail", "error found on get backtest  with optimization id", "not_set"

def get_backtest_with_walk_forward_test_id(walk_forward_test_id):
    try:
        yes = "yes"
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `walk_forward_test_id` = %s AND `is_final_walk_forward_backtest`=%s GROUP BY `status`"
            cursor.execute(sql, (walk_forward_test_id, yes))
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            value = get_backtest_status_summary(result)

            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` WHERE `walk_forward_test_id` = %s AND `is_final_walk_forward_backtest`=%s ORDER BY `id`"
            cursor.execute(sql, (walk_forward_test_id, yes))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['backtest'].append(row)

        if is_db_error:
            is_success = False
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest with walk forward test id", value
        else:
            return "fail", "error found on get backtest with walk forward test id", "not_set"
# endregion


# region Update method
def update_backtest_report(config):
    try:
        with open(config.report_directory + '\\backtest_summary.json') as json_data:
            d = json.load(json_data)
            d['report_folder_name'] = config.report_folder_name
            d['report_full_path'] = config.report_directory

            is_db_error = True
            is_success = True
            connection = connect_to_mysql()
            value = []

            d = utilities.prepare_backtest_report_insert_to_db(d)

            with connection.cursor() as cursor:
                sql = "UPDATE `backtest_report` SET `win_rate`=%s, `num_trade`=%s, `pnl`=%s, `net_pips`=%s, `profit_factor`=%s, `payoff_ratio`=%s, `roci`=%s, `sharpe_ratio`=%s, `standard_deviation`=%s, `standard_error`=%s, `tharp_expectancy`=%s, `expectancy`=%s, `mdd`=%s, `mdd_pct`=%s, `mdd_daily`=%s, `mdd_pct_daily`=%s, `dd_duration`=%s, `dd_duration_daily`=%s, `avg_pips_pre_contract`=%s, `report_folder_name`=%s, `report_full_path`=%s, `modified_time`=NOW() WHERE `id`=%s"
                cursor.execute(sql, (d['win_rate'], d['num_trade'], d['pnl'], d['net_pips'], d['profit_factor'], d['payoff_ratio'], d['roci'],
                                     d['sharpe_ratio'], d['standard_deviation'], d['standard_error'], d['tharp_expectancy'], d['expectancy'],
                                     d['mdd'], d['mdd_pct'], d['mdd_daily'], d['mdd_pct_daily'], d['dd_duration'],
                                     d['dd_duration_daily'], d['avg_pips_pre_contract'], d['report_folder_name'], d['report_full_path'], config.session_id))

                connection.commit()

            if is_db_error:
                is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update backtest start time success"
        else:
            return "fail", "error found update backtest start time"


def update_backtest_start_time(backtest_id, table="backtest_report"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `"+table+"` SET `backtest_start_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (backtest_id))
            connection.commit()

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update backtest start time success"
        else:
            return "fail", "error found update backtest start time"


def update_backtest_end_time(backtest_id, table="backtest_report"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `"+table+"` SET `backtest_end_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (backtest_id))
            connection.commit()

            result, message, backtest = get_backtest_by_id(backtest_id, table)

            if (backtest is not None) and (result == "success"):
                sec_diff = (backtest['backtest_end_time'] - backtest['backtest_start_time']).total_seconds()
                sec_diff = str(datetime.timedelta(seconds=int(sec_diff)))

                sql = "UPDATE `" + table + "` SET `backtest_used_time`=%s WHERE `id`=%s"
                cursor.execute(sql, (sec_diff, backtest_id))
                connection.commit()

            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update backtest end time success"
        else:
            return "fail", "error found update backtest end time"



def update_backtest_status(backtest_id, status, error_msg=""):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            result, message, backtest = get_backtest_by_id(backtest_id)
            if (backtest is not None) and (result == "success"):
                optimization_id = backtest['optimization_id']


            sql = "UPDATE `backtest_report` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, error_msg, backtest_id))
            connection.commit()
            is_db_error = False
            if status == "running":
                update_backtest_start_time(backtest_id)

                if optimization_id != 0:
                    sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id`=%s GROUP BY `status`"
                    cursor.execute(sql, (optimization_id))
                    connection.commit()

                    result = cursor.fetchall()
                    value = get_backtest_status_summary(result)
                    if value['num_backtest'] == value['num_running'] + value['num_pending'] and value['num_running']==1:
                        update_optimization_status(optimization_id, "running")



            elif status == "completed":
                update_backtest_end_time(backtest_id)

                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                backtest = cursor.fetchone()
                is_db_error = False

                if backtest is not None:
                    #check current backtest is a optimization
                    if optimization_id != 0:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (optimization_id))
                        connection.commit()

                        result = cursor.fetchall()
                        value = get_backtest_status_summary(result)

                        if value['num_backtest'] == value['num_completed']:
                            update_optimization_status(optimization_id, "backtest_complete")

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
                            update_walk_forward_test_status(backtest['walk_forward_test_id'], 'backtest_complete')


                else:
                    print("result is none")

            elif status=="error":
                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                result = cursor.fetchone()
                is_db_error = False

                if optimization_id != 0:
                    update_optimization_status(optimization_id, "error")

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update backtest status success"
        else:
            return "fail", "error found update backtest status"
# endregion


# region Create method
def add_backtest(data):
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    strategy_class = utilities.get_class_from_name('ants.strategy.'+data['strategy'], data['strategy'])
    data["strategy_name"] = strategy_class.STRATEGY_NAME
    data["strategy_slug"] = strategy_class.STRATEGY_SLUG
    data["last_update"] = strategy_class.VERSION
    data["version"] = strategy_class.LAST_UPDATE_DATE

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

        sql = "INSERT INTO `backtest_report` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategy_class`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `strategy_parameter`, `optimization_id`, `walk_forward_test_id`,`is_final_walk_forward_backtest`,`remark`,`created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
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
        is_db_error = False

        if is_db_error:
            is_success = False
        if is_success:
            return "success", "add backtest success"
        else:
            return "fail", "error found on add backtest"

def create_backtest_job_from_optimization():
    return
    result, description, jobs = get_optimization("pending")


    if len(jobs) == 0 or jobs is None or jobs == "not_set":
        return None
    else:
        for job in jobs:
            strategy_parameter_str = job['strategy_parameter']
            strategy_parameter = json.loads(strategy_parameter_str)
            strategy_class = utilities.get_class_from_name('ants.strategy.' + job['strategy_class'], job['strategy_class'])
            optimization_parameter = strategy_class.OPTIMIZATION_PARAMETER

            keys = []
            values = []
            for key, parameter in optimization_parameter.items():
                print(parameter)
                keys.append(key)
                value = []
                if key in strategy_parameter:
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

                result, msg = add_backtest(data)
# endregion


# endregion


# region Optimization related
# region Get method
def get_optimization_with_walk_forward_test_id(walk_forward_test_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
            cursor.execute(sql, walk_forward_test_id)
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

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
            cursor.execute(sql, walk_forward_test_id)
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['optimization'].append(row)

        if is_db_error:
            is_success = False
        print(value)
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization with pagination", value
        else:
            return "fail", "error found on get optimization with pagination", "not_set"


def get_optimization_with_pagination(page_size, page_no):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

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

            value['page_size'] = page_size
            value['page_no'] = page_no
            value['num_pages'] = int(math.ceil(value['num_optimization'] / page_size))

            sql = "SELECT * FROM `optimization` ORDER BY `id` DESC, `created_time` DESC LIMIT %s, %s"
            cursor.execute(sql, ((page_no-1)*page_size, page_size))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['optimization'].append(row)

        if is_db_error:
            is_success = False
        print(value)
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization with pagination", value
        else:
            return "fail", "error found on get optimization with pagination", "not_set"


def get_optimization_by_id(optimization_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()

        with connection.cursor() as cursor:
            #1 if have running multi process -> skip
            #2 if working single process == max workers -> skip
            #3 find pending backtest
            sql = "SELECT * FROM `optimization` WHERE `id`=%s  ORDER BY `created_time` DESC"
            cursor.execute(sql, (optimization_id))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False

            if result is not None:
                result['backtest_start_time'] = mysql_time_to_string(result['backtest_start_time'])
                result['backtest_end_time'] = mysql_time_to_string(result['backtest_end_time'])
                result['created_time'] = mysql_time_to_string(result['created_time'])
                result['modified_time'] = mysql_time_to_string(result['modified_time'])


        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization", result
        else:
            return "fail", "error found on get optimization.", "not_set"


def get_optimization(status="running"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
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
            is_db_error = False

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization", value
        else:
            return "fail", "error found on get optimization.", "not_set"


def get_optimization_status_summary(result):
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
def update_optimization(optimization_id:int, optimization_summary, first_backtest_report):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `optimization` SET `report_full_path`=%s, `report_folder_name`=%s, `num_trade`=%s, `num_trade_std`=%s, `num_trade_std_pct`=%s, `win_rate`=%s, `win_rate_std`=%s, `win_rate_std_pct`=%s, `pnl`=%s, `pnl_std`=%s, `pnl_std_pct`=%s, `net_pips`=%s, `net_pips_std`=%s, `net_pips_std_pct`=%s, `avg_pips_pre_contract`=%s, `avg_pips_pre_contract_std`=%s, `avg_pips_pre_contract_std_pct`=%s, `profit_factor`=%s, `profit_factor_std`=%s, `profit_factor_std_pct`=%s, `payoff_ratio`=%s, `payoff_ratio_std`=%s, `payoff_ratio_std_pct`=%s, `roci`=%s, `roci_std`=%s, `roci_std_pct`=%s, `sharpe_ratio`=%s, `sharpe_ratio_std`=%s, `sharpe_ratio_std_pct`=%s, `tharp_expectancy`=%s, `tharp_expectancy_std`=%s, `tharp_expectancy_std_pct`=%s, `expectancy`=%s, `expectancy_std`=%s, `expectancy_std_pct`=%s, `mdd`=%s, `mdd_std`=%s, `mdd_std_pct`=%s, `mdd_pct`=%s, `mdd_pct_std`=%s, `mdd_pct_std_pct`=%s, `mdd_daily`=%s, `mdd_daily_std`=%s, `mdd_daily_std_pct`=%s, `mdd_pct_daily`=%s, `mdd_pct_daily_std`=%s, `mdd_pct_daily_std_pct`=%s, `dd_duration`=%s, `dd_duration_std`=%s, `dd_duration_std_pct`=%s, `dd_duration_daily`=%s, `dd_duration_daily_std`=%s, `dd_duration_daily_std_pct`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (   first_backtest_report['performance']['report_full_path'],
                                    first_backtest_report['performance']['report_folder_name'],
                                    "{0:.8f}".format(float(optimization_summary['num_trade'])),
                                    "{0:.8f}".format(float(optimization_summary['num_trade_std'])),
                                    "{0:.8f}".format(float(optimization_summary['num_trade_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['win_rate'])),
                                    "{0:.8f}".format(float(optimization_summary['win_rate_std'])),
                                    "{0:.8f}".format(float(optimization_summary['win_rate_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['pnl'])),
                                    "{0:.8f}".format(float(optimization_summary['pnl_std'])),
                                    "{0:.8f}".format(float(optimization_summary['pnl_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['net_pips'])),
                                    "{0:.8f}".format(float(optimization_summary['net_pips_std'])),
                                    "{0:.8f}".format(float(optimization_summary['net_pips_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['avg_pips_pre_contract'])),
                                    "{0:.8f}".format(float(optimization_summary['avg_pips_pre_contract_std'])),
                                    "{0:.8f}".format(float(optimization_summary['avg_pips_pre_contract_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['profit_factor'])),
                                    "{0:.8f}".format(float(optimization_summary['profit_factor_std'])),
                                    "{0:.8f}".format(float(optimization_summary['profit_factor_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['payoff_ratio'])),
                                    "{0:.8f}".format(float(optimization_summary['payoff_ratio_std'])),
                                    "{0:.8f}".format(float(optimization_summary['payoff_ratio_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['roci'])),
                                    "{0:.8f}".format(float(optimization_summary['roci_std'])),
                                    "{0:.8f}".format(float(optimization_summary['roci_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['sharpe_ratio'])),
                                    "{0:.8f}".format(float(optimization_summary['sharpe_ratio_std'])),
                                    "{0:.8f}".format(float(optimization_summary['sharpe_ratio_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['tharp_expectancy'])),
                                    "{0:.8f}".format(float(optimization_summary['tharp_expectancy_std'])),
                                    "{0:.8f}".format(float(optimization_summary['tharp_expectancy_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['expectancy'])),
                                    "{0:.8f}".format(float(optimization_summary['expectancy_std'])),
                                    "{0:.8f}".format(float(optimization_summary['expectancy_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_std'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct_std'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_daily'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_daily_std'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_daily_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct_daily'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct_daily_std'])),
                                    "{0:.8f}".format(float(optimization_summary['mdd_pct_daily_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration_std'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration_std_pct'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration_daily'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration_daily_std'])),
                                    "{0:.8f}".format(float(optimization_summary['dd_duration_daily_std_pct'])),
                                    optimization_id))
            connection.commit()


            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update optimization status success"
        else:
            return "fail", "error found update optimization status"


def update_optimization_status(optimization_id, status, error_msg=""):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `optimization` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, error_msg, optimization_id))
            connection.commit()

            if status == "running":
                update_backtest_start_time(optimization_id, 'optimization')

                result, message, optimization = get_backtest_by_id(optimization_id, 'optimization')
                if (optimization is not None) and (result == "success"):
                    walk_forward_test_id = optimization['walk_forward_test_id']

                    if walk_forward_test_id != 0 or walk_forward_test_id is not None:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (walk_forward_test_id))
                        connection.commit()


                        result = cursor.fetchall()
                        value = get_optimization_status_summary(result)
                        if value['num_optimization'] == value['num_running'] + value['num_pending'] and value['num_running']==1:
                            update_walk_forward_test_status(walk_forward_test_id, "running")


            elif status=="backtest_complete":
                update_backtest_end_time(optimization_id, 'optimization')

            elif status == "completed":
                walk_forward_test_id = 0
                result, message, optimization = get_optimization_by_id(optimization_id)

                if (optimization is not None) and (result == "success"):
                    walk_forward_test_id = optimization['walk_forward_test_id']

                if result is not None:
                    #check current optimization is a walk forward test
                    if walk_forward_test_id != 0:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `optimization` WHERE `walk_forward_test_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (walk_forward_test_id))
                        connection.commit()

                        result = cursor.fetchall()
                        value = get_optimization_status_summary(result)

                        if value['num_optimization'] == value['num_completed']:
                            update_walk_forward_test_status(walk_forward_test_id, "optimization_complete")
                else:
                    print("result is none")

            elif status=="error":
                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                result = cursor.fetchone()
                is_db_error = False

                if optimization_id != 0:
                    update_optimization_status(optimization_id, "error")


            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update optimization status success"
        else:
            return "fail", "error found update optimization status"
# endregion


# region Create method
def add_optimization(data, is_return_response = True):
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    strategy_class = utilities.get_class_from_name('ants.strategy.'+data['strategy'], data['strategy'])
    data["strategy_name"] = strategy_class.STRATEGY_NAME
    data["strategy_slug"] = strategy_class.STRATEGY_SLUG
    data["last_update"] = strategy_class.VERSION
    data["version"] = strategy_class.LAST_UPDATE_DATE

    # ToDo mark as filter backtest
    strategy_parameter = strategy_class.OPTIMIZATION_PARAMETER

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

        sql = "INSERT INTO `optimization` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategy_class`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `strategy_parameter`, `walk_forward_test_id`, `remark`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.execute(sql, (
        data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"],
        data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"],
        data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"],
        data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"],
        data["strategy_slug"], data["last_update"], data["version"], data["parameter"], data["walk_forward_test_id"], data["remark"]))

        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

        optimization_id = cursor.lastrowid
        optimize_parameter = json.loads(data['parameter'])

        strategy_parameter_combination = utilities.get_optimization_parameter_combination(strategy_parameter, optimize_parameter)
        #add backtest job here
        for parameter in strategy_parameter_combination:
            new_data = copy.deepcopy(data)
            new_data["backtest_mode"] = data["backtest_mode_no"]
            new_data["parameter"] = json.dumps(parameter)
            new_data["optimization_id"] = optimization_id
            add_backtest(new_data)

        if is_db_error:
            is_success = False
        if is_return_response:
            if is_success:
                return "success", "add optimization success"
            else:
                return "fail", "error found on add optimization"
        else:
            if is_success:
                return optimization_id
            else:
                return None

# endregion


# endregion


# region Walk forward test
def add_walk_forward_test(data):
    import copy
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    strategy_class = utilities.get_class_from_name('ants.strategy.'+data['strategy'], data['strategy'])
    data["strategy_name"] = strategy_class.STRATEGY_NAME
    data["strategy_slug"] = strategy_class.STRATEGY_SLUG
    data["last_update"] = strategy_class.VERSION
    data["version"] = strategy_class.LAST_UPDATE_DATE

    if "remark" not in data:
        data["remark"] = ""
    strategy_parameter = strategy_class.OPTIMIZATION_PARAMETER

    data["backtest_mode_no"] = int(data["backtest_mode"])

    #1 add walk forward test
    with connection.cursor() as cursor:
        sql = "INSERT INTO `walk_forward_test` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategy_class`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `remark`,  `walk_forward_test`, `no_of_month`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.execute(sql, (data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"], data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"], data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"], data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"], data["strategy_slug"], data["last_update"], data["version"], data["remark"], data["walk_forward_test"], data["no_of_month"]))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

        data['walk_forward_test_id'] = cursor.lastrowid


        #add optimization
        optimization_pair = strategy_class.OPTIMIZATION_PAIR
        optimization_parameter = strategy_class.OPTIMIZATION_PARAMETER
        optimization_pair_for_checking = list(itertools.chain.from_iterable(optimization_pair))

        all_parameter_exist_in_pair = True

        for key in optimization_parameter:
            if key not in optimization_pair_for_checking:
                all_parameter_exist_in_pair = False

        if not all_parameter_exist_in_pair:
            return "fail", "error found on add walk forward test, optimization pair and optimization parameter not match"

        data_start_date_dt = datetime.datetime.strptime(data['data_start_date'], "%Y-%m-%d").date()
        start_date_dt = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date_dt = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d").date()

        month_diff = abs(utilities.diff_month(data_start_date_dt, start_date_dt))
        total_no_of_month = abs(utilities.diff_month(start_date_dt, end_date_dt)) + 1

        optimization_id_batch = []

        for i in range(0, total_no_of_month):
            optimization_id_single_batch = []
            next_start_date_dt = utilities.add_months(start_date_dt, i)

            # for optimization
            new_start_date_dt = utilities.add_months(next_start_date_dt, int(data['no_of_month'])*-1)
            new_data_start_date_dt = utilities.add_months(new_start_date_dt, -month_diff)
            new_end_date_dt = utilities.add_months_with_last_date(new_start_date_dt, int(data['no_of_month']))

            new_backtest_start_date = next_start_date_dt
            new_backtest_data_start_date = utilities.add_months(new_backtest_start_date, -month_diff)
            new_backtest_end_date_dt = utilities.add_months_with_last_date(new_backtest_start_date, 1)

            for pair in optimization_pair:
                new_optimize_parameter = {}
                for key in pair:
                    new_optimize_parameter[key] = optimization_parameter[key]

                new_data = copy.deepcopy(data)
                new_data['data_start_date'] = new_data_start_date_dt.strftime("%Y-%m-%d")
                new_data['start_date'] = new_start_date_dt.strftime("%Y-%m-%d")
                new_data['end_date'] = new_end_date_dt.strftime("%Y-%m-%d")
                new_data['parameter'] = json.dumps(new_optimize_parameter)

                optimization_id = add_optimization(new_data, False)
                optimization_id_single_batch.append(optimization_id)
                # add optimization here
                print("add optimization:", optimization_id)
            optimization_id_batch.append(optimization_id_single_batch)

        optimization_id_batch = json.dumps(optimization_id_batch)

        print("optimization_id_batch", optimization_id_batch)
        print("optimization_id_batch", type(optimization_id_batch))
        print("data['walk_forward_test_id']", data['walk_forward_test_id'])

        sql = "UPDATE `walk_forward_test` SET `optimization_batch`=%s, `modified_time`=NOW() WHERE `id`=%s"
        cursor.execute(sql, (optimization_id_batch, data['walk_forward_test_id']))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False


        if is_db_error:
            is_success = False
        if is_success:
            return "success", "add walk forward test success"
        else:
            return "fail", "error found on add walk forward test"

def get_walk_forward_test_status_summary(result):
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

def update_walk_forward_test_status(walk_forward_test_id, status, error_msg=""):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()

        with connection.cursor() as cursor:
            sql = "UPDATE `walk_forward_test` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (status, error_msg, walk_forward_test_id))
            connection.commit()

            if status == "running":
                update_backtest_start_time(walk_forward_test_id, 'walk_forward_test')

            elif status=="optimization_complete":
                update_backtest_end_time(walk_forward_test_id, 'walk_forward_test')

            elif status == "completed":
                pass

            elif status=="error":
                pass

            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update walk forward test status success"
        else:
            return "fail", "error found update walk forward test status"


def get_walk_forward_test(status="running"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
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
            is_db_error = False

            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization", value
        else:
            return "fail", "error found on get optimization.", "not_set"

def get_walk_forward_test_with_pagination(page_size, page_no):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `walk_forward_test` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            value = get_walk_forward_test_status_summary(result)
            value['page_size'] = page_size
            value['page_no'] = page_no
            value['num_pages'] = int(math.ceil(value['num_walk_forward_test'] / page_size))

            value['walk_forward_test'] = []

            sql = "SELECT * FROM `walk_forward_test` ORDER BY `id` DESC LIMIT %s, %s"
            cursor.execute(sql, ((page_no-1)*page_size, page_size))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['backtest_start_time'] = mysql_time_to_string(row['backtest_start_time'])
                    row['backtest_end_time'] = mysql_time_to_string(row['backtest_end_time'])
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['walk_forward_test'].append(row)

        if is_db_error:
            is_success = False
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get walk forward test with pagination", value
        else:
            return "fail", "error found on get walk forward test with pagination", "not_set"

# endregion


# region Strategy related
def reformat_timestr_in_strategy(strategy_record):
    if strategy_record['created_time'] is None:
        strategy_record['created_time'] = "0000-00-00 00:00:00"
    else:
        strategy_record['created_time'] = strategy_record['created_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategy_record['modified_time'] is None:
        strategy_record['modified_time'] = "0000-00-00 00:00:00"
    else:
        strategy_record['modified_time'] = strategy_record['modified_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategy_record['last_handshake_time'] is None:
        strategy_record['last_handshake_time'] = "0000-00-00 00:00:00"
    else:
        strategy_record['last_handshake_time'] = strategy_record['last_handshake_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategy_record['online_time'] is None:
        strategy_record['online_time'] = "0000-00-00 00:00:00"
    else:
        strategy_record['online_time'] = strategy_record['online_time'].strftime('%Y-%m-%d %H:%M:%S')

    if strategy_record['offline_time'] is None:
        strategy_record['offline_time'] = "0000-00-00 00:00:00"
    else:
        strategy_record['offline_time'] = strategy_record['offline_time'].strftime('%Y-%m-%d %H:%M:%S')

    return strategy_record



# region Create method
def add_strategy(data):
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    with connection.cursor() as cursor:
        sql = "INSERT INTO `strategy` (`name`, `slug`, `filename`, `class_name`, `data_ticker`, `trade_ticker`, `data_resolution`, `contract`, `exchange`, `sec_type`, `action`, `base_qty`, `parameter`, `description`, `version`, `parent_id`, `status`, `created_time`, `modified_time`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
        cursor.execute(sql, (data['name'], data['slug'], data['filename'], data['class_name'], data['data_ticker'], data['trade_ticker'], data['data_resolution'], data['contract'], data['exchange'], data['sec_type'], data['action'], data['base_qty'], data['parameter'], data['description'], data['version'], data['parent_id'], data['status']))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

    if is_db_error:
        is_success = False
    if is_success:
        return "success", "add strategy success"
    else:
        return "fail", "error found on add strategy"
# endregion


# region Update method
def update_strategy(data):
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    with connection.cursor() as cursor:
        sql = "UPDATE `strategy` SET `name`=%s, `slug`=%s, `filename`=%s, `class_name`=%s, `data_ticker`=%s, `trade_ticker`=%s, `data_resolution`=%s, `contract`=%s, `exchange`=%s, `sec_type`=%s, `action`=%s, `base_qty`=%s, `parameter`=%s, `description`=%s, `version`=%s, `parent_id`=%s, `status`=%s, `modified_time`=NOW() WHERE `id`=%s"
        cursor.execute(sql, (data['name'], data['slug'], data['filename'], data['class_name'], data['data_ticker'], data['trade_ticker'], data['data_resolution'], data['contract'], data['exchange'], data['sec_type'], data['action'], data['base_qty'], data['parameter'], data['description'], data['version'], data['parent_id'], data['status'], data['strategy_id']))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

    if is_db_error:
        is_success = False
    if is_success:
        return "success", "add strategy success"
    else:
        return "fail", "error found on add strategy"
# endregion


# region Delete method
def delete_strategy(strategy_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `strategy` SET `status`='delete' WHERE `id`=%s"
            cursor.execute(sql, (strategy_id))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "strategy marked as delete"
        else:
            return "fail", "error found on delete strategy"
# endregion


# region Get method
def get_strategy(status=None, strategy_id=None, parent_id=None):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if status is None and strategy_id is None and parent_id is not None:
                # search by parent_id
                if parent_id == -1:
                    parent_id = ""
                sql = "SELECT * FROM `strategy` WHERE `parent_id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (parent_id))
            elif status is None and parent_id is None and strategy_id is not None:
                # search by strategy_id
                sql = "SELECT * FROM `strategy` WHERE `id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (strategy_id))
            elif strategy_id is None and parent_id is None and status is not None:
                # search by status
                sql = "SELECT * FROM `strategy` WHERE `status`=%s ORDER BY `created_time`"
                cursor.execute(sql, (status))
            else:
                sql = "SELECT * FROM `strategy` WHERE NOT `status`='delete' ORDER BY `created_time`"
                cursor.execute(sql)

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    value.append(reformat_timestr_in_strategy(row))

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get strategy success", value
        else:
            return "fail", "error found on get strategy", value


def get_strategy_by_id(strategy_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `id`=%s ORDER BY `id` ASC"
            cursor.execute(sql, (strategy_id))

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    value = reformat_timestr_in_strategy(row)

        if is_db_error:
            is_success = False

    except e:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get strategy success", value
        else:
            return "fail", "error found on get strategy", value


def get_strategy_to_daily_backtest(status=None):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        online = "online"
        offline = "offline"

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `status`=%s or `status`=%s ORDER BY `id` ASC"
            cursor.execute(sql, (online, offline))

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    value.append(reformat_timestr_in_strategy(row))

        if is_db_error:
            is_success = False

    except e:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get strategy success", value
        else:
            return "fail", "error found on get strategy", value


def get_available_strategy_equity(status, date):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy` WHERE `status`=%s ORDER BY `created_time`"
            cursor.execute(sql, (status))

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

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

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get available strategy equity success", value
        else:
            return "fail", "error found on get available strategy equity", value

def get_single_strategy_equity(strategy_id):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = {}

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `strategy_equity` WHERE `strategy_id`=%s ORDER BY `date` ASC"
            cursor.execute(sql, (strategy_id))

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            live_equity = []
            backtest_equity = []

            if result is not None:
                for row in result:

                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')

                    if row['equity_type'] == "live":
                        live_equity.append(row)
                    else:
                        backtest_equity.append(row)

            value['live_equity'] = live_equity
            value['backtest_equity'] = backtest_equity

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get single strategy equity success", value
        else:
            return "fail", "error found on get single strategy equity", value


def get_next_strategy_to_online(exchange):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = {}

        with connection.cursor() as cursor:
            status = "online"
            ws_status = "offline"
            sql = "SELECT * FROM `strategy` WHERE `exchange`=%s AND `status`=%s AND `ws_status`=%s ORDER BY `id` ASC LIMIT 1"
            cursor.execute(sql, (exchange, status, ws_status))

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

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

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get online strategy success", value
        else:
            return "fail", "error found on get online strategy", value

# endregion


# endregion


# region Filter test

# region Create method
def add_filter_test(filter_class, backtest_name, remark=""):
    import copy
    is_db_error = True
    is_success = True
    connection = connect_to_mysql()
    value = []

    with connection.cursor() as cursor:
        sql = "INSERT INTO `filter_test` (`filter_class`, `backtest_name`, `status`, `remark`, `created_time`, `modified_time`) VALUES (%s,%s,%s,%s,NOW(),NOW())"
        cursor.execute(sql, (filter_class, backtest_name, "pending", remark))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

        filter_test_id = cursor.lastrowid

        if is_db_error:
            is_success = False
        if is_success:
            return "success", "add filter test success"
        else:
            return "fail", "error found on add filter test"
# endregion


# region Update method
def update_filter_test_status(filter_test_id, status, error_msg=""):
        try:
            is_db_error = True
            is_success = True
            connection = connect_to_mysql()
            value = []

            with connection.cursor() as cursor:
                sql = "UPDATE `filter_test` SET `status`=%s, `error_message`=%s, `modified_time`=NOW() WHERE `id`=%s"
                cursor.execute(sql, (status, error_msg, filter_test_id))
                connection.commit()
                is_db_error = False


            if is_db_error:
                is_success = False

        except:
            traceback.print_exc()
            is_success = False

        finally:
            disconnect_to_mysql(connection)

            if is_success:
                return "success", "update filter test status success"
            else:
                return "fail", "error found update filter test status"
# endregion


# region Get method
def get_filter_test(status="running"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
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
            is_db_error = False

            if result is not None:
                for row in result:
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get optimization", value
        else:
            return "fail", "error found on get optimization.", "not_set"


def get_filter_test_with_pagination(page_size, page_no):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `filter_test` GROUP BY `status`"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

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

            value['page_size'] = page_size
            value['page_no'] = page_no
            value['num_pages'] = int(math.ceil(value['num_filter_test'] / page_size))

            sql = "SELECT * FROM `filter_test` ORDER BY `created_time` DESC LIMIT %s, %s"
            cursor.execute(sql, ((page_no-1)*page_size, page_size))
            connection.commit()

            result = cursor.fetchall()
            if result is not None:
                for row in result:
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    value['filter_test'].append(row)

        if is_db_error:
            is_success = False
        print(value)
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get filter test with pagination", value
        else:
            return "fail", "error found on get filter test with pagination", "not_set"
# endregion
# endregion


# region Service related
def get_server():
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `services` ORDER BY `id` ASC"
            cursor.execute(sql)

            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    row['created_time'] = row['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                    row['modified_time'] = row['modified_time'].strftime('%Y-%m-%d %H:%M:%S')
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get services success", value
        else:
            return "fail", "error found on get services", value
# endregion



# region Live Order related

# region Add method
def add_live_order(order):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "INSERT INTO `live_orders` ( `oid`, `sid`, `client_id`, " \
                                                "`exchange`, `ticker`, `contract`, `action`," \
                                                " `qty`, `order_type`, `trigger_price`, `label`, " \
                                                "`account`, `status`, `adjusted_date`, `adjusted_time`, " \
                                                "`created_time`, `modified_time`) " \
                                                "VALUES (%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "%s,%s,%s,%s," \
                                                        "NOW(), NOW())"
            cursor.execute(sql, (order['oid'], order['sid'], order['client_id'],
                                 order['exchange'],order['ticker'],order['contract'], order['action'],
                                 order['qty'], order['order_type'],order['trigger_price'],order['label'],
                                 order['account'], order['status'], order['adjusted_date'],order['adjusted_time']))
            connection.commit()
            result = cursor.fetchone()
            is_db_error = False

            filter_test_id = cursor.lastrowid

            if is_db_error:
                is_success = False
    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update filter test status success"
        else:
            return "fail", "error found update filter test status"
# endregion


# region Get method
def get_live_order_by_date(date_str):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `live_orders` WHERE `adjusted_date`=%s ORDER BY `oid` DESC"
            cursor.execute(sql, (date_str))
            connection.commit()
            result = cursor.fetchall()
            is_db_error = False

            if result is not None:
                for row in result:
                    row['created_time'] = mysql_time_to_string(row['created_time'])
                    row['modified_time'] = mysql_time_to_string(row['modified_time'])
                    row['filled_time'] = mysql_time_to_string(row['filled_time'])
                    value.append(row)

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get live order by date string success", value
        else:
            return "fail", "error found on get live order by date string.", "not_set"


# endregion


# region Update method
def update_live_order_status(order_id, sid, status):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `status`=%s, `modified_time`=NOW() WHERE `oid`=%s AND `sid`=%s"
            cursor.execute(sql, (status, order_id, sid))
            connection.commit()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update live order status success"
        else:
            return "fail", "error found update live order status"


def update_live_order_column(order_id, sid, column, value):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `"+column+"`=%s, `modified_time`=NOW() WHERE `oid`=%s AND `sid`=%s"
            cursor.execute(sql, (value, order_id, sid))
            connection.commit()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update live order column success"
        else:
            return "fail", "error found update live order column"

def update_live_order_commission(order_id, commission):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `commission`=%s, `modified_time`=NOW() WHERE `oid`=%s"
            cursor.execute(sql, (commission, order_id))
            connection.commit()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update live order commission success"
        else:
            return "fail", "error found update live order commission"


def update_live_order_from_open_order(order_id, perm_id, status):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `live_orders` SET `status`=%s, `perm_id`=%s, `modified_time`=NOW() WHERE `oid`=%s"
            cursor.execute(sql, (status, perm_id, order_id))
            connection.commit()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update live order status success"
        else:
            return "fail", "error found update live order status"


def update_live_order_from_order_status(order_id, perm_id, status, filled, avg_fill_price):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if status =="Filled":
                sql = "UPDATE `live_orders` SET `perm_id`=%s, `status`=%s, `filled_qty`=%s, `filled_price`=%s, `modified_time`=NOW(), `filled_time`=NOW() WHERE `oid`=%s"
                cursor.execute(sql, (perm_id, status, filled, avg_fill_price, order_id))
            else:
                sql = "UPDATE `live_orders` SET `perm_id`=%s, `status`=%s, `filled_qty`=%s, `filled_price`=%s, `modified_time`=NOW() WHERE `oid`=%s"
                cursor.execute(sql, (perm_id, status, filled, avg_fill_price, order_id))
            connection.commit()
            is_db_error = False

        if is_db_error:
            is_success = False

    except:
        traceback.print_exc()
        is_success = False

    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "update live order success"
        else:
            return "fail", "error found update live order"

# endregion

# endregion




