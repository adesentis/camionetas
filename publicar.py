"""Regenera la página y la sube a GitHub Pages.

Uso:  python publicar.py
"""
import re
import subprocess
import sys
from datetime import datetime

import generar

sys.stdout.reconfigure(encoding="utf-8")


def git(*args):
    return subprocess.run(["git", *args], cwd=generar.RAIZ, text=True, capture_output=True)


def main():
    generar.main()
    if not git("remote", "get-url", "origin").stdout.strip():
        sys.exit("\nTodavía no hay repositorio en GitHub conectado. Sigue el paso 'Publicar por primera vez' del LEEME.md.")
    git("add", "-A")
    if not git("status", "--porcelain").stdout.strip():
        print("\nNo hubo cambios: la página publicada ya está al día.")
        return
    git("commit", "-m", f"Actualización {datetime.now():%Y-%m-%d %H:%M}")
    r = git("push")
    if r.returncode:
        sys.exit("\nNo se pudo subir a GitHub:\n" + r.stderr)
    print("\nPublicado. GitHub tarda 1 o 2 minutos en mostrar los cambios en el link.")
    # El navegador guarda la página hasta 10 minutos; este link con ?v= la abre recién subida.
    m = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", git("remote", "get-url", "origin").stdout)
    if m:
        version = git("rev-parse", "--short", "HEAD").stdout.strip()
        print(f"Para verla ya, sin la copia vieja del navegador: https://{m.group(1)}.github.io/{m.group(2)}/?v={version}")


if __name__ == "__main__":
    main()
