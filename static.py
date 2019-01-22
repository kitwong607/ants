RESOLUTION_IN_SEC = {"1S": 1, "2S": 2, "3S": 3, "5S": 5, "10S": 10, "12S": 12, "15S": 15, "20S": 30, "30S": 30,
                     "1T": 60, "2T": 120, "3T": 180, "5T": 300, "8T": 480, "10T": 600, "12T": 720, "15T": 900,
                     "20T": 1200, "30T": 1800,
                     "1H": 3600,"2H": 7200,
                     "1D": 86400}

EXCHANGE_TIME_ZONE = {"HKEX": 480, "HKFE": 480}

INTRA_DATE_DATA_RESOLUTION = ["1S", "2S", "3S", "5S", "10S", "12S", "15S", "20S", "30S",
     "1T", "2T", "3T", "5T", "8T", "10T", "12T", "15T", "20T", "30T",
     "1H", "2H"]


INDEX_TICKER = ['mhi','hsi']
COMMODITY_TICKER = ['brent','copper']
FX_TICKER = ['usdjpy','usdcad']


def GetTickerType(tickerType):
    if str(tickerType).lower() in INDEX_TICKER: return "INDEX"
    if str(tickerType).lower() in COMMODITY_TICKER: return "COMMODITY_TICKER"
    if str(tickerType).lower() in FX_TICKER: return "FX"

    return "NOT_SET"