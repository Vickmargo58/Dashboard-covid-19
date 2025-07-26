from flask import Blueprint, jsonify, current_app, request # current_app para acceder al engine
from sqlalchemy.sql import text # Para ejecutar consultas SQL
import pandas as pd # Para cualquier procesamiento de datos si es necesario

# Definir el Blueprint para las rutas de COVID-19
covid_bp = Blueprint('covid', __name__)

# Función para formatear grandes números (útil para consistencia)
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    return str(num)

# --- Endpoint 1: Estadísticas Globales ---
@covid_bp.route('/global-stats', methods=['GET'])
def get_global_stats():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION'] # Obtener la fábrica de sesiones

        with Session() as session:
            # Asumiendo que covid_data_unified tiene los datos acumulados
            # Query para obtener los totales más recientes para el mundo (última fecha en la tabla)
            result = session.execute(text("""
                SELECT
                    SUM(confirmed) AS total_confirmed,
                    SUM(deaths) AS total_deaths
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
            """)).fetchone()

            if result:
                total_confirmed = result.total_confirmed if result.total_confirmed is not None else 0
                total_deaths = result.total_deaths if result.total_deaths is not None else 0

                mortality_rate = 0.0
                if total_confirmed > 0:
                    mortality_rate = (total_deaths / total_confirmed) * 100

                # Datos de recuperados no disponibles en el dataset más reciente, como se menciona en tus archivos
                total_recovered = 0 # Valor por defecto, ya que los datos no están disponibles

                response_data = {
                    "confirmed": total_confirmed,
                    "deaths": total_deaths,
                    "mortality_rate": f"{mortality_rate:.2f}",
                    "recovered": total_recovered,
                    "last_update": "Marzo 2023" # O puedes obtener la última fecha de la DB
                }
                return jsonify(response_data), 200
            else:
                return jsonify({"error": "No se encontraron datos globales"}), 404

    except Exception as e:
        current_app.logger.error(f"Error al obtener estadísticas globales: {e}")
        return jsonify({"error": "Error interno del servidor", "message": "No se pudieron cargar las estadísticas globales.", "details": str(e)}), 500

# --- Endpoint 2: Top 10 Países por Casos Confirmados ---
@covid_bp.route('/top-confirmed', methods=['GET'])
def get_top_confirmed():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            # Consulta para los 10 países con más casos confirmados en la última fecha
            result = session.execute(text("""
                SELECT Country_Region, Confirmed
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                AND Confirmed > 0 -- Excluir países sin casos si los hay
                GROUP BY Country_Region, Confirmed -- Agrupar para sumar si hay provincias
                ORDER BY Confirmed DESC
                LIMIT 10
            """)).fetchall()

            top_countries = [
                {"Country_Region": row.Country_Region, "confirmed": row.Confirmed}
                for row in result
            ]
            return jsonify(top_countries), 200

    except Exception as e:
        current_app.logger.error(f"Error al obtener top confirmados: {e}")
        return jsonify({"error": "Error interno del servidor", "message": "No se pudo cargar el top de países por casos confirmados.", "details": str(e)}), 500

# --- Endpoint 3: Top 10 Países por Muertes ---
@covid_bp.route('/top-deaths', methods=['GET'])
def get_top_deaths():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            # Consulta para los 10 países con más muertes en la última fecha
            result = session.execute(text("""
                SELECT Country_Region, Deaths
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                AND Deaths > 0 -- Excluir países sin muertes
                GROUP BY Country_Region, Deaths
                ORDER BY Deaths DESC
                LIMIT 10
            """)).fetchall()

            top_deaths = [
                {"Country_Region": row.Country_Region, "deaths": row.Deaths}
                for row in result
            ]
            return jsonify(top_deaths), 200

    except Exception as e:
        current_app.logger.error(f"Error al obtener top muertes: {e}")
        return jsonify({"error": "Error interno del servidor", "message": "No se pudo cargar el top de países por muertes.", "details": str(e)}), 500

# --- Endpoint 4: Top 10 Países por Tasa de Mortalidad ---
@covid_bp.route('/top-mortality', methods=['GET'])
def get_top_mortality():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            # Consulta para calcular la tasa de mortalidad por país
            # Necesitamos sumar confirmados y muertes por país en la última fecha
            result = session.execute(text("""
                SELECT
                    Country_Region,
                    SUM(Confirmed) AS total_confirmed,
                    SUM(Deaths) AS total_deaths
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                GROUP BY Country_Region
                HAVING SUM(Confirmed) >= 1000 -- Solo países con al menos 1000 casos para una tasa significativa
                ORDER BY (SUM(Deaths)::NUMERIC / SUM(Confirmed)) DESC
                LIMIT 10
            """)).fetchall()

            top_mortality = []
            for row in result:
                if row.total_confirmed > 0:
                    rate = (row.total_deaths / row.total_confirmed) * 100
                    top_mortality.append({
                        "Country_Region": row.Country_Region,
                        "mortality_rate": f"{rate:.2f}"
                    })
            return jsonify(top_mortality), 200

    except Exception as e:
        current_app.logger.error(f"Error al obtener top mortalidad: {e}")
        return jsonify({"error": "Error interno del servidor", "message": "No se pudo cargar el top de países por tasa de mortalidad.", "details": str(e)}), 500


# --- Endpoint 5: Datos de México (Casos Diarios y Promedio Móvil) ---
@covid_bp.route('/mexico-daily', methods=['GET'])
def get_mexico_daily_cases():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            # Obtener datos diarios para México
            # Asegúrate de que Confirmed_Daily y Deaths_Daily se hayan calculado en prepare_covid_data.py
            result = session.execute(text("""
                SELECT Date, Confirmed_Daily, Deaths_Daily
                FROM covid_data_unified
                WHERE Country_Region = 'Mexico'
                ORDER BY Date ASC
            """)).fetchall()

            dates = [row.Date.strftime('%Y-%m-%d') for row in result]
            daily_cases = [row.Confirmed_Daily for row in result]
            daily_deaths = [row.Deaths_Daily for row in result]

            # Calcular promedio móvil de 7 días para casos diarios
            df_mexico = pd.DataFrame({'Date': dates, 'Confirmed_Daily': daily_cases})
            df_mexico['Moving_Average_7_Day'] = df_mexico['Confirmed_Daily'].rolling(window=7, min_periods=1).mean()

            response_data = {
                "dates": df_mexico['Date'].tolist(),
                "daily_cases": df_mexico['Confirmed_Daily'].tolist(),
                "daily_deaths": df_mexico['Deaths_Daily'].tolist(),
                "moving_average_7_day": df_mexico['Moving_Average_7_Day'].tolist()
            }
            return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error al obtener datos diarios de México: {e}")
        return jsonify({"error": "Error interno del servidor", "message": "No se pudieron cargar los datos diarios de México.", "details": str(e)}), 500

# --- Endpoints de Datos para Gráficos (Adaptación para Chart.js frontend) ---
# Tu frontend espera un formato específico para Chart.js
@covid_bp.route('/chart-data/top-confirmed', methods=['GET'])
def chart_top_confirmed():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            result = session.execute(text("""
                SELECT Country_Region, Confirmed
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                AND Confirmed > 0
                GROUP BY Country_Region, Confirmed
                ORDER BY Confirmed DESC
                LIMIT 10
            """)).fetchall()

            labels = [row.Country_Region for row in result]
            values = [row.Confirmed for row in result]

            # Invertir para que el gráfico tenga el más grande arriba
            return jsonify({"labels": labels[::-1], "values": values[::-1]}), 200

    except Exception as e:
        current_app.logger.error(f"Error al preparar datos de gráfico top confirmados: {e}")
        return jsonify({"error": "Error de datos", "message": "No se pudieron preparar los datos para el gráfico de casos confirmados."}), 500

@covid_bp.route('/chart-data/top-deaths', methods=['GET'])
def chart_top_deaths():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            result = session.execute(text("""
                SELECT Country_Region, Deaths
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                AND Deaths > 0
                GROUP BY Country_Region, Deaths
                ORDER BY Deaths DESC
                LIMIT 10
            """)).fetchall()

            labels = [row.Country_Region for row in result]
            values = [row.Deaths for row in result]

            return jsonify({"labels": labels[::-1], "values": values[::-1]}), 200

    except Exception as e:
        current_app.logger.error(f"Error al preparar datos de gráfico top muertes: {e}")
        return jsonify({"error": "Error de datos", "message": "No se pudieron preparar los datos para el gráfico de muertes."}), 500

@covid_bp.route('/chart-data/top-mortality', methods=['GET'])
def chart_top_mortality():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            result = session.execute(text("""
                SELECT
                    Country_Region,
                    SUM(Confirmed) AS total_confirmed,
                    SUM(Deaths) AS total_deaths
                FROM covid_data_unified
                WHERE Date = (SELECT MAX(Date) FROM covid_data_unified)
                GROUP BY Country_Region
                HAVING SUM(Confirmed) >= 1000
                ORDER BY (SUM(Deaths)::NUMERIC / SUM(Confirmed)) DESC
                LIMIT 10
            """)).fetchall()

            labels = []
            values = []
            for row in result:
                if row.total_confirmed > 0:
                    rate = (row.total_deaths / row.total_confirmed) * 100
                    labels.append(row.Country_Region)
                    values.append(float(f"{rate:.2f}")) # Asegurarse de que sea un float

            return jsonify({"labels": labels[::-1], "values": values[::-1]}), 200

    except Exception as e:
        current_app.logger.error(f"Error al preparar datos de gráfico top mortalidad: {e}")
        return jsonify({"error": "Error de datos", "message": "No se pudieron preparar los datos para el gráfico de tasa de mortalidad."}), 500

@covid_bp.route('/chart-data/mexico-daily', methods=['GET'])
def chart_mexico_daily():
    try:
        engine = current_app.config['DB_ENGINE']
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            result = session.execute(text("""
                SELECT Date, Confirmed_Daily
                FROM covid_data_unified
                WHERE Country_Region = 'Mexico'
                ORDER BY Date ASC
            """)).fetchall()

            df_mexico = pd.DataFrame([{"Date": row.Date, "Confirmed_Daily": row.Confirmed_Daily} for row in result])
            df_mexico['Moving_Average_7_Day'] = df_mexico['Confirmed_Daily'].rolling(window=7, min_periods=1).mean()

            response_data = {
                "dates": [d.strftime('%Y-%m-%d') for d in df_mexico['Date'].tolist()], # Formatear fechas a string
                "daily_cases": df_mexico['Confirmed_Daily'].tolist(),
                "moving_average_7_day": df_mexico['Moving_Average_7_Day'].tolist()
            }
            return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error al preparar datos de gráfico diario México: {e}")
        return jsonify({"error": "Error de datos", "message": "No se pudieron preparar los datos para el gráfico diario de México."}), 500
