"""
Orquestador del pipeline Juriscoop.

Uso:
  python run_pipeline.py                          # carga ambos procesos
  python run_pipeline.py --proceso cartera
  python run_pipeline.py --proceso creditos
  python run_pipeline.py --proceso cartera --archivo "ruta/al/archivo.xlsx"
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cartera_loader
import creditos_loader


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline Juriscoop")
    parser.add_argument(
        "--proceso",
        choices=["cartera", "creditos", "ambos"],
        default="ambos",
    )
    parser.add_argument("--archivo", help="Ruta del archivo a cargar")
    args = parser.parse_args()

    if args.proceso in ("cartera", "ambos"):
        archivo = Path(args.archivo) if args.archivo else cartera_loader.ultimo_archivo()
        if archivo:
            cartera_loader.cargar(archivo)
        else:
            print("[PIPELINE] No se encontró archivo de cartera en Reportes mensuales/")

    if args.proceso in ("creditos", "ambos"):
        archivo_cred = creditos_loader.ultimo_archivo()
        if archivo_cred:
            creditos_loader.cargar(archivo_cred)
        else:
            print("[PIPELINE] No se encontró archivo de créditos en Documentos de prueba/")


if __name__ == "__main__":
    main()
