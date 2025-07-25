from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

covid_bp = Blueprint('covid', __name__)

# Configuración de la base de datos
DATABASE_URL = 'postgresql://superset_user:Marte_9de9@localhost:5432/covid_data'

class CovidDataService:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    def get_country_aggregates(self):
        """Obtener datos agregados por país"""
        query = """
        SELECT "Country_Region", "Date", 
               SUM("Confirmed") as confirmed,
               SUM("Deaths") as deaths,
               SUM("Recovered") as recovered,
               SUM("Confirmed_Daily") as confirmed_daily,
               SUM("Deaths_Daily") as deaths_daily,
               SUM("Recovered_Daily") as recovered_daily
        FROM covid_data_unified 
        GROUP BY "Country_Region", "Date"
        ORDER BY "Country_Region", "Date"
        """
        df = pd.read_sql(query, self.engine)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
    def get_latest_country_stats(self):
        """Obtener estadísticas más recientes por país"""
        country_data = self.get_country_aggregates()
        
        # Obtener la fecha más reciente para cada país
        latest_data = country_data.loc[country_data.groupby('Country_Region')['Date'].idxmax()]
        
        # Calcular tasas
        latest_data['mortality_rate'] = np.where(
            latest_data['confirmed'] > 0,
            (latest_data['deaths'] / latest_data['confirmed']) * 100,
            0
        )
        latest_data['recovery_rate'] = np.where(
            latest_data['confirmed'] > 0,
            (latest_data['recovered'] / latest_data['confirmed']) * 100,
            0
        )
        
        return latest_data
    
    def get_global_stats(self):
        """Obtener estadísticas globales"""
        latest_stats = self.get_latest_country_stats()
        
        global_confirmed = latest_stats['confirmed'].sum()
        global_deaths = latest_stats['deaths'].sum()
        global_recovered = latest_stats['recovered'].sum()
        global_mortality = (global_deaths / global_confirmed) * 100 if global_confirmed > 0 else 0
        global_recovery = (global_recovered / global_confirmed) * 100 if global_confirmed > 0 else 0
        
        return {
            'confirmed': int(global_confirmed),
            'deaths': int(global_deaths),
            'recovered': int(global_recovered),
            'mortality_rate': round(global_mortality, 2),
            'recovery_rate': round(global_recovery, 2)
        }
    
    def get_top_countries(self, metric, n=10, ascending=False):
        """Obtener top N países por métrica"""
        latest_stats = self.get_latest_country_stats()
        valid_data = latest_stats[latest_stats[metric] > 0]
        
        if ascending:
            # Para tasas de mortalidad baja, filtrar países con al menos 1000 casos
            if metric in ['mortality_rate', 'recovery_rate']:
                valid_data = valid_data[valid_data['confirmed'] >= 1000]
            result = valid_data.nsmallest(n, metric)
        else:
            result = valid_data.nlargest(n, metric)
        
        return result[['Country_Region', metric, 'confirmed', 'deaths', 'recovered']].to_dict('records')
    
    def get_mexico_daily_cases(self):
        """Obtener datos diarios de México"""
        country_data = self.get_country_aggregates()
        mexico_data = country_data[country_data['Country_Region'] == 'Mexico'].copy()
        
        if len(mexico_data) == 0:
            return None
        
        # Calcular promedio móvil de 7 días
        mexico_data['confirmed_daily_ma7'] = mexico_data['confirmed_daily'].rolling(window=7, center=True).mean()
        
        # Convertir fechas a string para JSON
        mexico_data['Date'] = mexico_data['Date'].dt.strftime('%Y-%m-%d')
        
        return mexico_data[['Date', 'confirmed_daily', 'confirmed_daily_ma7']].to_dict('records')

# Instancia del servicio
covid_service = CovidDataService()

@covid_bp.route('/global-stats')
def global_stats():
    """Endpoint para estadísticas globales"""
    try:
        stats = covid_service.get_global_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/top-confirmed')
def top_confirmed():
    """Endpoint para top países por casos confirmados"""
    try:
        n = request.args.get('n', 10, type=int)
        data = covid_service.get_top_countries('confirmed', n)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/top-deaths')
def top_deaths():
    """Endpoint para top países por muertes"""
    try:
        n = request.args.get('n', 10, type=int)
        data = covid_service.get_top_countries('deaths', n)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/top-mortality')
def top_mortality():
    """Endpoint para top países por tasa de mortalidad"""
    try:
        n = request.args.get('n', 10, type=int)
        data = covid_service.get_top_countries('mortality_rate', n)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/low-mortality')
def low_mortality():
    """Endpoint para países con menor tasa de mortalidad"""
    try:
        n = request.args.get('n', 10, type=int)
        data = covid_service.get_top_countries('mortality_rate', n, ascending=True)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/top-recovery')
def top_recovery():
    """Endpoint para países con mayor tasa de recuperación"""
    try:
        n = request.args.get('n', 10, type=int)
        data = covid_service.get_top_countries('recovery_rate', n)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/mexico-daily')
def mexico_daily():
    """Endpoint para casos diarios de México"""
    try:
        data = covid_service.get_mexico_daily_cases()
        if data is None:
            return jsonify({'error': 'No se encontraron datos para México'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@covid_bp.route('/chart-data/<chart_type>')
def chart_data(chart_type):
    """Endpoint para datos de gráficos específicos"""
    try:
        if chart_type == 'top-confirmed':
            data = covid_service.get_top_countries('confirmed', 10)
            return jsonify({
                'labels': [item['Country_Region'] for item in data],
                'values': [item['confirmed'] for item in data],
                'title': 'Top 10 Países - Casos Confirmados'
            })
        elif chart_type == 'top-deaths':
            data = covid_service.get_top_countries('deaths', 10)
            return jsonify({
                'labels': [item['Country_Region'] for item in data],
                'values': [item['deaths'] for item in data],
                'title': 'Top 10 Países - Muertes'
            })
        elif chart_type == 'top-mortality':
            data = covid_service.get_top_countries('mortality_rate', 10)
            return jsonify({
                'labels': [item['Country_Region'] for item in data],
                'values': [item['mortality_rate'] for item in data],
                'title': 'Top 10 Países - Tasa de Mortalidad (%)'
            })
        elif chart_type == 'mexico-daily':
            data = covid_service.get_mexico_daily_cases()
            if data is None:
                return jsonify({'error': 'No se encontraron datos para México'}), 404
            return jsonify({
                'dates': [item['Date'] for item in data],
                'daily_cases': [item['confirmed_daily'] for item in data],
                'moving_average': [item['confirmed_daily_ma7'] if item['confirmed_daily_ma7'] is not None else 0 for item in data],
                'title': 'Casos Diarios COVID-19 - México'
            })
        else:
            return jsonify({'error': 'Tipo de gráfico no válido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

