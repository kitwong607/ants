RESOLUTION_IN_SEC = {"1S": 1, "2S": 2, "3S": 3, "5S": 5, "10S": 10, "12S": 12, "15S": 15, "20S": 30, "30S": 30,
                     "1T": 60, "2T": 120, "3T": 180, "5T": 300, "8T": 480, "10T": 600, "12T": 720, "15T": 900,
                     "20T": 1200, "30T": 1800,
                     "1H": 3600,"2H": 7200,
                     "1D": 86400}


RESOLUTION_IN_SEC = {'1T': 60, '2T': 120, '3T': 180, '4T': 240, '5T': 300, '6T': 360, '7T': 420, '8T': 480, '9T': 540,
                     '10T': 600, '12T': 720, '13T': 780, '14T': 840, '15T': 900, '16T': 960, '17T': 1020, '18T': 1080,
                     '20T': 1200, '22T': 1320, '24T': 1440, '25T': 1500, '26T': 1560, '28T': 1680, '30T': 1800,
                     '40T': 2400, '45T': 2700, '50T': 3000, '60T': 3600, '70T': 4200, '80T': 4800, '90T': 5400,
                     '120T': 7200}

EXCHANGE_TIME_ZONE = {"HKEX": 480, "HKFE": 480}

INTRA_DATE_DATA_RESOLUTION = ["1S", "2S", "3S", "5S", "10S", "12S", "15S", "20S", "30S",
     "1T", "2T", "3T", "5T", "8T", "10T", "12T", "15T", "20T", "30T",
     "1H", "2H"]



INTRA_DATE_DATA_RESOLUTION = ["1T", "2T", "3T", "4T", "5T", "6T", "7T", "8T", "9T", "10T",
                              "12T", "13T", "14T", "15T", "16T", "17T", "18T", "20T",
                              "22T", "24T", "25T", "26T", "28T", "30T",
                              "30T", "40T", "45T", "50T", "60T", "70T", "80T", "90T", "120T"]

CONTRACT_MULTIPLY = {
    "MHI": 10,
    "HSI": 50,
}

INDEX_TICKER = ['mhi','hsi']
COMMODITY_TICKER = ['brent','copper']
FX_TICKER = ['usdjpy','usdcad']


DEFAULT_JSON_RETURN = {"status": None, "message":"not_set", "data":{}}
PHP_STATUS_FAIL = 'fail'
PHP_STATUS_SUCCESS = 'success'

def GetTickerType(tickerType):
    if str(tickerType).lower() in INDEX_TICKER: return "INDEX"
    if str(tickerType).lower() in COMMODITY_TICKER: return "COMMODITY_TICKER"
    if str(tickerType).lower() in FX_TICKER: return "FX"

    return "NOT_SET"