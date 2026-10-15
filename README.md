# Pipeline ETL para Procesamiento de Encuestas de Opinión

Este repositorio sirve como un ejemplo público, agnóstico y libre de contexto de un pipeline ETL (Extracción, Transformación y Carga) diseñado específicamente para el procesamiento de encuestas de opinión e investigación social.

El objetivo es proporcionar a investigadores y analistas de datos una arquitectura robusta para automatizar la limpieza, recodificación y estructuración de datos provenientes de plataformas como Google Forms, SurveyMonkey o similares, separando la lógica de negocio del código base mediante archivos de configuración.

## 🏗️ Arquitectura y Estructura del Proyecto

El pipeline sigue un enfoque modular dividido en etapas lógicas de calidad de datos (Bronce, Plata y Oro):

```text
/etl-encuestas-ejemplo
│
├── data/
│   ├── raw/             <- (Bronce) Datos crudos, simulando exportaciones directas con ruido y errores.
│   ├── interim/         <- (Plata) Datos con limpieza estructural (nombres de columnas, tipos de datos).
│   └── processed/       <- (Oro) Datos recodificados, transformados y listos para análisis o BI.
│
├── src/
│   ├── 1_generate_mock.py  <- Genera una base sintética con ruido realista (errores de tipeo, nulos).
│   ├── 2_clean.py          <- Estandariza nombres, parsea fechas y corrige tipos de datos numéricos.
│   ├── 3_transform.py      <- Aplica recodificación de escalas Likert y One-Hot Encoding.
│   └── 4_melt.py           <- Despivota preguntas de opción múltiple a formato Long/Relacional.
│
├── config/
│   └── codebook.yml        <- Diccionario de datos estático (fuente de la verdad para los mapeos).
│
├── requirements.txt        <- Dependencias del proyecto.
└── README.md
```

## 🚀 Características Principales

*   **Configuración Desacoplada (`codebook.yml`):** Evita el *hardcoding* en Python. Los nombres de las variables, las escalas numéricas y las opciones válidas se definen en un archivo YAML estático y fácil de editar por investigadores sin conocimientos avanzados de programación.
*   **Manejo de Respuestas Múltiples:** 
    *   Generación de variables Dummies (One-Hot Encoding) en la tabla principal para modelado estadístico.
    *   Generación de una tabla relacional secundaria (`encuesta_preg_mult.csv`) mediante despivotado (*melt*), ideal para tableros en Data Studio, Power BI o Tableau.
*   **Ruido Realista:** Para que el repositorio sea fácil de probar se agregó un script que genera datos de prueba. Para que el script se acerque levemente al tipo de datos reales simula errores de carga, espacios en blanco extra y respuestas inconsistentes. Esto permite demostrar el valor real de las capas de limpieza.

## 🛠️ Cómo Ejecutar el Pipeline

### 1. Preparar el entorno
Se recomienda utilizar un entorno virtual. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar los procesos en orden
Ejecuta los scripts desde la raíz del proyecto para respetar las rutas relativas:

**Paso 1: Generar los datos crudos**
```bash
python src/1_generate_mock.py
```
*Output: `data/raw/encuesta_cruda.csv`*

**Paso 2: Limpieza estructural**
```bash
python src/2_clean.py
```
*Output: `data/interim/encuesta_limpia.csv`*

**Paso 3: Transformación y recodificación**
```bash
python src/3_transform.py
```
*Output: `data/processed/encuesta_procesada.csv`*

**Paso 4: Despivotado de preguntas múltiples**
```bash
python src/4_melt.py
```
*Output: `data/processed/encuesta_preg_mult.csv`*

## 📈 Siguientes Pasos y Personalización
Para adaptar este pipeline a tu propia encuesta, simplemente reemplaza el archivo `data/raw/encuesta_cruda.csv` con tus datos reales y actualiza las reglas de mapeo dentro de `config/codebook.yml` para que coincidan con las preguntas de tu formulario.