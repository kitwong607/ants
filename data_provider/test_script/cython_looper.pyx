import os, pandas as pd

def loop():
    csv_file_path = "C:\\data\\hkex\\csv\\1S\\201612_HSI_1S.csv"
    df = pd.DataFrame.from_csv(csv_file_path)
    df['ticker'] = "HSI"
    df['resolution'] = "1S"
    for dt, open_price, high_price, low_price, close_price, vol, ticker, resolution in df.itertuples():
        price = my_logic(open_price, high_price, low_price, close_price, vol)

def loop2():
    csv_file_path = "C:\\data\\hkex\\csv\\1S\\201612_HSI_1S.csv"
    df = pd.DataFrame.from_csv(csv_file_path)
    df['ticker'] = "HSI"
    df['resolution'] = "1S"

    for row_id, row in enumerate(df.values):
        open_price, high_price, low_price, close_price, volume, ticker, resolution = row
        price = my_logic(open_price, high_price, low_price, close_price, volume)

cdef my_logic(float open_price, float high_price, float low_price, float close_price, float vol):
    cdef float price = 0
    for i in range(1000):
        if open_price > close_price:
            price += open_price + high_price + low_price + close_price + vol
        else:
            price -= open_price + high_price + low_price + close_price + vol
    return price