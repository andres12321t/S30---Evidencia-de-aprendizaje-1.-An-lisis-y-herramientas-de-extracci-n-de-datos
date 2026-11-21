# Documentación del proyecto

## Introducción

Este proyecto desarrolla un scraper educativo para recopilar información pública
de un producto publicado en AliExpress. El artículo seleccionado es un aspirador
inalámbrico para automóvil, identificado por el código `1005009259589970`.

El programa obtiene el título, el precio mostrado en la página y la fecha y hora
en que se realiza la extracción, expresada en UTC. Los resultados se presentan
en la terminal y se guardan en un archivo CSV para facilitar su consulta y
análisis posterior.

Para el proceso se emplean tres herramientas de Python: Selenium carga la página
en un navegador y permite obtener contenido que se genera dinámicamente;
BeautifulSoup analiza el HTML para localizar los datos; y Scrapy está disponible
como alternativa para realizar solicitudes y exportar resultados. Como la
página carga su información dinámicamente, Selenium es el motor predeterminado
del proyecto.

El scraper tiene fines académicos. Su uso debe respetar las condiciones de
AliExpress, sus políticas de acceso y las limitaciones establecidas por el sitio.

## Descripción de la página y artículo a analizar

AliExpress es una plataforma de comercio electrónico donde distintos vendedores
publican productos para su venta. Las fichas de producto pueden mostrar
información como el nombre del artículo, el precio, imágenes, características y
disponibilidad. Parte del contenido se carga dinámicamente en el navegador, por
lo que la respuesta HTML inicial puede no incluir todos los datos visibles.

El artículo seleccionado es un aspirador inalámbrico para automóvil, con el
código de producto `1005009259589970`. La página individual analizada es:

`https://www.aliexpress.com/item/1005009259589970.html`

En la ficha inspeccionada, el título describe un aspirador portátil de 9000 Pa,
con carga USB y uso para limpieza del automóvil y el hogar. También se encontró
la marca HAOYUNMA en los datos estructurados de la página. Durante una ejecución
de prueba, el precio mostrado fue de 33 740 COP; este valor es variable y puede
cambiar según la fecha, la región, las promociones o las opciones seleccionadas.

El enlace original de ofertas incluía este identificador en el parámetro
`productIds`, pero al abrirlo directamente respondió con una página 404. Por
ello, el análisis se realiza sobre la ficha individual construida con el código
del artículo.

## Tema de interés de la primera práctica

El tema de interés es la extracción automatizada de información pública de
productos publicados en plataformas de comercio electrónico. En esta primera
práctica se aplican herramientas de scraping para identificar y recopilar datos
concretos —el título, el precio y la fecha de extracción— de una ficha de
AliExpress.

La práctica también permite reconocer cómo se presenta el contenido de una
página web y comparar el papel de BeautifulSoup, Selenium y Scrapy en la
obtención de datos. En particular, se observa que las páginas con contenido
dinámico pueden requerir la carga de un navegador antes de analizar su HTML.
El resultado se guarda en CSV para que los datos puedan revisarse y utilizarse
en ejercicios posteriores de organización y análisis.

## Objetivos

### Objetivo general

Analizar un artículo publicado en AliExpress mediante técnicas de scraping para
comprender cómo se obtiene y organiza información pública de un producto en una
plataforma de comercio electrónico.

### Objetivos específicos

- Identificar información relevante del aspirador seleccionado, como su título
  y precio, para conocer cómo se presenta la oferta al consumidor.
- Aplicar Selenium, BeautifulSoup y Scrapy para explorar distintas formas de
  cargar una página y extraer información de su contenido.
- Guardar los datos recopilados en un archivo CSV y mostrarlos en la terminal,
  de modo que puedan consultarse y analizarse posteriormente.
- Reconocer las características del contenido dinámico y las limitaciones de
  acceso que pueden influir en la extracción de datos de AliExpress.

## Metodología empleada de scraping

La extracción se realizó sobre la ficha individual del producto identificado
con el código `1005009259589970`. Se utilizó Selenium como motor de navegación,
ya que el contenido de la página se carga dinámicamente. Una vez abierta la
ficha, el programa espera a que aparezcan el título y el elemento del precio en
la página antes de continuar.

Con la página cargada, se entrega su HTML a BeautifulSoup, que busca el título
en el encabezado principal (`h1`) y el precio en los datos estructurados
JSON-LD. Si esos datos no están disponibles, se consultan metadatos y elementos
HTML del precio. El programa también agrega la fecha y hora UTC de la consulta.

Finalmente, el resultado se imprime en la terminal y se almacena en
`articulo.csv`, con las columnas `titulo`, `precio` y `fecha_extraccion`. Scrapy
está incluido como opción de solicitud y exportación, pero la ejecución usada
para obtener el resultado reportado se hizo con Selenium y BeautifulSoup. No se
usa Scrapy para ejecutar JavaScript; por ello, puede no obtener los mismos
datos dinámicos de esta página.

La extracción depende del contenido que AliExpress entregue al momento de la
consulta. El precio puede variar y el sitio puede modificar su estructura,
mostrar verificaciones o limitar solicitudes; el proceso no intenta evadir
esas restricciones.

## Resultados

La ejecución de prueba con Selenium y BeautifulSoup identificó el producto y
generó el archivo `articulo.csv`. El registro guardado contiene:

- **Título:** Aspirador de coche inalámbrico de 9000Pa, dispositivo de limpieza
  portátil con carga USB de 1200mAh, Mini aspirador húmedo y seco para el hogar.
- **Precio observado:** 33740 COP.
- **Fecha de extracción:** 2026-10-25 18:45:09 UTC.

El precio corresponde a una observación durante la prueba, no a un valor
permanente. Puede cambiar según la fecha, la región, las promociones y las
opciones disponibles en la ficha.

## Conclusiones

La práctica permitió extraer y organizar el título y el precio de un producto
de AliExpress utilizando Selenium para cargar el contenido dinámico y
BeautifulSoup para analizar su HTML. El resultado quedó disponible tanto en la
terminal como en un archivo CSV, lo que facilita su consulta posterior.

También se comprobó que el enlace de ofertas no siempre conduce directamente a
la información del producto y que puede ser necesario utilizar la ficha
individual. La extracción web depende de la respuesta y estructura actuales del
sitio; por tanto, los selectores y el resultado deben verificarse cada vez que
se ejecute el programa. Scrapy se conserva como herramienta alternativa, aunque
por sí solo no ejecuta JavaScript.

## Bibliografía

- AliExpress. (s. f.). *Aspirador de coche inalámbrico de 9000 Pa* [ficha del
  producto, código 1005009259589970].
  https://www.aliexpress.com/item/1005009259589970.html
- Beautiful Soup. (s. f.). *Beautiful Soup Documentation*.
  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Scrapy. (s. f.). *Scrapy Documentation*.
  https://docs.scrapy.org/en/latest/
- Selenium. (s. f.). *Selenium Documentation*.
  https://www.selenium.dev/documentation/

Fuentes consultadas el 25 de octubre de 2026.

## Gestión de versiones con Git y GitHub

El proyecto utiliza Git para controlar los cambios y GitHub como repositorio
remoto. La rama `main` contiene la versión estable. Los cambios nuevos deben
realizarse en ramas descriptivas, por ejemplo `feature/pruebas-unitarias`, y
integrarse mediante un pull request. Antes de fusionar se recomienda ejecutar:

```bash
python -m unittest discover -v
```

Se pueden crear versiones etiquetadas cuando una versión estable esté lista:

```bash
git tag -a v1.0.0 -m "Versión 1.0.0"
git push origin v1.0.0
```

## Integración y entrega continua

El flujo ubicado en `.github/workflows/ci.yml` se ejecuta automáticamente ante
push a `main`, creación de tags `v*` y pull requests. Sus etapas son:

1. Descargar el repositorio.
2. Instalar Python 3.11 y 3.12.
3. Instalar las dependencias de `requirements.txt`.
4. Validar la sintaxis del scraper y sus pruebas.
5. Ejecutar las pruebas unitarias.
6. Crear y publicar un artefacto comprimido del proyecto en cada entrega exitosa
   desde `main` o desde un tag.

Los resultados quedan registrados en la pestaña **Actions** de GitHub. Para
descargar el paquete generado, abrir la ejecución correcta y utilizar la
sección **Artifacts**.

## Aplicación web y despliegue en Render

El proyecto incluye una aplicación web sencilla en Flask que presenta el último
registro de `articulo.csv`: título, precio observado, fecha de extracción y un
enlace a la ficha del producto. La aplicación solo consulta el CSV existente;
no realiza solicitudes de scraping cada vez que una persona abre la página.
El endpoint `/health` permite verificar que el servicio esté disponible.

El archivo `render.yaml` define el servicio web, el comando de instalación y
arranque con Gunicorn y la ruta de comprobación de salud. Para crear el servicio,
se debe conectar el repositorio en Render y elegir la opción **New Blueprint
Instance**.

Para probar la aplicación localmente, instalar las dependencias y ejecutar:

```bash
python -m pip install -r requirements.txt
python app.py
```

Luego se puede abrir `http://127.0.0.1:5000`. El endpoint
`http://127.0.0.1:5000/health` debe responder con `{"status":"ok"}`.
También se puede iniciar con `python -m flask --app app run`. No se debe abrir
`templates/index.html` directamente ni servirlo con Live Server: es una
plantilla Jinja que Flask debe procesar para reemplazar los datos y cargar los
estilos.

El workflow ejecuta las pruebas primero. Después, para los cambios recibidos en
`main` o cuando se ejecuta manualmente, activa el despliegue en Render mediante
un deploy hook. Para habilitar esa etapa:

1. En Render, crear el servicio usando el Blueprint del repositorio.
2. En la configuración del servicio de Render, copiar su URL de deploy hook.
3. En GitHub, abrir **Settings > Secrets and variables > Actions**.
4. Agregar el hook como el secreto `RENDER_DEPLOY_HOOK_URL`.
5. Agregar la variable de repositorio `RENDER_DEPLOY_ENABLED` con el valor
   `true`.

La URL del hook es confidencial; debe guardarse como secreto y no incluirse en
el código ni en los registros. Hasta que se configuren el servicio y estas dos
variables, GitHub Actions informa que el despliegue está pendiente y no lo
ejecuta.
