import pandas as pd
from ..ta.SMA import SMA
from .base import DailyFilter
from ..data_provider.base import BarData

class MultipleSMATrendFilter(DailyFilter):
    OPTIMIZATION_PARAMETER = {
        "fast_sma_window": {
            "name": "fast_sma_window",
            "value": 3,
            "min_value": 3,
            "max_value": 9,
            #"max_value": 20,
            "step": 1
        },
        "slow_sma_window": {
            "name": "slow_sma_window",
            "value": 10,
            "min_value": 10,
            "max_value": 30,
            #"max_value": 60,
            "step": 2
        }
    }

    RESOLUTION = ["1D"]
    NAME = "MultipleSMATrendFilter"

    def __init__(self, df, parameter):
        for key in MultipleSMATrendFilter.OPTIMIZATION_PARAMETER:
            if key not in parameter:
                raise IndexError("Filter parameter missed")

        self.df = df
        self.resolution = MultipleSMATrendFilter.RESOLUTION
        self.fast_sma_window = int(parameter['fast_sma_window']['value'])
        self.slow_sma_window = int(parameter['slow_sma_window']['value'])
        self.name = MultipleSMATrendFilter.NAME + "_" + str(self.fast_sma_window) + "x" + str(self.slow_sma_window)


        self.fast_sma = SMA(None, int(self.fast_sma_window))
        self.slow_sma = SMA(None, int(self.slow_sma_window))
        self.data_df = df


    def run(self):
        result_df = pd.DataFrame(columns=['val'])
        for row in self.data_df.itertuples():
            idx, dt,  open_price, high_price, low_price, close_price, volume, ticker, resolution, resolution_in_sec, adjusted_date, adjusted_time  = row
            bar = BarData(ticker, resolution, dt, open_price, high_price, low_price, close_price, volume, adjusted_date, adjusted_time)
            if resolution == "1D":
                fast_sma_value = self.fast_sma.push_data(bar)
                slow_sma_value = self.slow_sma.push_data(bar)

                filter_value = 0
                if(fast_sma_value > slow_sma_value and close_price > fast_sma_value):
                    filter_value = 1
                elif(fast_sma_value < slow_sma_value and close_price < fast_sma_value):
                    filter_value = -1
                else:
                    filter_value = 0
                result_df.loc[idx] = filter_value
        result_df['val'] = result_df['val'].shift(1)
        result_df['val'] = result_df['val'].fillna(0)
        return result_df