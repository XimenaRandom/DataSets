## README

Trabajo de **Tecnologías Emergentes I** (Unidad 3: Big Data y Herramientas Esenciales).
Este reto carga `netflix_clean.csv` en HDFS y cuenta, con Hadoop Streaming y Python, en cuántos títulos distintos participa cada actor.

- **Entrada:** `netflix_clean.csv` (generado en el Reto 1, carpeta `../Limpieza/`)
- **Salida final:** `mapreduce_actores.csv` (columnas `actor`, `cantidad_titulos`)

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `02_mapper_actores.py` | Mapper. Lee el CSV por entrada estándar, omite la cabecera, interpreta las filas con el módulo `csv`, separa los actores de `cast` y emite `actor<TAB>show_id`. |
| `02_reducer_actores.py` | Reducer. Cuenta los `show_id` distintos de cada actor y emite `actor<TAB>cantidad_titulos`. |
| `02_ejecutar_mapreduce.txt` | Comando completo de Hadoop Streaming usado en la ejecución. |
| `02_exportar_resultado.py` | Reúne las partes `part-*` descargadas de HDFS y genera `mapreduce_actores.csv`. |
| `docker-compose.yml` | Define el clúster Hadoop (NameNode, DataNode, ResourceManager, NodeManager). |
| `hadoop.env` | Configuración de Hadoop para los contenedores. |
| `mapreduce_actores.csv` | Resultado final del reto. |

## Versiones utilizadas

| Componente | Versión |
|---|---|
| Sistema operativo | Windows [ ] |
| Docker Desktop | [ ] (`docker --version`) |
| Imagen de Hadoop | `apache/hadoop:3` (Hadoop [ ], ver `hadoop version`) |
| Python en el NodeManager | 3.6.8 (instalado con `yum`) |
| Python en Windows | [ ] (`python --version`) |
| pandas | [ ] (`pip show pandas`) |

## Requisitos previos

1. Docker Desktop instalado y en estado **Engine running**.
2. Python y pandas instalados en Windows (`pip install pandas`).
3. Al menos **10 GB libres** en el disco C. Con el disco lleno, Docker pasa a modo solo lectura y falla.
4. El archivo `netflix_clean.csv` dentro de la carpeta `Limpieza/` del repositorio. El `docker-compose.yml` la monta desde `../Limpieza`, así que la estructura debe ser:

```
DataSets/
├── Limpieza/
│   └── netflix_clean.csv
└── reto2_mapreduce/
```

## Pasos de ejecución (en orden)

Todos los comandos con `PS>` se ejecutan en PowerShell, dentro de `DataSets\reto2_mapreduce`.
Los que dicen `bash` se ejecutan dentro del contenedor.

### 1. Levantar el clúster

```powershell
PS> docker compose up -d
PS> docker compose ps
```

Deben aparecer 4 servicios en estado *running*: `namenode`, `datanode`, `resourcemanager`, `nodemanager`.
Paneles web opcionales: HDFS en http://localhost:9870 y YARN en http://localhost:8088.

### 2. Instalar Python 3 en el NodeManager (solo la primera vez)

La imagen de Hadoop no incluye Python 3, y el mapper y el reducer se ejecutan en el NodeManager.
La imagen usa CentOS 7, cuyos repositorios oficiales ya no responden, así que se apuntan al archivo histórico:

```powershell
PS> docker compose exec -u root nodemanager bash
```

```bash
sed -i 's|^mirrorlist=|#mirrorlist=|g; s|^#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo
yum install -y python3
python3 --version
exit
```

Debe mostrar `Python 3.6.8`. Los scripts son compatibles con Python 3.6 en adelante.

> **Importante:** esta instalación vive dentro del contenedor.
> Para pausar usa `docker compose stop` y para reanudar `docker compose start`.
> **No uses `docker compose down`**: elimina los contenedores y habría que repetir este paso.

### 3. Cargar el archivo limpio en HDFS (Reto 2.1)

```powershell
PS> docker compose exec resourcemanager bash
```

```bash
hdfs dfsadmin -safemode get
hdfs dfs -mkdir -p /data/netflix/clean/
hdfs dfs -put -f /limpieza/netflix_clean.csv /data/netflix/clean/
hdfs dfs -ls -h /data/netflix/clean/
```

`safemode get` debe responder `Safe mode is OFF`. El listado final debe mostrar `netflix_clean.csv` con su tamaño.

### 4. Ejecutar MapReduce (Reto 2.3)

Dentro del mismo contenedor:

```bash
cd /work
hdfs dfs -rm -r -f /data/netflix/results/actores/

hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files 02_mapper_actores.py,02_reducer_actores.py \
  -mapper "python3 02_mapper_actores.py" \
  -reducer "python3 02_reducer_actores.py" \
  -input /data/netflix/clean/netflix_clean.csv \
  -output /data/netflix/results/actores/
```

- Hadoop no escribe en una carpeta de salida que ya existe, por eso se borra antes de cada ejecución.
- `/work` es esta carpeta (`reto2_mapreduce`) montada en el contenedor `resourcemanager`.
- Al terminar debe verse `map 100% reduce 100%` y `Job ... completed successfully`.

Verificar la salida y descargarla:

```bash
hdfs dfs -ls /data/netflix/results/actores/
hdfs dfs -get /data/netflix/results/actores /work/resultado_hdfs
exit
```

El listado debe mostrar `_SUCCESS` y al menos un archivo `part-00000`.

### 5. Generar `mapreduce_actores.csv`

```powershell
PS> $env:PYTHONUTF8 = "1"
PS> python 02_exportar_resultado.py resultado_hdfs mapreduce_actores.csv
```

El programa imprime la cantidad de partes leídas, el total de actores y los diez primeros (Tabla 2).
El CSV queda ordenado por `cantidad_titulos` descendente y, en caso de empate, por `actor` ascendente.

### 6. Apagar

```powershell
PS> docker compose stop
```

## Reglas aplicadas en el conteo

- Los actores de `cast` se separan por comas y se eliminan los espacios sobrantes de cada nombre.
- Se excluyen los nombres vacíos.
- Se conserva la escritura original de los nombres, incluidas las tildes (UTF-8).
- Un mismo `show_id` cuenta una sola vez por actor.
- Las filas se leen con el módulo `csv` y no con `split(",")`, porque campos como `description` contienen comas dentro de comillas.

## Resultado

`mapreduce_actores.csv` contiene **[ ] actores distintos**.
Este número debe coincidir con la tabla `mapreduce_actores` cargada en Databricks (Reto 3.1) y con el conteo de PySpark (Reto 3.3).

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `read-only file system` o `input/output error` al descargar la imagen | Disco C lleno. Liberar espacio (más de 10 GB), ejecutar `wsl --shutdown` y reiniciar Docker Desktop. |
| `python3: executable file not found` | Falta el paso 2 (instalar Python 3 en el NodeManager). |
| El trabajo falla con `subprocess failed with code 1` | Error en el mapper o el reducer. Probar con una muestra: `cat netflix_clean.csv \| python3 02_mapper_actores.py \| sort -k1,1 \| python3 02_reducer_actores.py \| head`. Comprobar la versión de Python (los scripts requieren 3.6 o superior). |
| `Output directory ... already exists` | Borrar la salida con `hdfs dfs -rm -r -f /data/netflix/results/actores/` antes de ejecutar. |
| `cd /work: No such file` | Se está dentro del contenedor equivocado. `/work` y `/limpieza` solo existen en `resourcemanager`. |
| Tildes mal mostradas en PowerShell | Ejecutar antes `$env:PYTHONUTF8 = "1"`. El archivo CSV sí queda en UTF-8. |
