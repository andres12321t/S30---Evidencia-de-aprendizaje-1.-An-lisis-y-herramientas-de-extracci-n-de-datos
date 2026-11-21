import tempfile
import unittest
from pathlib import Path

from app import create_app
from scraper import _jsonld_price, parse_product, save_csv


class ScraperTests(unittest.TestCase):
    def test_parse_product_with_html_elements(self):
        html = """
        <html>
          <head>
            <meta property="product:price:amount" content="33740">
            <meta property="product:price:currency" content="COP">
          </head>
          <body><h1>Aspirador de coche inalámbrico</h1></body>
        </html>
        """

        record = parse_product(html)

        self.assertEqual(record["titulo"], "Aspirador de coche inalámbrico")
        self.assertEqual(record["precio"], "33740 COP")
        self.assertIn("+00:00", record["fecha_extraccion"])

    def test_parse_product_accepts_json_ld_offer(self):
        html = """
        <html>
          <body>
            <h1>Producto de prueba</h1>
            <script type="application/ld+json">
              {"@graph": [{"offers": {"price": "45999", "priceCurrency": "COP"}}]}
            </script>
          </body>
        </html>
        """

        record = parse_product(html)

        self.assertEqual(record["precio"], "45999 COP")

    def test_jsonld_price_handles_nested_json_ld(self):
        data = {"@graph": [{"offers": {"price": "120.00", "priceCurrency": "USD"}}]}

        self.assertEqual(_jsonld_price(data), "120.00 USD")

    def test_save_csv_writes_expected_columns(self):
        record = {
            "titulo": "Producto de prueba",
            "precio": "45999 COP",
            "fecha_extraccion": "2026-11-21T16:30:00+00:00",
        }

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "articulo.csv"
            save_csv(record, output)

            content = output.read_text(encoding="utf-8-sig")
            self.assertIn("titulo,precio,fecha_extraccion", content)
            self.assertIn("Producto de prueba", content)
            self.assertIn("45999 COP", content)


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.directory.name) / "articulo.csv"
        self.csv_path.write_text(
            "titulo,precio,fecha_extraccion\n"
            "Producto de prueba,45999 COP,2026-11-21T16:30:00+00:00\n",
            encoding="utf-8",
        )
        self.client = create_app(self.csv_path).test_client()

    def tearDown(self):
        self.directory.cleanup()

    def test_homepage_displays_product_from_csv(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Producto de prueba", response.data)
        self.assertIn(b"45999 COP", response.data)
        self.assertIn(b"2026-11-21T16:30:00+00:00", response.data)

    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_stylesheet_is_served(self):
        with self.client.get("/static/style.css") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b".product-card", response.data)

    def test_homepage_reports_unavailable_csv(self):
        self.csv_path.unlink()

        response = self.client.get("/")

        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
