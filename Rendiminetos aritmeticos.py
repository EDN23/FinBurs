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
df = df.drop("IPyC", axis=1)

# Eliminar NaN
df.dropna(inplace=True)

# Calcular rendimientos aritméticos
retornos = df.pct_change().dropna().round(4)

# Calcular rendimiento esperado y riesgo
retornos_esp_diarios = retornos.mean() #diarios
retornos_esp_anuales = retornos.mean() * 252 #anualizados
retornos_esp_anuales_porc = round(retornos_esp_anuales*100,2)
 

riesgo = retornos.std(ddof=0)
riesgo_anual = retornos.std(ddof=0)*np.sqrt(252)
riesgo_anual_porc = round(riesgo_anual*100,2)

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
matriz_cov = retornos.cov()

#Graficar la matriz
plt.figure(figsize=(8,6))
sns.heatmap(matriz_cov, annot=True, fmt=".5f", cmap="coolwarm", linewidths=0.5)
plt.title("Matriz de Covarianza")
plt.show()

#Ahora hay que asignar pesos a los activos
def generar_pesos(n):
    pesos = np.random.rand(n)  # Genera n números aleatorios entre 0 y 1
    pesos /= pesos.sum()  # Normaliza para que sumen 1
    return pesos

# Pesos aleatorios
n_activos = len(retornos_esp_anuales)
pesos_aleatorios = generar_pesos(n_activos)
pesos_aleat_porc = pesos_aleatorios*100

# Imprimir los pesos aleatorios junto a sus tickers
print("Pesos Aleatorios:")
for activo, peso in zip(retornos_esp_anuales.index, pesos_aleat_porc):
    print(f"{activo}: {peso:.4f}%")
print("Suma de Pesos:", round(pesos_aleatorios.sum(), n_activos))  # Debe ser 1

#Obtener rendimiento y riesgo del portafolio
rendimiento_portafolio = (pesos_aleatorios * retornos_esp_anuales).sum()
print(f"Rendimiento esperado del portafolio: {rendimiento_portafolio:.4f}")








