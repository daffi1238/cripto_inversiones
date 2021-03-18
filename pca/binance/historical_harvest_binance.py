from binance.client import Client
import urllib3 #Para conexiones en https
urllib3.disable_warnings()
from key_secret.key_secret import * #get_api, get_secret
from binance.websockets import BinanceSocketManager
api_key=get_api()
api_secret=get_secret()

import datetime
import csv
import time
import numpy as np
import pandas as pd

import threading
threads=10      #sin definir diria yo

import matplotlib.pyplot as plt

#api_key="AAAAAAAAAAAAAAAAAA"
#api_secret="BBBBBBBBBBBBBBBB"

##Funcion de interrupcion######################################################

import signal
import sys
def signal_handler_function(signum, frame):
    print("Se cierra con control C")


    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler_function)

###############################################################################

client = Client(api_key, api_secret, {"verify": False, "timeout": 20})

#####Creamos fichero y definimos las columnas#####

try:
    f = open("outFile.csv")
    existe=True
    print("Elimina el fichero para el correcto funcionamiento del programa")
    #sys.exit(0)

    # Do something with the file############################################
except IOError:
    print("El fichero no existe, vamos a generarlo de 0")
    existe=False


file = open("outFile.csv", "w")   #file = open("outFile.csv", "a")

csvWriter = csv.writer( file )
if existe==False:
    print("El fichero no existe asi que le añadimos una fila")
    csvWriter.writerow( ["timestamp", "BTC_open", "BTC_high","BTC_low", "BTC_close", "ETH_open", "ETH_high", "ETH_low", "ETH_close", "ADA_open", "ADA_high", "ADA_low", "ADA_close", "BNB_open", "BNB_high","BNB_low", "BNB_close" ] )  #    csvWriter.writerow( ["timestamp", "BTC", "ETH", "BNB", "DODGE", "DOT"] )
else:
    pass




#############################################################################
#Symbols
#It's necessary add more coins in anycase
coins = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT" ]



def check_minmax(current, coin):
    #print("Entering in minmax function")
    if coin=="BTC":
        global min_btc
        global max_btc
        if current>max_btc:
            max_btc=current
        elif current<min_btc:
            min_btc=current
        else:
            pass

    if coin=="ETH":
        global min_eth
        global max_eth
        if current>max_eth:
            max_eth=current
        elif current<min_eth:
            min_eth=current
        else:
            pass

####Calculo de la EWMA##########################################################
def __EWMA__():
    global btc_values
    global eth_values

    window_size = contador+1
    numbers_series = pd.Series(btc_values)
#    numbers_series_eth = pd.Series(numbers)

    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()

    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]

    global ewma
    ewma.append(without_nans)

    print(without_nans)
################################################################################

#Función principal
if __name__=='__main__':
    timestamp_status=False
    init_date="1 Jan, 2021"
    end_date="18 Mar, 2021"
    historical_BTC = client.get_historical_klines(coins[0], Client.KLINE_INTERVAL_30MINUTE, init_date, end_date)
    historical_ETH = client.get_historical_klines(coins[1], Client.KLINE_INTERVAL_30MINUTE, init_date, end_date)
    historical_ADA = client.get_historical_klines(coins[2], Client.KLINE_INTERVAL_30MINUTE, init_date, end_date)
    historical_BNB = client.get_historical_klines(coins[3], Client.KLINE_INTERVAL_30MINUTE, init_date, end_date)
    '''
    get_historical_klines returns:
    https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
    [
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
    '''

#####Bucle principal############################################################
    #Not dinamical data programmed but it could be a good next step

    i=0
    #just for writting the timestamp column
    while i != len(historical_BTC):
        timestamp=datetime.datetime.utcfromtimestamp(int(historical_BTC[i][0]) // 1000).strftime('%Y-%m-%d %H:%M:%S')
        #BTC
        btcOpen=historical_BTC[i][1]
        btcHigh=historical_BTC[i][2]
        btcLow=historical_BTC[i][3]
        btcClose=historical_BTC[i][4]

        ethOpen=historical_ETH[i][1]
        ethHigh=historical_ETH[i][2]
        ethLow=historical_ETH[i][3]
        ethClose=historical_ETH[i][4]

        adaOpen=historical_ADA[i][1]
        adaHigh=historical_ADA[i][2]
        adaLow=historical_ADA[i][3]
        adaClose=historical_ADA[i][4]

        bnbOpen=historical_BNB[i][1]
        bnbHigh=historical_BNB[i][2]
        bnbLow=historical_BNB[i][3]
        bnbClose=historical_BNB[i][4]

        csvWriter.writerow( [timestamp, btcOpen, btcHigh, btcHigh, btcClose, ethOpen, ethHigh, ethHigh, ethClose, adaOpen, adaHigh, adaHigh, adaClose, bnbOpen, bnbHigh, bnbHigh, bnbClose ] )

        i+=1
    print("Se acabó")
