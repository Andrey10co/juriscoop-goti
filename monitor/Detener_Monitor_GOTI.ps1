# Detiene todos los procesos powershell que no sean la sesion actual
$miPID = $PID
Get-Process powershell -ErrorAction SilentlyContinue | Where-Object { $_.Id -ne $miPID } | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    Write-Host "Detenido PID: $($_.Id)"
}
Write-Host "Listo. Ahora ejecuta Iniciar_Monitor_GOTI.bat para relanzar."
