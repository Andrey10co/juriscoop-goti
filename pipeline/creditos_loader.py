import sys
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH, DOCS_PRUEBA
from init_db import init


def cargar(archivo: Path) -> None:
    import pandas as pd

    init()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_PATH) as conn:
        try:
            df_sol = pd.read_excel(archivo, sheet_name="Solicitudes_Credito")
            df_eta = pd.read_excel(archivo, sheet_name="Etapas_Proceso")
            df_emp = pd.read_excel(archivo, sheet_name="Empleados")

            # Snapshot completo: reemplaza todo
            conn.execute("DELETE FROM solicitudes_credito")
            conn.execute("DELETE FROM etapas_proceso")
            conn.execute("DELETE FROM empleados")

            df_sol["fecha_carga"] = ts
            df_sol.columns = [c.lower() for c in df_sol.columns]
            df_sol.to_sql("solicitudes_credito", conn, if_exists="append", index=False)

            df_eta.columns = [c.lower() for c in df_eta.columns]
            df_eta.to_sql("etapas_proceso", conn, if_exists="append", index=False)

            df_emp.columns = [c.lower() for c in df_emp.columns]
            df_emp.to_sql("empleados", conn, if_exists="append", index=False)

            conn.execute(
                "INSERT INTO ejecuciones_log "
                "(proceso, timestamp, archivo, estado, mensaje) VALUES (?,?,?,?,?)",
                (
                    "creditos", ts, archivo.name, "exitoso",
                    f"{len(df_sol)} solicitudes | {len(df_eta)} etapas | {len(df_emp)} empleados",
                ),
            )
            print(f"[CRÉDITOS] {len(df_sol)} solicitudes cargadas desde {archivo.name}")

        except Exception as exc:
            conn.execute(
                "INSERT INTO ejecuciones_log "
                "(proceso, timestamp, archivo, estado, mensaje) VALUES (?,?,?,?,?)",
                ("creditos", ts, archivo.name, "error", str(exc)),
            )
            print(f"[CRÉDITOS] ERROR: {exc}")
            raise


def ultimo_archivo() -> Path | None:
    archivos = sorted(DOCS_PRUEBA.glob("Exportacion_Creditos_*.xlsx"), reverse=True)
    return archivos[0] if archivos else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archivo", help="Ruta completa del Excel a cargar")
    args = parser.parse_args()

    archivo = Path(args.archivo) if args.archivo else ultimo_archivo()
    if not archivo:
        print("[CRÉDITOS] No se encontró archivo para cargar")
        sys.exit(1)
    cargar(archivo)
