@echo off
:: Lanza el monitor en background sin ventana visible
powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0Monitor_GOTI.ps1"
