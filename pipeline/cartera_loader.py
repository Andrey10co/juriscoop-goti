import sys
import sqlite3
import json
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH, REPORTES
from init_db import init


def ya_cargado(conn: sqlite3.Connection, nombre_archivo: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM ejecuciones_log "
        "WHERE proceso='cartera' AND archivo=? AND estado='exitoso'",
        (nombre_archivo,),
    )
    return cur.fetchone() is not None


def cargar(archivo: Path) -> None:
    import pandas as pd

    init()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_PATH) as conn:
        if ya_cargado(conn, archivo.name):
            print(f"[CARTERA] Ya cargado previamente: {archivo.name}")
            return

        try:
            df = pd.read_excel(archivo, dtype=str)
            df.columns = df.columns.str.strip()

            fecha_corte = (
                df["Fecha_Corte"].iloc[0]
                if "Fecha_Corte" in df.columns
                else ts[:10]
            )

            rows = [
                (fecha_corte, archivo.name, json.dumps(row, ensure_ascii=False), ts)
                for row in df.to_dict(orient="records")
            ]

            conn.executemany(
                "INSERT INTO cartera_raw "
                "(fecha_corte, archivo_origen, datos_json, fecha_carga) "
                "VALUES (?,?,?,?)",
                rows,
            )
            conn.execute(
                "INSERT INTO ejecuciones_log "
                "(proceso, timestamp, archivo, estado, mensaje) VALUES (?,?,?,?,?)",
                ("cartera", ts, archivo.name, "exitoso", f"{len(rows)} registros cargados"),
            )
            print(f"[CARTERA] {len(rows)} registros cargados desde {archivo.name}")

        except Exception as exc:
            conn.execute(
                "INSERT INTO ejecuciones_log "
                "(proceso, timestamp, archivo, estado, mensaje) VALUES (?,?,?,?,?)",
                ("cartera", ts, archivo.name, "error", str(exc)),
            )
            print(f"[CARTERA] ERROR: {exc}")
            raise


def ultimo_archivo() -> Path | None:
    archivos = sorted(REPORTES.glob("Cierre_Cartera_*.xlsx"), reverse=True)
    return archivos[0] if archivos else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archivo", help="Ruta completa del Excel a cargar")
    args = parser.parse_args()

    archivo = Path(args.archivo) if args.archivo else ultimo_archivo()
    if not archivo:
        print("[CARTERA] No se encontró archivo para cargar")
        sys.exit(1)
    cargar(archivo)
