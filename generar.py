"""Genera index.html a partir de datos.json y baja las fotos que falten.

Uso:  python generar.py
"""
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent
FOTOS = RAIZ / "fotos"
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}
ANCHO_MAX = 1200
CALIDAD = 78
MAX_FOTOS = 8
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

# Kavak nombra sus fotos por ángulo; este es el orden en que las queremos.
KAVAK_ANGULOS = [
    ("front", "frente"), ("copilotSide", "lateral"), ("pilotSide", "lateral"),
    ("back", "trasera"), ("frontBoard", "interior"), ("OtherInterior", "interior-2"),
    ("openDoorBackPilot", "segunda-fila"), ("openTrunk", "cajuela"),
    ("frontSidePilotNear", "tres-cuartos"), ("frontSideCopilot", "tres-cuartos"),
]


def bajar(url, intentos=3):
    """Reintenta solo fallas de red; si el sitio responde con bloqueo (403, etc.) se rinde."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-MX"})
    for intento in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, TimeoutError):
            if intento == intentos:
                raise
            time.sleep(3)


def guardar_foto(contenido, destino):
    img = Image.open(io.BytesIO(contenido)).convert("RGB")
    if img.width > ANCHO_MAX:
        img = img.resize((ANCHO_MAX, round(img.height * ANCHO_MAX / img.width)), Image.LANCZOS)
    img.save(destino, "JPEG", quality=CALIDAD, optimize=True, progressive=True)


def fotos_kavak(html, unidad):
    """Kavak muestra varias unidades por link: la principal debe coincidir en km."""
    m = re.search(r'"mileageFromOdometer"\s*:\s*\{[^}]*"value"\s*:\s*(\d+)', html)
    km = int(m.group(1)) if m else None
    if km != unidad["km"]:
        raise ValueError(f"la unidad que muestra Kavak tiene {km} km, no {unidad['km']}")
    completas = {}
    for u in re.finditer(r'https://images\.prd\.kavak\.io/images/\d+/(?:EXTERIOR|INTERIOR)-(\w+)-\d+\.jpe?g', html):
        completas.setdefault(u.group(1), u.group(0))
    elegidas, nombres = [], set()
    for angulo, nombre in KAVAK_ANGULOS:
        if angulo in completas and nombre not in nombres:
            elegidas.append((nombre, completas[angulo]))
            nombres.add(nombre)
    return elegidas[:MAX_FOTOS]


def fotos_seminuevos(html, unidad):
    """Seminuevos.com: las fotos del anuncio llevan su número en la ruta."""
    id_anuncio = re.search(r"(\d{6,})/?$", unidad["anuncio"]).group(1)
    if f"{unidad['km']:,}" not in html and str(unidad["km"]) not in html:
        print(f"    Aviso: no encontré {unidad['km']:,} km en el anuncio; revisa que sea la unidad correcta")
    # A veces la ruta no trae extensión (termina en "."), por eso el nombre es libre.
    patron = rf'https://images\.latamautos\.com/thumbs/w/\w+/[\w/]*?/{id_anuncio}/o_o/([\w.-]+)'
    vistas, elegidas = set(), []
    for m in re.finditer(patron, html):
        archivo = re.sub(r"\.(jpe?g|png|webp)?$", "", m.group(1))
        if archivo in vistas:
            continue
        vistas.add(archivo)
        url = re.sub(r"/thumbs/w/\w+/", "/thumbs/w/lg/", m.group(0))
        elegidas.append(("foto", url))
    # Los vendedores ponen primero el exterior y al final el interior:
    # se toman las 4 primeras y 4 repartidas en el resto para que haya de los dos.
    if len(elegidas) > MAX_FOTOS:
        resto = elegidas[4:]
        paso = len(resto) / (MAX_FOTOS - 4)
        elegidas = elegidas[:4] + [resto[int(i * paso + paso / 2)] for i in range(MAX_FOTOS - 4)]
    return elegidas


def fotos_genericas(html, unidad):
    urls = re.findall(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
    return [("foto", u) for u in dict.fromkeys(urls)][:MAX_FOTOS]


def descargar_fotos(unidad):
    """Regresa None si todo salió bien, o el motivo por el que no hay fotos."""
    carpeta = FOTOS / unidad["id"]
    if lista_fotos(unidad["id"]):
        return None
    if not unidad.get("anuncio") or unidad.get("descargar_fotos") is False:
        return "sin descarga automática"
    print(f"  Bajando fotos de {unidad['id']}...")
    try:
        html = bajar(unidad["anuncio"]).decode("utf-8", "replace")
        if "kavak.com" in unidad["anuncio"]:
            elegidas = fotos_kavak(html, unidad)
        elif "seminuevos.com" in unidad["anuncio"]:
            elegidas = fotos_seminuevos(html, unidad)
        else:
            elegidas = fotos_genericas(html, unidad)
        if not elegidas:
            return "el anuncio no dejó encontrar fotos"
        # Primero se bajan todas; solo si todas llegaron se guardan (no quedan carpetas a medias).
        contenidos = [(nombre, bajar(url)) for nombre, url in elegidas]
        carpeta.mkdir(parents=True, exist_ok=True)
        for n, (nombre, contenido) in enumerate(contenidos, 1):
            guardar_foto(contenido, carpeta / f"{n:02d}-{nombre}.jpg")
        print(f"    {len(elegidas)} fotos guardadas en fotos/{unidad['id']}/")
        return None
    except Exception as e:  # el sitio bloqueó o cambió: no insistimos
        return f"no se pudo bajar ({e})"


def lista_fotos(id_unidad):
    carpeta = FOTOS / id_unidad
    if not carpeta.is_dir():
        return []
    return sorted(f"fotos/{id_unidad}/{p.name}" for p in carpeta.iterdir()
                  if p.suffix.lower() in EXTENSIONES)


def puntaje(calificaciones, criterios):
    suma = sum(calificaciones[c["id"]] * c["peso"] for c in criterios)
    total = sum(c["peso"] for c in criterios)
    return int(suma * 100 / total + 0.5) / 100


def main():
    datos = json.loads((RAIZ / "datos.json").read_text(encoding="utf-8"))
    criterios = datos["criterios"]
    total = sum(c["peso"] for c in criterios)
    if total != 100:
        print(f"Aviso: los pesos suman {total}, no 100. El puntaje se calcula igual (dividido entre {total}).")

    print("Revisando fotos...")
    sin_fotos = []
    for opcion in datos["opciones"]:
        faltan = [c["id"] for c in criterios if c["id"] not in opcion["calificaciones"]]
        if faltan:
            sys.exit(f"Error: a '{opcion['nombre']}' le falta calificación en: {', '.join(faltan)}")
        for unidad in opcion["unidades"]:
            motivo = descargar_fotos(unidad)
            unidad["fotos"] = lista_fotos(unidad["id"])
            if not unidad["fotos"]:
                sin_fotos.append(f"{unidad['id']} ({motivo})")

    plantilla = (RAIZ / "plantilla.html").read_text(encoding="utf-8")
    json_datos = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = plantilla.replace("/*DATOS*/", f"const DATOS = {json_datos};")
    (RAIZ / "index.html").write_text(html, encoding="utf-8")

    print("\nRanking:")
    orden = sorted(datos["opciones"], key=lambda o: -puntaje(o["calificaciones"], criterios))
    for i, o in enumerate(orden, 1):
        print(f"  {i}. {o['nombre']}: {puntaje(o['calificaciones'], criterios):.2f}")
    if sin_fotos:
        print("\nUnidades SIN fotos (pásame capturas de pantalla):")
        for s in sin_fotos:
            print("  - " + s)
    print("\nListo: index.html actualizado.")


if __name__ == "__main__":
    main()
