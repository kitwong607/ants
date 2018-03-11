import pymysql.cursors, json, traceback, datetime
from ants import utilities


#<editor-fold desc="Datetime calculation functions">#############################################################
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
#</editor-fold>#################################################################################################

def mysql_time_to_string(dt):
    if dt is None:
        return "0000-00-00 00:00:00"
    return dt.strftime('%Y-%m-%d %H:%M:%S')

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

def get_backtest_by_id(backtest_id, table="backtest"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if table == "optimization":
                sql = "SELECT * FROM `optimization` WHERE `id`=%s  LIMIT 1"
            else:
                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s  LIMIT 1"

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


def update_backtest_start_time(backtest_id, table="backtest"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if table == "optimization":
                sql = "UPDATE `optimization` SET `backtest_start_time`=NOW() WHERE `id`=%s"
            else:
                sql = "UPDATE `backtest_report` SET `backtest_start_time`=NOW() WHERE `id`=%s"
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


def update_backtest_end_time(backtest_id, table="backtest"):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if table=="optimization":
                sql = "UPDATE `optimization` SET `backtest_end_time`=NOW() WHERE `id`=%s"
            else:
                sql = "UPDATE `backtest_report` SET `backtest_end_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (backtest_id))
            connection.commit()

            result, message, backtest = get_backtest_by_id(backtest_id, table)

            if (backtest is not None) and (result == "success"):
                sec_diff = (backtest['backtest_end_time'] - backtest['backtest_start_time']).total_seconds()
                sec_diff = str(datetime.timedelta(seconds=int(sec_diff)))

                if table == "optimization":
                    sql = "UPDATE `optimization` SET `backtest_used_time`=%s WHERE `id`=%s"
                else:
                    sql = "UPDATE `backtest_report` SET `backtest_used_time`=%s WHERE `id`=%s"
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
                    if value['num_backtest'] == value['num_running'] + value['num_pending']:
                        update_optimization_status(optimization_id, "running")



            elif status == "complete":
                update_backtest_end_time(backtest_id)

                sql = "SELECT * FROM `backtest_report` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, (backtest_id))
                connection.commit()
                result = cursor.fetchone()
                is_db_error = False

                if result is not None:
                    #check current backtest is a optimization
                    if optimization_id != 0:
                        sql = "SELECT COUNT(*) as `num_rows`, `status` FROM `backtest_report` WHERE `optimization_id`=%s GROUP BY `status`"
                        cursor.execute(sql, (optimization_id))
                        connection.commit()

                        result = cursor.fetchall()
                        value = get_backtest_status_summary(result)

                        if value['num_backtest'] == value['num_complete']:
                            update_optimization_status(optimization_id, "backtest_complete")
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


def get_backtest_status_summary(result):
    value = {}
    value['num_backtest'] = 0
    value['num_complete'] = 0
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
            value['backtest'] = []

            sql = "SELECT * FROM `backtest_report` ORDER BY `created_time` DESC LIMIT %s, %s"
            cursor.execute(sql, ((page_no-1)*page_size, page_size))
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
        print(value)
    except:
        is_success = False
        print(traceback.print_exc())
    finally:
        disconnect_to_mysql(connection)

        if is_success:
            return "success", "get backtest with pagination", value
        else:
            return "fail", "error found on get backtest  with pagination", "not_set"


##########################################################

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
            value['num_complete'] = 0
            value['num_error'] = 0
            value['num_running'] = 0
            value['num_pending'] = 0
            value['num_delete'] = 0
            value['num_completed'] = 0
            value['num_backtest_complete'] = 0
            value['page_size'] = page_size
            value['page_no'] = page_no

            value['optimization'] = []

            if result is not None:
                for row in result:
                    value["num_"+row['status']] += row['num_rows']
                    value['num_optimization'] += row['num_rows']

            sql = "SELECT * FROM `optimization` ORDER BY `created_time` DESC LIMIT %s, %s"
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
                sql = "SELECT * FROM `optimization` ORDER BY `created_time`"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM `optimization` WHERE `status`=%s  ORDER BY `created_time`"
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

def update_optimization(optimization_id:int, optimization_summary, first_backtest_report):
    print(optimization_summary)
    print(first_backtest_report)
    # first_backtest_report['description']['report_full_path']
    # first_backtest_report['description']['report_folder_name']
    #report_full_path
    #report_folder_name


    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            sql = "UPDATE `optimization` SET `report_full_path`=%s, `report_folder_name`=%s, `num_trade`=%s, `num_trade_std`=%s, `num_trade_std_pct`=%s, `win_rate`=%s, `win_rate_std`=%s, `win_rate_std_pct`=%s, `pnl`=%s, `pnl_std`=%s, `pnl_std_pct`=%s, `net_pips`=%s, `net_pips_std`=%s, `net_pips_std_pct`=%s, `avg_pips_pre_contract`=%s, `avg_pips_pre_contract_std`=%s, `avg_pips_pre_contract_std_pct`=%s, `profit_factor`=%s, `profit_factor_std`=%s, `profit_factor_std_pct`=%s, `payoff_ratio`=%s, `payoff_ratio_std`=%s, `payoff_ratio_std_pct`=%s, `roci`=%s, `roci_std`=%s, `roci_std_pct`=%s, `sharpe_ratio`=%s, `sharpe_ratio_std`=%s, `sharpe_ratio_std_pct`=%s, `tharp_expectancy`=%s, `tharp_expectancy_std`=%s, `tharp_expectancy_std_pct`=%s, `expectancy`=%s, `expectancy_std`=%s, `expectancy_std_pct`=%s, `mdd`=%s, `mdd_std`=%s, `mdd_std_pct`=%s, `mdd_pct`=%s, `mdd_pct_std`=%s, `mdd_pct_std_pct`=%s, `mdd_daily`=%s, `mdd_daily_std`=%s, `mdd_daily_std_pct`=%s, `mdd_pct_daily`=%s, `mdd_pct_daily_std`=%s, `mdd_pct_daily_std_pct`=%s, `dd_duration`=%s, `dd_duration_std`=%s, `dd_duration_std_pct`=%s, `dd_duration_daily`=%s, `dd_duration_daily_std`=%s, `dd_duration_daily_std_pct`=%s, `modified_time`=NOW() WHERE `id`=%s"
            cursor.execute(sql, (   first_backtest_report['description']['report_full_path'],
                                    first_backtest_report['description']['report_folder_name'],
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
            elif status=="backtest_complete":
                update_backtest_end_time(optimization_id, 'optimization')

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


def get_option(option_key):
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
            return "success", "option updated", value
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

        sql = "INSERT INTO `backtest_report` (`exchange`=%s, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategy_class`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `strategy_parameter`, `optimization_id`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.execute(sql, (data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"], data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"], data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"], data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"], data["strategy_slug"], data["last_update"], data["version"], data["parameter"], data["optimization_id"]))
        connection.commit()
        result = cursor.fetchone()
        is_db_error = False

        if is_db_error:
            is_success = False
        if is_success:
            return "success", "add backtest success"
        else:
            return "fail", "error found on add backtest"

def add_optimization(data):
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
        sql = "INSERT INTO `optimization` (`exchange`, `trade_ticker`, `data_ticker`, `data_resolution`, `contract`, `base_quantity`, `cash`, `data_start_date`, `start_date`, `end_date`, `backtest_mode_no`, `backtest_mode`, `commission`, `slippage_pips`, `data_provider_class`, `order_handler_class`, `portfolio_class`, `strategy_class`, `strategy_name`, `strategy_slug`, `last_update`, `version`, `strategy_parameter`, `created_time`, `modified_time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.execute(sql, (data["exchange"], data["trade_ticker"], data["data_ticker"], data["data_resolution"], data["contract"], data["base_quantity"], data["cash"], data["data_start_date"], data["start_date"], data["end_date"], data["backtest_mode_no"], data["backtest_mode"], data["commission"], data["slippage_pips"], data["data_provider"], data["order_handler"], data["portfolio"], data["strategy"], data["strategy_name"], data["strategy_slug"], data["last_update"], data["version"], data["parameter"]))
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
        if is_success:
            return "success", "add optimization success"
        else:
            return "fail", "error found on add optimization"

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

def get_strategy(status=None, strategy_id=None, parent_id=None):
    try:
        is_db_error = True
        is_success = True
        connection = connect_to_mysql()
        value = []

        with connection.cursor() as cursor:
            if status is None and strategy_id is None and parent_id is not None:
                #search by parent_id
                if parent_id == -1:
                    parent_id = ""
                sql = "SELECT * FROM `strategy` WHERE `parent_id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (parent_id))
            elif status is None and parent_id is None and strategy_id is not None:
                #search by strategy_id
                sql = "SELECT * FROM `strategy` WHERE `id`=%s ORDER BY `created_time`"
                cursor.execute(sql, (strategy_id))
            elif strategy_id is None and parent_id is None and status is not None:
                #search by status
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



def update_backtest_report(config):
    try:
        with open(config.report_directory + '\\backtest_summary.json') as json_data:
            d = json.load(json_data)

            d['win_rate'] = utilities.round(d['win_rate'], 3)
            d['num_trade'] = utilities.round(d['num_trade'], 3)
            d['pnl'] = utilities.round(d['pnl'], 3)
            d['net_pips'] = utilities.round(d['net_pips'], 3)
            d['profit_factor'] = utilities.round(d['profit_factor'], 3)
            d['payoff_ratio'] = utilities.round(d['payoff_ratio'], 3)
            d['roci'] = utilities.round(d['roci'], 3)

            d['sharpe_ratio'] = utilities.round(d['sharpe_ratio'], 3)
            d['standard_deviation'] = utilities.round(d['standard_deviation'], 3)
            d['standard_error'] = utilities.round(d['standard_error'], 3)
            d['tharp_expectancy'] = utilities.round(d['tharp_expectancy'], 3)
            d['expectancy'] = utilities.round(d['expectancy'], 3)

            d['mdd'] = utilities.round(d['mdd'], 3)
            d['mdd_pct'] = utilities.round(d['mdd_pct'], 3)
            d['mdd_daily'] = utilities.round(d['mdd_daily'], 3)
            d['mdd_pct_daily'] = utilities.round(d['mdd_pct_daily'], 3)
            d['dd_duration'] = utilities.round(d['dd_duration'], 3)

            d['dd_duration_daily'] = utilities.round(d['dd_duration_daily'], 3)
            d['avg_pips_pre_contract'] = utilities.round(d['avg_pips_pre_contract'], 3)
            d['report_folder_name'] = config.report_folder_name
            d['report_full_path'] = config.report_directory

            is_db_error = True
            is_success = True
            connection = connect_to_mysql()
            value = []

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