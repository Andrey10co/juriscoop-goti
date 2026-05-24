# ============================================================
#  Monitor_GOTI.ps1
#  Detecta archivos Excel nuevos o modificados en la carpeta
#  compartida, los copia a Reportes mensuales y activa el
#  pipeline de carga a la base de datos.
# ============================================================

. "$PSScriptRoot\config.ps1"

if (-not (Test-Path $origen)) {
    Add-Content $log "[$(Get-Date)] ERROR: Carpeta origen no encontrada: $origen"
    exit 1
}
if (-not (Test-Path $destino)) {
    New-Item -ItemType Directory -Path $destino | Out-Null
    Add-Content $log "[$(Get-Date)] INFO: Carpeta destino creada: $destino"
}

Add-Content $log "[$(Get-Date)] INFO: Monitor iniciado (polling cada $intervalo seg). Vigilando: $origen"

$estadoAnterior = @{}
foreach ($filtro in $filtros) {
    Get-ChildItem -Path $origen -Filter $filtro -ErrorAction SilentlyContinue | ForEach-Object {
        $estadoAnterior[$_.Name] = $_.LastWriteTime
    }
}
Add-Content $log "[$(Get-Date)] INFO: Archivos Excel existentes al inicio: $($estadoAnterior.Count)"

while ($true) {
    Start-Sleep -Seconds $intervalo

    $estadoActual = @{}
    foreach ($filtro in $filtros) {
        Get-ChildItem -Path $origen -Filter $filtro -ErrorAction SilentlyContinue | ForEach-Object {
            $estadoActual[$_.Name] = $_.LastWriteTime
        }
    }

    foreach ($nombre in $estadoActual.Keys) {
        $esNuevo  = -not $estadoAnterior.ContainsKey($nombre)
        $fueModif = (-not $esNuevo) -and ($estadoActual[$nombre] -ne $estadoAnterior[$nombre])

        if ($esNuevo -or $fueModif) {
            $tipo       = if ($esNuevo) { "NUEVO" } else { "MODIFICADO" }
            $archivoOri = Join-Path $origen  $nombre
            $archivoDst = Join-Path $destino $nombre

            Start-Sleep -Seconds 3  # esperar descarga completa de OneDrive

            try {
                Copy-Item -Path $archivoOri -Destination $archivoDst -Force
                Add-Content $log "[$(Get-Date)] $tipo`: $nombre -> $destino"

                # Activar pipeline de carga a la base de datos
                $resultado = & $PYTHON "$PIPELINE_DIR\run_pipeline.py" --proceso cartera --archivo $archivoDst 2>&1
                Add-Content $log "[$(Get-Date)] PIPELINE: $resultado"

            } catch {
                Add-Content $log "[$(Get-Date)] ERROR al copiar '$nombre': $_"
            }
        }
    }

    $estadoAnterior = $estadoActual
}
