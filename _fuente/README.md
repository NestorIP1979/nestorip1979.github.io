<!-- Prompt de ejemplo: "Publica las 2 noticias más virales de hoy en Lo Más Viral siguiendo _fuente/README.md" -->

# Lo Más Viral — cómo funciona

Web estática alojada en GitHub Pages (repo `NestorIP1979/nestorip1979.github.io`, rama `main`, carpeta raíz).
Todo lo que está en `_fuente/` es el código fuente; GitHub Pages no lo publica (Jekyll ignora las carpetas que empiezan por `_`).

## Publicar noticias nuevas
1. Crear un archivo `_fuente/noticias/AAAA-MM-DD-slug-corto.json` por noticia (formato abajo).
2. Ejecutar `python3 _fuente/build.py` desde la raíz del repo: regenera portada, artículos, categorías, sitemap y RSS.
3. `git add -A && git commit -m "Noticias AAAA-MM-DD" && git push`.

## Formato de una noticia
```json
{
  "slug": "titulo-en-minusculas-con-guiones",
  "titulo": "Titular claro, sin clickbait",
  "fecha": "AAAA-MM-DD",
  "hora": "HH:MM (hora de publicación, Europe/Madrid; ordena la portada cuando hay varias noticias el mismo día)",
  "categoria": "Videojuegos | Tecnología | Ciencia | Inteligencia artificial | Internet | Espacio",
  "resumen": "Una o dos frases (se usa como entradilla y meta description).",
  "cuerpo": [
    {"p": "Párrafo. Se permite <strong> y <em>."},
    {"h2": "Subtítulo"},
    {"ul": ["punto 1", "punto 2"]}
  ],
  "fuentes": [{"nombre": "Medio – titular", "url": "https://..."}]
}
```

## Reglas editoriales
- 450–700 palabras, castellano de España.
- TONO: cercano e informal, como si se lo contaras a un amigo. Tutear al lector ("si estás jugando...", "te lo explicamos"), frases cortas, algo de humor ligero, titulares con gancho pero sin engañar (nada de clickbait falso).
- ENFOQUE: escribir para quien le interesa el tema, no para inversores. Videojuegos → para jugadores (qué tiene el juego, qué se puede hacer, qué gusta y qué no, curiosidades); las cifras de ventas o económicas solo como dato de color al final. Ciencia y tecnología → explicar sin tecnicismos qué es, por qué mola o importa y qué cambia para la gente normal.
- Se puede cerrar con una pregunta al lector.
- Todo dato debe salir de las fuentes enlazadas; distinguir dato oficial de estimación o rumor.
- Redactar con palabras propias: nada de copiar frases de los medios (como mucho una cita breve, entre comillas y atribuida).
- Mínimo 3 fuentes por noticia, preferiblemente fuentes originales.
- No repetir un tema ya publicado salvo que haya una novedad importante (entonces, artículo de actualización).
- Imagen: debe identificar la noticia a primera vista (el logo de la empresa o del producto, la portada o arte oficial del juego, el producto...). Orden de preferencia:
  1. Logo o imagen reconocible con licencia libre en Wikimedia Commons (CC0, dominio público, CC BY, CC BY-SA). Campo: `"imagen": {"archivo": "Nombre_exacto.svg", "alt": "...", "autor": "...", "licencia": "...", "licencia_url": "..."}`. Para logos añadir `"ajuste": "logo"` (fondo claro, sin recortar).
  2. Si no hay ninguna libre reconocible: imagen OFICIAL de prensa de la propia empresa (su sala de prensa, media kit o web oficial de medios), nunca de otros medios ni de redes. Campo: `"imagen": {"url": "URL directa de la imagen", "fuente_url": "página oficial de prensa", "alt": "...", "autor": "Empresa", "licencia": "material oficial de prensa", "licencia_url": "página oficial de prensa"}`.
  - Nunca fotos de personas reales identificables. Si la imagen no carga, la web muestra el degradado de la categoría.

## AdSense
Cuando Google apruebe la web, rellenar en `config.json` `adsense_client` (ca-pub-…) y los `adsense_slot_*`, y volver a generar: se añaden el script, los bloques de anuncio y `ads.txt`.
El aviso de cookies se activa en AdSense → Privacidad y mensajes → Normativa europea (CMP certificada de Google).
