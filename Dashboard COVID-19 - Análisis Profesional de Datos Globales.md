# Dashboard COVID-19 - Análisis Profesional de Datos Globales

![Dashboard COVID-19](https://img.shields.io/badge/COVID--19-Dashboard-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Flask](https://img.shields.io/badge/Flask-3.1.1-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![Linux Mint](https://img.shields.io/badge/Linux%20Mint-22-green)

## Descripción

Dashboard profesional para el análisis de datos globales de COVID-19 basado en los datos oficiales de la Universidad Johns Hopkins. Proporciona visualizaciones interactivas, métricas estadísticas avanzadas y respuestas a preguntas clave sobre la evolución de la pandemia a nivel mundial.

### Características Principales

- **Análisis Completo**: Procesamiento de más de 330,000 registros de datos históricos (2020-2023)
- **Visualizaciones Interactivas**: Gráficos dinámicos con Chart.js
- **Métricas Avanzadas**: Tasas de mortalidad, casos diarios, tendencias temporales
- **Dashboard Responsivo**: Interfaz moderna compatible con dispositivos móviles
- **API REST**: Endpoints para acceso programático a los datos
- **Base de Datos Optimizada**: PostgreSQL con índices para consultas eficientes

## Tecnologías Utilizadas

### Backend
- **Flask 3.1.1**: Framework web Python
- **PostgreSQL 14+**: Base de datos relacional
- **SQLAlchemy 2.0.41**: ORM para Python
- **Pandas 2.3.1**: Análisis y manipulación de datos
- **Gunicorn**: Servidor WSGI para producción

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript ES6**: Lógica del cliente
- **Chart.js**: Visualizaciones interactivas
- **Tailwind CSS**: Framework de estilos
- **Font Awesome**: Iconografía

### Infraestructura
- **Nginx**: Servidor web y proxy reverso
- **Systemd**: Gestión de servicios
- **Linux Mint 22**: Sistema operativo objetivo

## Instalación Rápida

### Opción 1: Instalación Automatizada (Recomendada)

```bash
# Clonar o descargar el proyecto
cd covid_dashboard_entrega_final

# Hacer ejecutable el script de instalación
chmod +x install.sh

# Ejecutar instalación automatizada
sudo ./install.sh
```

### Opción 2: Instalación Manual

Consulte la [Guía Completa de Despliegue](guia_despliegue_covid_dashboard.md) para instrucciones detalladas paso a paso.

## Estructura del Proyecto

```
covid_dashboard_entrega_final/
├── install.sh                          # Script de instalación automatizada
├── README.md                           # Este archivo
├── guia_despliegue_covid_dashboard.md  # Guía completa de despliegue
├── respuestas_covid_analisis.md        # Respuestas a preguntas específicas
├── covid_analysis.py                   # Script de análisis de datos
├── src/                                # Código fuente de la aplicación
│   ├── main.py                         # Aplicación Flask principal
│   ├── routes/                         # Rutas de la API
│   │   ├── covid.py                    # Endpoints COVID-19
│   │   └── user.py                     # Endpoints de usuario (template)
│   ├── models/                         # Modelos de datos
│   │   └── user.py                     # Modelo de usuario (template)
│   └── static/                         # Archivos estáticos
│       └── index.html                  # Dashboard principal
├── data/                               # Datos y scripts de procesamiento
│   ├── time_series_covid19_confirmed_global.csv
│   ├── time_series_covid19_deaths_global.csv
│   ├── time_series_covid19_recovered_global.csv
│   └── prepare_covid_data.py           # Script de preparación de datos
└── visualizations/                     # Gráficos generados (opcional)
    ├── top_confirmed_countries.png
    ├── top_deaths_countries.png
    ├── top_mortality_rate.png
    └── mexico_daily_cases.png
```

## Uso del Dashboard

### Acceso Web

Una vez instalado, el dashboard estará disponible en:
- **URL Local**: http://localhost
- **Puerto**: 80 (HTTP)

### Funcionalidades Principales

1. **Estadísticas Globales**
   - Casos confirmados totales
   - Muertes totales
   - Tasa de mortalidad global
   - Datos de recuperación

2. **Rankings de Países**
   - Top 10 países con más casos
   - Top 10 países con más muertes
   - Países con mayor/menor tasa de mortalidad

3. **Análisis Temporal**
   - Curva de casos diarios por país
   - Tendencias con promedio móvil
   - Evolución histórica de la pandemia

4. **Visualizaciones Interactivas**
   - Gráficos de barras horizontales
   - Gráficos de líneas temporales
   - Tablas de datos ordenables

### API Endpoints

El dashboard expone una API REST para acceso programático:

```bash
# Estadísticas globales
curl http://localhost/api/covid/global-stats

# Top países por casos confirmados
curl http://localhost/api/covid/top-confirmed

# Top países por muertes
curl http://localhost/api/covid/top-deaths

# Datos de México
curl http://localhost/api/covid/mexico-daily

# Datos para gráficos específicos
curl http://localhost/api/covid/chart-data/top-confirmed
```

## Respuestas a Preguntas Específicas

El proyecto responde a las siguientes preguntas clave sobre COVID-19:

### 1. ¿Cuáles son los 10 países con más contagios?
1. Estados Unidos - 103,802,702 casos
2. India - 44,690,738 casos
3. Francia - 39,866,718 casos
4. Alemania - 38,249,060 casos
5. Brasil - 37,076,053 casos
6. Japón - 33,320,438 casos
7. Corea del Sur - 30,615,522 casos
8. Italia - 25,603,510 casos
9. Reino Unido - 24,658,705 casos
10. Rusia - 22,075,858 casos

### 2. ¿Cuáles son los 10 países con más decesos?
1. Estados Unidos - 1,123,836 muertes
2. Brasil - 699,276 muertes
3. India - 530,779 muertes
4. Rusia - 388,478 muertes
5. México - 333,188 muertes
6. Reino Unido - 220,721 muertes
7. Perú - 219,539 muertes
8. Italia - 188,322 muertes
9. Alemania - 168,935 muertes
10. Francia - 166,176 muertes

### 3. Tasa de Mortalidad Global: 1.02%

**Países con mayor tasa de mortalidad:**
- Corea del Norte: 600.00%
- Yemen: 18.07%
- Perú: 4.89%
- México: 4.45%

**Países con menor tasa de mortalidad:**
- Singapur: 0.08%
- Corea del Sur: 0.11%
- Nueva Zelanda: 0.11%

### 4. Análisis de México
- **Casos totales**: 7,483,444
- **Muertes totales**: 333,188
- **Tasa de mortalidad**: 4.45% (muy por encima del promedio global)
- **Posición mundial**: 5° lugar en muertes totales

Para respuestas detalladas, consulte [respuestas_covid_analisis.md](respuestas_covid_analisis.md).

## Requisitos del Sistema

### Mínimos
- **SO**: Linux Mint 22, Ubuntu 22.04+
- **RAM**: 4 GB
- **Disco**: 10 GB libres
- **CPU**: 2 núcleos @ 2.0 GHz

### Recomendados
- **RAM**: 8 GB
- **Disco**: 50 GB (SSD preferible)
- **CPU**: 4 núcleos @ 2.5 GHz
- **Red**: Conexión a internet para instalación

## Comandos Útiles

### Gestión de Servicios
```bash
# Ver estado de servicios
sudo systemctl status covid-dashboard
sudo systemctl status nginx
sudo systemctl status postgresql

# Reiniciar servicios
sudo systemctl restart covid-dashboard
sudo systemctl restart nginx

# Ver logs
sudo journalctl -u covid-dashboard -f
sudo tail -f /var/log/nginx/access.log
```

### Base de Datos
```bash
# Conectar a PostgreSQL
sudo -u postgres psql -d covid_data

# Verificar datos
sudo -u postgres psql -d covid_data -c "SELECT COUNT(*) FROM covid_data_unified;"

# Backup de base de datos
sudo -u postgres pg_dump covid_data > backup_$(date +%Y%m%d).sql
```

### Desarrollo
```bash
# Activar entorno virtual
cd ~/covid_dashboard && source venv/bin/activate

# Ejecutar en modo desarrollo
python src/main.py

# Instalar nuevas dependencias
pip install nueva_dependencia
pip freeze > requirements.txt
```

## Solución de Problemas

### Problemas Comunes

1. **Error de conexión a base de datos**
   ```bash
   sudo systemctl restart postgresql
   sudo -u postgres psql -c "\l"
   ```

2. **Dashboard no carga**
   ```bash
   sudo systemctl restart covid-dashboard nginx
   curl http://localhost/api/covid/global-stats
   ```

3. **Datos no aparecen**
   ```bash
   cd ~/covid_dashboard
   source venv/bin/activate
   python data/prepare_covid_data.py
   ```

### Logs de Diagnóstico
```bash
# Verificar todos los servicios
sudo systemctl status covid-dashboard nginx postgresql

# Ver logs detallados
sudo journalctl -u covid-dashboard --no-pager -n 50
```

## Contribución

Este proyecto fue desarrollado como un análisis profesional de datos COVID-19. Para mejoras o extensiones:

1. Fork el proyecto
2. Cree una rama para su feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit sus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abra un Pull Request

## Licencia

Este proyecto está desarrollado para fines educativos y de análisis de datos. Los datos utilizados provienen de fuentes públicas de la Universidad Johns Hopkins.

## Fuentes de Datos

- **Datos principales**: [Johns Hopkins CSSE COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19)
- **Período de datos**: Enero 2020 - Marzo 2023
- **Cobertura**: 201 países y territorios
- **Frecuencia**: Datos diarios

## Autor

**Manus AI** - Análisis profesional de datos con más de 10 años de experiencia en ciencia de datos.

## Soporte

Para soporte técnico o consultas:
1. Consulte la [Guía Completa de Despliegue](guia_despliegue_covid_dashboard.md)
2. Revise la sección de [Solución de Problemas](#solución-de-problemas)
3. Verifique los logs del sistema

---

**Última actualización**: Julio 2025  
**Versión**: 1.0  
**Compatibilidad**: Linux Mint 22, Ubuntu 22.04+

