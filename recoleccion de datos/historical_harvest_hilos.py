#Script para obtener el precio historico por dia, hora minuto
#https://pypi.org/project/cryptocompare/
import cryptocompare
#from datetime import datetime
import datetime

import csv
import time
import numpy as np
#Para la función crear_dir
import os
import errno

import threading
threads=10

def main():
    #Una lista de todas todas las monedas
    coins=cryptocompare.get_coin_list(format=True)
    coins=['ETH']

    #Definimos una fecha inicial y calculamos la distancia de días con la actual
    print("Definiendo la fecha inicial:")
    from datetime import date
    date0 = date(2021, 1, 1)
    today = date.today()
    delta = today - date0
    print(delta.days)
    print (date0)

    #date0 = datetime(2021, 1, 1)

    #Obtenemos el historico de precios, uno por día
    for i in coins:
        #Creamos los directrios para cada moneda y los ficheros respectivos
        crear_dir(i)#Creamos un directorio con el nombre de la moneda

        file = open(str(i)+"/"+"outFile.csv", "a")
        csvWriter = csv.writer( file )

        header = ['Nombre', 'Fecha', 'Precio']
        csvWriter.writerow( header )

        fecha=date0
        j=1
        print("Antes de while")
        while j < int(delta.days):
                print("Dentro del while con valor de delta.days: ",delta.days)
                for k in range(threads):
                    if(j<=int(delta.days)):
                        print("Hilo nº ",k)
                        t=threading.Thread(target=func_hilo(fecha, i, csvWriter))
                        t.start()
                        fecha += datetime.timedelta(days=1)
                        j=j+1
                        print("EL VALOR DE J: ", j)
                    else:
                        pass
#        for j in range(int(delta.days)):#Repito el for tantas veces como días de distancia entre la fecha inicial y la actual halla
#            print("Desplegando hilos para j = ",j)
#            for k in range(threads):
#                print("Hilo nº ",k)
#                t=threading.Thread(target=func_hilo(fecha, i, csvWriter))
#                t.start()
#                fecha += datetime.timedelta(days=1)
#                j=50
#                print("EL VALOR DE J: ", j)


def crear_dir(nombre_dir):
    print("Creando el directorio ", nombre_dir)
    try:
        os.mkdir(nombre_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
#    pass

def func_hilo(fecha, i, csvWriter):
    print("Precios para la fecha: ", str(fecha))
    precio=cryptocompare.get_historical_price(i, 'USD', fecha)
    data=[i, fecha, precio]
    csvWriter.writerow( data)

    print("Antes de sumarle un dia a la fecha")
    print(type(fecha))


main()
