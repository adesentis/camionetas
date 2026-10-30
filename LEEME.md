# Comparador de compras — instructivo

Una página que compara opciones de compra con una matriz de decisión ponderada.
Hoy compara camionetas, pero sirve para cualquier cosa: solo cambias los datos.

**Link publicado:** POR DEFINIR (se llena al publicar por primera vez)

---

## Qué hay en esta carpeta

| Archivo | Para qué sirve | ¿Lo tocas? |
|---|---|---|
| `datos.json` | **Todo el contenido**: requisitos, criterios, pesos, opciones, calificaciones, notas y links. | **Sí, este es el que editas** |
| `fotos\` | Una subcarpeta por unidad con sus fotos. | Sí, si agregas fotos a mano |
| `generar.bat` | Doble clic: baja fotos nuevas y rehace la página. | Lo usas |
| `publicar.bat` | Doble clic: rehace la página y la sube a internet. | Lo usas |
| `index.html` | La página ya armada. Se rehace sola; no la edites. | No |
| `plantilla.html`, `generar.py`, `publicar.py` | El diseño y los programas. | No |

---

## 1. Cambiar datos (precios, calificaciones, notas, pesos)

1. Clic derecho en `datos.json` → **Abrir con** → **Bloc de notas**.
2. Cambia lo que necesites y guarda (Ctrl + G).
3. Doble clic en `generar.bat`. Se abre una ventana negra que dice el ranking nuevo.
   Revisa que no diga "Error". Presiona una tecla para cerrarla.
4. Doble clic en `index.html` para ver cómo quedó en tu compu.

**Reglas para no romper el archivo** (si algo falla, casi siempre es una de estas):
- Los textos van entre comillas dobles: `"Kavak"`.
- Los números van **sin** comillas, **sin** signo de pesos y **sin** comas de miles: `379990`, no `"$379,990"`.
- Los decimales llevan **punto**: `3.5`, no `3,5`.
- Cada elemento de una lista lleva coma al final, **menos el último**.
- Las calificaciones van de 1 a 5. Los pesos deberían sumar 100 (si no, el programa te avisa).

## 2. Agregar una unidad nueva (otro anuncio)

1. En `datos.json`, busca la opción a la que pertenece (por ejemplo `"MG RX8 4x4 2023-2024"`).
2. Dentro de `"unidades": [ ... ]`, copia un bloque completo de `{` a `}` y pégalo después de una coma.
3. Cambia sus datos:
   - `"id"`: un nombre corto **sin espacios, sin acentos y sin mayúsculas**, distinto a los demás. Ejemplo: `"mgrx8-2024-toluca"`. Es el nombre de su carpeta de fotos.
   - `"anio"`, `"km"`, `"precio"`, `"ciudad"`, `"vendedor"`, `"anuncio"` (el link).
   - `"precio_nota"`: algo como `"más tarifa de servicio"`, o déjalo vacío: `""`.
4. Doble clic en `generar.bat`. **Baja solo las fotos del anuncio nuevo**; las que ya existen no se vuelven a descargar.
5. Si la ventana dice "Unidades SIN fotos", el sitio no dejó bajarlas. Ve al punto 4.

**Ojo con Kavak:** un mismo link de Kavak muestra varias unidades. El programa solo baja las fotos si la unidad principal del link tiene **exactamente** el kilometraje que pusiste. Si no coincide, te avisa y no baja nada (para no poner fotos de otro carro).

## 3. Agregar una opción nueva (otro modelo)

Copia un bloque completo de opción (desde `{ "id": "commander", ...` hasta su `}` final), pégalo después de una coma y cambia:
`"id"`, `"nombre"`, las 9 `"calificaciones"`, `"por_que"` y sus `"unidades"`.

## 4. Poner fotos a mano (capturas de pantalla)

1. En `fotos\`, crea una carpeta con el mismo nombre que el `"id"` de la unidad.
2. Pega ahí las imágenes con nombres en orden: `01-frente.jpg`, `02-lateral.jpg`, `03-trasera.jpg`...
   La página las muestra en orden alfabético.
3. Doble clic en `generar.bat`.

Si son capturas del celular, pásaselas a Claude para que les recorte botones, flechas y marcas de la app.

- **Cambiar una foto:** reemplaza el archivo en la carpeta.
- **Volver a bajar todas las fotos de una unidad:** borra todo lo que hay dentro de su carpeta y corre `generar.bat`.
- **Que el programa nunca intente bajar fotos de una unidad:** agrega `"descargar_fotos": false,` en esa unidad.

## 5. Publicar los cambios en internet

Doble clic en `publicar.bat`. Rehace la página y la sube. En 1 o 2 minutos el link muestra la versión nueva
(si no la ves en el celular, recarga la página).

El link no cambia nunca: lo que ya mandaste por WhatsApp siempre muestra la versión más reciente.

## 6. Usarlo para otra compra (no camionetas)

Copia toda la carpeta con otro nombre, borra lo de dentro de `fotos\` y cambia `datos.json`:
título, requisitos, criterios con sus pesos, opciones y unidades.
- `"filtros"` revisa año, km y presupuesto; si no aplica, déjalo así: `"filtros": {}`.
- `"criterio_opinion"` es el criterio que la otra persona califica con los botones del 1 al 5 (hoy `"estetica"`).

Para publicarla aparte necesitas otro repositorio en GitHub (ver la sección siguiente).

## 7. Publicar por primera vez (ya está hecho para las camionetas)

POR DEFINIR: se documenta al terminar la configuración de GitHub.

---

## Privacidad

- La página la puede ver cualquiera que tenga el link. No pongas apellidos, teléfonos, direcciones ni placas en `datos.json`.
- Tiene la etiqueta para que Google y otros buscadores **no** la muestren.
- GitHub Pages gratis exige que el repositorio sea **público**: los datos y las fotos también se pueden ver en github.com
  si alguien encuentra tu usuario. Por eso aplica lo mismo: nada personal en los datos.
- Las fotos son de los vendedores: se usan solo aquí y siempre con el link a su anuncio.
- Lo que tu esposa califica en "Tu opinión" se queda en su celular; solo te llega lo que mande por WhatsApp.

## Si algo falla

- **La ventana dice "Error" o se cierra de golpe:** casi siempre es una coma o comilla en `datos.json`. Revisa el último cambio.
  Puedes pegar el contenido del archivo en https://jsonlint.com para que te diga en qué línea está el problema.
- **"python no se reconoce":** Python no está instalado en esa computadora.
- **No sube a GitHub:** abre `publicar.bat` otra vez; si pide iniciar sesión, entra con tu cuenta de GitHub.
