"""Aplicación web para consultar el último registro del producto extraído."""

import csv
import os
from pathlib import Path

from flask import Flask, abort, jsonify, render_template

BASE_DIR = Path(__file__).resolve().parent
PRODUCT_CSV = Path(os.environ.get("PRODUCT_CSV", str(BASE_DIR / "articulo.csv")))
PRODUCT_URL = "https://www.aliexpress.com/item/1005009259589970.html"
REQUIRED_FIELDS = {"titulo", "precio", "fecha_extraccion"}


def create_app(csv_path=PRODUCT_CSV):
    app = Flask(__name__)

    @app.get("/")
    def index():
        try:
            with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                missing_fields = REQUIRED_FIELDS.difference(reader.fieldnames or ())
                if missing_fields:
                    raise ValueError(
                        f"Faltan columnas requeridas: {', '.join(sorted(missing_fields))}"
                    )
                product = next(reader, None)
                if product is None:
                    raise ValueError("El archivo CSV no contiene registros.")
        except (OSError, UnicodeError, csv.Error, ValueError):
            app.logger.exception("No se pudo leer el registro del producto.")
            abort(503, description="La información del producto no está disponible.")

        return render_template(
            "index.html",
            product=product,
            product_url=PRODUCT_URL,
        )

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
    )
