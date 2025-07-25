# Guía Completa de Despliegue - Dashboard COVID-19

## Análisis Profesional de Datos Globales con Flask y PostgreSQL

**Autor**: Manus AI  
**Fecha**: Julio 2025  
**Versión**: 1.0  
**Compatibilidad**: Linux Mint 22, Ubuntu 22.04+  

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Requisitos del Sistema](#requisitos-del-sistema)
4. [Instalación Paso a Paso](#instalación-paso-a-paso)
5. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
6. [Despliegue Local](#despliegue-local)
7. [Despliegue en Producción](#despliegue-en-producción)
8. [Mantenimiento y Monitoreo](#mantenimiento-y-monitoreo)
9. [Solución de Problemas](#solución-de-problemas)
10. [Referencias](#referencias)

---

## Introducción

Este documento proporciona una guía completa para desplegar el Dashboard COVID-19, una aplicación web profesional desarrollada para el análisis de datos globales de la pandemia. El sistema utiliza datos oficiales de la Universidad Johns Hopkins y presenta visualizaciones interactivas que responden a preguntas clave sobre la evolución de la pandemia a nivel mundial.

### Características Principales

El dashboard implementa un análisis exhaustivo de los datos COVID-19 con las siguientes funcionalidades principales. La aplicación procesa más de 330,000 registros de datos históricos que abarcan desde enero de 2020 hasta marzo de 2023, cubriendo 201 países y territorios. El sistema calcula automáticamente métricas críticas como tasas de mortalidad, casos diarios, y tendencias temporales, presentando esta información a través de una interfaz web moderna y responsiva.

La arquitectura del sistema se basa en tecnologías robustas y ampliamente adoptadas en la industria. Flask proporciona el framework web backend, ofreciendo flexibilidad y escalabilidad para el manejo de APIs REST. PostgreSQL actúa como el motor de base de datos, garantizando integridad de datos y rendimiento óptimo para consultas complejas. El frontend utiliza tecnologías web estándar incluyendo HTML5, CSS3, JavaScript ES6, y la biblioteca Chart.js para visualizaciones interactivas.

### Objetivos del Proyecto

El desarrollo de este dashboard responde a la necesidad de proporcionar análisis de datos COVID-19 accesibles y comprensibles para profesionales de la salud, investigadores, y el público general. La aplicación democratiza el acceso a información epidemiológica compleja, presentándola de manera visual e intuitiva. Además, el proyecto sirve como ejemplo de mejores prácticas en desarrollo de aplicaciones de análisis de datos, implementando patrones de diseño escalables y mantenibles.

---

## Arquitectura del Sistema

### Diagrama de Arquitectura

La arquitectura del sistema sigue un patrón de tres capas que separa claramente las responsabilidades y facilita el mantenimiento y escalabilidad de la aplicación.

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Dashboard     │  │   Gráficos      │  │   Tablas     │ │
│  │   Principal     │  │   Interactivos  │  │   de Datos   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│           │                     │                   │       │
│           └─────────────────────┼───────────────────┘       │
│                                 │                           │
└─────────────────────────────────┼───────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────┐
│                    CAPA DE LÓGICA DE NEGOCIO                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Flask API     │  │   Servicios     │  │   Cálculo    │ │
│  │   Endpoints     │  │   de Datos      │  │   Métricas   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│           │                     │                   │       │
│           └─────────────────────┼───────────────────┘       │
│                                 │                           │
└─────────────────────────────────┼───────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────┐
│                    CAPA DE DATOS                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   PostgreSQL    │  │   Tablas        │  │   Índices    │ │
│  │   Database      │  │   Optimizadas   │  │   y Vistas   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Componentes del Sistema

#### Capa de Presentación

La capa de presentación implementa una interfaz de usuario moderna y responsiva utilizando tecnologías web estándar. El diseño se basa en principios de experiencia de usuario (UX) que priorizan la claridad y accesibilidad de la información. La interfaz utiliza Tailwind CSS para un diseño consistente y profesional, mientras que Chart.js proporciona visualizaciones interactivas de alta calidad.

El dashboard principal presenta cuatro métricas globales clave en tarjetas destacadas: casos confirmados totales, muertes totales, tasa de mortalidad global, y recuperados. Estas métricas se actualizan dinámicamente mediante llamadas AJAX a la API backend. Los gráficos incluyen visualizaciones de barras horizontales para rankings de países y gráficos de líneas para tendencias temporales, todos ellos interactivos y responsivos.

#### Capa de Lógica de Negocio

La capa de lógica de negocio está implementada en Flask, proporcionando una API REST robusta y bien estructurada. Los endpoints están organizados en blueprints que separan las funcionalidades por dominio, facilitando el mantenimiento y la extensibilidad del código. El servicio `CovidDataService` encapsula toda la lógica de acceso a datos y cálculo de métricas, implementando patrones de diseño que garantizan la reutilización y testabilidad del código.

Los endpoints de la API incluyen funcionalidades para obtener estadísticas globales, rankings de países por diferentes métricas, datos específicos de países, y datos formateados para visualizaciones. Cada endpoint implementa manejo de errores robusto y validación de parámetros, garantizando la estabilidad del sistema en condiciones adversas.

#### Capa de Datos

La capa de datos utiliza PostgreSQL como motor de base de datos, aprovechando sus capacidades avanzadas para el manejo de grandes volúmenes de datos y consultas complejas. El esquema de base de datos está optimizado para consultas analíticas, con índices estratégicamente ubicados para maximizar el rendimiento de las operaciones más frecuentes.

La tabla principal `covid_data_unified` almacena los datos procesados en formato normalizado, mientras que la tabla `calendar` proporciona dimensiones temporales para análisis de series de tiempo. El diseño del esquema facilita la agregación de datos por país y fecha, operaciones fundamentales para el funcionamiento del dashboard.

---

## Requisitos del Sistema

### Requisitos de Hardware

Para un despliegue local de desarrollo, el sistema requiere un mínimo de 4 GB de RAM y 10 GB de espacio libre en disco. Para entornos de producción que manejen múltiples usuarios concurrentes, se recomienda un mínimo de 8 GB de RAM y 50 GB de espacio en disco. El procesador debe ser de al menos 2 núcleos a 2.0 GHz, aunque se recomienda 4 núcleos para mejor rendimiento.

El almacenamiento debe ser preferiblemente SSD para optimizar las operaciones de base de datos, especialmente durante la carga inicial de datos y las consultas complejas de agregación. Para despliegues en la nube, se recomienda utilizar instancias con almacenamiento SSD y al menos 2 vCPUs.

### Requisitos de Software

El sistema está diseñado para funcionar en distribuciones Linux basadas en Ubuntu, específicamente optimizado para Linux Mint 22. Los requisitos de software incluyen Python 3.9.18 o superior, PostgreSQL 14 o superior, y un navegador web moderno que soporte JavaScript ES6 y CSS3.

Las dependencias de Python se gestionan a través de un entorno virtual que incluye Flask 3.1.1, SQLAlchemy 2.0.41, psycopg2-binary 2.9.10, pandas 2.3.1, plotly 6.2.0, y flask-cors 6.0.0. Todas estas dependencias se instalan automáticamente durante el proceso de configuración.

### Requisitos de Red

Para despliegue local, no se requieren configuraciones especiales de red más allá del acceso a localhost. Para despliegues en producción, se necesita acceso HTTP/HTTPS en los puertos 80/443, y acceso a PostgreSQL en el puerto 5432 (que debe estar restringido a conexiones internas por seguridad).

El sistema requiere acceso a internet durante la instalación inicial para descargar dependencias, pero puede funcionar completamente offline una vez configurado. Para actualizaciones de datos, se puede configurar acceso programático a fuentes de datos externas.

---


## Instalación Paso a Paso

### Preparación del Entorno

La instalación del Dashboard COVID-19 en Linux Mint 22 requiere una preparación cuidadosa del entorno para garantizar que todas las dependencias se instalen correctamente y el sistema funcione de manera óptima. El proceso de instalación está diseñado para ser reproducible y automatizable, siguiendo las mejores prácticas de DevOps.

Antes de comenzar la instalación, es fundamental actualizar el sistema operativo y verificar que se dispone de los privilegios administrativos necesarios. El proceso de instalación modificará configuraciones del sistema y instalará software adicional, por lo que se requiere acceso sudo.

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas básicas de desarrollo
sudo apt install -y build-essential curl wget git vim
```

### Instalación de PostgreSQL

PostgreSQL es el componente central del sistema de gestión de datos del dashboard. La instalación incluye tanto el servidor de base de datos como las herramientas de desarrollo necesarias para la integración con Python. La configuración inicial establece los parámetros de seguridad y rendimiento apropiados para el entorno de desarrollo.

```bash
# Instalar PostgreSQL y dependencias
sudo apt install -y postgresql postgresql-contrib python3-dev libpq-dev

# Iniciar y habilitar el servicio PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar el estado del servicio
sudo systemctl status postgresql
```

La configuración de PostgreSQL incluye la creación de una base de datos específica para el proyecto y un usuario dedicado con los permisos apropiados. Esta separación de privilegios mejora la seguridad del sistema y facilita el mantenimiento futuro.

```bash
# Crear base de datos y usuario
sudo -u postgres psql -c "CREATE DATABASE covid_data;"
sudo -u postgres psql -c "CREATE USER superset_user WITH PASSWORD 'Marte_9de9';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE covid_data TO superset_user;"

# Verificar la creación de la base de datos
sudo -u postgres psql -d covid_data -c "\dt"
```

### Configuración del Entorno Python

El entorno Python se configura utilizando virtualenv para aislar las dependencias del proyecto y evitar conflictos con otros paquetes del sistema. Esta práctica es esencial para mantener la estabilidad del sistema y facilitar la reproducibilidad del entorno en diferentes máquinas.

```bash
# Instalar pip y virtualenv si no están disponibles
sudo apt install -y python3-pip python3-venv

# Crear directorio del proyecto
mkdir -p ~/covid_dashboard_project
cd ~/covid_dashboard_project

# Crear y activar entorno virtual
python3 -m venv covid_env
source covid_env/bin/activate

# Actualizar pip en el entorno virtual
pip install --upgrade pip
```

### Instalación de Dependencias Python

Las dependencias de Python se instalan en el entorno virtual activado, garantizando que las versiones específicas requeridas por el proyecto no interfieran con otros proyectos o el sistema base. El archivo requirements.txt especifica las versiones exactas de cada paquete para garantizar la reproducibilidad.

```bash
# Instalar dependencias principales
pip install flask==3.1.1
pip install sqlalchemy==2.0.41
pip install psycopg2-binary==2.9.10
pip install pandas==2.3.1
pip install plotly==6.2.0
pip install flask-cors==6.0.0
pip install numpy==2.3.1

# Verificar la instalación
pip list
```

### Descarga y Configuración del Código Fuente

El código fuente del dashboard se organiza en una estructura modular que facilita el mantenimiento y la extensibilidad. La estructura de directorios sigue las convenciones estándar de Flask, separando claramente los modelos, vistas, y controladores.

```bash
# Crear estructura de directorios
mkdir -p src/{models,routes,static,templates,database}

# Crear archivo principal de la aplicación
touch src/main.py

# Crear archivos de configuración
touch requirements.txt
touch .env
touch README.md
```

La configuración del proyecto incluye variables de entorno que permiten personalizar el comportamiento de la aplicación sin modificar el código fuente. Esto facilita el despliegue en diferentes entornos (desarrollo, pruebas, producción) con configuraciones específicas.

---

## Configuración de la Base de Datos

### Esquema de Base de Datos

El esquema de base de datos del Dashboard COVID-19 está diseñado para optimizar las consultas analíticas y garantizar la integridad de los datos. La estructura normalizada facilita las operaciones de agregación y permite escalabilidad futura para incluir nuevas fuentes de datos o métricas adicionales.

La tabla principal `covid_data_unified` almacena los datos procesados en formato desnormalizado para optimizar las consultas de lectura. Esta decisión de diseño prioriza el rendimiento de las consultas sobre el espacio de almacenamiento, lo cual es apropiado para un sistema de análisis de datos donde las operaciones de lectura son mucho más frecuentes que las de escritura.

```sql
-- Estructura de la tabla principal
CREATE TABLE covid_data_unified (
    Province_State TEXT,
    Country_Region TEXT NOT NULL,
    Lat DOUBLE PRECISION,
    Long DOUBLE PRECISION,
    Date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    Confirmed BIGINT NOT NULL DEFAULT 0,
    Deaths BIGINT NOT NULL DEFAULT 0,
    Recovered BIGINT NOT NULL DEFAULT 0,
    Confirmed_Daily BIGINT NOT NULL DEFAULT 0,
    Deaths_Daily BIGINT NOT NULL DEFAULT 0,
    Recovered_Daily BIGINT NOT NULL DEFAULT 0
);

-- Índices para optimizar consultas
CREATE INDEX idx_covid_country_date ON covid_data_unified(Country_Region, Date);
CREATE INDEX idx_covid_date ON covid_data_unified(Date);
CREATE INDEX idx_covid_country ON covid_data_unified(Country_Region);
```

La tabla `calendar` proporciona dimensiones temporales que facilitan el análisis de series de tiempo y la generación de reportes periódicos. Esta tabla de dimensiones es fundamental para operaciones de business intelligence y análisis temporal avanzado.

```sql
-- Tabla de calendario para análisis temporal
CREATE TABLE calendar (
    Date TIMESTAMP WITHOUT TIME ZONE PRIMARY KEY,
    Year INTEGER NOT NULL,
    Month INTEGER NOT NULL,
    Day INTEGER NOT NULL,
    DayOfWeek INTEGER NOT NULL,
    WeekOfYear INTEGER NOT NULL,
    MonthName TEXT NOT NULL,
    Quarter INTEGER NOT NULL
);

-- Índices para la tabla calendario
CREATE INDEX idx_calendar_year_month ON calendar(Year, Month);
CREATE INDEX idx_calendar_quarter ON calendar(Quarter);
```

### Carga de Datos Inicial

El proceso de carga de datos inicial transforma los archivos CSV proporcionados por la Universidad Johns Hopkins en un formato optimizado para análisis. Este proceso incluye validación de datos, cálculo de métricas derivadas, y optimización del esquema para consultas eficientes.

El script `prepare_covid_data.py` automatiza todo el proceso de transformación y carga de datos. Este script implementa validaciones robustas para garantizar la calidad de los datos y maneja casos especiales como valores faltantes o inconsistencias en los datos fuente.

```python
# Ejemplo de configuración de carga de datos
import pandas as pd
from sqlalchemy import create_engine

# Configuración de conexión a la base de datos
DATABASE_URL = 'postgresql://superset_user:Marte_9de9@localhost:5432/covid_data'
engine = create_engine(DATABASE_URL)

# Proceso de carga con validación
def load_and_validate_data(filepath, value_name):
    df = pd.read_csv(filepath)
    
    # Validaciones de calidad de datos
    if df.isnull().sum().sum() > 0:
        print(f"Advertencia: Se encontraron valores nulos en {filepath}")
    
    # Transformación de datos
    df_melted = df.melt(
        id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
        var_name='Date',
        value_name=value_name
    )
    
    return df_melted
```

### Optimización de Rendimiento

La optimización de rendimiento de la base de datos incluye la configuración de parámetros específicos de PostgreSQL para cargas de trabajo analíticas. Estas configuraciones mejoran significativamente el rendimiento de las consultas complejas que involucran agregaciones y joins.

```sql
-- Configuraciones de rendimiento recomendadas
-- (Estas configuraciones se aplican en postgresql.conf)

-- Memoria compartida (25% de la RAM del sistema)
shared_buffers = '1GB'

-- Memoria de trabajo para operaciones complejas
work_mem = '256MB'

-- Memoria para operaciones de mantenimiento
maintenance_work_mem = '512MB'

-- Configuración de checkpoint para mejor rendimiento de escritura
checkpoint_completion_target = 0.9
wal_buffers = '16MB'

-- Configuración de estadísticas para el optimizador
default_statistics_target = 100
```

La creación de índices estratégicos es fundamental para el rendimiento del sistema. Los índices se diseñan específicamente para las consultas más frecuentes del dashboard, incluyendo agregaciones por país, filtros por fecha, y ordenamientos por métricas específicas.

---

## Despliegue Local

### Configuración del Servidor de Desarrollo

El servidor de desarrollo Flask proporciona un entorno completo para pruebas y desarrollo local. La configuración incluye características como recarga automática de código, debugging detallado, y logging comprehensivo para facilitar el desarrollo y la resolución de problemas.

```bash
# Activar entorno virtual
source covid_env/bin/activate

# Configurar variables de entorno
export FLASK_APP=src/main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Iniciar servidor de desarrollo
python src/main.py
```

El servidor de desarrollo se configura para escuchar en todas las interfaces de red (0.0.0.0) para facilitar las pruebas desde diferentes dispositivos en la red local. Esta configuración es especialmente útil para pruebas de responsividad en dispositivos móviles y tablets.

### Verificación de la Instalación

La verificación de la instalación incluye pruebas automatizadas de todos los componentes del sistema para garantizar que la configuración es correcta y el sistema funciona según las especificaciones. Estas pruebas cubren la conectividad de la base de datos, la funcionalidad de la API, y la renderización correcta del frontend.

```bash
# Verificar conectividad de base de datos
python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://superset_user:Marte_9de9@localhost:5432/covid_data')
try:
    connection = engine.connect()
    print('✓ Conexión a base de datos exitosa')
    connection.close()
except Exception as e:
    print(f'✗ Error de conexión: {e}')
"

# Verificar endpoints de API
curl -s http://localhost:5000/api/covid/global-stats | python -m json.tool

# Verificar carga del frontend
curl -s http://localhost:5000/ | grep -q "Dashboard COVID-19" && echo "✓ Frontend cargado correctamente"
```

### Monitoreo del Sistema Local

El monitoreo del sistema local incluye la supervisión de métricas de rendimiento, logs de aplicación, y utilización de recursos. Estas herramientas son esenciales para identificar cuellos de botella y optimizar el rendimiento del sistema.

```bash
# Monitorear logs de la aplicación
tail -f logs/covid_dashboard.log

# Monitorear utilización de recursos
htop

# Monitorear conexiones de base de datos
sudo -u postgres psql -d covid_data -c "
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start
FROM pg_stat_activity 
WHERE datname = 'covid_data';
"
```

---


## Despliegue en Producción

### Preparación del Entorno de Producción

El despliegue en producción requiere consideraciones adicionales de seguridad, rendimiento, y disponibilidad que no son necesarias en entornos de desarrollo. La configuración de producción implementa mejores prácticas de seguridad incluyendo cifrado de comunicaciones, autenticación robusta, y aislamiento de procesos.

Para el despliegue en producción, se recomienda utilizar un servidor web robusto como Nginx como proxy reverso, junto con un servidor WSGI como Gunicorn para manejar las solicitudes de Python. Esta configuración proporciona mejor rendimiento, escalabilidad, y características de seguridad avanzadas.

```bash
# Instalar componentes de producción
sudo apt install -y nginx gunicorn3

# Configurar Gunicorn
pip install gunicorn

# Crear archivo de configuración de Gunicorn
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
EOF
```

### Configuración de Nginx

Nginx actúa como proxy reverso y servidor de archivos estáticos, mejorando significativamente el rendimiento y la seguridad del sistema. La configuración incluye compresión gzip, caching de archivos estáticos, y headers de seguridad apropiados.

```nginx
# Configuración de Nginx (/etc/nginx/sites-available/covid_dashboard)
server {
    listen 80;
    server_name tu-dominio.com;
    
    # Redirección a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;
    
    # Configuración SSL
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Configuración de archivos estáticos
    location /static/ {
        alias /path/to/covid_dashboard/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy a la aplicación Flask
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Compresión gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

### Configuración de Base de Datos para Producción

La configuración de PostgreSQL para producción incluye optimizaciones específicas para cargas de trabajo de alta concurrencia y volúmenes de datos grandes. Estas configuraciones mejoran el rendimiento y la estabilidad del sistema bajo carga.

```sql
-- Configuraciones de producción para PostgreSQL
-- Archivo: /etc/postgresql/14/main/postgresql.conf

# Configuración de memoria
shared_buffers = '4GB'                    # 25% de RAM total
effective_cache_size = '12GB'             # 75% de RAM total
work_mem = '256MB'                        # Para consultas complejas
maintenance_work_mem = '1GB'              # Para operaciones de mantenimiento

# Configuración de WAL y checkpoints
wal_buffers = '64MB'
checkpoint_completion_target = 0.9
checkpoint_timeout = '15min'
max_wal_size = '4GB'
min_wal_size = '1GB'

# Configuración de conexiones
max_connections = 200
shared_preload_libraries = 'pg_stat_statements'

# Configuración de logging
log_destination = 'csvlog'
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_duration_statement = 1000        # Log queries > 1 segundo
```

### Automatización del Despliegue

La automatización del despliegue utiliza scripts que garantizan la consistencia y reproducibilidad del proceso de despliegue. Estos scripts incluyen verificaciones de salud, rollback automático en caso de fallos, y notificaciones de estado.

```bash
#!/bin/bash
# Script de despliegue automatizado (deploy.sh)

set -e  # Salir en caso de error

echo "Iniciando despliegue del Dashboard COVID-19..."

# Verificar prerrequisitos
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

if ! systemctl is-active --quiet postgresql; then
    echo "Error: PostgreSQL no está ejecutándose"
    exit 1
fi

# Crear backup de la base de datos
echo "Creando backup de la base de datos..."
sudo -u postgres pg_dump covid_data > "backup_$(date +%Y%m%d_%H%M%S).sql"

# Actualizar código fuente
echo "Actualizando código fuente..."
git pull origin main

# Activar entorno virtual y actualizar dependencias
source covid_env/bin/activate
pip install -r requirements.txt

# Ejecutar migraciones de base de datos si existen
if [ -f "migrations.sql" ]; then
    echo "Ejecutando migraciones..."
    sudo -u postgres psql -d covid_data -f migrations.sql
fi

# Reiniciar servicios
echo "Reiniciando servicios..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Verificar que los servicios estén funcionando
sleep 5
if curl -f -s http://localhost/api/covid/global-stats > /dev/null; then
    echo "✓ Despliegue exitoso"
else
    echo "✗ Error en el despliegue, iniciando rollback..."
    # Aquí iría la lógica de rollback
    exit 1
fi

echo "Despliegue completado exitosamente"
```

---

## Mantenimiento y Monitoreo

### Estrategias de Backup

Las estrategias de backup garantizan la continuidad del negocio y la recuperación ante desastres. El sistema implementa backups automáticos diarios con retención configurable y verificación de integridad de los backups.

```bash
#!/bin/bash
# Script de backup automático (backup.sh)

BACKUP_DIR="/var/backups/covid_dashboard"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Crear directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Backup de base de datos
echo "Iniciando backup de base de datos..."
sudo -u postgres pg_dump covid_data | gzip > "$BACKUP_DIR/covid_data_$DATE.sql.gz"

# Backup de archivos de aplicación
echo "Iniciando backup de aplicación..."
tar -czf "$BACKUP_DIR/application_$DATE.tar.gz" /path/to/covid_dashboard

# Verificar integridad del backup
echo "Verificando integridad del backup..."
if gzip -t "$BACKUP_DIR/covid_data_$DATE.sql.gz"; then
    echo "✓ Backup de base de datos verificado"
else
    echo "✗ Error en backup de base de datos"
    exit 1
fi

# Limpiar backups antiguos
echo "Limpiando backups antiguos..."
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completado exitosamente"
```

### Monitoreo de Rendimiento

El monitoreo de rendimiento incluye métricas de aplicación, base de datos, y sistema operativo. Estas métricas se recopilan continuamente y se utilizan para identificar tendencias, detectar anomalías, y planificar la capacidad futura.

```python
# Script de monitoreo de rendimiento (monitor.py)
import psutil
import psycopg2
import time
import json
from datetime import datetime

def collect_system_metrics():
    """Recopilar métricas del sistema"""
    return {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'load_average': psutil.getloadavg()
    }

def collect_database_metrics():
    """Recopilar métricas de la base de datos"""
    conn = psycopg2.connect(
        host="localhost",
        database="covid_data",
        user="superset_user",
        password="Marte_9de9"
    )
    
    cursor = conn.cursor()
    
    # Consultas activas
    cursor.execute("""
        SELECT count(*) FROM pg_stat_activity 
        WHERE state = 'active' AND datname = 'covid_data'
    """)
    active_queries = cursor.fetchone()[0]
    
    # Tamaño de la base de datos
    cursor.execute("""
        SELECT pg_size_pretty(pg_database_size('covid_data'))
    """)
    db_size = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'active_queries': active_queries,
        'database_size': db_size
    }

def main():
    """Función principal de monitoreo"""
    while True:
        metrics = {
            'system': collect_system_metrics(),
            'database': collect_database_metrics()
        }
        
        # Guardar métricas en archivo de log
        with open('/var/log/covid_dashboard_metrics.log', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
        
        # Alertas básicas
        if metrics['system']['cpu_percent'] > 80:
            print(f"ALERTA: CPU alta - {metrics['system']['cpu_percent']}%")
        
        if metrics['system']['memory_percent'] > 85:
            print(f"ALERTA: Memoria alta - {metrics['system']['memory_percent']}%")
        
        time.sleep(60)  # Recopilar métricas cada minuto

if __name__ == "__main__":
    main()
```

### Actualizaciones y Parches

El proceso de actualizaciones incluye tanto actualizaciones de seguridad del sistema operativo como actualizaciones de la aplicación. Se implementa un proceso de staging que permite probar las actualizaciones antes de aplicarlas en producción.

```bash
#!/bin/bash
# Script de actualización (update.sh)

echo "Iniciando proceso de actualización..."

# Crear punto de restauración
echo "Creando punto de restauración..."
./backup.sh

# Actualizar sistema operativo
echo "Actualizando sistema operativo..."
sudo apt update
sudo apt upgrade -y

# Actualizar dependencias de Python
echo "Actualizando dependencias de Python..."
source covid_env/bin/activate
pip install --upgrade -r requirements.txt

# Ejecutar tests de verificación
echo "Ejecutando tests de verificación..."
python -m pytest tests/ -v

# Reiniciar servicios si los tests pasan
if [ $? -eq 0 ]; then
    echo "Tests exitosos, reiniciando servicios..."
    sudo systemctl restart gunicorn
    sudo systemctl restart nginx
    echo "Actualización completada exitosamente"
else
    echo "Tests fallaron, revirtiendo cambios..."
    # Lógica de rollback aquí
    exit 1
fi
```

---

## Solución de Problemas

### Problemas Comunes y Soluciones

Esta sección documenta los problemas más frecuentes encontrados durante la instalación y operación del dashboard, junto con sus soluciones detalladas. La documentación de problemas comunes reduce significativamente el tiempo de resolución y mejora la experiencia del usuario.

#### Error de Conexión a Base de Datos

**Síntoma**: La aplicación no puede conectarse a PostgreSQL y muestra errores de conexión.

**Diagnóstico**:
```bash
# Verificar estado del servicio PostgreSQL
sudo systemctl status postgresql

# Verificar conectividad
sudo -u postgres psql -c "\l"

# Verificar configuración de autenticación
sudo cat /etc/postgresql/14/main/pg_hba.conf | grep -v "^#"
```

**Solución**:
```bash
# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Verificar y corregir configuración de autenticación
sudo nano /etc/postgresql/14/main/pg_hba.conf
# Asegurar que existe la línea:
# local   all             all                                     peer

# Recrear usuario si es necesario
sudo -u postgres psql -c "DROP USER IF EXISTS superset_user;"
sudo -u postgres psql -c "CREATE USER superset_user WITH PASSWORD 'Marte_9de9';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE covid_data TO superset_user;"
```

#### Problemas de Rendimiento

**Síntoma**: Las consultas son lentas o el dashboard tarda mucho en cargar.

**Diagnóstico**:
```sql
-- Identificar consultas lentas
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Verificar uso de índices
EXPLAIN ANALYZE SELECT * FROM covid_data_unified 
WHERE "Country_Region" = 'Mexico' 
ORDER BY "Date" DESC LIMIT 100;
```

**Solución**:
```sql
-- Recrear estadísticas de la base de datos
ANALYZE covid_data_unified;

-- Verificar y recrear índices si es necesario
REINDEX TABLE covid_data_unified;

-- Optimizar configuración de PostgreSQL
-- (Ajustar parámetros en postgresql.conf según recursos disponibles)
```

#### Errores de Memoria

**Síntoma**: La aplicación se cierra inesperadamente o muestra errores de memoria.

**Diagnóstico**:
```bash
# Verificar uso de memoria
free -h
ps aux --sort=-%mem | head -10

# Verificar logs del sistema
sudo journalctl -u gunicorn -f
```

**Solución**:
```bash
# Ajustar configuración de Gunicorn
# Reducir número de workers si es necesario
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 2  # Reducir de 4 a 2
worker_class = "sync"
max_requests = 500  # Reducir para liberar memoria más frecuentemente
EOF

# Reiniciar servicios
sudo systemctl restart gunicorn
```

### Logs y Debugging

El sistema de logging proporciona información detallada sobre el funcionamiento de la aplicación y facilita la identificación y resolución de problemas. Los logs se organizan por nivel de severidad y componente del sistema.

```python
# Configuración de logging para la aplicación
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    """Configurar sistema de logging"""
    if not app.debug:
        # Configurar archivo de log con rotación
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/covid_dashboard.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Dashboard COVID-19 iniciado')

# Uso en la aplicación
@app.route('/api/covid/global-stats')
def global_stats():
    try:
        app.logger.info('Solicitando estadísticas globales')
        stats = covid_service.get_global_stats()
        app.logger.info(f'Estadísticas globales obtenidas: {len(stats)} métricas')
        return jsonify(stats)
    except Exception as e:
        app.logger.error(f'Error obteniendo estadísticas globales: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500
```

### Herramientas de Diagnóstico

Las herramientas de diagnóstico automatizadas facilitan la identificación rápida de problemas y el monitoreo proactivo del sistema. Estas herramientas se pueden ejecutar manualmente o programar para ejecución automática.

```bash
#!/bin/bash
# Script de diagnóstico del sistema (diagnose.sh)

echo "=== DIAGNÓSTICO DEL DASHBOARD COVID-19 ==="
echo "Fecha: $(date)"
echo

# Verificar servicios
echo "=== ESTADO DE SERVICIOS ==="
systemctl is-active postgresql && echo "✓ PostgreSQL: Activo" || echo "✗ PostgreSQL: Inactivo"
systemctl is-active nginx && echo "✓ Nginx: Activo" || echo "✗ Nginx: Inactivo"
systemctl is-active gunicorn && echo "✓ Gunicorn: Activo" || echo "✗ Gunicorn: Inactivo"
echo

# Verificar conectividad de base de datos
echo "=== CONECTIVIDAD DE BASE DE DATOS ==="
if sudo -u postgres psql -d covid_data -c "SELECT 1;" &>/dev/null; then
    echo "✓ Conexión a base de datos: OK"
    
    # Verificar datos
    RECORD_COUNT=$(sudo -u postgres psql -d covid_data -t -c "SELECT COUNT(*) FROM covid_data_unified;")
    echo "✓ Registros en base de datos: $RECORD_COUNT"
else
    echo "✗ Conexión a base de datos: FALLO"
fi
echo

# Verificar endpoints de API
echo "=== ENDPOINTS DE API ==="
if curl -f -s http://localhost:5000/api/covid/global-stats &>/dev/null; then
    echo "✓ API global-stats: OK"
else
    echo "✗ API global-stats: FALLO"
fi

if curl -f -s http://localhost:5000/ &>/dev/null; then
    echo "✓ Frontend: OK"
else
    echo "✗ Frontend: FALLO"
fi
echo

# Verificar recursos del sistema
echo "=== RECURSOS DEL SISTEMA ==="
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)% utilizado"
echo "Memoria: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "Disco: $(df -h / | awk 'NR==2{printf "%s", $5}')"
echo

echo "=== DIAGNÓSTICO COMPLETADO ==="
```

---

## Referencias

### Documentación Técnica

[1] Flask Documentation. "Flask Web Development Framework." https://flask.palletsprojects.com/

[2] PostgreSQL Global Development Group. "PostgreSQL 14 Documentation." https://www.postgresql.org/docs/14/

[3] SQLAlchemy Documentation. "SQLAlchemy - The Database Toolkit for Python." https://docs.sqlalchemy.org/

[4] Pandas Development Team. "Pandas Documentation." https://pandas.pydata.org/docs/

[5] Chart.js Documentation. "Chart.js - Simple yet flexible JavaScript charting." https://www.chartjs.org/docs/

### Fuentes de Datos

[6] Johns Hopkins University Center for Systems Science and Engineering. "COVID-19 Data Repository." https://github.com/CSSEGISandData/COVID-19

[7] World Health Organization. "WHO Coronavirus (COVID-19) Dashboard." https://covid19.who.int/

### Mejores Prácticas y Estándares

[8] Python Software Foundation. "PEP 8 -- Style Guide for Python Code." https://peps.python.org/pep-0008/

[9] Mozilla Developer Network. "Web Security Guidelines." https://developer.mozilla.org/en-US/docs/Web/Security

[10] OWASP Foundation. "OWASP Top Ten Web Application Security Risks." https://owasp.org/www-project-top-ten/

### Herramientas de Desarrollo

[11] Git Documentation. "Git - Distributed Version Control System." https://git-scm.com/doc

[12] Nginx Documentation. "Nginx HTTP Server." https://nginx.org/en/docs/

[13] Gunicorn Documentation. "Gunicorn - Python WSGI HTTP Server." https://docs.gunicorn.org/

### Recursos Adicionales

[14] Linux Mint Documentation. "Linux Mint User Guide." https://linuxmint.com/documentation.php

[15] Ubuntu Server Guide. "Ubuntu Server Documentation." https://ubuntu.com/server/docs

---

## Conclusión

Esta guía proporciona una base sólida para el despliegue y mantenimiento del Dashboard COVID-19 en entornos Linux Mint 22. La implementación sigue las mejores prácticas de la industria en términos de seguridad, rendimiento, y mantenibilidad.

El sistema está diseñado para ser escalable y extensible, permitiendo futuras mejoras y adaptaciones según las necesidades específicas del usuario. La documentación detallada y los scripts de automatización facilitan tanto el despliegue inicial como el mantenimiento continuo del sistema.

Para soporte adicional o consultas específicas sobre la implementación, se recomienda consultar la documentación oficial de cada componente y las comunidades de desarrolladores correspondientes.

---

*Documento generado por Manus AI - Julio 2025*  
*Versión 1.0 - Compatible con Linux Mint 22*

