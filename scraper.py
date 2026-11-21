"""Extrae título y precio de un producto seleccionado en AliExpress."""

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

PRODUCT_URL = "https://www.aliexpress.com/item/1005009259589970.html"
FIELDS = ("titulo", "precio", "fecha_extraccion")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def _jsonld_price(data):
    if isinstance(data, list):
        for item in data:
            price = _jsonld_price(item)
            if price:
                return price
    elif isinstance(data, dict):
        if data.get("price") is not None:
            currency = data.get("priceCurrency", "")
            price = str(data["price"]).strip().rstrip(".")
            return f"{price} {currency}".strip()
        if "offers" in data:
            return _jsonld_price(data["offers"])
        if "@graph" in data:
            return _jsonld_price(data["@graph"])
    return None


def parse_product(html):
    soup = BeautifulSoup(html, "html.parser")
    title_element = soup.select_one("h1")
    title = title_element.get_text(" ", strip=True) if title_element else None
    if not title:
        title_meta = soup.select_one('meta[property="og:title"]')
        if title_meta:
            title = title_meta.get("content")

    price = None
    meta_price = (
        soup.select_one('meta[property="product:price:amount"]')
        or soup.select_one('meta[property="og:price:amount"]')
    )
    if meta_price:
        price = meta_price.get("content")
        meta_currency = soup.select_one(
            'meta[property="product:price:currency"]'
        )
        if meta_currency and meta_currency.get("content"):
            price = f"{price} {meta_currency['content']}"

    if not price:
        for script in soup.select('script[type="application/ld+json"]'):
            try:
                price = _jsonld_price(json.loads(script.string or script.get_text()))
            except (json.JSONDecodeError, TypeError):
                continue
            if price:
                break

    if not price:
        price_element = soup.select_one(
            '[class*="price-default--current--"], '
            '[class*="price--current--"]'
        )
        if price_element:
            price = price_element.get_text(" ", strip=True)

    if not title or not price:
        missing = " y ".join(
            field
            for field, value in (("título", title), ("precio", price))
            if not value
        )
        raise ValueError(
            f"No se encontró {missing} en la página. "
            "El sitio pudo cambiar o no entregar los datos."
        )

    return {
        "titulo": title,
        "precio": price,
        "fecha_extraccion": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def save_csv(record, output):
    with output.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(record)


def scrape_with_bs4():
    request = Request(PRODUCT_URL, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")
    return parse_product(html)


def scrape_with_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1365,1000")
    with webdriver.Chrome(options=options) as browser:
        browser.get(PRODUCT_URL)
        WebDriverWait(browser, 30).until(
            lambda driver: (
                driver.find_elements("css selector", "h1")
                and driver.find_elements(
                    "css selector",
                    '[class*="price-default--current--"], '
                    '[class*="price--current--"]',
                )
            )
        )
        return parse_product(browser.page_source)


def scrape_with_scrapy(output):
    class ProductSpider(scrapy.Spider):
        name = "articulo_seleccionado"
        start_urls = [PRODUCT_URL]

        def parse(self, response):
            yield parse_product(response.text)

    output.parent.mkdir(parents=True, exist_ok=True)
    process = scrapy.crawler.CrawlerProcess(
        settings={
            "FEEDS": {
                str(output.resolve()): {
                    "format": "csv",
                    "fields": list(FIELDS),
                    "encoding": "utf-8-sig",
                    "overwrite": True,
                }
            },
            "ROBOTSTXT_OBEY": True,
            "DOWNLOAD_DELAY": 2,
            "USER_AGENT": USER_AGENT,
            "LOG_LEVEL": "INFO",
        }
    )
    process.crawl(ProductSpider)
    process.start()
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("Scrapy no generó el CSV; revisa los mensajes del crawler.")


def main():
    parser = argparse.ArgumentParser(
        description="Extrae título y precio del producto seleccionado en AliExpress."
    )
    parser.add_argument(
        "--motor",
        choices=("bs4", "selenium", "scrapy"),
        default="selenium",
        help="Librería/motor de extracción (por defecto: selenium).",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("articulo.csv"),
        help="Nombre del CSV de salida.",
    )
    args = parser.parse_args()
    args.salida.parent.mkdir(parents=True, exist_ok=True)

    if args.motor == "bs4":
        save_csv(scrape_with_bs4(), args.salida)
    elif args.motor == "selenium":
        save_csv(scrape_with_selenium(), args.salida)
    else:
        scrape_with_scrapy(args.salida)

    with args.salida.open(encoding="utf-8-sig", newline="") as csv_file:
        record = next(csv.DictReader(csv_file), None)
    if record is None:
        raise RuntimeError(f"No se encontraron datos en el archivo {args.salida}.")

    print(f"Título: {record['titulo']}")
    print(f"Precio: {record['precio']}")
    print(f"Fecha de extracción (UTC): {record['fecha_extraccion']}")
    print(f"Artículo guardado en: {args.salida}")


if __name__ == "__main__":
    main()
