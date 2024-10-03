# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 21:12:29 2024

@author: edson

Mostrar la relación de la tasa de referencia de la FED, la inflación
y el desempleo
"""

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
        
data = pd.read_csv("C:/Users/edson/OneDrive/Documents/FinBurs/index.csv").fillna(method='ffill')
data['Date'] = data['Year'].map(str)+"/"+data['Month'].map(str)+"/"+data['Day'].map(str)

data_index_2007 = data[data.Year>=2005]
data_index_2007 = data_index_2007[data_index_2007.Year<=2017]
data_index_2007 = data_index_2007.set_index("Date")
data_kept_2007 = data_index_2007[['Federal Funds Target Rate','Unemployment Rate','Inflation Rate']]


# Tamaño de la figura
plt.figure(figsize=(20, 10))

# Graficar los datos (asumiendo que data_kept_2007 tiene un índice de fechas)
data_kept_2007.plot()

# Configurar el título y etiquetas de los ejes
plt.title("Economía post-crisis")
plt.xlabel("Fecha")
plt.ylabel("Niveles")

# Rotar las etiquetas del eje X si es necesario
plt.xticks(rotation=45)

# Mostrar leyenda y grid
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()
