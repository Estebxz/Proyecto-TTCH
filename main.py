import glob
import pandas as pd
import numpy as np

path = "C:\\Users\\USER\\Code\\proyecto-TTCH\\data"
archives = glob.glob(f"{path}\\*.csv")

df_raw = pd.concat((pd.read_csv(f) for f in archives), ignore_index=True)

Nulls = df_raw.isnull().sum().sum()
Duplicated = df_raw.duplicated().sum()
NaNs = df_raw.isna().sum().sum()

df_raw.columns = df_raw.columns.str.replace(" ", "_")

df_raw = df_raw.rename(columns={
    "time_(ms)": "Duracion_(ms)",
    "_surface": "Superficie",
    "_speed": "Velocidad",
    "_eval_id": "Evaluacion_ID",
})

orden_base = [
    "Duracion_(ms)",
    "Duracion_(s)",
    "Evaluacion_ID",
    "Superficie",
    "Superficie_ID",
    "Velocidad",
    "Frecuencia_(Hz)",
    "Longitud_zancada_(mm)",
    "_BL_x_(N)", "_BL_y_(N)", "_BL_z_(N)",
    "_BR_x_(N)", "_BR_y_(N)", "_BR_z_(N)",
    "_FL_x_(N)", "_FL_y_(N)", "_FL_z_(N)",
    "_FR_x_(N)", "_FR_y_(N)", "_FR_z_(N)"
]

df_raw = df_raw.reindex(columns=orden_base)

df_raw["Duracion_(s)"] = df_raw["Duracion_(ms)"] / 1000

df_raw["Frecuencia_(Hz)"] = np.select(
    [
    df_raw["Velocidad"].between(0, 1, inclusive="both"),
    df_raw["Velocidad"].between(2, 3, inclusive="both"),
    df_raw["Velocidad"].between(4, 5, inclusive="both"),
    ], [0.125, 0.1875, 0.25],
    default= 0.025
)

df_raw["Longitud_zancada_(mm)"] = np.select(
    [
        df_raw["Velocidad"].isin([2, 4, 6]),
        df_raw["Velocidad"].isin([1, 3, 5])
    ],
    [80, 120],
    default=np.nan  
)

df_raw["Superficie"] = df_raw["Superficie"].replace({
    0: "Concreto",
    1: "Cesped",
    2: "Grava",
    3: "Mantillo",
    4: "Tierra",
    5: "Arena"
})

df_raw["Superficie_ID"] = df_raw["Superficie"].map({
    "Concreto": 0,
    "Cesped": 1,
    "Grava": 2,
    "Mantillo": 3,
    "Tierra": 4,
    "Arena": 5
})

print("-"*50)
print(f"Archivos encontrados: {len(archives)}")
print("-"*50)
print("========== INFORME DEL DATASET ==========\n")
print("Dimensiones del DataFrame:")
print(f"Filas: {df_raw.shape[0]}")
print(f"Columnas: {df_raw.shape[1]}")
print("Nombres de columnas:", df_raw.columns.tolist())
print("-"*50)
print("Resumen estadístico:")
print(f"Nulos: {Nulls}")
print(f"Duplicados: {Duplicated}")
print(f"NaNs: {NaNs}")
print("-"*50)
print("Columnas y sus tipos de datos:")
for col, dtype in zip(df_raw.columns, df_raw.dtypes):
    print(f"- {col}: {dtype}")
print("-"*50)
print("DataFrame principal:")
print(df_raw)
print("-"*50)
df_raw.to_csv("data/df_raw_sensor.csv", index=False, encoding="utf-8", sep=",")
df_check = pd.read_csv("data/df_raw_sensor.csv")
df_check.head()
print("-"*50)