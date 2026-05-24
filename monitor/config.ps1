# ============================================================
#  config.ps1 — Configuracion central de rutas y parametros
#  Importar con: . "$PSScriptRoot\config.ps1"
#  Todos los scripts de Prototipo Cartera/ usan este archivo.
# ============================================================

$BASE         = Split-Path -Parent $PSScriptRoot
$origen       = Join-Path $BASE "entrada\cartera"
$destino      = Join-Path $BASE "reportes"
$PIPELINE_DIR = Join-Path $BASE "pipeline"
$PYTHON       = "C:\Users\Andrey Esteban\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$log          = Join-Path $PSScriptRoot "Monitor_GOTI_log.txt"
$intervalo    = 15
$filtros      = @("*.xlsx", "*.xls", "*.xlsm", "*.xlsb")
