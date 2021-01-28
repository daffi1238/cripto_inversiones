#Script para obtener el precio historico por dia, hora minuto
#https://pypi.org/project/cryptocompare/
import cryptocompare
from datetime import datetime
import csv
import time
import numpy as np

file = open("historical_outFile.csv", "a")
csvWriter = csv.writer( file )

#Una lista de todas todas las monedas
coins=cryptocompare.get_coin_list(format=True)
coins=['ETH']

#Definimos una fecha inicial y calculamos la distancia de días con la actual
from datetime import date
date0 = date(2021, 1, 1)
today = date.today()
delta = today - date0
print(delta.days)

#Obtenemos el historico de precios, uno por día
for i in coins:
    cryptocompare.get_price(i)
    fecha=datetime(2021,1,1)
    for j in range(delta):#Repito el for tantas veces como días de distancia entre la fecha inicial y la actual halla
        print("Precios para la fecha: ", str(fecha))
        cryptocompare.get_historical_price(i, 'USD', date0)
        fecha += datetime.timedelta(days=1)


date = datetime.datetime(2003,8,1)
for i in range(5):
    date += datetime.timedelta(days=1)
    print(date)
