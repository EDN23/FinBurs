# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:13:00 2025

@author: edson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("/Users/edson/iCloudDrive/Octavo Semestre/Portafolios de inversión/Libro1.csv")

# Limpiar y convertir datos
df["IPyC"] = df["IPyC"].str.replace(",", "").str.strip()
df["IPyC"] = pd.to_numeric(df["IPyC"], errors="coerce")  # Manejo de errores

# Convertir Fecha a índice
df = df.set_index("Fecha")

# Eliminar NaN
df.dropna(inplace=True)

# Calcular rendimientos aritméticos
retornos = df.pct_change().dropna().round(4)

# Calcular rendimiento esperado y riesgo
retornos_esp_diarios = retornos.mean() #diarios
retornos_esp_anuales = retornos.mean() * 252 #anualizados
retornos_esp_anuales_porc = round(retornos_esp_anuales*100,2)
 

riesgo = retornos.std(ddof=0)*np.sqrt(252)
riesgo_anual = retornos.std(ddof=0)*np.sqrt(252)
riesgo_anual_porc = round(retornos_esp_anuales*100,2)

# Imprimir resultados de cada uno de los activos
print("Los rendimientos esperados anualizados de cada activo son:")
for activo, rendimiento in retornos_esp_anuales_porc.items():
    print(f"{activo}: {rendimiento}%")
    
print("Los riesgos anualizados de cada activo son:")
for activo, riesgo in riesgo_anual_porc.items():
    print(f"{activo}: {riesgo}%")

coef_var = round(riesgo_anual/retornos_esp_anuales,2)
print(f"Los coeficientes de variacion son: \n{coef_var}")

#Obtener la matriz de covarianzas
matriz_cov = retornos.cov() * 252  # Matriz de covarianza anualizada

#Graficar la matriz
plt.figure(figsize=(8,6))
sns.heatmap(matriz_cov, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Matriz de Covarianza")
plt.show()



