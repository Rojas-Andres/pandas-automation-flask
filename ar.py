import csv
import io 

ar ='csv.csv'
#f = open(ar, "r")
f = r"D:\Andres\automatizacion"
#f = f+f"\{ar}"
f = io.open(ar, mode="r", encoding="utf-8")


print(type(f))
#print(csv)
datos = csv.reader(f,delimiter=';')
print(datos)
'''
datos = csv.reader(f,delimiter=';')
for linea in datos:
    print(linea)
'''
#with open('csv.csv') as archivo:
#    datos = csv.reader(archivo,delimiter=';')
#    for linea in datos:
#        print(linea)