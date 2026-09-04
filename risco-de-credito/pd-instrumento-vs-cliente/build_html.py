"""Injeta resultados.json no template e gera o HTML autocontido."""
from __future__ import annotations

import json
from pathlib import Path

AQUI = Path(__file__).parent


def main() -> str:
    dados = json.loads((AQUI / "resultados.json").read_text())
    template = (AQUI / "template.html").read_text()
    corpo = template.replace("__DADOS__", json.dumps(dados, ensure_ascii=False, separators=(",", ":")))
    html = (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + corpo + "\n</head>\n</html>\n"
    )
    # o <title>, <link> e <style> ficam no head; o <main> e o <script> são movidos para o body
    i = html.index("<main>")
    html = html[:i] + "</head>\n<body>\n" + html[i:].replace("\n</head>\n</html>\n", "\n</body>\n</html>\n")
    (AQUI / "pd_instrumento_vs_cliente.html").write_text(html)
    print("gerado:", AQUI / "pd_instrumento_vs_cliente.html", f"({len(html)/1024:.0f} KB)")
    return corpo


if __name__ == "__main__":
    main()
