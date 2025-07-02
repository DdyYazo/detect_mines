import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Leer CSV con las columnas partida, columna, fila, mina
df = pd.read_csv('minas.csv')

# 2. Filtrar solo las posiciones con mina
df_minas = df[df['mina'] == 1]

# 3. Contar cuántas veces aparece una mina en cada coordenada (columna, fila)
freq = df_minas.groupby(['columna', 'fila']).size().reset_index(name='count')

# 4. Construir una matriz 5×5 con los conteos
matrix = np.zeros((5, 5), dtype=int)
for _, row in freq.iterrows():
    col_idx = int(row['columna']) - 1
    row_idx = int(row['fila']) - 1
    matrix[row_idx, col_idx] = row['count']

# 5. Generar el mapa de calor
plt.figure()
plt.imshow(matrix, aspect='equal')
plt.colorbar(label='Número de minas')
plt.xticks(ticks=np.arange(5), labels=np.arange(1, 6))
plt.yticks(ticks=np.arange(5), labels=np.arange(1, 6))
plt.xlabel('Columna')
plt.ylabel('Fila')
plt.title('Mapa de calor de recurrencia de minas')
plt.show()
