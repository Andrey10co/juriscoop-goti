# Guión de Demostración — Pipeline Juriscoop v2

## Cambios visibles entre v1 y v2

| Indicador | Datos actuales (v1) | Datos nuevos (v2) | Cambio |
|---|---|---|---|
| Contratos cartera | 80 | 90 | +10 contratos |
| Contratos en mora | 38 | 47 | +9 en mora |
| % cartera en mora | 47.5% | 52.2% | +4.7 pp |
| Solicitudes crédito | 120 | 140 | +20 solicitudes |
| Solicitudes finalizadas | ~18 | ~27 | +9 finalizadas |
| Pesos en mora (estimado) | ~$1.0B | ~$1.2B | Incremento visible |

---

## Preparación antes de la demo (hacer con anticipación)

**1. Abrir Power BI Desktop**
Archivo:
```
C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\
Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\
Power BI - Prototipo de Creditos.pbix
```
Verificar que las gráficas carguen con los datos actuales (v1).

**2. Iniciar el monitor de archivos** (si no está corriendo)
Doble clic en:
```
...\Prototipo Cartera\Iniciar_Monitor_GOTI.bat
```
No aparece ninguna ventana — corre en background. Verificar con:
```
...\Prototipo Cartera\Diagnostico_GOTI.ps1
```

**3. Abrir las 3 pestañas de Explorador de archivos**

> Usar Windows + E para abrir el Explorador. Navegar a cada ruta y anclarla a la barra de tareas o dejarla abierta en segundo plano.

**Pestaña 1 — Archivos nuevos (origen de la demo):**
```
C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\
Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\Demo
```
Archivos que verás aquí:
- `Cierre_Cartera_20260522_v2.xlsx` ← archivo nuevo de cartera
- `Exportacion_Creditos_20260522_v2.xlsx` ← archivo nuevo de créditos
- `Cargar_Creditos_v2.bat` ← ejecutable de un clic para créditos

**Pestaña 2 — Carpeta compartida (donde llega el archivo del proveedor):**
```
C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\
Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\
Prototipo funcional - 2 entrega\Carpeta_Compartida-GOTI
```
Aquí ya existe: `Cierre_Cartera_20260522.xlsx` (el archivo v1)

**Pestaña 3 — Documentos de prueba (destino del archivo de créditos):**
```
C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\
Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\
Prototipo funcional - 2 entrega\Documentos de prueba
```
Aquí ya existe: `Exportacion_Creditos_20260522.xlsx` (el archivo v1)

**4. Abrir el log del monitor** (para mostrarlo en vivo)
Abrir con el Bloc de notas:
```
...\Prototipo Cartera\Monitor_GOTI_log.txt
```
Mantenerlo visible para mostrar que el sistema registra cada acción.

---

## Ejecución de la demostración

### MOMENTO 1 — Estado actual (datos v1)

Con Power BI en primer plano, mostrar:
- **Cartera:** 80 contratos totales, 38 en mora, % mora ~47.5%
- **Créditos:** 120 solicitudes, distribución por etapa y estado

*Mensaje clave:* "Este es el estado de hoy a las 8 AM, cargado automáticamente
desde los archivos del día anterior."

---

### MOMENTO 2 — Llega el nuevo archivo de cartera

**Acción:** Cambiar a la **Pestaña 1** (Demo/).

Señalar el archivo:
```
Cierre_Cartera_20260522_v2.xlsx
```
*"Este es el archivo de cierre que el proveedor externo depositó en la carpeta
compartida. Vamos a copiarlo como si él lo hubiera dejado ahí."*

**Acción:** Copiar `Cierre_Cartera_20260522_v2.xlsx` con Ctrl+C.

**Acción:** Cambiar a la **Pestaña 2** (Carpeta_Compartida-GOTI/) y pegar con Ctrl+V.

*"El archivo acaba de llegar a la carpeta compartida. El monitor está vigilando
esta carpeta cada 15 segundos."*

**Esperar ~20 segundos.**

**Acción:** Cambiar al **Bloc de notas del log** y presionar F5 para refrescar.

Mostrar las líneas nuevas al final del log:
```
[fecha hora] NUEVO: Cierre_Cartera_20260522_v2.xlsx -> Reportes mensuales
[fecha hora] PIPELINE: [CARTERA] 90 registros cargados...
```

*"El sistema detectó el archivo, lo copió a Reportes mensuales y lo cargó
automáticamente en la base de datos. Sin intervención humana."*

---

### MOMENTO 3 — Actualizar cartera en Power BI

**Acción:** Cambiar a **Power BI Desktop**.

**Acción:** Clic en **Inicio → Actualizar**.

Esperar ~5 segundos mientras corre el script Python.

Mostrar los cambios en las gráficas de cartera:
- Total contratos: 80 → **90**
- Contratos en mora: 38 → **47**
- % mora: 47.5% → **~52%**
- El gráfico de barras por estado y calificación cambia visiblemente

*"En tiempo real, la directora puede ver que la cartera se deterioró respecto al
día anterior: 9 contratos adicionales entraron en mora."*

---

### MOMENTO 4 — Llega el nuevo archivo de créditos

**Acción:** Cambiar a la **Pestaña 1** (Demo/).

Señalar el archivo:
```
Exportacion_Creditos_20260522_v2.xlsx
```
*"Este es el archivo exportado desde la plataforma interna de créditos,
que se genera periódicamente durante el día."*

**Acción:** Copiar `Exportacion_Creditos_20260522_v2.xlsx` con Ctrl+C.

**Acción:** Cambiar a la **Pestaña 3** (Documentos de prueba/) y pegar con Ctrl+V.

*"El archivo se coloca en la carpeta de documentos de prueba. Ahora ejecutamos
el pipeline de créditos."*

**Acción:** Volver a la **Pestaña 1** (Demo/) y hacer doble clic en:
```
Cargar_Creditos_v2.bat
```

Aparece una ventana negra con el mensaje:
```
Cargando Creditos v2 a la base de datos...
[CRÉDITOS] 140 solicitudes cargadas desde Exportacion_Creditos_20260522_v2.xlsx
Listo. Actualiza Power BI para ver los cambios.
```

Presionar cualquier tecla para cerrar la ventana.

---

### MOMENTO 5 — Actualizar créditos en Power BI

**Acción:** Cambiar a **Power BI Desktop**.

**Acción:** Clic en **Inicio → Actualizar**.

Mostrar los cambios en las gráficas de créditos:
- Total solicitudes: 120 → **140**
- Solicitudes finalizadas: ~18 → **~27**
- Distribución por etapa y estado cambia
- KPIs de equipo y proyección se recalculan automáticamente

*"Con un solo clic de Actualizar, el tablero refleja el estado más reciente
de toda la operación."*

---

## Resumen del flujo demostrado

```
Proveedor externo          Sistema interno
      ↓                         ↓
Cierre_Cartera_v2.xlsx    Exportacion_Creditos_v2.xlsx
      ↓                         ↓
Carpeta_Compartida-GOTI   Documentos de prueba
      ↓ (automático)            ↓ (Cargar_Creditos_v2.bat)
Monitor_GOTI.ps1          run_pipeline.py
      ↓                         ↓
         juriscoop.db (SQLite)
                  ↓
       Power BI → Actualizar
                  ↓
         Dashboard actualizado
```
