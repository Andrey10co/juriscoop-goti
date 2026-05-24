@echo off
echo Cargando Creditos v2 a la base de datos...
"C:\Users\Andrey Esteban\AppData\Local\Python\pythoncore-3.14-64\python.exe" ^
  "..\pipeline\run_pipeline.py" --proceso creditos
echo.
echo Listo. Actualiza Power BI para ver los cambios.
pause
