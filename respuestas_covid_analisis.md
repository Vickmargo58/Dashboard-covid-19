# Respuestas al Análisis COVID-19
## Análisis de Datos Globales - Universidad Johns Hopkins

### Estadísticas Globales (Datos hasta marzo 2023)
- **Total de casos confirmados**: 676,570,149
- **Total de muertes**: 6,881,802
- **Tasa de mortalidad global**: 1.02%
- **Recuperados**: 0 (datos no disponibles en el dataset más reciente)

---

## Respuestas a las Preguntas Específicas

### 1. ¿Cuáles son los 10 países con más contagios?

**Top 10 Países con Más Casos Confirmados:**

1. **Estados Unidos (US)** - 103,802,702 casos
2. **India** - 44,690,738 casos
3. **Francia** - 39,866,718 casos
4. **Alemania** - 38,249,060 casos
5. **Brasil** - 37,076,053 casos
6. **Japón** - 33,320,438 casos
7. **Corea del Sur** - 30,615,522 casos
8. **Italia** - 25,603,510 casos
9. **Reino Unido** - 24,658,705 casos
10. **Rusia** - 22,075,858 casos

### 2. ¿Cuáles son los 10 países con más decesos?

**Top 10 Países con Más Muertes:**

1. **Estados Unidos (US)** - 1,123,836 muertes
2. **Brasil** - 699,276 muertes
3. **India** - 530,779 muertes
4. **Rusia** - 388,478 muertes
5. **México** - 333,188 muertes
6. **Reino Unido** - 220,721 muertes
7. **Perú** - 219,539 muertes
8. **Italia** - 188,322 muertes
9. **Alemania** - 168,935 muertes
10. **Francia** - 166,176 muertes

### 3. ¿Cuál es la tasa de mortalidad y cuáles son los 10 países con la tasa de mortalidad más alta?

**Tasa de mortalidad global**: 1.02%

**Top 10 Países con Mayor Tasa de Mortalidad:**

1. **Corea del Norte** - 600.00%
2. **MS Zaandam** - 22.22%
3. **Yemen** - 18.07%
4. **Sudán** - 7.86%
5. **Siria** - 5.51%
6. **Somalia** - 4.98%
7. **Perú** - 4.89%
8. **Egipto** - 4.81%
9. **México** - 4.45%
10. **Bosnia y Herzegovina** - 4.05%

### 4. ¿Cuáles son los 10 países con la tasa de mortalidad más baja?

**Top 10 Países con Menor Tasa de Mortalidad (con al menos 1,000 casos):**

1. **Nauru** - 0.02%
2. **Bután** - 0.03%
3. **Burundi** - 0.07%
4. **Singapur** - 0.08%
5. **Tonga** - 0.08%
6. **Brunéi** - 0.08%
7. **Islas Marshall** - 0.11%
8. **Corea del Sur** - 0.11%
9. **Nueva Zelanda** - 0.11%
10. **Vanuatu** - 0.12%

### 5. ¿Cuáles son los países con mayor índice de recuperación?

**Nota importante**: Los datos de recuperación no están disponibles en el dataset más reciente de la Universidad Johns Hopkins. A partir de 2022, muchos países dejaron de reportar datos de recuperación debido a cambios en las políticas de seguimiento de la pandemia.

**Tasa de recuperación global**: 0.00% (datos no disponibles)

### 6. ¿Cómo se ve la curva de contagios diarios para México?

**Análisis de México:**
- **Casos totales confirmados**: 7,483,444
- **Muertes totales**: 333,188
- **Tasa de mortalidad**: 4.45%
- **Posición en ranking mundial**: 5° lugar en muertes, fuera del top 10 en casos confirmados

**Características de la curva de contagios diarios en México:**
- El dashboard muestra la evolución temporal de casos diarios con promedio móvil de 7 días
- México experimentó múltiples olas de contagio durante la pandemia
- La tasa de mortalidad de México (4.45%) está significativamente por encima del promedio global (1.02%)

---

## Observaciones Importantes

### Limitaciones de los Datos
1. **Datos de recuperación**: No disponibles en el dataset más reciente
2. **Subregistro**: Muchos países pueden tener subregistro de casos y muertes
3. **Políticas de testeo**: Diferentes estrategias de testeo entre países afectan las comparaciones

### Metodología
- **Fuente**: Universidad Johns Hopkins COVID-19 Data Repository
- **Período**: Enero 2020 - Marzo 2023
- **Procesamiento**: Agregación por país, cálculo de tasas y métricas diarias
- **Visualización**: Dashboard interactivo con Flask y Chart.js

### Conclusiones Clave
1. **Estados Unidos** lidera tanto en casos confirmados como en muertes absolutas
2. **México** tiene una tasa de mortalidad preocupantemente alta (4.45%)
3. Los países asiáticos como **Corea del Sur** y **Singapur** muestran tasas de mortalidad muy bajas
4. La pandemia tuvo impactos muy desiguales entre países y regiones

---

*Análisis realizado con tecnologías: Python, PostgreSQL, Flask, Chart.js*
*Compatible con Linux Mint 22*

