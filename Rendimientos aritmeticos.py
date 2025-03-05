# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:55:34 2025

@author: edson
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Seleccionar los tickers y las fechas que vamos a utilizar
tickers = ["GOOG","JPM"]
start = "2020-02-25"
end = "2025-02-25"

#Descargar  el
df = yf.download(tickers,start,end)["Close"].round(4)
df.index = df.index.strftime('%Y-%m-%d')

#Vamos a contar cuentos Nan hay por columna 
nan_columna = df.isna().sum()

print(nan_columna)

df1 = df.dropna()
nan_df1 = df1.isna().sum()
print(nan_df1)
print("=====================================")



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
print("=====================================")

    
print("Los riesgos anualizados de cada activo son:")
for activo, riesgo in riesgo_anual_porc.items():
    print(f"{activo}: {riesgo}%")


#Obtenemos e imprimimos los coeficientes de variacion
coef_var = round(riesgo_anual/retornos_esp_anuales,2)
print("=====================================")
print("Los coeficientes de variacion son:")
for activo, coef in coef_var.items():
    print(f"{activo}:{coef}")

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

from scipy.optimize import minimize

#Función para calcular rendimiento del portafolio
def rendimiento(pesos, retornos):
    return np.sum(pesos * retornos)

#Función para calcular el riesgo del portafolio
def riesgo(pesos, matriz_cov):
    return np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))

#Función para minimizar la varianza (Portafolio de mínima varianza)
def objetivo(pesos, matriz_cov):
    return riesgo(pesos, matriz_cov)

#Restricción: Suma de los pesos = 1
def restriccion(pesos):
    return np.sum(pesos) - 1

#Pesos iniciales
pesos_iniciales = np.ones(n_activos) / n_activos

#Definir restricciones
restriccion_dict = {'type': 'eq', 'fun': restriccion}

#Limites para los pesos (0 a 1 para evitar ventas en corto)
limites = tuple((0, 1) for activo in range(n_activos))

#Optimización
optimizacion = minimize(objetivo,
                        pesos_iniciales,
                        args=(matriz_cov),
                        method='SLSQP',
                        constraints=restriccion_dict,
                        bounds=limites)

#Resultados
pesos_optimos = optimizacion.x
rendimiento_optimo = rendimiento(pesos_optimos, retornos_esp_anuales)
riesgo_optimo = riesgo(pesos_optimos, matriz_cov)*252**(1/2)

print("\nPesos Óptimos:")
for activo, peso in zip(retornos_esp_anuales.index, pesos_optimos):
    print(f"{activo}: {peso:.4f}")

print(f"\nRendimiento esperado del portafolio óptimo: {rendimiento_optimo:.4f}")
print(f"Riesgo esperado del portafolio óptimo: {riesgo_optimo:.4f}")


#Graficar la frontera eficiente
# Número de simulaciones
num_simulaciones = 10_000

# Inicializar listas para guardar valores
rendimientos_sim = []
riesgos_sim = []
sharpe_ratios = []
pesos_sim = []

# Simulación de portafolios aleatorios
for _ in range(num_simulaciones):
    pesos = np.random.rand(n_activos)
    pesos /= np.sum(pesos)  # Normalizar para que sumen 1
    
    rendimiento_p = np.sum(pesos * retornos_esp_anuales)
    riesgo_p = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos))) * np.sqrt(252)
    sharpe_p = rendimiento_p / riesgo_p  # Tasa libre de riesgo = 0%

    rendimientos_sim.append(rendimiento_p)
    riesgos_sim.append(riesgo_p)
    sharpe_ratios.append(sharpe_p)
    pesos_sim.append(pesos)

# Convertir listas en arrays
rendimientos_sim = np.array(rendimientos_sim)
riesgos_sim = np.array(riesgos_sim)
sharpe_ratios = np.array(sharpe_ratios)

# Encontrar portafolios óptimos
idx_max_sharpe = np.argmax(sharpe_ratios)  # Índice del máximo Sharpe Ratio
idx_min_varianza = np.argmin(riesgos_sim)  # Índice de la mínima varianza

# Pesos de los portafolios óptimos
pesos_max_sharpe = pesos_sim[idx_max_sharpe]
pesos_min_varianza = pesos_sim[idx_min_varianza]

# Graficar la Frontera Eficiente
plt.figure(figsize=(10, 6))
plt.scatter(riesgos_sim, rendimientos_sim, c=sharpe_ratios, cmap='viridis', alpha=0.5)
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Riesgo (Desviación Estándar)")
plt.ylabel("Rendimiento Esperado")
plt.title("Frontera Eficiente - Simulación Monte Carlo")

# Marcar los portafolios óptimos
plt.scatter(riesgos_sim[idx_max_sharpe], rendimientos_sim[idx_max_sharpe], c='red', marker='*', s=300, label="Máximo Sharpe Ratio")
plt.scatter(riesgos_sim[idx_min_varianza], rendimientos_sim[idx_min_varianza], c='blue', marker='D', s=200, label="Mínima Varianza")

plt.legend()
plt.show()

# Mostrar pesos de los portafolios óptimos
print("\nPesos del Portafolio de Máximo Sharpe Ratio:")
for activo, peso in zip(retornos_esp_anuales.index, pesos_max_sharpe):
    print(f"{activo}: {peso:.4f}")

print("\nPesos del Portafolio de Mínima Varianza:")
for activo, peso in zip(retornos_esp_anuales.index, pesos_min_varianza):
    print(f"{activo}: {peso:.4f}")
