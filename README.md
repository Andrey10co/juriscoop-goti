# Juriscoop GOTI — Sistema de Monitoreo de Cartera y Fabrica de Credito

Prototipo funcional desarrollado para Juriscoop (cooperativa financiera colombiana) como solución a dos problemas operativos identificados en el área de créditos. El sistema automatiza la recepción de reportes externos, la carga de datos a una base de datos local y la actualización del tablero de control en Power BI.

---

## Descripcion general

El prototipo está compuesto por dos módulos independientes que comparten la misma base de datos SQLite:

**Módulo 1 — Monitor de Cartera**
Servicio en segundo plano (PowerShell) que vigila la carpeta `entrada/cartera/` simulando la llegada del reporte nocturno del proveedor externo. Al detectar un archivo nuevo, lo copia a `reportes/` e invoca automáticamente el pipeline de carga. No requiere intervención del usuario.

**Módulo 2 — Fábrica de Crédito**
Tablero Power BI de cuatro páginas (Estratégico, Operativo, Equipo, Proyección) conectado a la base de datos SQLite mediante scripts Python embebidos. El usuario actualiza el tablero con un clic cuando llega un nuevo archivo de créditos.

---

## Arquitectura del sistema

```
Proveedor externo                Sistema interno
        |                               |
Cierre_Cartera_*.xlsx     Exportacion_Creditos_*.xlsx
        |                               |
   entrada/cartera/           entrada/creditos/
        |                               |
   (automatico)              demo/Cargar_Creditos_v2.bat
        |                               |
  monitor/Monitor_GOTI.ps1   pipeline/run_pipeline.py
        |                               |
        +-------------------------------+
                        |
               pipeline/juriscoop.db
                  (SQLite local)
                        |
              Power BI -> Actualizar
                        |
              Dashboard actualizado
```

### Base de datos

Archivo: `pipeline/juriscoop.db` (generado al ejecutar `init_db.py`)

| Tabla | Descripcion |
|-------|-------------|
| `cartera_raw` | Filas del Excel de cartera almacenadas como JSON. Acumula historico. |
| `ejecuciones_log` | Registro de cada carga ejecutada. Garantiza idempotencia. |
| `solicitudes_credito` | Snapshot completo de solicitudes. Se reemplaza en cada carga. |
| `etapas_proceso` | Catalogo de etapas y tiempos estandar. |
| `empleados` | Catalogo de analistas y capacidad diaria. |

### Monitor de cartera

El monitor hace polling cada 15 segundos sobre `entrada/cartera/`. El diseño de polling (en lugar de `FileSystemWatcher`) es intencional: OneDrive escribe archivos en dos fases y el watcher dispara antes de que la sincronización esté completa. Al detectar un archivo nuevo, el monitor verifica en `ejecuciones_log` si ya fue procesado, lo copia a `reportes/` y llama al pipeline. La carga es idempotente; el mismo archivo nunca se procesa dos veces.

---

## Requisitos del sistema

- Windows 10 u 11
- Python 3.10 o superior con los paquetes: `pandas`, `openpyxl`, `matplotlib`
- Power BI Desktop (versión de mayo 2024 o posterior)
- Política de ejecución de PowerShell configurada: `RemoteSigned`

Verificar paquetes Python:
```powershell
python -m pip install pandas openpyxl matplotlib
```

Configurar política PowerShell (ejecutar una sola vez como administrador):
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Instalacion y configuracion inicial

### 1. Clonar el repositorio

```powershell
git clone <url-del-repositorio>
cd juriscoop-goti
```

### 2. Ajustar las rutas de Python

Editar `pipeline/config.py` y reemplazar la ruta del intérprete Python con la ruta correcta en el equipo de destino:

```python
PYTHON = r"C:\ruta\a\python.exe"
```

Editar `monitor/config.ps1` y hacer el mismo ajuste:

```powershell
$PYTHON = "C:\ruta\a\python.exe"
```

### 3. Inicializar la base de datos

```powershell
python pipeline\init_db.py
```

Esto crea el archivo `pipeline/juriscoop.db` con el esquema de cinco tablas.

---

## Uso del monitor de cartera

### Iniciar el monitor

```powershell
.\monitor\Iniciar_Monitor_GOTI.bat
```

El monitor se ejecuta en segundo plano sin ventana visible. El archivo `monitor/Monitor_GOTI_log.txt` registra cada acción en tiempo real.

### Verificar el estado

```powershell
.\monitor\Diagnostico_GOTI.ps1
```

### Detener el monitor

```powershell
.\monitor\Detener_Monitor_GOTI.ps1
```

### Flujo automatico

Cuando se deposita un archivo `Cierre_Cartera_*.xlsx` en `entrada/cartera/`, el monitor lo detecta en menos de 15 segundos, lo copia a `reportes/` y ejecuta el pipeline de cartera. El tablero Power BI refleja los cambios al presionar Actualizar.

---

## Uso del pipeline de datos

### Carga manual de cartera

```powershell
python pipeline\run_pipeline.py --proceso cartera --archivo "ruta\Cierre_Cartera.xlsx"
```

### Carga de creditos

```powershell
python pipeline\run_pipeline.py --proceso creditos
```

El pipeline toma automáticamente el archivo más reciente de `entrada/creditos/`. Para especificar un archivo concreto:

```powershell
python pipeline\run_pipeline.py --proceso creditos --archivo "ruta\Exportacion_Creditos.xlsx"
```

### Carga de ambos procesos

```powershell
python pipeline\run_pipeline.py --proceso ambos
```

---

## Conexion con Power BI

El archivo Power BI es `Power BI - Prototipo de Creditos.pbix`.

La fuente de datos son scripts Python embebidos directamente en el archivo `.pbix`. Para reconectar en un equipo nuevo:

1. Abrir Power BI Desktop y dirigirse a **Archivo > Opciones y configuracion > Opciones > Script de Python**.
2. Establecer el directorio de Python al que contiene `python.exe` (no a un subdirectorio).
3. Abrir el Editor de Power Query (Inicio > Transformar datos).
4. Para la consulta `cartera`: seleccionar el paso **Origen**, abrir el editor de script y pegar el contenido de `pipeline/pbi_cartera_query.py`.
5. Para la consulta `solicitudes_credito`: mismo procedimiento con el contenido de `pipeline/pbi_creditos_query.py`. Este script define las tres tablas (`solicitudes_credito`, `etapas_proceso`, `empleados`) en un solo bloque.
6. Cerrar y aplicar.

### Medidas DAX relevantes

Las tablas en la base de datos usan nombres en minúsculas. Las medidas deben referirse a ellas en minúsculas:

| Medida | Formula simplificada |
|--------|---------------------|
| Total Solicitudes | `COUNTROWS(solicitudes_credito)` |
| Solicitudes Finalizadas | `CALCULATE(COUNTROWS(solicitudes_credito), solicitudes_credito[estado_credito] = "Finalizado")` |
| Porcentaje Retraso | `DIVIDE([Solicitudes con Retraso], [Total Solicitudes])` donde retraso es `= 1` (no `TRUE()`) |
| Tiempo Estandar Promedio | Usar `TREATAS` en lugar de `RELATED()` en contexto de medida |

---

## Ejecucion de la demostracion

El archivo `demo/GUION_DEMOSTRACION.md` contiene el guión detallado de cinco momentos con rutas exactas, nombres de archivo y salida esperada en los logs.

### Resumen del flujo demostrado

| Momento | Accion | Resultado visible |
|---------|--------|------------------|
| 1 | Power BI con datos v1 | 80 contratos, 120 solicitudes |
| 2 | Copiar archivo cartera v2 a `entrada/cartera/` | Monitor detecta el archivo en menos de 15 s |
| 3 | Actualizar Power BI | 90 contratos, mora sube a 52% |
| 4 | Copiar creditos v2 a `entrada/creditos/` y ejecutar bat | Pipeline carga 140 solicitudes |
| 5 | Actualizar Power BI | 140 solicitudes, mas finalizadas |

---

## Estructura del repositorio

```
.
|-- README.md
|-- .gitignore
|-- Power BI - Prototipo de Creditos.pbix
|
|-- pipeline/
|   |-- config.py                  Rutas centralizadas del pipeline Python
|   |-- init_db.py                 Creacion del esquema SQLite
|   |-- run_pipeline.py            Orquestador principal (cartera / creditos / ambos)
|   |-- cartera_loader.py          Carga Excel de cartera a cartera_raw
|   |-- creditos_loader.py         Carga Excel de creditos a tres tablas
|   |-- pbi_cartera_query.py       Script para pegar en Power BI (tabla cartera)
|   `-- pbi_creditos_query.py      Script para pegar en Power BI (tablas creditos)
|
|-- monitor/
|   |-- config.ps1                 Rutas centralizadas del monitor PowerShell
|   |-- Monitor_GOTI.ps1           Monitor de archivos (polling cada 15 s)
|   |-- Iniciar_Monitor_GOTI.bat   Inicia el monitor en segundo plano
|   |-- Detener_Monitor_GOTI.ps1   Detiene el proceso del monitor
|   `-- Diagnostico_GOTI.ps1       Verifica rutas, permisos y estado del proceso
|
|-- demo/
|   |-- Cargar_Creditos_v2.bat     Carga el archivo de creditos con doble clic
|   `-- GUION_DEMOSTRACION.md      Guion paso a paso de la demostracion
|
|-- entrada/
|   |-- cartera/                   Deposito del proveedor externo (origen cartera)
|   `-- creditos/                  Exportacion del sistema interno (origen creditos)
|
`-- reportes/                      Archivos de cartera procesados por el monitor
```

---

## Autores

Proyecto desarrollado por el Grupo D — Universidad de la Sabana  
Asignatura: Gerencia de Operaciones con Tecnologia de Informacion (GOTI)  
Entrega final — Periodo 2026-1
