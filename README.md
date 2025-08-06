# Dashboard COVID-19: Análisis Global de Datos 📊

Este proyecto presenta un **Dashboard COVID-19** interactivo, una aplicación web profesional diseñada para el análisis de datos globales de la pandemia. Integra datos históricos de la Universidad Johns Hopkins (hasta marzo de 2023), procesados y persistidos en una base de datos PostgreSQL alojada en NeonDB. [cite_start]La visualización se logra mediante una interfaz web construida con Flask (backend) y HTML/CSS/JavaScript (frontend), desplegada eficientemente en la plataforma Render. [cite: 2, 3, 4]

[cite_start]Este proyecto no solo demuestra la capacidad para construir soluciones de datos de extremo a extremo, sino que también resalta la adaptabilidad y persistencia frente a los desafíos inherentes a la ciencia de datos en entornos reales. [cite: 5]

---

## 🚀 Demo en Vivo

Puedes explorar el dashboard desplegado en el siguiente enlace:
[cite_start][**Dashboard COVID-19 en Render**](https://dashboard-covid-19-9z64.onrender.com/) [cite: 7]

---

## ✨ Características Principales

[cite_start]El dashboard ofrece una vista integral de la pandemia, basada en los datos disponibles hasta marzo de 2023. [cite: 7]

* [cite_start]**Estadísticas Globales:** [cite: 11]
    * [cite_start]**Casos Confirmados Totales:** Suma acumulada global de casos confirmados. [cite: 12, 13, 20]
    * [cite_start]**Total de Muertes:** Suma acumulada global de muertes. [cite: 14, 21]
    * [cite_start]**Tasa de Mortalidad Global:** Calculada como $(Total\ de\ Muertes\ /\ Total\ de\ Confirmados) * 100$. [cite: 15, 22]
    * [cite_start]**Recuperados:** Muestra el pico máximo histórico de casos recuperados globales registrado en el dataset, debido a inconsistencias en los reportes más recientes de la fuente. [cite: 16, 18, 23, 24, 26]
* [cite_start]**Top 10 Países con Más Contagios:** Visualización de los países más afectados en términos de casos confirmados, con datos de la última fecha del dataset. [cite: 27, 28, 29, 30]
* [cite_start]**Top 10 Países con Más Decesos:** Destaca los países con el mayor número de fallecimientos, con datos de la última fecha del dataset. [cite: 43, 44, 45, 47]
* [cite_start]**Top 10 Países con la Tasa de Mortalidad Más Alta:** Gráfica que detalla los países con las tasas más elevadas, filtrando aquellos con al menos 1000 casos para mayor relevancia estadística. [cite: 61, 62, 63, 64]
* [cite_start]**Top 10 Países con la Tasa de Mortalidad Más Baja:** Identifica los países con las tasas de mortalidad más bajas, manteniendo el filtro de 1000 casos confirmados. [cite: 84, 85, 86, 87]
* [cite_start]**Histórico Global de Casos Recuperados:** Gráfico que muestra la evolución de los casos recuperados globalmente, evidenciando la inconsistencia de los datos de recuperación en las últimas fechas de la fuente original. [cite: 106, 107, 108, 109, 110]
* **Curva de Contagios Diarios para México:** Presenta los casos diarios confirmados para México. [cite_start]Se destaca que la calidad de los datos para México impide una visualización clara de las "olas" de contagio. [cite: 129, 134, 135, 136, 137, 138, 139, 140, 141, 153]

---

## 🛠️ Tecnologías Utilizadas

* [cite_start]**Backend:** Flask [cite: 4]
* [cite_start]**Frontend:** HTML, CSS, JavaScript [cite: 4]
* [cite_start]**Base de Datos:** PostgreSQL (NeonDB) [cite: 3]
* [cite_start]**Despliegue:** Render (PaaS) [cite: 4, 174, 176, 177, 178, 179]
* [cite_start]**Ingeniería de Datos:** Pandas [cite: 166]
* [cite_start]**ORM:** SQLAlchemy [cite: 171]
* **Control de Versiones:** Git / GitHub
* [cite_start]**Entorno de Desarrollo:** Linux Mint [cite: 157, 160]
* [cite_start]**Fuente de Datos:** Universidad Johns Hopkins (datos hasta marzo de 2023) [cite: 3, 7, 107]

---

## ⚙️ Proceso de Desarrollo y Despliegue

[cite_start]La realización de este dashboard fue un testimonio de perseverancia y adaptabilidad. [cite: 156] [cite_start]Desarrollado íntegramente en un entorno Linux debido a limitaciones de acceso a herramientas propietarias como Power BI Desktop, este proyecto fortaleció habilidades valiosas en la industria. [cite: 157, 158, 187]

### Retos Superados:

* [cite_start]**Fundamentos en Linux:** Consolidación de una base sólida para trabajar en servidores. [cite: 160]
* **Maestría en Bases de Datos (PostgreSQL):**
    * [cite_start]**Ubicación de Archivos de Configuración:** Debugging sistémico para encontrar la ruta correcta de `postgresql.conf`. [cite: 162, 163]
    * [cite_start]**Optimización de Rendimiento:** Ajuste de parámetros de memoria y configuración de WAL para cargas de trabajo analíticas. [cite: 164]
* [cite_start]**Gestión de Entornos Python Aislados:** Implementación rigurosa de entornos virtuales (`venv`) para reproducibilidad. [cite: 165]
* **Ingeniería de Datos con Pandas:**
    * [cite_start]**Inconsistencias de Datos de Origen:** Limpieza, cálculo de métricas diarias y manejo de valores anómalos de los CSV de Johns Hopkins, aplicando `max(0, x)` a casos diarios para evitar negativos. [cite: 167, 168]
    * [cite_start]**Desafío de la Métrica "Recuperados":** Adaptación de la visualización para mostrar el "pico histórico" en lugar de un cero engañoso debido a datos inconsistentes en las últimas fechas. [cite: 169, 170]
* [cite_start]**Desarrollo Backend con Flask y SQLAlchemy:** Construcción de una API RESTful robusta e interacción con la base de datos. [cite: 171]
    * [cite_start]**Errores de Sensibilidad a Mayúsculas/Minúsculas en SQL:** Superación de `Undefined Column` en PostgreSQL, aprendiendo la importancia de las convenciones y comillas dobles en SQL. [cite: 172, 173]
* **Despliegue Profesional con Render (PaaS):**
    * [cite_start]**Elección y Adaptación de Plataforma:** Transición a Render desde un despliegue manual, aprovechando los beneficios de PaaS. [cite: 176]
    * [cite_start]**Diagnóstico de Gunicorn:** Resolución de `ModuleNotFoundError` en Gunicorn, entendiendo la importación de aplicaciones Python. [cite: 177]
    * [cite_start]**Estrategia de Carga de Datos en la Nube:** Decisión sobre la carga inicial para optimizar recursos y aprovechar el Free Tier de NeonDB. [cite: 178]
    * [cite_start]**Errores de Sintaxis en Despliegue:** Depuración de `SyntaxError` debido a caracteres de escape en cadenas SQL de Python. [cite: 179]
* [cite_start]**Depuración Multi-Capa:** Capacidad para diagnosticar problemas en diferentes capas (base de datos, API Flask, frontend JavaScript) utilizando herramientas de logs y navegador. [cite: 180]
* [cite_start]**Persistencia y Creatividad ante los Retos:** Abordaje de cada error como una oportunidad de aprendizaje, demostrando una mentalidad de "ver el problema desde otra perspectiva" y una depuración constante. [cite: 181, 182, 183, 184]

---

## 📂 Estructura del Proyecto

├── app.py                  # Aplicación principal Flask (backend)
├── templates/              # Archivos HTML (frontend)
│   └── index.html
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── scripts.js
├── requirements.txt        # Dependencias de Python
├── data/                   # Scripts de ingesta de datos o datos iniciales
└── .gitignore              # Archivos y directorios a ignorar por Git

---

## 🏃 ¿Cómo Ejecutar el Proyecto Localmente?

Para correr el dashboard en tu máquina local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Vickmargo58/Dashboard-covid-19.git](https://github.com/Vickmargo58/Dashboard-covid-19.git)
    cd Dashboard-covid-19
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate   # En Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos PostgreSQL:**
    * Asegúrate de tener PostgreSQL instalado y configurado, o utiliza un servicio como NeonDB.
    * Crea una base de datos.
    * Define tus variables de entorno para la conexión a la base de datos (e.g., `DATABASE_URL`). Puedes usar un archivo `.env` y cargar las variables con `python-dotenv`.
        ```
        # Ejemplo de .env
        DATABASE_URL="postgresql://user:password@host:port/database_name"
        ```

5.  **Cargar los datos (si no lo hiciste con un job de Render):**
    * Tendrás que adaptar un script para cargar los datos de Johns Hopkins (los CSV originales) a tu base de datos PostgreSQL. Esto implicaría la limpieza y transformación de los datos como se menciona en el proceso de desarrollo.

6.  **Ejecutar la aplicación Flask:**
    ```bash
    export FLASK_APP=app.py
    flask run
    ```
    (En Windows, usa `set FLASK_APP=app.py`)

7.  Abre tu navegador y visita `http://127.0.0.1:5000/` para ver el dashboard.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una mejora, no dudes en abrir un *issue* o enviar un *pull request*.

---

## 📧 Contacto

[cite_start][Tu Nombre Completo] (Mario Fernandez Castillo) [cite: 198]
[cite_start] Científico de Datos [cite: 199]
[Tu Email] Mario.fernandezc23@gmail.com
[Tu Perfil de LinkedIn] https://www.linkedin.com/in/mario-fernandez-castillo/

---

## Licencia

Este proyecto está bajo la Licencia MIT.
