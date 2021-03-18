from binance.client import Client
import urllib3 #Para conexiones en https
urllib3.disable_warnings()
from key_secret.key_secret import * #get_api, get_secret
from binance.websockets import BinanceSocketManager
api_key=get_api()
api_secret=get_secret()

import cryptocompare
from datetime import datetime
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
    print("El menor valor de BTC fue: ", min_btc)
    print("El mayor valor de BTC fue: ", max_btc)
    print("\n")
    print("El menor valor de ETH fue: ", min_eth)
    print("El mayor valor de ETH fue: ", max_eth)

    #Grafica precio btc
    # plotting the points
    plt.plot(timestamp, btc_values)
    # naming the x axis
    plt.xlabel('Tiempo')
    # naming the y axis
    plt.ylabel('Precio - Bitcoin')
    # giving a title to my graph
    plt.title('My first graph!')
    # function to show the plot
    plt.show()

    #Grafica ewma
    # plotting the points
    plt.plot(timestamp, emwa)
    # naming the x axis
    plt.xlabel('Tiempo')
    # naming the y axis
    plt.ylabel('EWMA')
    # giving a title to my graph
    plt.title('My second graph!')
    # function to show the plot
    plt.show()


    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler_function)

###############################################################################

client = Client(api_key, api_secret, {"verify": False, "timeout": 20})
client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5})


''' #Uso de proxys
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080'
}

# in the Client instantiation
client = Client("api-key", "api-secret", {'proxies': proxies})

# or on an individual call
client.get_all_orders(symbol='BNBBTC', requests_params={'proxies': proxies})
'''

##Simbolos
#BTCEUR
#ETHEUR
#
#
#

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
    csvWriter.writerow( ["timestamp", "BTC", "ETH", "DODGE", ] )  #    csvWriter.writerow( ["timestamp", "BTC", "ETH", "BNB", "DODGE", "DOT"] )
else:
    pass




#############################################################################
#Contadores    min-Max
min_btc=float(client.get_symbol_ticker(symbol="BTCUSDT").get('price'))
max_btc=float(client.get_symbol_ticker(symbol="BTCUSDT").get('price'))
min_eth=float(client.get_symbol_ticker(symbol="ETHUSDT").get('price'))
max_eth=float(client.get_symbol_ticker(symbol="ETHUSDT").get('price'))

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

#####Bucle principal############################################################
fin=0
contador=0
btc_values = []
eth_values = []
moving_averages = []
timestamp=[]
ewma=[]###Esto no furulaaa
while True:
    btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT").get('price'))
    print("BTC: ", btc_price)
    eth_price = float(client.get_symbol_ticker(symbol="ETHUSDT").get('price'))
    print("ETH: ", eth_price)
    print("\n")

    now = datetime.now()
    csvWriter.writerow( [now, btc_price, eth_price] )
    btc_values.append(btc_price)
    eth_values.append(eth_price)
    timestamp.append(now)
    #test_list.pop(0)   to remove the first element


    check_minmax(btc_price, "BTC")

    check_minmax(eth_price, "ETH")

    if contador>0:
        t=threading.Thread(target=__EWMA__())
        t.start()
        t.join()
        #btc_values.pop(0)
        #eth_values.pop(0)

    contador=contador+1
    time.sleep(1)

     #Para esperar a que el hilo termine sus calculos en caso de que no fuera asi
##################################################################################
