#Script para obtener la media del valor del bitcoin a cada minuto
#script para obtener el valor del bitcoin a cada segundo
import cryptocompare
from datetime import datetime
import csv
import time
import numpy as np

file = open("outFile.csv", "a")
csvWriter = csv.writer( file )

cryptocompare.get_price('BTC')

for x in range(10):#10 minutos
    minuto=datetime.now().minute
    valor_btc=[]

    i=1
    while i<60:  #Lo idoneo sería 60, pero por condición de carrera pudiera fallar
        now = datetime.now()
        if(now.minute==minuto):
            print("El valor de minuto: " + str(now.minute))
            #print("El valor de la moneda " + str(cryptocompare.get_price('BTC')['BTC']['EUR'])
            valor_btc.append(cryptocompare.get_price('BTC')['BTC']['EUR'])
        else:
            print("El valor de minuto dentro del else: " + str(now.minute))
            print("El valor de i "+str(i) + "El valor del sumatorio: "+str(sum(valor_btc)))
            media_minuto=np.sum(valor_btc)/i
            fecha=str(now.year) +'/'+str(now.month)+'/'+str(now.day)+'/'+str(now.minute)
            csvWriter.writerow( [fecha, media_minuto] )

            print("El valor de la media en el minuto " + str(now.minute) +" es " + str(media_minuto))

            i=60#para salir del for interno
        i+=1
        print("ciclo interno")
        time.sleep(1)
    print("Ciclo externo")
