# Análisis del catálogo de Netflix: Pandas, MapReduce, SQL y PySpark

Proyecto del **Segundo Momento Evaluativo** de **Tecnologías Emergentes I** (Unidad 3: Big Data y Herramientas Esenciales).

## 1. ¿Qué hace este proyecto?

Analiza el catálogo de Netflix (`netflix_titles.csv`, conjunto de datos *Netflix Movies and TV Shows* de Kaggle) para responder tres preguntas:

1. ¿Cuántas películas y series contiene?
2. ¿Qué actores participan en la mayor cantidad de títulos?
3. ¿Cuál es la duración promedio de las películas por país?

Para responderlas se construye un proceso en cuatro retos:

| Reto | Qué se hace | Herramientas | Carpeta |
|---|---|---|---|
| **1** | Limpiar el archivo original y generar `netflix_clean.csv` | Python, Pandas | `Limpieza/` |
| **2** | Contar en cuántos títulos participa cada actor | HDFS, Hadoop Streaming, Python, Docker | `reto2_mapreduce/` |
| **3** | Analizar con SQL y PySpark y verificar que coincidan con MapReduce | Databricks, Apache Spark | [ ] |
| **4** | Gráficos, tablas, diagrama y conclusiones | Databricks, Matplotlib | [ ] |

### Flujo de los datos

```
netflix_titles.csv ──(Reto 1: limpieza, Pandas)──> netflix_clean.csv
                                                        │
                    ┌───────────────────────────────────┴──────────────────────────┐
                    │ netflix_clean.csv                                             │ netflix_clean.csv
                    ▼                                                               ▼
        HDFS ──> MapReduce (Reto 2)                                   Databricks (Reto 3): SQL y PySpark
                    │                                                               │
                    ▼                                                               │
          mapreduce_actores.csv ─────────(carga en Databricks)──────────> comparación MapReduce vs. Spark
```

Todos los análisis usan **el mismo archivo limpio**. Si se modifica la limpieza, hay que generar `netflix_clean.csv` de nuevo y **repetir los retos 2, 3 y 4**.

## 2. Equipo

| Integrante | Reto |
|---|---|
| Ximena Fernanda Mollo Olivarez | [ ] |
| Sarahy Lacoa Imaña | [ ] |
| Minerva Yolanda Olga Rodriguez Diaz | [ ] |

Exposición: lunes 16 y miércoles 18 de noviembre de 2026 (según la asignación del grupo).

## 3. Estructura del repositorio

```
DataSets/
├── README.md                  <- esta guía
├── Limpieza/                  <- Reto 1
│   ├── netflix_titles.csv     <- archivo original
│   ├── netflix_clean.csv      <- archivo limpio (entrada de los retos 2 y 3)
│   └── 01_limpiar_netflix.py  <- programa de limpieza  [verificar el nombre]
├── reto2_mapreduce/           <- Reto 2
│   ├── README.md              <- guía detallada del Reto 2
│   ├── 02_mapper_actores.py
│   ├── 02_reducer_actores.py
│   ├── 02_ejecutar_mapreduce.txt
│   ├── 02_exportar_resultado.py
│   ├── docker-compose.yml
│   ├── hadoop.env
│   ├── mapreduce_actores.csv
│   └── evidencias/            <- capturas
├── [ ] carpeta del Reto 3     <- notebook 03_analisis_netflix.ipynb exportado
└── [ ] informe y presentación (opcional)
```

Cada integrante trabaja en **su propia carpeta y su propia rama**, para evitar conflictos.

## 4. Versiones utilizadas

| Componente | Versión |
|---|---|
| Sistema operativo | Windows [ ] |
| Git | [ ] (`git --version`) |
| Python (Windows) | [ ] (`python --version`) |
| pandas | [ ] (`pip show pandas`) |
| Docker Desktop | [ ] (`docker --version`) |
| Imagen de Hadoop | `apache/hadoop:3` (Hadoop [ ], ver `hadoop version`) |
| Python en el NodeManager | 3.6.8 |
| Databricks | [ ] (versión del runtime del clúster o de la edición gratuita) |
| Apache Spark | [ ] (`spark.version` en el notebook) |

## 5. Requisitos previos (instalar una sola vez)

| Herramienta | Para qué | Cómo verificarla |
|---|---|---|
| **Git** (git-scm.com) | Clonar el repositorio y trabajar con ramas | `git --version` |
| **Python 3** (python.org) | Limpieza y exportación | `python --version` |
| **pandas** | Retos 1 y 2 | `pip install pandas` |
| **Docker Desktop** (docker.com) | Clúster Hadoop (Reto 2) | `docker --version` y `docker compose version` |
| **Visual Studio Code** (opcional) | Editor. Extensión recomendada: *Python* | |
| **Cuenta de Databricks** | Reto 3 y 4 | |

Además, para el Reto 2:

- Docker Desktop debe estar abierto y en estado **Engine running**.
- Se necesitan **al menos 10 GB libres** en el disco C. Con el disco lleno, Docker pasa a modo solo lectura y falla.

## 6. Clonar el repositorio

```powershell
cd $HOME\Desktop
git clone https://github.com/XimenaRandom/DataSets.git
cd DataSets
```

Esto descarga el repositorio con la rama principal (`main`). Se puede clonar en cualquier carpeta; `Desktop` es solo un ejemplo.

## 7. Trabajar con ramas

### 7.1. Ver todas las ramas

```powershell
git fetch origin
git branch -a
```

### 7.2. Usar la rama principal (`main`)

```powershell
git checkout main
git pull origin main
```

### 7.3. Usar la rama de otra persona (para probar su trabajo)

Ejemplo con la rama del Reto 2:

```powershell
git fetch origin
git checkout reto2-mapreduce
git pull origin reto2-mapreduce
```

### 7.4. Crear tu propia rama (para trabajar sin conflictos)

Siempre partiendo de una `main` actualizada:

```powershell
git checkout main
git pull origin main
git checkout -b nombre-de-tu-rama
```

Ejemplos de nombres: `reto1-limpieza`, `reto3-databricks`, `reto4-presentacion`.

### 7.5. Subir tu trabajo y abrir un Pull Request

```powershell
git status
git add nombre_de_tu_carpeta
git commit -m "Descripción corta de lo que hiciste"
git push -u origin nombre-de-tu-rama
```

Luego, en GitHub: **Compare & pull request** (o **Pull requests > New pull request**), comprobar que diga *base: `main` ← compare: tu rama*, escribir una descripción y pulsar **Create pull request**. Cuando el equipo lo revise, se usa **Merge pull request**.

### 7.6. Actualizar tu copia después de un merge

```powershell
git checkout main
git pull origin main
```

### Reglas del equipo

- No editar archivos fuera de tu carpeta.
- No subir a `main` directamente; usar siempre una rama y un Pull Request.
- Hacer `git pull origin main` antes de empezar a trabajar.
- Si `git status` muestra cambios de otras carpetas, no subirlos.

## 8. Cómo ejecutar el proyecto, en orden

### Reto 1. Limpieza con Python y Pandas

Carpeta: `Limpieza/`.

1. Descargar `netflix_titles.csv` desde Kaggle (*Netflix Movies and TV Shows*) y colocarlo en `Limpieza/`.
2. Ejecutar:

```powershell
cd Limpieza
pip install pandas
python 01_limpiar_netflix.py
```

3. El programa genera `netflix_clean.csv` en la misma carpeta e imprime la **Tabla 1** (resultado de la limpieza).

**Qué hace la limpieza:**

- Reemplaza saltos de línea y tabulaciones por espacios, quita espacios al inicio y al final y convierte los textos vacíos en nulos.
- Convierte `date_added` a `dd/mm/aaaa` (vacío si no puede interpretarse).
- Crea `duration_min` (minutos de las películas, entero que admite nulos; vacío en las series).
- Elimina filas duplicadas, registros sin `show_id` y `show_id` repetidos, conservando la primera aparición.
- Guarda el CSV con cabecera, separado por comas y sin el índice de Pandas.

> **Nota técnica:** el archivo se guarda con codificación `utf-8-sig`, que añade una marca BOM al inicio. Los programas posteriores deben leerlo con `utf-8-sig` (el mapper del Reto 2 ya lo hace) y, en Databricks, conviene revisar que la primera columna se llame `show_id` y no `\ufeffshow_id`.

### Reto 2. Conteo de títulos por actor con MapReduce

Carpeta: `reto2_mapreduce/`. La guía completa, con todos los comandos y la solución de problemas, está en [`reto2_mapreduce/README.md`](reto2_mapreduce/README.md). Resumen de los pasos:

```powershell
cd reto2_mapreduce
docker compose up -d                       # 1. levantar el clúster Hadoop
docker compose exec -u root nodemanager bash   # 2. instalar Python 3 (solo la primera vez)
docker compose exec resourcemanager bash   # 3. cargar a HDFS y ejecutar MapReduce
python 02_exportar_resultado.py resultado_hdfs mapreduce_actores.csv   # 4. generar el CSV
docker compose stop                        # 5. apagar (no usar "down")
```

Resultado: `mapreduce_actores.csv` con las columnas `actor` y `cantidad_titulos`, ordenado por cantidad descendente y, en caso de empate, por nombre ascendente.

### Reto 3. Análisis y verificación en Databricks

Carpeta: [ ].

1. Crear una cuenta o abrir el espacio de trabajo de Databricks.
2. Subir `Limpieza/netflix_clean.csv` y `reto2_mapreduce/mapreduce_actores.csv`.
3. Crear las tablas `netflix_clean` y `mapreduce_actores`.
4. Importar el notebook `03_analisis_netflix` y ejecutarlo de arriba hacia abajo.
5. Comprobar que:
   - las cabeceras se interpretan como nombres de columnas,
   - los campos con comas se leen correctamente,
   - la cantidad de registros de `netflix_clean` coincide con la Tabla 1,
   - la cantidad de actores de `mapreduce_actores` coincide con las filas del CSV exportado.

Catálogo, esquema y nombres completos de las tablas: [ ].

### Reto 4. Hallazgos

Carpeta: [ ]. Dos gráficos (tipos y diez actores con más títulos), la Tabla 6 (duración promedio por país), el diagrama del proceso y las conclusiones (menos de 250 palabras).

## 9. Entregables y dónde encontrarlos

| Entregable pedido | Ubicación | Estado |
|---|---|---|
| Archivo original y archivo limpio | `Limpieza/netflix_titles.csv`, `Limpieza/netflix_clean.csv` | [ ] |
| Programa de limpieza | `Limpieza/01_limpiar_netflix.py` | [ ] |
| Mapper y reducer | `reto2_mapreduce/02_mapper_actores.py`, `02_reducer_actores.py` | [ ] |
| Programa de exportación | `reto2_mapreduce/02_exportar_resultado.py` | [ ] |
| Comando de ejecución de MapReduce | `reto2_mapreduce/02_ejecutar_mapreduce.txt` | [ ] |
| `mapreduce_actores.csv` | `reto2_mapreduce/mapreduce_actores.csv` | [ ] |
| Notebook `.ipynb` con resultados visibles | [ ] | [ ] |
| README con versiones y pasos de ejecución | este archivo y `reto2_mapreduce/README.md` | [ ] |
| Informe `Informe_Netflix_<equipo>.pdf` | entrega por Teams | [ ] |
| Presentación `Presentacion_Netflix_Grupo.pdf` | entrega por Teams | [ ] |

## 10. Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `git clone` pide usuario o contraseña | Autorizar en la ventana del navegador que abre Git. |
| `git checkout nombre-rama` no encuentra la rama | Ejecutar antes `git fetch origin`. |
| `ModuleNotFoundError: No module named 'pandas'` | Ejecutar `pip install pandas` (o `python -m pip install pandas`). |
| Docker: `read-only file system` o `input/output error` | Disco C lleno. Liberar más de 10 GB, ejecutar `wsl --shutdown` y reiniciar Docker Desktop. |
| MapReduce: `Cannot run program "python3"` | Falta instalar Python 3 en el NodeManager (ver `reto2_mapreduce/README.md`, paso 4). |
| Aparece un actor llamado `cast` en el resultado | Se usó un mapper antiguo sin soporte de BOM. Usar el actual y repetir el MapReduce. |
| Tildes mal mostradas en PowerShell | Ejecutar antes `$env:PYTHONUTF8 = "1"`. El CSV sí queda en UTF-8. |

## 11. Referencias

- Kaggle: *Netflix Movies and TV Shows* (`netflix_titles.csv`).
- Apache Hadoop: documentación de Hadoop Streaming.
- Databricks y Apache Spark: documentación oficial.
- Imagen de Docker utilizada: `apache/hadoop:3`.
