# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 18:35:10 2024

@author: edson
"""
import matplotlib.pyplot as plt
import pandas as pd

#Coeficiente de Ginni
df = pd.read_csv("C:/Users/edson/OneDrive/Documents/FinBurs/gini.csv")
df_con_indice = df.set_index("Año")


df_con_indice.plot()#Pueden cambiar c
plt.title("Coeficiente Ginni EEUU") #título
plt.xlabel("año") #eje x
plt.xticks(rotation=45)
plt.ylabel("Ginni") # eje y
plt.legend() # Mostrar la leyenda
plt.grid(True) # Hace una cuadricula
plt.figtext(0.5, -0.2, "Elaboración propia con datos obtenidos del Banco Mundial", ha="center", fontsize=10)

plt.show() # Muestra 