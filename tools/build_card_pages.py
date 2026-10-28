"""Génère une page d'aperçu par fiche (c/<slug>.html en FR, c/<slug>.en.html en EN, c/<slug>.zh.html en chinois).

Discord, WhatsApp, etc. lisent les balises og: d'une page sans exécuter son JavaScript : avec un seul
index.html, tous les liens de fiches montrent le même aperçu. Chaque page générée porte le titre, les
premières étapes et l'image de la vidéo de sa fiche, puis renvoie tout de suite vers la fiche du wiki.
Le chinois vient de zh.js : un texte pas encore traduit reste en anglais, comme sur le site.

À relancer après avoir ajouté, renommé ou modifié une fiche :
    python tools/build_card_pages.py
Il faut Playwright (pip install playwright) et Microsoft Edge ou Chromium. Les slugs sont lus dans la
page elle-même, donc ils sont toujours identiques à ceux du site. Si une page manque, le lien marche
quand même : 404.html renvoie vers la fiche, seul l'aperçu est générique.
"""
import html
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "c"
BASE = "https://rotkguide.com/"
SITE = {"fr": "ROTK Wiki (non officiel)", "en": "ROTK Wiki (unofficial)", "zh": "ROTK Wiki（非官方）"}
HTML_LANG = {"fr": "fr", "en": "en", "zh": "zh-CN"}
LANGS = ("fr", "en", "zh")
SUFFIX = {"fr": "", "en": ".en", "zh": ".zh"}


def summary(steps, limit=300):
    text = " ".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:.")
    return cut + "…"


def page(slug, card, lang):
    title = card["t"][lang]
    desc = summary(card["f"][lang])
    image = BASE + (f"videos/{card['v']}-{lang}.jpg" if card.get("v") else "og.png")
    target = "../?lang=" + lang + "#" + slug
    own = BASE + "c/" + slug + SUFFIX[lang] + ".html"
    e = lambda s: html.escape(s, quote=True)
    return f"""<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · {e(SITE[lang])}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{e(SITE[lang])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(own)}">
<meta property="og:image" content="{e(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#e10600">
<link rel="canonical" href="{e(BASE + target[3:])}">
<meta http-equiv="refresh" content="0; url={e(target)}">
<script>location.replace({target!r});</script>
<style>body{{margin:0;background:#0c0b09;color:#efede7;font:16px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}a{{color:#ff3b2f}}</style>
</head>
<body><p><a href="{e(target)}">{e(title)}</a></p></body>
</html>
"""


NOT_FOUND = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ROTK Wiki (non officiel)</title>
<meta name="robots" content="noindex">
<script>
/* Lien de fiche sans page d'aperçu (fiche ajoutée sans relancer tools/build_card_pages.py) : on renvoie vers la fiche. */
(function(){
  var m = location.pathname.match(/^(.*\\/)c\\/([a-z0-9-]+?)(?:\\.(en|zh))?(?:\\.html)?$/);
  if (m) location.replace(m[1] + "?lang=" + (m[3] || "fr") + "#" + m[2]);
})();
</script>
<style>body{margin:0;background:#0c0b09;color:#efede7;font:16px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;text-align:center;padding:20px}a{color:#ff3b2f}</style>
</head>
<body><p>Page introuvable. <a href="/">Retour au wiki</a><br>Page not found. <a href="/?lang=en">Back to the wiki</a><br><span lang="zh-CN">找不到页面。<a href="/?lang=zh">返回 Wiki</a></span></p></body>
</html>
"""


def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="msedge")
        except Exception:
            browser = p.chromium.launch()
        # navigateur en chinois (la page prend la langue du visiteur avant ?lang=) : elle charge zh.js, chaque texte a alors sa version fr, en et zh
        pg = browser.new_page(locale="zh-CN")
        pg.goto((ROOT / "index.html").as_uri() + "?lang=zh")
        pg.wait_for_function("document.documentElement.lang === 'zh-CN' && document.querySelectorAll('#list .row').length > 0")
        cards = pg.evaluate("[...document.querySelectorAll('#list .row')].map(r => ({id: r.id, x: {t: r._x.t, f: r._x.f, v: r._x.v || null}}))")
        missing = pg.evaluate("zhStatus().missing.length")
        browser.close()
    OUT.mkdir(exist_ok=True)
    keep = set()
    for c in cards:
        for lang in LANGS:
            name = c["id"] + SUFFIX[lang] + ".html"
            (OUT / name).write_text(page(c["id"], c["x"], lang), encoding="utf-8", newline="\n")
            keep.add(name)
    for old in OUT.glob("*.html"):
        if old.name not in keep:
            old.unlink()
    (ROOT / "404.html").write_text(NOT_FOUND, encoding="utf-8", newline="\n")
    print(f"{len(cards)} fiches, {len(keep)} pages dans c/")
    if missing:
        print(f"zh.js : {missing} textes encore en anglais dans la version chinoise (zhStatus() dans la console de ?lang=zh)")


if __name__ == "__main__":
    main()
