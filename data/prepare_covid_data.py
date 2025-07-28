import pandas as pd
from sqlalchemy import create_engine
import os

# Rutas de los archivos CSV
confirmed_path = 'time_series_covid19_confirmed_global.csv'
deaths_path = 'time_series_covid19_deaths_global.csv'
recovered_path = 'time_series_covid19_recovered_global.csv'

# Columnas de identificación que no son fechas
id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']

# --- Función auxiliar para cargar y despivotar un archivo ---
def load_and_melt(filepath, value_name):
    df = pd.read_csv(filepath)
    # Despivotar todas las columnas que no están en id_vars
    df_melted = df.melt(id_vars=id_vars, var_name='Date', value_name=value_name)
    return df_melted

# --- Cargar y despivotar cada dataset ---
print("Cargando y despivotando datos confirmados...")
df_confirmed = load_and_melt(confirmed_path, 'Confirmed')
print("Cargando y despivotando datos de decesos...")
df_deaths = load_and_melt(deaths_path, 'Deaths')
print("Cargando y despivotando datos recuperados...")
df_recovered = load_and_melt(recovered_path, 'Recovered')

# --- Unir los datasets en una única tabla ---
print("Uniendo los datasets...")
# Unir confirmados y decesos
df_unified = pd.merge(df_confirmed, df_deaths, on=id_vars + ['Date'], how='left')
# Unir el resultado con recuperados
df_unified = pd.merge(df_unified, df_recovered, on=id_vars + ['Date'], how='left')

# --- Limpieza y formateo de datos ---
print("Limpiando y formateando datos...")
# Convertir la columna 'Date' a formato de fecha
df_unified['Date'] = pd.to_datetime(df_unified['Date'], format='%m/%d/%y')

# Renombrar columnas para evitar caracteres especiales y facilitar el uso en SQL/Superset
df_unified = df_unified.rename(columns={
    'Province/State': 'Province_State',
    'Country/Region': 'Country_Region'
})

# Reemplazar valores NaN (no un número) con 0 y asegurar tipo entero para métricas
df_unified['Deaths'] = df_unified['Deaths'].fillna(0).astype(int)
df_unified['Recovered'] = df_unified['Recovered'].fillna(0).astype(int)
df_unified['Confirmed'] = df_unified['Confirmed'].fillna(0).astype(int)

# --- Crear métricas diarias (diferencias día a día) ---
print("Calculando métricas diarias...")
# Asegurar el orden de los datos para un cálculo correcto de diferencias
df_unified = df_unified.sort_values(by=['Country_Region', 'Province_State', 'Date'])

# Calcular casos diarios, decesos diarios y recuperados diarios
df_unified['Confirmed_Daily'] = df_unified.groupby(['Country_Region', 'Province_State'])['Confirmed'].diff().fillna(0).astype(int)
df_unified['Deaths_Daily'] = df_unified.groupby(['Country_Region', 'Province_State'])['Deaths'].diff().fillna(0).astype(int)
df_unified['Recovered_Daily'] = df_unified.groupby(['Country_Region', 'Province_State'])['Recovered'].diff().fillna(0).astype(int)

# Asegurarse de que los valores diarios no sean negativos (los datos fuente a veces pueden tener pequeñas inconsistencias)
df_unified['Confirmed_Daily'] = df_unified['Confirmed_Daily'].apply(lambda x: max(0, x))
df_unified['Deaths_Daily'] = df_unified['Deaths_Daily'].apply(lambda x: max(0, x))
df_unified['Recovered_Daily'] = df_unified['Recovered_Daily'].apply(lambda x: max(0, x))


# --- Crear una tabla de calendario ---
print("Creando tabla de calendario...")
# Obtener el rango de fechas de tus datos unificados
min_date = df_unified['Date'].min()
max_date = df_unified['Date'].max()
date_range = pd.date_range(start=min_date, end=max_date, freq='D')
df_calendar = pd.DataFrame({'Date': date_range})

# Añadir columnas útiles a la tabla calendario
df_calendar['Year'] = df_calendar['Date'].dt.year
df_calendar['Month'] = df_calendar['Date'].dt.month
df_calendar['Day'] = df_calendar['Date'].dt.day
df_calendar['DayOfWeek'] = df_calendar['Date'].dt.dayofweek # Lunes=0, Domingo=6
df_calendar['WeekOfYear'] = df_calendar['Date'].dt.isocalendar().week.astype(int)
df_calendar['MonthName'] = df_calendar['Date'].dt.month_name()
df_calendar['Quarter'] = df_calendar['Date'].dt.quarter


# --- Guardar los datos procesados en PostgreSQL ---
print("Conectando a PostgreSQL y guardando datos...")


# Tu cadena de conexión de Supabase (ASEGÚRATE DE REEMPLAZAR [YOUR-PASSWORD] CON TU CONTRASEÑA REAL)
SUPABASE_CONNECTION_STRING = "postgresql://postgres:iNyNoz4nA3fD6xmL@db.yahulcmoumuaadhzwyrq.supabase.co:5432/postgres"

# SQLAlchemy URI para PostgreSQL
engine = create_engine(SUPABASE_CONNECTION_STRING)


# Guardar la tabla unificada de COVID-19
print(f"Guardando datos unificados en la tabla 'covid_data_unified' en PostgreSQL...")
df_unified.to_sql('covid_data_unified', engine, if_exists='replace', index=False)

# Guardar la tabla calendario
print(f"Guardando tabla de calendario en la tabla 'calendar' en PostgreSQL...")
df_calendar.to_sql('calendar', engine, if_exists='replace', index=False)

# Cierra la conexión
engine.dispose()
print("¡Preparación de datos completada exitosamente en PostgreSQL!")
