from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.sql import text
import pandas as pd

# Definir el Blueprint para las rutas de COVID-19
covid_bp = Blueprint('covid', __name__)

# Función para formatear grandes números (útil para consistencia)
def format_large_number(num):
    if num is None: # Manejo si el número es None
        return "0"
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
        Session = current_app.config['DB_SESSION']

        with Session() as session:
            # CORREGIDO: Usar 'confirmed', 'deaths', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT
                    SUM(confirmed) AS total_confirmed,
                    SUM(deaths) AS total_deaths
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
            """)).fetchone()

            if result:
                total_confirmed = result.total_confirmed if result.total_confirmed is not None else 0
                total_deaths = result.total_deaths if result.total_deaths is not None else 0

                mortality_rate = 0.0
                if total_confirmed > 0:
                    mortality_rate = (total_deaths / total_confirmed) * 100

                # Datos de recuperados no disponibles en el dataset más reciente, como se menciona en tus archivos
                total_recovered = 0 # Valor por defecto

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
            # CORREGIDO: Usar 'country_region', 'confirmed', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT country_region, confirmed
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                AND confirmed > 0
                GROUP BY country_region, confirmed
                ORDER BY confirmed DESC
                LIMIT 10
            """)).fetchall()

            top_countries = [
                {"Country_Region": row.country_region, "confirmed": row.confirmed} # Mapear al nombre original si el frontend lo espera
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
            # CORREGIDO: Usar 'country_region', 'deaths', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT country_region, deaths
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                AND deaths > 0
                GROUP BY country_region, deaths
                ORDER BY deaths DESC
                LIMIT 10
            """)).fetchall()

            top_deaths = [
                {"Country_Region": row.country_region, "deaths": row.deaths} # Mapear al nombre original si el frontend lo espera
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
            # CORREGIDO: Usar 'country_region', 'confirmed', 'deaths', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT
                    country_region,
                    SUM(confirmed) AS total_confirmed,
                    SUM(deaths) AS total_deaths
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                GROUP BY country_region
                HAVING SUM(confirmed) >= 1000
                ORDER BY (SUM(deaths)::NUMERIC / SUM(confirmed)) DESC
                LIMIT 10
            """)).fetchall()

            top_mortality = []
            for row in result:
                if row.total_confirmed > 0:
                    rate = (row.total_deaths / row.total_confirmed) * 100
                    top_mortality.append({
                        "Country_Region": row.country_region, # Mapear al nombre original si el frontend lo espera
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
            # CORREGIDO: Usar 'date', 'confirmed_daily', 'deaths_daily', 'country_region' en MINÚSCULAS
            result = session.execute(text("""
                SELECT date, confirmed_daily, deaths_daily
                FROM covid_data_unified
                WHERE country_region = 'Mexico'
                ORDER BY date ASC
            """)).fetchall()

            dates = [row.date.strftime('%Y-%m-%d') for row in result]
            daily_cases = [row.confirmed_daily for row in result]
            daily_deaths = [row.deaths_daily for row in result]

            # Calcular promedio móvil de 7 días para casos diarios
            df_mexico = pd.DataFrame({'Date': dates, 'Confirmed_Daily': daily_cases}) # Ojo: aquí pandas crea el DF con estos nombres, está bien.
            df_mexico['Moving_Average_7_Day'] = df_mexico['Confirmed_Daily'].rolling(window=7, min_periods=1).mean()

            response_data = {
                "dates": df_mexico['Date'].tolist(), # Aquí usas 'Date' del DataFrame, no de la DB directamente
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
            # CORREGIDO: Usar 'country_region', 'confirmed', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT country_region, confirmed
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                AND confirmed > 0
                GROUP BY country_region, confirmed
                ORDER BY confirmed DESC
                LIMIT 10
            """)).fetchall()

            labels = [row.country_region for row in result] # Usar el nombre de columna del resultado de la DB
            values = [row.confirmed for row in result] # Usar el nombre de columna del resultado de la DB

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
            # CORREGIDO: Usar 'country_region', 'deaths', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT country_region, deaths
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                AND deaths > 0
                GROUP BY country_region, deaths
                ORDER BY deaths DESC
                LIMIT 10
            """)).fetchall()

            labels = [row.country_region for row in result] # Usar el nombre de columna del resultado de la DB
            values = [row.deaths for row in result] # Usar el nombre de columna del resultado de la DB

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
            # CORREGIDO: Usar 'country_region', 'confirmed', 'deaths', 'date' en MINÚSCULAS
            result = session.execute(text("""
                SELECT
                    country_region,
                    SUM(confirmed) AS total_confirmed,
                    SUM(deaths) AS total_deaths
                FROM covid_data_unified
                WHERE date = (SELECT MAX(date) FROM covid_data_unified)
                GROUP BY country_region
                HAVING SUM(confirmed) >= 1000
                ORDER BY (SUM(deaths)::NUMERIC / SUM(confirmed)) DESC
                LIMIT 10
            """)).fetchall()

            labels = []
            values = []
            for row in result:
                if row.total_confirmed > 0:
                    rate = (row.total_deaths / row.total_confirmed) * 100
                    labels.append(row.country_region) # Usar el nombre de columna del resultado de la DB
                    values.append(float(f"{rate:.2f}"))

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
            # CORREGIDO: Usar 'date', 'confirmed_daily', 'deaths_daily', 'country_region' en MINÚSCULAS
            result = session.execute(text("""
                SELECT date, confirmed_daily, deaths_daily
                FROM covid_data_unified
                WHERE country_region = 'Mexico'
                ORDER BY date ASC
            """)).fetchall()

            # Ojo: aquí cuando creas el DataFrame con pandas, puedes usar los nombres Pythonic o los que devuelve la DB
            # pandas creará columnas en el DF con los nombres exactos que le pasas en el dict o en el row.campo
            df_mexico = pd.DataFrame([{"Date": row.date, "Confirmed_Daily": row.confirmed_daily, "Deaths_Daily": row.deaths_daily} for row in result])
            df_mexico['Moving_Average_7_Day'] = df_mexico['Confirmed_Daily'].rolling(window=7, min_periods=1).mean()

            response_data = {
                "dates": [d.strftime('%Y-%m-%d') for d in df_mexico['Date'].tolist()],
                "daily_cases": df_mexico['Confirmed_Daily'].tolist(),
                "daily_deaths": df_mexico['Deaths_Daily'].tolist(),
                "moving_average_7_day": df_mexico['Moving_Average_7_Day'].tolist()
            }
            return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error al preparar datos de gráfico diario México: {e}")
        return jsonify({"error": "Error de datos", "message": "No se pudieron preparar los datos para el gráfico diario de México."}), 500
