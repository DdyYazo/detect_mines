#!/usr/bin/env python3
import os
import sys
import pandas as pd
import time

def main():
    # 1. Pedir al usuario la ruta del Excel
    excel_path = input("Introduce la ruta al archivo .xlsx con posiciones de minas: ").strip()
    if not os.path.isfile(excel_path):
        print(f"❌ Error: no se encontró el archivo '{excel_path}'")
        sys.exit(1)

    # 2. Cargar el Excel
    df_pos = pd.read_excel(excel_path, engine='openpyxl')
    required = {'partida', 'fila', 'columna'}
    if not required.issubset(df_pos.columns):
        print(f"❌ El archivo debe tener columnas: {required}")
        sys.exit(1)

    # 3. Construir lista de registros (iterando columnas primero)
    registros = []
    for partida, grupo in df_pos.groupby('partida'):
        bombas = set(zip(grupo['columna'], grupo['fila']))
        for col in range(1, 6):
            for fila in range(1, 6):
                registros.append({
                    'partida': partida,
                    'columna': col,
                    'fila':    fila,
                    'mina':    1 if (col, fila) in bombas else 0
                })

    # 4. Crear DataFrame con el orden de columnas deseado
    df_reg = pd.DataFrame(registros, columns=['partida', 'columna', 'fila', 'mina'])

    # 5. Añadir al CSV existente o crearlo si no existe
    salida = 'minas.csv'
    if os.path.exists(salida):
        df_reg.to_csv(salida, mode='a', header=False, index=False, encoding='utf-8')
    else:
        df_reg.to_csv(salida, mode='w', header=True,  index=False, encoding='utf-8')

    print(f"✅ Datos procesados y agregados en '{salida}'")
    print("El programa se cerrará en 10 segundos...")
    time.sleep(10)

if __name__ == "__main__":
    main()
