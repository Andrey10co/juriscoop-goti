import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS solicitudes_credito (
    id_solicitud        INTEGER PRIMARY KEY,
    fecha_solicitud     TEXT,
    fecha_actualizacion TEXT,
    tipo_credito        TEXT,
    documento_cliente   TEXT,
    nombre_cliente      TEXT,
    estado_credito      TEXT,
    etapa_proceso       TEXT,
    responsable         TEXT,
    tiempo_etapa_min    REAL,
    tiempo_total_min    REAL,
    prioridad           TEXT,
    canal_ingreso       TEXT,
    fecha_limite        TEXT,
    retraso             INTEGER,
    fecha_carga         TEXT
);

CREATE TABLE IF NOT EXISTS etapas_proceso (
    etapa_proceso       TEXT PRIMARY KEY,
    orden               INTEGER,
    tiempo_estandar_min REAL
);

CREATE TABLE IF NOT EXISTS empleados (
    responsable      TEXT PRIMARY KEY,
    rol              TEXT,
    capacidad_diaria REAL
);

CREATE TABLE IF NOT EXISTS cartera_raw (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_corte    TEXT,
    archivo_origen TEXT,
    datos_json     TEXT,
    fecha_carga    TEXT
);

CREATE TABLE IF NOT EXISTS ejecuciones_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    proceso   TEXT,
    timestamp TEXT,
    archivo   TEXT,
    estado    TEXT,
    mensaje   TEXT
);
"""

def init():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)

if __name__ == "__main__":
    init()
    print(f"[DB] Inicializada: {DB_PATH}")
