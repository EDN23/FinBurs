# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:03:54 2024

@author: edson
"""

# Importar librerias
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

# Descargar información histórica
tickers = ['BAC', 'GS', 'JPM', 'MS', 'WFC',"C","LEHKQ"] 


#Elegir fechas
# Pueden poner las fechas que gusten en el formato AAAA-MM-DD
inicio = "2005-01-01"
final = "2017-01-01"

#Crear el data frame y elegir variables
df = yf.download(tickers, start=inicio, end=final) #Esta es la base completa
datos_req = ["Close"] #Aqui pueden poner los datos que quieran usar
df_aj = df[datos_req] #Crea un df con los datos que quieren
df_aj.columns = df_aj.columns.droplevel(0) #elimina la fila Close

# Generar gráfica de todos los tickers
for ticker in tickers: #Va a usar todos los tickers dentro de la lista tickers
    df_aj[ticker].plot(label=ticker) # Crea la gráfica de cierre
plt.title("Precios de Cierre de las Acciones") #título
plt.xlabel("Fecha") #eje x
plt.ylabel("Precio de Cierre") # eje y
plt.legend() # Mostrar la leyenda
plt.grid(True) # Hace una cuadricula
plt.show() # Muestra 


#Genera una gráfica para cada una de las acciones
#Como esta identado hará una gráfica para cada ticker
for ticker in tickers: #Va a usar todos los tickers dentro de la lista tickers
    plt.figure(figsize=(10,6)) #asi crea una grafica para cada accion
    df_aj[ticker].plot(label=ticker,color="red")#Pueden cambiar c
    plt.title(f"Precio de cierre {ticker}") #titulo 
    plt.xlabel("Fecha") #eje x
    plt.ylabel("Precio de cierre") #eje y
    plt.legend() #muestra la leyenda
    plt.grid(True) # hace una cuadricula
    plt.figtext(0.5, 0, "Elaboración propia con datos obtenidos de yahoo finance.", ha="center", fontsize=10)
    plt.show() #muestra el gráfico