#!/bin/bash
set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si el comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar privilegios sudo
check_sudo() {
    if ! sudo -n true 2>/dev/null; then
        print_error "Este script requiere privilegios sudo. Por favor, ejecute con sudo o configure sudo sin contraseña."
        exit 1
    fi
}

# Función para verificar sistema operativo
check_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" == "linuxmint" ]] || [[ "$ID" == "ubuntu" ]]; then
            print_success "Sistema operativo compatible detectado: $PRETTY_NAME"
        else
            print_warning "Sistema operativo no probado: $PRETTY_NAME"
            print_warning "Este script está optimizado para Linux Mint 22 y Ubuntu 22.04+"
            read -p "¿Desea continuar? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_error "No se pudo detectar el sistema operativo"
        exit 1
    fi
}

# Función para instalar dependencias del sistema
install_system_dependencies() {
    print_status "Actualizando repositorios del sistema..."
    sudo apt update

    print_status "Instalando dependencias del sistema..."
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        postgresql \
        postgresql-contrib \
        libpq-dev \
        build-essential \
        curl \
        wget \
        git \
        nginx \
        supervisor

    print_success "Dependencias del sistema instaladas correctamente"
}

# Función para configurar PostgreSQL
setup_postgresql() {
    print_status "Configurando PostgreSQL..."
    
    # Iniciar y habilitar PostgreSQL
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # Crear base de datos y usuario
    print_status "Creando base de datos y usuario..."
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS covid_data;" 2>/dev/null || true
    sudo -u postgres psql -c "DROP USER IF EXISTS superset_user;" 2>/dev/null || true
    
    sudo -u postgres psql -c "CREATE DATABASE covid_data;"
    sudo -u postgres psql -c "CREATE USER superset_user WITH PASSWORD 'Marte_9de9';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE covid_data TO superset_user;"
    
    print_success "PostgreSQL configurado correctamente"
}

# Función para crear entorno Python
setup_python_environment() {
    print_status "Configurando entorno Python..."
    
    # Crear directorio del proyecto
    PROJECT_DIR="$HOME/covid_dashboard"
    if [[ -d "$PROJECT_DIR" ]]; then
        print_warning "El directorio $PROJECT_DIR ya existe. Eliminando..."
        rm -rf "$PROJECT_DIR"
    fi
    
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Crear entorno virtual
    python3 -m venv venv
    source venv/bin/activate
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias
    print_status "Instalando dependencias de Python..."
    pip install \
        flask==3.1.1 \
        sqlalchemy==2.0.41 \
        psycopg2-binary==2.9.10 \
        pandas==2.3.1 \
        plotly==6.2.0 \
        flask-cors==6.0.0 \
        numpy==2.3.1 \
        gunicorn
    
    # Crear requirements.txt
    pip freeze > requirements.txt
    
    print_success "Entorno Python configurado correctamente"
}

# Función para crear estructura del proyecto
create_project_structure() {
    print_status "Creando estructura del proyecto..."
    
    cd "$PROJECT_DIR"
    
    # Crear directorios
    mkdir -p src/{models,routes,static,database}
    mkdir -p logs
    mkdir -p data
    
    print_success "Estructura del proyecto creada"
}

# Función para copiar archivos del proyecto
copy_project_files() {
    print_status "Copiando archivos del proyecto..."
    
    # Copiar archivos desde el directorio actual del script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Copiar archivos de código fuente
    if [[ -f "$SCRIPT_DIR/src/main.py" ]]; then
        cp -r "$SCRIPT_DIR/src/"* "$PROJECT_DIR/src/"
    else
        print_error "No se encontraron archivos de código fuente en $SCRIPT_DIR"
        exit 1
    fi
    
    # Copiar archivos de datos
    if [[ -f "$SCRIPT_DIR/data/time_series_covid19_confirmed_global.csv" ]]; then
        cp "$SCRIPT_DIR/data/"*.csv "$PROJECT_DIR/data/"
        cp "$SCRIPT_DIR/data/prepare_covid_data.py" "$PROJECT_DIR/data/"
    else
        print_error "No se encontraron archivos de datos en $SCRIPT_DIR"
        exit 1
    fi
    
    print_success "Archivos del proyecto copiados"
}

# Función para cargar datos iniciales
load_initial_data() {
    print_status "Cargando datos iniciales..."
    
    cd "$PROJECT_DIR"
    source venv/bin/activate
    
    # Copiar archivos CSV al directorio del proyecto
    cp data/*.csv .
    cp data/prepare_covid_data.py .
    
    # Ejecutar script de carga de datos
    python prepare_covid_data.py
    
    # Limpiar archivos temporales
    rm -f *.csv prepare_covid_data.py
    
    print_success "Datos iniciales cargados correctamente"
}

# Función para configurar servicios del sistema
setup_system_services() {
    print_status "Configurando servicios del sistema..."
    
    # Crear archivo de configuración de Gunicorn
    cat > "$PROJECT_DIR/gunicorn.conf.py" << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
user = "$(whoami)"
group = "$(whoami)"
EOF

    # Crear archivo de servicio systemd para Gunicorn
    sudo tee /etc/systemd/system/covid-dashboard.service > /dev/null << EOF
[Unit]
Description=COVID Dashboard Gunicorn Application
After=network.target

[Service]
User=$(whoami)
Group=$(whoami)
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config gunicorn.conf.py src.main:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Configurar Nginx
    sudo tee /etc/nginx/sites-available/covid-dashboard > /dev/null << EOF
server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias $PROJECT_DIR/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
EOF

    # Habilitar sitio de Nginx
    sudo ln -sf /etc/nginx/sites-available/covid-dashboard /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Recargar configuraciones
    sudo systemctl daemon-reload
    sudo systemctl enable covid-dashboard
    sudo systemctl restart nginx
    
    print_success "Servicios del sistema configurados"
}

# Función para iniciar servicios
start_services() {
    print_status "Iniciando servicios..."
    
    sudo systemctl start covid-dashboard
    sudo systemctl restart nginx
    
    # Esperar a que los servicios inicien
    sleep 5
    
    # Verificar que los servicios estén funcionando
    if systemctl is-active --quiet covid-dashboard; then
        print_success "Servicio COVID Dashboard iniciado correctamente"
    else
        print_error "Error al iniciar el servicio COVID Dashboard"
        sudo journalctl -u covid-dashboard --no-pager -n 20
        exit 1
    fi
    
    if systemctl is-active --quiet nginx; then
        print_success "Nginx iniciado correctamente"
    else
        print_error "Error al iniciar Nginx"
        exit 1
    fi
}

# Función para verificar la instalación
verify_installation() {
    print_status "Verificando instalación..."
    
    # Verificar conectividad de base de datos
    if sudo -u postgres psql -d covid_data -c "SELECT COUNT(*) FROM covid_data_unified;" >/dev/null 2>&1; then
        RECORD_COUNT=$(sudo -u postgres psql -d covid_data -t -c "SELECT COUNT(*) FROM covid_data_unified;" | tr -d ' ')
        print_success "Base de datos verificada: $RECORD_COUNT registros"
    else
        print_error "Error en la verificación de base de datos"
        exit 1
    fi
    
    # Verificar API
    if curl -f -s http://localhost/api/covid/global-stats >/dev/null 2>&1; then
        print_success "API verificada correctamente"
    else
        print_error "Error en la verificación de API"
        exit 1
    fi
    
    # Verificar frontend
    if curl -f -s http://localhost/ | grep -q "Dashboard COVID-19"; then
        print_success "Frontend verificado correctamente"
    else
        print_error "Error en la verificación de frontend"
        exit 1
    fi
}

# Función para mostrar información final
show_final_info() {
    echo
    echo "=================================================================="
    echo -e "${GREEN}    INSTALACIÓN COMPLETADA EXITOSAMENTE${NC}"
    echo "=================================================================="
    echo
    echo "El Dashboard COVID-19 está ahora disponible en:"
    echo -e "${BLUE}    http://localhost${NC}"
    echo
    echo "Ubicación del proyecto:"
    echo -e "${BLUE}    $PROJECT_DIR${NC}"
    echo
    echo "Comandos útiles:"
    echo -e "${YELLOW}    # Ver logs del servicio${NC}"
    echo "    sudo journalctl -u covid-dashboard -f"
    echo
    echo -e "${YELLOW}    # Reiniciar servicios${NC}"
    echo "    sudo systemctl restart covid-dashboard"
    echo "    sudo systemctl restart nginx"
    echo
    echo -e "${YELLOW}    # Verificar estado de servicios${NC}"
    echo "    sudo systemctl status covid-dashboard"
    echo "    sudo systemctl status nginx"
    echo
    echo -e "${YELLOW}    # Acceder al entorno virtual${NC}"
    echo "    cd $PROJECT_DIR && source venv/bin/activate"
    echo
    echo "=================================================================="
}

# Función principal
main() {
    echo "=================================================================="
    echo "    Dashboard COVID-19 - Instalación Automatizada"
    echo "    Compatible con Linux Mint 22 y Ubuntu 22.04+"
    echo "=================================================================="
    echo
    
    # Verificaciones previas
    check_sudo
    check_os
    
    # Proceso de instalación
    install_system_dependencies
    setup_postgresql
    setup_python_environment
    create_project_structure
    copy_project_files
    load_initial_data
    setup_system_services
    start_services
    verify_installation
    show_final_info
    
    print_success "¡Instalación completada exitosamente!"
}

# Ejecutar función principal
main "$@"

