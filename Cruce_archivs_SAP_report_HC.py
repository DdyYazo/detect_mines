#!/usr/bin/env python
# coding: utf-

import pandas as pd
import os
from tabulate import tabulate
import time
import logging
# modulos internos

# openpyxl
# xlsxwriter

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para archivo (todos los niveles)
fh = logging.FileHandler('extractor.log')
fh.setLevel(logging.DEBUG)
# Handler para consola (solo errores)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

""" Construccion de funciones auxiliares """
# 1. Funcion para obtener la lista de archivos .xlsx
def get_excel_files(folder_path):
    """
    Retorna la lista de archivos .xlsx (sin importar mayúsculas/minúsculas)
    encontrados en folder_path.
    """
    try:
        files = [os.path.join(folder_path, file)
                 for file in os.listdir(folder_path)
                 if file.lower().endswith('.xlsx')]
        logger.info(f"Found {len(files)} Excel files in {folder_path}")
        return files
    except Exception:
        logger.exception("Error in get_excel_files")
        raise

# 2. Funcion para obtener los archivos requeridos
def get_target_files(excel_files):
    """
    Busca en la lista de archivos los que correspondan a los nombres requeridos.
    Retorna un diccionario con la ruta de cada archivo.
    """
    target_names = {
        "me2n hc.xlsx": None,
        "mb51 hc.xlsx": None,
        "facturas hc.xlsx": None
    }
    try:
        for file in excel_files:
            basename = os.path.basename(file).lower()
            if basename in target_names:
                target_names[basename] = file

        for key, path in target_names.items():
            if path is None:
                logger.error(f"Missing required file: {key}")
                raise FileNotFoundError(f"Falta el archivo: {key}")
        logger.info("All target files found")
        return target_names
    except Exception:
        logger.exception("Error in get_target_files")
        raise

# 3. Funcion para leer los archivos Excel
def read_excel_files(target_names):
    """
    Lee cada uno de los tres archivos en la hoja "Sheet1" y retorna
    los tres DataFrames.
    """
    try:
        logger.info("Reading Excel files...")
        print("\nLeyendo los archivos Excel:")
        df_me2n = pd.read_excel(target_names["me2n hc.xlsx"], sheet_name="Sheet1")
        df_mb51 = pd.read_excel(target_names["mb51 hc.xlsx"], sheet_name="Sheet1")
        df_facturas = pd.read_excel(target_names["facturas hc.xlsx"], sheet_name="Sheet1")
        logger.info("Excel files read successfully")
        return df_me2n, df_mb51, df_facturas
    except Exception:
        logger.exception("Error reading Excel files")
        raise

# 4. Funcion para formatear valores
def format_val(x):
    """
    Convierte el valor a string evitando decimales innecesarios:
    Si es float sin parte decimal, se convierte a int antes.
    """
    try:
        if isinstance(x, float) and x.is_integer():
            return str(int(x))
        return str(x)
    except Exception:
        logger.exception("Error in format_val")
        return str(x)

# 5. Funcion para agregar la columna CONCATENAR
def add_concat_field(df, field1, field2, delimiter="-"):
    """
    Agrega al DataFrame la columna 'CONCATENAR' concatenando field1 y field2
    usando el delimitador dado "-" (se consideran field1 y field2 debido a la relacion entre dos campos de los archivos).
    """
    try:
        df["CONCATENAR"] = df[field1].apply(format_val) + delimiter + df[field2].apply(format_val)
        logger.info(f"Added CONCATENAR field using {field1} and {field2}")
        return df
    except Exception:
        logger.exception("Error in add_concat_field")
        raise

# 6. Funcion para procesar ME2N HC
def process_me2n(df_me2n):
    """
    Selecciona y renombra las columnas requeridas para ME2N.
    Se asume que ya se creó la columna CONCATENAR.
    """
    try:
        df = df_me2n[[
            "CONCATENAR",
            "Contrato marco",
            "Proveedor/Centro suministrador",
            "Documento compras",
            "Fecha documento",
            "Texto breve",
            "Indicador de borrado"
        ]].copy()
        df = df.rename(columns={
            "Documento compras": "Numero Pedido",
            "Fecha documento": "Fecha creacion PO",
            "Texto breve": "Texto PO"
        })
        logger.info("Processed ME2N dataframe")
        return df
    except Exception:
        logger.exception("Error in process_me2n")
        raise

""" Funciones para tomar los datos requeridos de los archivos """

# 7. Funcion para procesar MB51 HC
def process_mb51(df_mb51):
    """
    Selecciona y renombra las columnas requeridas para MB51.
    Se busca el campo 'Texto EA' entre "Cuenta de mayor" y "Indicador Debe/Haber".
    """
    try:
        mb51_cols = list(df_mb51.columns)
        try:
            idx_start = mb51_cols.index("Cuenta de mayor")
            idx_end = mb51_cols.index("Indicador Debe/Haber")
            texto_ea_col = None
            for col in mb51_cols[idx_start+1:idx_end]:
                if col.strip().lower() == "texto":
                    texto_ea_col = col
                    break
            if texto_ea_col is None:
                texto_ea_col = "Texto"
        except ValueError:
            texto_ea_col = "Texto"

        df = df_mb51[[
            "CONCATENAR",
            "Fe.contabilización",
            texto_ea_col,
            "Documento material"
        ]].copy()
        df = df.rename(columns={
            "Fe.contabilización": "Fecha creacion EA",
            texto_ea_col: "Texto EA",
            "Documento material": "Numero EA"
        })
        df = df.drop_duplicates(subset=["CONCATENAR"])
        logger.info("Processed MB51 dataframe")
        return df
    except Exception:
        logger.exception("Error in process_mb51")
        raise

# 8. Funcion para procesar FACTURAS HC
def process_facturas(df_facturas):
    """
    Selecciona y renombra la columna requerida para FACTURAS.
    Se toma el primer campo "Referencia" y se renombra a "Factura".
    """
    try:
        df = df_facturas[["CONCATENAR", "Referencia"]].copy()
        df = df.rename(columns={"Referencia": "Factura"})
        df = df.drop_duplicates(subset=["CONCATENAR"])
        logger.info("Processed FACTURAS dataframe")
        return df
    except Exception:
        logger.exception("Error in process_facturas")
        raise

# 9. Funcion para realizar el merge de los DataFrames
def merge_dataframes(df_me2n_sel, df_mb51_sel, df_facturas_sel):
    """
    Realiza el merge de los DataFrames usando ME2N como base (left join).
    """
    try:
        df_merge = df_me2n_sel.merge(df_mb51_sel, on="CONCATENAR", how="left") \
                              .merge(df_facturas_sel, on="CONCATENAR", how="left")
        logger.info(f"Merged dataframes, final record count: {len(df_merge)}")
        return df_merge
    except Exception:
        logger.exception("Error in merge_dataframes")
        raise

# 10. Funcion para finalizar el merge con el formateo de fechas
def finalize_merge(df_merge):
    """
    Convierte las fechas, calcula la diferencia en días y formatea las fechas a dd/mm/yyyy.
    """
    try:
        df_merge["Fecha creacion PO"] = pd.to_datetime(df_merge["Fecha creacion PO"], errors="coerce")
        df_merge["Fecha creacion EA"] = pd.to_datetime(df_merge["Fecha creacion EA"], errors="coerce")
        df_merge["Diferencia Dias"] = (df_merge["Fecha creacion EA"] - df_merge["Fecha creacion PO"]).dt.days

        df_merge["Fecha creacion PO"] = df_merge["Fecha creacion PO"].dt.strftime("%d/%m/%Y")
        df_merge["Fecha creacion EA"] = df_merge["Fecha creacion EA"].dt.strftime("%d/%m/%Y")
        logger.info("Finalized merge dataframe")
        return df_merge
    except Exception:
        logger.exception("Error in finalize_merge")
        raise

# 11. Funcion para guardar el reporte final en la ruta que sea indicada por el usuario
def save_report(df_final, folder_path):
    """
    Guarda el DataFrame final en un archivo Excel con autofiltro.
    """
    try:
        output_filename = os.path.join(folder_path, "Reporte PO-EA.xlsx")
        with pd.ExcelWriter(output_filename, engine="xlsxwriter", date_format='dd/mm/yyyy') as writer:
            df_final.to_excel(writer, index=False, sheet_name="Reporte")
            workbook  = writer.book
            worksheet = writer.sheets["Reporte"]
            (max_row, max_col) = df_final.shape
            worksheet.autofilter(0, 0, max_row, max_col - 1)
        logger.info(f"Report saved successfully at {output_filename}")
        print("\nReporte generado y guardado en:", output_filename)
    except Exception:
        logger.exception("Error in save_report")
        raise

# Funcion principal
def main():
    try:
        # Solicitar la ruta de la carpeta al usuario
        folder_input = input("Ingrese la ruta de la carpeta que contiene los archivos de Excel generados desde SAP: ").strip()
        folder_path = os.path.abspath(os.path.join(folder_input))
        logger.info(f"Using folder: {folder_path}")
        print("Ruta de la carpeta:", folder_path)

        # Obtener la lista de archivos Excel y mostrarlos
        excel_files = get_excel_files(folder_path)
        print("Archivos Excel encontrados en la carpeta:")
        for file in excel_files:
            print(file)

        # Obtener los archivos requeridos
        target_names = get_target_files(excel_files)

        # Leer cada uno de los archivos en la hoja "Sheet1"
        df_me2n, df_mb51, df_facturas = read_excel_files(target_names)

        # Agregar la columna CONCATENAR en cada DataFrame
        df_me2n = add_concat_field(df_me2n, "Documento compras", "Posición")
        df_mb51  = add_concat_field(df_mb51, "Pedido", "Posición")
        df_facturas = add_concat_field(df_facturas, "Documento compras", "Posición")

        logger.info(f"Registros en ME2N: {len(df_me2n)}")
        logger.info(f"Registros en MB51: {len(df_mb51)}")
        logger.info(f"Registros en FACTURAS: {len(df_facturas)}")
        print("Registros en ME2N:", len(df_me2n))
        print("Registros en MB51:", len(df_mb51))
        print("Registros en FACTURAS:", len(df_facturas))

        # Procesar cada DataFrame para seleccionar y renombrar columnas
        df_me2n_sel = process_me2n(df_me2n)
        df_mb51_sel = process_mb51(df_mb51)
        df_facturas_sel = process_facturas(df_facturas)

        # Realizar el merge usando ME2N como base
        df_merge = merge_dataframes(df_me2n_sel, df_mb51_sel, df_facturas_sel)
        print("Registros en el merge final:", len(df_merge))

        # Finalizar el merge: convertir fechas, calcular diferencia y formatear
        df_merge = finalize_merge(df_merge)

        # Seleccionar las columnas finales en el orden requerido,
        # agregando la columna "Indicador de borrado" (de ME2N) para filtrado
        final_columns = [
            "Contrato marco",
            "Proveedor/Centro suministrador",
            "Numero Pedido",
            "Fecha creacion PO",
            "Fecha creacion EA",
            "Diferencia Dias",
            "Factura",
            "Texto PO",
            "Texto EA",
            "Numero EA",
            "Indicador de borrado"
        ]
        df_final = df_merge[final_columns].copy()

        # Guardar el reporte final en un nuevo archivo Excel con autofiltro
        save_report(df_final, folder_path)

        print("\nRecuerda realizar la limpieza del Reporte generado eliminando columnas duplicadas y dando formato a la tabla")
        print("\nCerrando ventana en 15 segundos...")
        time.sleep(15)
    except Exception:
        logger.exception("Unhandled exception in main")
        print("Ocurrió un error. Revisa el archivo de log para más detalles.")
        time.sleep(15)

if __name__ == '__main__':
    main()
