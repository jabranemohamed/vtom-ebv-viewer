#!/usr/bin/env python3
"""Produit dist/ebv-vtom-en-direct-hors-ligne.html : index.html avec SheetJS et les
polices embarquées, pour un poste sans accès Internet. Aucune dépendance Python externe.

    python3 build-offline.py
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.html"
VENDOR = ROOT / "vendor"
OUT = ROOT / "dist" / "ebv-vtom-en-direct-hors-ligne.html"

FONT_LINK = re.compile(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">')
XLSX_TAG = re.compile(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/xlsx/[^"]*/xlsx\.full\.min\.js"></script>')
EXTERNAL = re.compile(r'(?:src|href)\s*=\s*"(?:https?:)?//|url\(\s*["\']?(?:https?:)?//|@import', re.I)


def replace_once(pattern, repl, text, what):
    new, n = pattern.subn(lambda _m: repl, text)
    if n != 1:
        sys.exit(f"build-offline: {what} trouvé {n} fois dans index.html (attendu 1)")
    return new


def inline_fonts():
    css = (VENDOR / "fonts.css").read_text(encoding="utf-8")

    def data_uri(m):
        data = (VENDOR / m.group(1)).read_bytes()
        return "url(data:font/woff2;base64," + base64.b64encode(data).decode("ascii") + ")"

    return "<style>\n" + re.sub(r"url\(([^)]+\.woff2)\)", data_uri, css) + "</style>"


def inline_xlsx():
    js = (VENDOR / "xlsx.full.min.js").read_text(encoding="utf-8")
    js = js.replace("</script", "<\\/script")
    return "<script>/* SheetJS CE 0.18.5, Apache 2.0, embarqué pour la version hors ligne */\n" + js + "\n</script>"


def main():
    html = SRC.read_text(encoding="utf-8")
    html = replace_once(FONT_LINK, inline_fonts(), html, "le lien Google Fonts")
    html = replace_once(XLSX_TAG, inline_xlsx(), html, "le script SheetJS cdnjs")
    html = html.replace("<title>EBV VTOM en direct</title>",
                        "<title>EBV VTOM en direct</title>\n<meta name=\"ebv-build\" content=\"hors-ligne\">", 1)

    page = re.sub(r"<script>/\* SheetJS.*?</script>", "", html, flags=re.S)  # le code de la lib n'est pas une ressource
    leaks = EXTERNAL.findall(page)
    if leaks:
        sys.exit(f"build-offline: ressources externes restantes : {leaks}")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} : {OUT.stat().st_size / 1024:.0f} Ko, aucune ressource externe")


if __name__ == "__main__":
    main()
