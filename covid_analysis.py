#!/usr/bin/env python3
"""
Análisis de datos COVID-19
Script para crear métricas y responder preguntas específicas sobre los datos de COVID-19
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de matplotlib para mejor visualización
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class CovidAnalyzer:
    def __init__(self):
        """Inicializar el analizador de datos COVID-19"""
        self.engine = create_engine('postgresql://superset_user:Marte_9de9@localhost:5432/covid_data')
        self.df = None
        self.calendar = None
        self.load_data()
    
    def load_data(self):
        """Cargar datos desde PostgreSQL"""
        print("Cargando datos desde PostgreSQL...")
        
        # Cargar datos principales
        query = """
        SELECT * FROM covid_data_unified 
        ORDER BY "Country_Region", "Province_State", "Date"
        """
        self.df = pd.read_sql(query, self.engine)
        
        # Cargar tabla calendario
        calendar_query = "SELECT * FROM calendar ORDER BY \"Date\""
        self.calendar = pd.read_sql(calendar_query, self.engine)
        
        # Convertir fechas
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.calendar['Date'] = pd.to_datetime(self.calendar['Date'])
        
        print(f"Datos cargados: {len(self.df)} registros")
        print(f"Rango de fechas: {self.df['Date'].min()} a {self.df['Date'].max()}")
        print(f"Países únicos: {self.df['Country_Region'].nunique()}")
    
    def create_country_aggregates(self):
        """Crear agregados por país"""
        print("Creando agregados por país...")
        
        # Agrupar por país y fecha para obtener totales nacionales
        country_data = self.df.groupby(['Country_Region', 'Date']).agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Confirmed_Daily': 'sum',
            'Deaths_Daily': 'sum',
            'Recovered_Daily': 'sum'
        }).reset_index()
        
        return country_data
    
    def calculate_mortality_rate(self, data):
        """Calcular tasa de mortalidad"""
        # Evitar división por cero
        data['mortality_rate'] = np.where(
            data['Confirmed'] > 0,
            (data['Deaths'] / data['Confirmed']) * 100,
            0
        )
        return data
    
    def calculate_recovery_rate(self, data):
        """Calcular tasa de recuperación"""
        # Evitar división por cero
        data['recovery_rate'] = np.where(
            data['Confirmed'] > 0,
            (data['Recovered'] / data['Confirmed']) * 100,
            0
        )
        return data
    
    def get_latest_country_stats(self):
        """Obtener estadísticas más recientes por país"""
        country_data = self.create_country_aggregates()
        
        # Obtener la fecha más reciente para cada país
        latest_data = country_data.loc[country_data.groupby('Country_Region')['Date'].idxmax()]
        
        # Calcular tasas
        latest_data = self.calculate_mortality_rate(latest_data)
        latest_data = self.calculate_recovery_rate(latest_data)
        
        return latest_data
    
    def top_countries_by_metric(self, metric, n=10, ascending=False):
        """Obtener top N países por métrica específica"""
        latest_stats = self.get_latest_country_stats()
        
        # Filtrar países con datos válidos
        valid_data = latest_stats[latest_stats[metric] > 0]
        
        return valid_data.nlargest(n, metric) if not ascending else valid_data.nsmallest(n, metric)
    
    def analyze_mexico_daily_cases(self):
        """Analizar curva de contagios diarios para México"""
        mexico_data = self.create_country_aggregates()
        mexico_data = mexico_data[mexico_data['Country_Region'] == 'Mexico'].copy()
        
        if len(mexico_data) == 0:
            print("No se encontraron datos para México")
            return None
        
        # Calcular promedio móvil de 7 días para suavizar la curva
        mexico_data['confirmed_daily_ma7'] = mexico_data['Confirmed_Daily'].rolling(window=7, center=True).mean()
        
        return mexico_data
    
    def generate_summary_report(self):
        """Generar reporte resumen con todas las métricas"""
        print("\n" + "="*60)
        print("REPORTE DE ANÁLISIS COVID-19")
        print("="*60)
        
        latest_stats = self.get_latest_country_stats()
        
        # Estadísticas globales
        global_confirmed = latest_stats['Confirmed'].sum()
        global_deaths = latest_stats['Deaths'].sum()
        global_recovered = latest_stats['Recovered'].sum()
        global_mortality = (global_deaths / global_confirmed) * 100 if global_confirmed > 0 else 0
        global_recovery = (global_recovered / global_confirmed) * 100 if global_confirmed > 0 else 0
        
        print(f"\nESTADÍSTICAS GLOBALES:")
        print(f"Total de casos confirmados: {global_confirmed:,}")
        print(f"Total de muertes: {global_deaths:,}")
        print(f"Total de recuperados: {global_recovered:,}")
        print(f"Tasa de mortalidad global: {global_mortality:.2f}%")
        print(f"Tasa de recuperación global: {global_recovery:.2f}%")
        
        # Top 10 países con más contagios
        print(f"\nTOP 10 PAÍSES CON MÁS CONTAGIOS:")
        top_confirmed = self.top_countries_by_metric('Confirmed', 10)
        for i, (_, row) in enumerate(top_confirmed.iterrows(), 1):
            print(f"{i:2d}. {row['Country_Region']:<20} {row['Confirmed']:>12,} casos")
        
        # Top 10 países con más muertes
        print(f"\nTOP 10 PAÍSES CON MÁS MUERTES:")
        top_deaths = self.top_countries_by_metric('Deaths', 10)
        for i, (_, row) in enumerate(top_deaths.iterrows(), 1):
            print(f"{i:2d}. {row['Country_Region']:<20} {row['Deaths']:>12,} muertes")
        
        # Top 10 países con mayor tasa de mortalidad
        print(f"\nTOP 10 PAÍSES CON MAYOR TASA DE MORTALIDAD:")
        top_mortality = self.top_countries_by_metric('mortality_rate', 10)
        for i, (_, row) in enumerate(top_mortality.iterrows(), 1):
            print(f"{i:2d}. {row['Country_Region']:<20} {row['mortality_rate']:>8.2f}%")
        
        # Top 10 países con menor tasa de mortalidad
        print(f"\nTOP 10 PAÍSES CON MENOR TASA DE MORTALIDAD:")
        low_mortality = self.top_countries_by_metric('mortality_rate', 10, ascending=True)
        # Filtrar países con al menos 1000 casos para que sea significativo
        low_mortality = low_mortality[low_mortality['Confirmed'] >= 1000]
        for i, (_, row) in enumerate(low_mortality.iterrows(), 1):
            print(f"{i:2d}. {row['Country_Region']:<20} {row['mortality_rate']:>8.2f}%")
        
        # Top 10 países con mayor tasa de recuperación
        print(f"\nTOP 10 PAÍSES CON MAYOR TASA DE RECUPERACIÓN:")
        top_recovery = self.top_countries_by_metric('recovery_rate', 10)
        # Filtrar países con al menos 1000 casos para que sea significativo
        top_recovery = top_recovery[top_recovery['Confirmed'] >= 1000]
        for i, (_, row) in enumerate(top_recovery.iterrows(), 1):
            print(f"{i:2d}. {row['Country_Region']:<20} {row['recovery_rate']:>8.2f}%")
        
        return {
            'global_stats': {
                'confirmed': global_confirmed,
                'deaths': global_deaths,
                'recovered': global_recovered,
                'mortality_rate': global_mortality,
                'recovery_rate': global_recovery
            },
            'top_confirmed': top_confirmed,
            'top_deaths': top_deaths,
            'top_mortality': top_mortality,
            'low_mortality': low_mortality,
            'top_recovery': top_recovery
        }
    
    def create_visualizations(self):
        """Crear visualizaciones principales"""
        print("\nCreando visualizaciones...")
        
        # Crear directorio para gráficos
        import os
        os.makedirs('visualizations', exist_ok=True)
        
        latest_stats = self.get_latest_country_stats()
        
        # 1. Top 10 países por casos confirmados
        plt.figure(figsize=(12, 8))
        top_confirmed = self.top_countries_by_metric('Confirmed', 10)
        plt.barh(range(len(top_confirmed)), top_confirmed['Confirmed'])
        plt.yticks(range(len(top_confirmed)), top_confirmed['Country_Region'])
        plt.xlabel('Casos Confirmados')
        plt.title('Top 10 Países con Más Casos Confirmados de COVID-19')
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_confirmed['Confirmed']):
            plt.text(v + max(top_confirmed['Confirmed'])*0.01, i, f'{v:,}', va='center')
        plt.tight_layout()
        plt.savefig('visualizations/top_confirmed_countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Top 10 países por muertes
        plt.figure(figsize=(12, 8))
        top_deaths = self.top_countries_by_metric('Deaths', 10)
        plt.barh(range(len(top_deaths)), top_deaths['Deaths'])
        plt.yticks(range(len(top_deaths)), top_deaths['Country_Region'])
        plt.xlabel('Muertes')
        plt.title('Top 10 Países con Más Muertes por COVID-19')
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_deaths['Deaths']):
            plt.text(v + max(top_deaths['Deaths'])*0.01, i, f'{v:,}', va='center')
        plt.tight_layout()
        plt.savefig('visualizations/top_deaths_countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Curva de contagios diarios para México
        mexico_data = self.analyze_mexico_daily_cases()
        if mexico_data is not None:
            plt.figure(figsize=(15, 8))
            plt.plot(mexico_data['Date'], mexico_data['Confirmed_Daily'], alpha=0.3, color='blue', label='Casos diarios')
            plt.plot(mexico_data['Date'], mexico_data['confirmed_daily_ma7'], color='red', linewidth=2, label='Promedio móvil 7 días')
            plt.xlabel('Fecha')
            plt.ylabel('Casos Diarios')
            plt.title('Curva de Contagios Diarios de COVID-19 en México')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('visualizations/mexico_daily_cases.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 4. Tasa de mortalidad por países
        plt.figure(figsize=(12, 8))
        top_mortality = self.top_countries_by_metric('mortality_rate', 10)
        plt.barh(range(len(top_mortality)), top_mortality['mortality_rate'])
        plt.yticks(range(len(top_mortality)), top_mortality['Country_Region'])
        plt.xlabel('Tasa de Mortalidad (%)')
        plt.title('Top 10 Países con Mayor Tasa de Mortalidad por COVID-19')
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_mortality['mortality_rate']):
            plt.text(v + max(top_mortality['mortality_rate'])*0.01, i, f'{v:.2f}%', va='center')
        plt.tight_layout()
        plt.savefig('visualizations/top_mortality_rate.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Visualizaciones guardadas en el directorio 'visualizations/'")

def main():
    """Función principal"""
    analyzer = CovidAnalyzer()
    
    # Generar reporte completo
    summary = analyzer.generate_summary_report()
    
    # Crear visualizaciones
    analyzer.create_visualizations()
    
    # Análisis específico de México
    print(f"\nANÁLISIS ESPECÍFICO DE MÉXICO:")
    mexico_data = analyzer.analyze_mexico_daily_cases()
    if mexico_data is not None:
        max_daily = mexico_data['Confirmed_Daily'].max()
        max_date = mexico_data[mexico_data['Confirmed_Daily'] == max_daily]['Date'].iloc[0]
        print(f"Pico máximo de casos diarios: {max_daily:,} casos el {max_date.strftime('%Y-%m-%d')}")
        
        # Estadísticas finales de México
        latest_mexico = mexico_data.iloc[-1]
        print(f"Casos totales confirmados: {latest_mexico['Confirmed']:,}")
        print(f"Muertes totales: {latest_mexico['Deaths']:,}")
        print(f"Recuperados totales: {latest_mexico['Recovered']:,}")
        
        mortality_rate = (latest_mexico['Deaths'] / latest_mexico['Confirmed']) * 100 if latest_mexico['Confirmed'] > 0 else 0
        recovery_rate = (latest_mexico['Recovered'] / latest_mexico['Confirmed']) * 100 if latest_mexico['Confirmed'] > 0 else 0
        
        print(f"Tasa de mortalidad: {mortality_rate:.2f}%")
        print(f"Tasa de recuperación: {recovery_rate:.2f}%")
    
    print(f"\n{'='*60}")
    print("ANÁLISIS COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()

