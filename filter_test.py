import queue, copy,datetime, calendar, multiprocessing, pandas as pd, numpy as np, json
from .data_provider.base import DataType
from . import utilities
from .session_config import SessionMode, SessionStaticVariable
from shutil import copyfile


class FilterTest(object):
    def __init__(self, config):
        self.config = config
        self.backtest_name = config.backtest_name
        self.filter_class = config.filter_class

    def run(self):
        #get start date end date from backtest report
        print("#1","load backtest data")
        backtest_report_dir = SessionStaticVariable.base_report_directory + self.backtest_name + "\\"

        session_config = utilities.load_json(backtest_report_dir +"session_config.json")
        positions = utilities.load_json(backtest_report_dir +"positions.json")
        orders = utilities.load_json(backtest_report_dir +"orders.json")

        start_date = session_config['start_date']
        end_date = session_config['end_date']
        data_ticker = session_config['data_ticker']
        exchange = session_config['exchange']


        print("#2", "load OHLC data")
        dfs = []
        is_first = True
        for month_str in self.config.data_period:
            for resolution in self.config.filter_resolution:
                csv_filename = month_str + "_" + data_ticker + "_"+resolution+".csv"
                csv_file_path = SessionStaticVariable.data_path + exchange + "\\csv\\" + resolution + "\\" + csv_filename

                if utilities.check_file_exist(csv_file_path):
                    df = pd.read_csv(csv_file_path, parse_dates=['datetime'])
                    df.reset_index(drop=True)

                    if 'adjusted_time' not in df.columns:
                        df['datetime_for_sort'] = df['datetime']
                        df['adjusted_date'] = df.apply(lambda x: x['datetime_for_sort'].strftime('%Y%m%d'), axis=1)
                        df['adjusted_date'] = df['adjusted_date'].astype(int)

                        df['hour'] = df['datetime'].dt.hour
                        df['hour'] = df['hour'].astype(str)
                        df['hour'] = df['hour'].str.zfill(2)

                        df['minute'] = df['datetime'].dt.minute
                        df['minute'] = df['minute'].astype(str)
                        df['minute'] = df['minute'].str.zfill(2)

                        df['second'] = df['datetime'].dt.second
                        df['second'] = df['second'].astype(str)
                        df['second'] = df['second'].str.zfill(2)

                        if resolution not in utilities.INTRA_DATE_DATA_RESOLUTION:
                            df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                            df['hour'] = "33"
                            df['minute'] = "00"
                            df['second'] = "00"

                        df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                        df['adjusted_time'] = df['adjusted_time'].astype(int)
                    else:
                        if resolution not in utilities.INTRA_DATE_DATA_RESOLUTION:
                            df['datetime_for_sort'] = df['datetime'] - np.timedelta64(9, 'h')

                            df['hour'] = "33"
                            df['minute'] = "00"
                            df['second'] = "00"

                            df['adjusted_time'] = df['hour'] + df['minute'] + df['second']
                            df['adjusted_time'] = df['adjusted_time'].astype(int)
                        else:
                            df['hour'] = df['hour'].astype(str)
                            df['hour'] = df['hour'].str.zfill(2)
                            df['minute'] = df['minute'].astype(str)
                            df['minute'] = df['minute'].str.zfill(2)
                            df['second'] = df['second'].astype(str)
                            df['second'] = df['second'].str.zfill(2)

                    df['ticker'] = self.config.data_ticker
                    df['resolution'] = resolution
                    df['resolution_in_sec'] = utilities.RESOLUTION_IN_SEC[resolution]
                    dfs.append(df)
                is_first = False

        df = pd.concat(dfs)
        df['adjusted_time'] = df['adjusted_time'] + df['resolution_in_sec']

        df = df.sort_values(["adjusted_date", "adjusted_time", "resolution_in_sec"])
        df = df.drop('datetime_for_sort', 1)
        df = df[['datetime','open', 'high', 'low', 'close', 'volume', 'ticker', 'resolution', 'resolution_in_sec',
                 'adjusted_date', 'adjusted_time']]
        df = df.reset_index(drop=True)



        print("#3", "Setup and calculate filter")
        filter_df = df.copy(deep=True)

        parameter = self.filter_class.OPTIMIZATION_PARAMETER;
        parameter_combination = utilities.get_optimization_parameter_combination(parameter, parameter)

        count = 0
        filters = []
        for parameter in parameter_combination:
            self.config.filter_parameter = parameter
            count += 1
            print("start:", str(count),"/", str(len(parameter_combination)))
            filter = self.filter_class(df, parameter)
            filter_result = filter.run()
            #filter_df = pd.concat([filter_df, filter_result], axis=1)

            filter_df[filter.name] = filter_result['val']
            filters.append({"name":filter.name, "parameter":parameter})
        filter_df.index = filter_df['adjusted_date']
        self.config.filter_list = filters

        filter_df_filename = self.config.data_ticker + "_" + self.filter_class.NAME+ "_" +".csv"
        filter_df.to_csv(SessionStaticVariable.base_filter_directory + filter_df_filename)


        print("#4", "Filter trade and save result")
        report_directory = SessionStaticVariable.base_report_directory + self.backtest_name + "\\filtered"
        utilities.create_folder(report_directory)


        for filter in filters:
            new_positions = []
            new_orders = []
            filter_result = {"total": 0,
                             "filtered": 0,
                             "bypassed": 0,
                             "filtered_winner": 0,
                             "filtered_losser": 0,
                             "bypassed_winner": 0,
                             "bypassed_losser": 0}

            for position in positions:
                filter_result['total'] += 1

                threshold = filter_df.at[position['adjusted_date'], filter['name']]
                qty = position['qty']
                new_qty = qty
                is_add = False
                if threshold > 0 and position['action']=="BUY":
                    is_add = True
                    if abs(threshold)>1:
                        new_qty = abs(threshold)

                elif threshold < 0 and position['action'] == "SELL":
                    is_add = True
                    if abs(threshold)>1:
                        new_qty = abs(threshold)

                if is_add:
                    position['qty'] = new_qty
                    position['pnl'] = position['pnl'] / qty * new_qty
                    position['net_pips'] = position['net_pips'] / qty * new_qty
                    position['slippage'] = position['slippage'] / qty * new_qty
                    position['max_net'] = position['max_net'] / qty * new_qty
                    position['commission'] = position['commission'] / qty * new_qty
                    position['realised_pnl'] = position['realised_pnl'] / qty * new_qty
                    position['unrealised_pnl'] = position['unrealised_pnl'] / qty * new_qty
                    new_positions.append(position)

                    filter_result['bypassed'] += 1

                    if position['pnl'] > 0:
                        filter_result['bypassed_winner'] += 1
                    else:
                        filter_result['bypassed_losser'] += 1
                else:
                    filter_result['filtered'] += 1
                    if position['pnl'] > 0:
                        filter_result['filtered_winner'] += 1
                    else:
                        filter_result['filtered_losser'] += 1


            for order in orders:
                qty = order['quantity']
                new_qty = qty
                is_add = False

                if threshold > 0 and order['action']=="BUY":
                    is_add = True
                    if abs(threshold)>1:
                        new_qty = abs(threshold)

                elif threshold < 0 and order['action'] == "SELL":
                    is_add = True
                    if abs(threshold)>1:
                        new_qty = abs(threshold)

                if is_add:
                    order['quantity'] = new_qty
                    order['commission'] = order['commission'] / qty * new_qty
                    order['slippage'] = order['slippage'] / qty * new_qty
                    new_orders.append(order)

            filter_report_directory = report_directory + "\\" + filter['name'] + "\\"
            utilities.create_folder(filter_report_directory)

            self.config.filter_result = filter_result
            self.config.filter_test_name = filter['name']
            copyfile(backtest_report_dir +"session_config.json", filter_report_directory +"session_config.json")

            self.config.save()

            with open(filter_report_directory + "positions.json", 'w') as fp:
                json.dump(new_positions, fp)

            with open(filter_report_directory + "orders.json", 'w') as fp:
                json.dump(new_orders, fp)

            with open(backtest_report_dir + "filters.json", 'w') as fp:
                json.dump(filters, fp)

            utilities.create_report_summary(filter_report_directory)


        print("#5", "Create new backtest report")
        utilities.create_filter_report(self.backtest_name)

