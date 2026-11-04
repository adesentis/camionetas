# Estado del proyecto (para retomar en un chat nuevo)

Última actualización: 4 de noviembre de 2026.

## Qué es

Comparador para elegir la camioneta que reemplaza la Mazda CX-5 de Alfredo. Página pública (no se
indexa): https://adesentis.github.io/camionetas/. Repositorio: `adesentis/camionetas`. En la PC de
escritorio está en `C:\Users\Alfredo Oficina\Downloads\Proyectos Claude Code\Comparador de Compras`.

- `datos.json`: todo el contenido (filtros, criterios, modelos, unidades, descartadas, novedades).
- `generar.py` arma `index.html` y baja fotos; `publicar.py` (o `publicar.bat`) hace pull, genera y publica.
- `busqueda-diaria/instrucciones.md`: lo que Claude Code hace cada mañana a las 8:00 en la PC de
  escritorio (tarea de Windows "Camionetas - busqueda diaria"): revisa anuncios, busca unidades,
  escribe Novedades y el "Análisis del día" (top 5 en texto corrido). Ver `LEEME.md`.

## Cómo trabajar con Alfredo

- No programa. Español de México, pasos cortos y claros. Muchas veces escribe desde el celular.
- Preguntar antes de crear cuentas, publicar algo nuevo, instalar programas o comprometer citas o fechas.
- Nunca dar por buena una unidad sin abrir su anuncio: precio, km, disponibilidad y tracción confirmados.
  Ya pasó que un anuncio decía "Pro Max 2.0T 4WD" y era 1.6T (emblema 290T), y que un precio era de crédito.
- No saltarse bloqueos de sitios. Desde la nube no se pueden abrir Kavak, Mercado Libre ni Dalton;
  desde la PC de escritorio sí (excepto Mercado Libre, que bloquea la lectura automática).
- Privacidad: sin apellidos, teléfonos, direcciones ni placas (tapar placas en fotos).

## Decisiones tomadas

- Presupuesto: diferencia máxima de $250,000 después de entregar la CX-5. Kavak (respuesta del 4-nov, cifras
  preliminares, sujetas a inspección, vigentes hasta el 7 de noviembre de 2026): $221,944 en intercambio (a cuenta
  de una unidad de su catálogo) o $213,805 si solo se la vendemos (pago el mismo día, al validar documentos; sin
  tarifa de servicio). La página usa $221,944 para unidades de Kavak y $213,805 para las de otros vendedores
  (`venta_actual` y `venta_directa` en `filtros`).
- Kavak: comparar con precio de contado + tarifa de servicio (5% del precio, tope $25,000 según Kavak;
  sus términos dicen 5% sin tope y que el precio publicado ya la incluye: contradicción a favor de Alfredo).
  La tarifa solo se cobra al comprar con ellos. Kavak confirmó el 4-nov: RX8 2024 $19,350 y RX8 2023 $17,950;
  con la RX8 2023 de contado la diferencia es de unos $155,000 (cuadra con la página).
  Su crédito a 72 meses tiene CAT de 33.1%: no conviene salvo liquidarlo pronto (sin penalización desde el mes 4).
- Montaña y lluvia: basta con que suba mejor que la CX-5 (2.0 sin turbo, 155 hp, 203 Nm). La tracción
  integral suma puntos pero no es obligatoria (`montana_minima` 1.5).
- Descartadas por gusto: GAC y Peugeot. Estética: RX9 = 5 (la favorita), RX8 = 3, GAC = 1.
- MG RX8: descontinuada (alerta roja); costo de tenerla 2.5.
- Las unidades confirmadas como disponibles van antes en el ranking; las que no suben bien, al final.

## Situación actual

- Favorita: MG RX9 Premier AWD. Ninguna dentro del presupuesto (precio máximo $471,944 en Kavak, $463,805 en otro lado): dos 2025 en Dalton
  Guadalajara ($517,563 "con garantía incluida", unos $54,000 arriba del tope; Dalton y Mercado Libre también dicen $504,063 de contado;
  falta confirmar por escrito tracción y 7 asientos; la versión dice "7Pas.") y una en Kavak Lerma
  ($572,999 de contado + $25,000). El resto en Mercado Libre pide $560,000 o más (revisado 3-nov).
- Opciones dentro del presupuesto: Tiggo 8 Pro Max AWD 2024 en Guadalajara ($415,000 y $429,900, Mercado
  Libre; 1.ª y 2.ª del ranking), (revisado 4-nov: son Tiggo 8 Pro Max de 3 filas; en México
  ese modelo solo es de 7; la tercera fila va doblada en el piso de la cajuela y ninguna foto la muestra; falta
  que cada vendedor mande foto de la cajuela con la tercera fila arriba), MG RX8 2023 y 2024 (Kavak y Mercado Libre), Pro Max AWD 2024 de Puebla.
- Pendiente de Alfredo: refactura y cambio de propietario de la CX-5 con Dalton (sin eso no se puede vender);
  Kavak ya contestó las cifras (4-nov), pero no si la tarifa tiene tope de $25,000 (pesa en la RX9 de Lerma)
  ni mejoró la oferta. Kavak invita a ver las dos RX8 en El Rosario. La oferta vence el 7 de noviembre.
- Mercado Libre (investigado 3-nov): la API oficial NO sirve. Sin token responde 403; su documentación ya solo
  ofrece buscar en las publicaciones propias o de un vendedor, y desde 2025 hay reportes de 403 en la búsqueda
  pública incluso con app y token. Decisión: no crear la app. Sus páginas normales sí se leen (el 2-nov
  bloqueó, el 3-nov funcionó, con límite de velocidad a media revisión): se sigue así, sin saltarse límites.
  Opcional para Alfredo: "Guardar búsqueda" de MG RX9 en Mercado Libre para que le lleguen avisos por correo.
- Búsqueda diaria: el 3-nov corrió a las 8:52 (la PC estaba apagada a las 8:00) y terminó bien, pero no
  actualizó el "Análisis del día"; se rehizo a mano. Si se repite, revisar el paso 7 de las instrucciones.
