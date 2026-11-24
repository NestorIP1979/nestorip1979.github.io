# Prompt de ejemplo para usar este generador:
#   "Añade dos noticias nuevas a Lo Más Viral y vuelve a generar la web con python3 _fuente/build.py"
#
# Generador estático de "Lo Más Viral".
# Lee _fuente/config.json y _fuente/noticias/*.json y escribe la web en la raíz del repositorio
# (index.html, noticias/, categoria/, páginas legales, sitemap.xml, feed.xml, robots.txt, ads.txt).
# Uso: python3 _fuente/build.py

import json, html, re, shutil, unicodedata
from pathlib import Path
from datetime import datetime, timezone

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
CFG = json.loads((SRC / "config.json").read_text(encoding="utf-8"))
URL = CFG["url"].rstrip("/")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
CAT_ESTILO = {
    "Videojuegos": ("🎮", "#7c3aed", "#db2777"),
    "Tecnología": ("💻", "#0ea5e9", "#6366f1"),
    "Ciencia": ("🔭", "#059669", "#0891b2"),
    "Inteligencia artificial": ("🤖", "#f59e0b", "#ef4444"),
    "Internet": ("🌐", "#ec4899", "#8b5cf6"),
    "Espacio": ("🚀", "#1e3a8a", "#7c3aed"),
}
DEFECTO = ("🔥", "#ef4444", "#f97316")


def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def fecha_larga(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def e(t):
    return html.escape(t, quote=True)


def texto_plano(t):
    return re.sub(r"<[^>]+>", "", t)


def cargar_noticias():
    out = []
    for f in sorted((SRC / "noticias").glob("*.json")):
        n = json.loads(f.read_text(encoding="utf-8"))
        n["url"] = f"/noticias/{n['slug']}.html"
        n["cat_slug"] = slugify(n["categoria"])
        out.append(n)
    out.sort(key=lambda n: (n["fecha"], n["slug"]), reverse=True)
    return out


def ad(slot):
    if not (CFG.get("adsense_client") and slot):
        return ""
    return (f'<div class="ad"><span class="ad-label">Publicidad</span>'
            f'<ins class="adsbygoogle" style="display:block" data-ad-client="{e(CFG["adsense_client"])}" '
            f'data-ad-slot="{e(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            f'<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')


def portada(n, grande=False):
    emoji, c1, c2 = CAT_ESTILO.get(n["categoria"], DEFECTO)
    cls = "cover big" if grande else "cover"
    return (f'<div class="{cls}" style="--c1:{c1};--c2:{c2}" aria-hidden="true">'
            f'<span>{emoji}</span></div>')


def pagina(titulo, contenido, descripcion=None, canonical="/", extra_head=""):
    descripcion = descripcion or CFG["descripcion"]
    adsense = ""
    if CFG.get("adsense_client"):
        adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
                   f'{e(CFG["adsense_client"])}" crossorigin="anonymous"></script>')
    analytics = ""
    if CFG.get("ga4_id"):
        gid = e(CFG["ga4_id"])
        analytics = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
                     '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
                     "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',"
                     "analytics_storage:'denied',wait_for_update:500});"
                     f"gtag('js',new Date());gtag('config','{gid}');</script>")
    if CFG.get("google_site_verification"):
        analytics += f'<meta name="google-site-verification" content="{e(CFG["google_site_verification"])}">'
    full_title = titulo if titulo == CFG["nombre"] else f"{titulo} | {CFG['nombre']}"
    cats = sorted({c for c in CAT_ESTILO} & set(CATEGORIAS_USADAS)) or []
    nav = "".join(f'<a href="/categoria/{slugify(c)}.html">{e(c)}</a>' for c in cats)
    return f"""<!DOCTYPE html>
<html lang="{CFG['idioma']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{URL}{canonical}">
<meta property="og:site_name" content="{e(CFG['nombre'])}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{URL}{canonical}">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{e(CFG['nombre'])}" href="/feed.xml">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔥</text></svg>">
<link rel="stylesheet" href="/estilos.css">
{analytics}
{adsense}
{extra_head}
</head>
<body>
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="/">🔥 {e(CFG['nombre'])}</a>
    <nav>{nav}</nav>
  </div>
</header>
<main class="wrap">
{contenido}
</main>
<footer class="foot">
  <div class="wrap">
    <p><strong>{e(CFG['nombre'])}</strong> · {e(CFG['lema'])}</p>
    <p><a href="/sobre.html">Quiénes somos</a> · <a href="/contacto.html">Contacto</a> · <a href="/aviso-legal.html">Aviso legal</a> · <a href="/privacidad.html">Privacidad</a> · <a href="/cookies.html">Cookies</a> · <a href="/feed.xml">RSS</a></p>
    <p class="muted">© {datetime.now().year} {e(CFG['nombre'])}. Las marcas y nombres citados pertenecen a sus propietarios.</p>
  </div>
</footer>
</body>
</html>
"""


def tarjeta(n, grande=False):
    cls = "card big" if grande else "card"
    return f"""<article class="{cls}">
  <a href="{n['url']}">{portada(n, grande)}</a>
  <div class="card-body">
    <p class="meta"><a class="tag" href="/categoria/{n['cat_slug']}.html">{e(n['categoria'])}</a> · <time datetime="{n['fecha']}">{fecha_larga(n['fecha'])}</time></p>
    <h2><a href="{n['url']}">{e(n['titulo'])}</a></h2>
    <p>{e(n['resumen'])}</p>
  </div>
</article>"""


def render_cuerpo(bloques):
    out = []
    for b in bloques:
        if "p" in b:
            out.append(f"<p>{b['p']}</p>")
        elif "h2" in b:
            out.append(f"<h2>{e(b['h2'])}</h2>")
        elif "ul" in b:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in b["ul"]) + "</ul>")
        elif "cita" in b:
            out.append(f"<blockquote>{b['cita']}</blockquote>")
    # anuncio tras el tercer bloque
    if len(out) > 4:
        out.insert(3, ad(CFG.get("adsense_slot_articulo")))
    return "\n".join(out)


def escribir(ruta, texto):
    p = ROOT / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


NOTICIAS = cargar_noticias()
CATEGORIAS_USADAS = sorted({n["categoria"] for n in NOTICIAS})
for c in CATEGORIAS_USADAS:
    CAT_ESTILO.setdefault(c, DEFECTO)


def build():
    # limpiar salida generada
    for d in ("noticias", "categoria"):
        shutil.rmtree(ROOT / d, ignore_errors=True)
    shutil.copy(SRC / "estilos.css", ROOT / "estilos.css")

    # portada
    ultimas, resto = NOTICIAS[:2], NOTICIAS[2:]
    portada_html = f"""<section class="hero">
  <h1>Lo más viral de la semana</h1>
  <p class="lead">{e(CFG['descripcion'])}</p>
</section>
<section class="destacadas">
{''.join(tarjeta(n, True) for n in ultimas)}
</section>
{ad(CFG.get('adsense_slot_portada'))}
"""
    if resto:
        portada_html += f"""<section><h2 class="sec">Anteriores</h2><div class="grid">
{''.join(tarjeta(n) for n in resto)}
</div></section>"""
    escribir("index.html", pagina(CFG["nombre"], portada_html))

    # artículos
    for i, n in enumerate(NOTICIAS):
        relacionadas = [m for m in NOTICIAS if m is not n][:3]
        fuentes = "".join(f'<li><a href="{e(f["url"])}" rel="nofollow noopener" target="_blank">{e(f["nombre"])}</a></li>'
                          for f in n["fuentes"])
        ld = {
            "@context": "https://schema.org", "@type": "NewsArticle",
            "headline": n["titulo"], "description": n["resumen"],
            "datePublished": n["fecha"], "dateModified": n.get("actualizado", n["fecha"]),
            "author": {"@type": "Organization", "name": CFG["nombre"]},
            "publisher": {"@type": "Organization", "name": CFG["nombre"]},
            "mainEntityOfPage": URL + n["url"], "inLanguage": "es",
        }
        cuerpo = f"""<article class="post">
  <p class="meta"><a class="tag" href="/categoria/{n['cat_slug']}.html">{e(n['categoria'])}</a> · <time datetime="{n['fecha']}">{fecha_larga(n['fecha'])}</time></p>
  <h1>{e(n['titulo'])}</h1>
  <p class="lead">{e(n['resumen'])}</p>
  {portada(n, True)}
  <div class="content">
{render_cuerpo(n['cuerpo'])}
  </div>
  <aside class="fuentes">
    <h2>Fuentes</h2>
    <ul>{fuentes}</ul>
    <p class="muted">Artículo redactado por {e(CFG['nombre'])} a partir de las fuentes citadas. Si ves un error, <a href="/contacto.html">avísanos</a>.</p>
  </aside>
</article>
{ad(CFG.get('adsense_slot_articulo'))}
<section><h2 class="sec">Más noticias</h2><div class="grid">{''.join(tarjeta(m) for m in relacionadas)}</div></section>
"""
        head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        escribir(n["url"].lstrip("/"), pagina(n["titulo"], cuerpo, n["resumen"], n["url"], head))

    # categorías
    for c in CATEGORIAS_USADAS:
        lista = [n for n in NOTICIAS if n["categoria"] == c]
        cs = slugify(c)
        cuerpo = f'<section class="hero"><h1>{e(c)}</h1><p class="lead">Las noticias más virales de {e(c.lower())}.</p></section><div class="grid">{"".join(tarjeta(n) for n in lista)}</div>'
        escribir(f"categoria/{cs}.html", pagina(c, cuerpo, f"Noticias virales de {c}", f"/categoria/{cs}.html"))

    # páginas fijas
    for f in sorted((SRC / "paginas").glob("*.html")):
        texto = f.read_text(encoding="utf-8")
        titulo = re.search(r"<h1>(.*?)</h1>", texto).group(1)
        for k, v in CFG.items():
            texto = texto.replace("{{" + k + "}}", e(str(v)))
        escribir(f.name, pagina(texto_plano(titulo), f'<article class="post page">{texto}</article>', canonical="/" + f.name))

    # 404
    escribir("404.html", pagina("Página no encontrada", '<section class="hero"><h1>Vaya, esta página no existe</h1><p class="lead"><a href="/">Vuelve a la portada</a> para ver lo más viral.</p></section>'))

    # sitemap
    urls = ["/"] + [n["url"] for n in NOTICIAS] + [f"/categoria/{slugify(c)}.html" for c in CATEGORIAS_USADAS] \
        + ["/" + f.name for f in sorted((SRC / "paginas").glob("*.html"))]
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{URL}{u}</loc><lastmod>{hoy}</lastmod></url>\n"
    escribir("sitemap.xml", sm + "</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")

    # RSS
    items = ""
    for n in NOTICIAS[:20]:
        d = datetime.strptime(n["fecha"], "%Y-%m-%d").strftime("%a, %d %b %Y 08:00:00 +0000")
        items += (f"<item><title>{e(n['titulo'])}</title><link>{URL}{n['url']}</link>"
                  f"<guid>{URL}{n['url']}</guid><pubDate>{d}</pubDate><category>{e(n['categoria'])}</category>"
                  f"<description>{e(n['resumen'])}</description></item>\n")
    escribir("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{e(CFG["nombre"])}</title>'
             f'<link>{URL}/</link><description>{e(CFG["descripcion"])}</description><language>es-es</language>\n{items}</channel></rss>\n')

    # ads.txt solo cuando haya ID de AdSense
    pub = CFG.get("adsense_client", "").replace("ca-", "")
    if pub:
        escribir("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    elif (ROOT / "ads.txt").exists():
        (ROOT / "ads.txt").unlink()

    print(f"OK: {len(NOTICIAS)} noticias, {len(CATEGORIAS_USADAS)} categorías")


if __name__ == "__main__":
    build()
