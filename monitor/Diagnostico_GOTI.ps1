# ============================================================
#  Diagnostico_GOTI.ps1
#  Verifica rutas, permisos, estado del monitor y pipeline
# ============================================================

. "$PSScriptRoot\config.ps1"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   DIAGNOSTICO MONITOR GOTI" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. Politica de ejecucion
Write-Host "[1] Politica de ejecucion de PowerShell:" -ForegroundColor Yellow
$policy = Get-ExecutionPolicy -Scope CurrentUser
Write-Host "    CurrentUser : $policy"
if ($policy -in @("Restricted","AllSigned")) {
    Write-Host "    PROBLEMA: Ejecuta en PowerShell admin:" -ForegroundColor Red
    Write-Host "    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
} else {
    Write-Host "    OK" -ForegroundColor Green
}

# 2. Carpeta origen
Write-Host "`n[2] Carpeta ORIGEN:" -ForegroundColor Yellow
if (Test-Path $origen) {
    Write-Host "    OK - Existe: $origen" -ForegroundColor Green
    try {
        $items = Get-ChildItem $origen -ErrorAction Stop
        $excels = $items | Where-Object { $_.Extension -match 'xls' }
        Write-Host "    OK - Permiso de lectura. Archivos Excel: $($excels.Count)" -ForegroundColor Green
        $excels | ForEach-Object { Write-Host "       - $($_.Name)" -ForegroundColor Gray }
    } catch {
        Write-Host "    PROBLEMA: Sin permiso de lectura -> $_" -ForegroundColor Red
    }
} else {
    Write-Host "    PROBLEMA: No existe: $origen" -ForegroundColor Red
}

# 3. Carpeta destino
Write-Host "`n[3] Carpeta DESTINO:" -ForegroundColor Yellow
if (Test-Path $destino) {
    Write-Host "    OK - Existe: $destino" -ForegroundColor Green
    try {
        $testFile = Join-Path $destino "test_$([System.Guid]::NewGuid()).tmp"
        [System.IO.File]::WriteAllText($testFile, "test")
        Remove-Item $testFile -Force
        Write-Host "    OK - Permiso de escritura" -ForegroundColor Green
    } catch {
        Write-Host "    PROBLEMA: Sin permiso de escritura -> $_" -ForegroundColor Red
    }
} else {
    Write-Host "    Se creara automaticamente al iniciar el monitor" -ForegroundColor DarkYellow
}

# 4. Python y Pipeline
Write-Host "`n[4] Python y Pipeline:" -ForegroundColor Yellow
if (Test-Path $PYTHON) {
    $ver = & $PYTHON --version 2>&1
    Write-Host "    OK - $ver en $PYTHON" -ForegroundColor Green
} else {
    Write-Host "    PROBLEMA: Python no encontrado en: $PYTHON" -ForegroundColor Red
}
if (Test-Path "$PIPELINE_DIR\run_pipeline.py") {
    Write-Host "    OK - Pipeline encontrado: $PIPELINE_DIR" -ForegroundColor Green
} else {
    Write-Host "    PROBLEMA: Pipeline no encontrado en: $PIPELINE_DIR" -ForegroundColor Red
}

# 5. Base de datos
Write-Host "`n[5] Base de datos SQLite:" -ForegroundColor Yellow
$db = Join-Path $PIPELINE_DIR "juriscoop.db"
if (Test-Path $db) {
    $kb = [math]::Round((Get-Item $db).Length / 1KB, 1)
    Write-Host "    OK - juriscoop.db existe ($kb KB)" -ForegroundColor Green
} else {
    Write-Host "    No existe aun - se crea al ejecutar el pipeline por primera vez" -ForegroundColor DarkYellow
}

# 6. Estado del monitor
Write-Host "`n[6] Estado del proceso monitor:" -ForegroundColor Yellow
$procesos = Get-Process powershell -ErrorAction SilentlyContinue
if ($procesos) {
    Write-Host "    Procesos PowerShell activos: $($procesos.Count)" -ForegroundColor Green
} else {
    Write-Host "    PROBLEMA: No hay procesos PowerShell -> monitor no activo" -ForegroundColor Red
    Write-Host "    Ejecuta Iniciar_Monitor_GOTI.bat" -ForegroundColor White
}

# 7. Log
Write-Host "`n[7] Log:" -ForegroundColor Yellow
if (Test-Path $log) {
    Write-Host "    OK - Ultimas 5 lineas:" -ForegroundColor Green
    Get-Content $log -Tail 5 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
} else {
    Write-Host "    Log aun no existe (monitor nunca ha corrido)" -ForegroundColor DarkYellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   FIN DEL DIAGNOSTICO" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
Read-Host "Presiona Enter para cerrar"
