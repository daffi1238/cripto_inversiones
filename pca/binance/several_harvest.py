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
    # Do something with the file############################################
except IOError:
    print("El fichero no existe, vamos a generarlo de 0")
    existe=False


file = open("outFile.csv", "a")

csvWriter = csv.writer( file )
if existe==False:
    print("El fichero no existe asi que le añadimos una fila")
    csvWriter.writerow( ["timestamp", "BTC", "ETH"] )  #    csvWriter.writerow( ["timestamp", "BTC", "ETH", "BNB", "DODGE", "DOT"] )
else:
    pass
#############################################################################
#Contadores
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

#####Bucle principal#####
fin=0
while True:
    btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT").get('price'))
    print("BTC: ", btc_price)
    eth_price = float(client.get_symbol_ticker(symbol="ETHUSDT").get('price'))
    print("ETH: ", eth_price)
    print("\n")

    now = datetime.now()
    csvWriter.writerow( [now, btc_price, eth_price] )

    check_minmax(btc_price, "BTC")

    check_minmax(eth_price, "ETH")

    time.sleep(1)
