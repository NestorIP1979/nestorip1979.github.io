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
- 450–700 palabras, castellano de España, tono claro y divulgativo.
- Todo dato debe salir de las fuentes enlazadas; distinguir dato oficial de estimación o rumor.
- Redactar con palabras propias: nada de copiar frases de los medios (como mucho una cita breve, entre comillas y atribuida).
- Mínimo 3 fuentes por noticia, preferiblemente fuentes originales.
- No repetir un tema ya publicado salvo que haya una novedad importante (entonces, artículo de actualización).
- Imagen: una foto o ilustración REAL relacionada con la noticia, solo de Wikimedia Commons con licencia libre (CC0, dominio público, CC BY o CC BY-SA). Añadir en el JSON `"imagen": {"archivo": "Nombre_exacto_en_Commons.jpg", "alt": "descripción", "autor": "...", "licencia": "CC BY-SA 4.0", "licencia_url": "https://creativecommons.org/licenses/by-sa/4.0/"}` tras comprobar autor y licencia en la página del archivo. Nunca fotos de medios, notas de prensa ni capturas oficiales, ni fotos de personas reales identificables: mejor el producto, el lugar, el objeto o un diagrama. Si la imagen tiene ejes o márgenes blancos, se puede recortar con "escala" (p. ej. 1.6) y "posicion" (p. ej. "50% 50%") dentro de "imagen". Si no hay imagen adecuada, omitir "imagen" (sale el degradado con emoji).

## AdSense
Cuando Google apruebe la web, rellenar en `config.json` `adsense_client` (ca-pub-…) y los `adsense_slot_*`, y volver a generar: se añaden el script, los bloques de anuncio y `ads.txt`.
El aviso de cookies se activa en AdSense → Privacidad y mensajes → Normativa europea (CMP certificada de Google).
