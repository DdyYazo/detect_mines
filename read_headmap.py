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
    row_idx = int(row['fila'])    - 1
    matrix[row_idx, col_idx] = row['count']

# 5. Generar el mapa de calor con anotaciones
fig, ax = plt.subplots()
cax = ax.imshow(matrix, aspect='equal')

# Añadir anotaciones de los conteos en cada casilla
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax.text(j, i, matrix[i, j],
                ha='center', va='center',
                color="#e63636" if matrix[i, j] > matrix.max()/2 else "white")

# Ajustes de ejes y colorbar
ax.set_xticks(np.arange(5))
ax.set_yticks(np.arange(5))
ax.set_xticklabels(np.arange(1, 6))
ax.set_yticklabels(np.arange(1, 6))
ax.set_xlabel('Columna')
ax.set_ylabel('Fila')
ax.set_title('Mapa de calor de recurrencia de minas')
fig.colorbar(cax, label='Número de minas')

plt.tight_layout()
plt.show()
