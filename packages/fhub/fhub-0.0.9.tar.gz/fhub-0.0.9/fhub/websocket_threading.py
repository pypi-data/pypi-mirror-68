from requests import get
import threading
from time import sleep
from  pandas import Series
from datetime import datetime

# Function get information in json format from Yahoo Finance
def stream(
    symbol,
    callback=None,
    wait_time=1,
    verbose=False
):
    """Make a call to Yahoo Finance to capture information about the ticker
    passed as a symbol and performs a callback if the function is passed.
    """
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
    while True:
        response = get(url)
        info_dict = response.json()
        # Si se ha definido una función callback la llama
        if callback:
            callback(info_dict, verbose)
        sleep(wait_time)

# Función callback de ejemplo, puede ser sustituida por cualquier otra.
def get_data(info_dict, verbose=False):
    """ It receives the answer to the call to Yahoo Finance and saves the last
    price and time in a series of pandas, if verbose is True it also prints
    the last value.
    """
    symbol = info_dict['chart']['result'][0]['meta']['symbol']
    time = datetime.fromtimestamp(info_dict['chart']['result'][0]['meta']['regularMarketTime'])
    quote = info_dict['chart']['result'][0]['meta']['regularMarketPrice']
    data[time] = quote
    if verbose:
        print(f"{time}:  {symbol}  {quote}")



if __name__ == "__main__":
#     We create a thread like a daemon and leave it running indefinitely.
#     As arguments (args) we pass the ticker of the asset, the function
#     for callback and the timeout between two calls
    data = Series()
    hilo = threading.Thread(
        target=stream,
        daemon=True,
        args=('TSLA', get_data, 10, True)
    )
    hilo.start()
    hilo.join()
