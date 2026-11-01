# Circuitos base (probados, Java y Bedrock salvo que se indique)

Combínalos como piezas. Leyenda común de los planos (vista desde arriba salvo que se diga):
`═` polvo · `▶ ◀ ▲ ▼` repetidor mirando en esa dirección (número = retardo) · `C▶` comparador ·
`█` bloque sólido · `*` antorcha de redstone · `P` palanca · `B` botón · `·` aire · `N` bloque musical.

## Contenido
1. NOT (inversor)
2. OR
3. AND
4. Generador de pulso al encender (flanco de subida)
5. Memoria con bloqueo de repetidor
6. Biestable T con bombilla de cobre (1.21+)
7. Reloj de antorcha controlable
8. Puerta de pistones 1×2
9. Retardo largo

---

## 1. NOT (inversor)

Entrada → bloque sólido → antorcha en otra cara del bloque.

```
  ═ ═ █ *  ═ ═ →
```
Entrada encendida → antorcha apagada; entrada apagada → antorcha encendida. 1 tick de retardo.
Truco: si la palanca está pegada al bloque, la antorcha ya es "palanca invertida".

## 2. OR

Une dos líneas de polvo. Si una línea no debe recibir la señal de la otra, pon un repetidor (diodo) en cada entrada justo antes de la unión.

```
  A ═ ▶ ═ ═ → salida
            ║
  B ═ ▶ ═ ═╝
```

## 3. AND

Vista de frente (las entradas llegan por detrás):

```
Capa Y=2:   *  ═  *        ← antorchas encima de los bloques 1 y 3, polvo encima del bloque 2
Capa Y=1:   █  █  █
                  *        ← antorcha en la cara delantera del bloque 2 = SALIDA
```
- Entrada A energiza el bloque 1 (por detrás), entrada B el bloque 3.
- Si las dos están encendidas, las dos antorchas de arriba se apagan → el polvo del medio se apaga → el bloque 2 deja de estar energizado → la antorcha de salida se **enciende**.
- Retardo: 2 ticks.

## 4. Generador de pulso al encender

Convierte "palanca encendida" en un pulso corto **solo al encender**. Ideal para disparar una canción en bucle o cualquier cosa que deba pasar una vez.

```
        x=0  x=1  x=2   x=3
  z=0:   P    ═   C▶     ═ → pulso
  z=1:   ·    ═   ▲1
  z=2:   ·    ═    ═
```
- Comparador en **modo resta** (antorcha delantera encendida).
- Al encender: la entrada trasera recibe 15 al momento; el costado recibe 15 un tick después → salida = 15 durante ~1 tick y luego 0.
- Al apagar: no sale nada.
- Duración del pulso ≈ retardo del repetidor `▲` (1 a 4 ticks).
- Alternativa: un **observador** que mire a la palanca emite un pulso al encender **y** al apagar.

## 5. Memoria con bloqueo de repetidor

```
  dato ═ ▶ ═ → salida
         ▲
         ═  ← "guardar" (cuando está ENCENDIDO, el repetidor ▶ queda congelado)
         ▲
       control
```
- El repetidor de control (`▲` justo al costado de `▶`) bloquea a `▶` mientras está encendido.
- Desbloqueado: la salida sigue al dato. Bloqueado: la salida mantiene lo último que había.

## 6. Biestable T con bombilla de cobre (1.21+, Java y Bedrock)

Un botón que actúa como palanca (pulsar = encender, volver a pulsar = apagar):

```
  B █  ═  Bombilla  C▶  ═ → salida estable
```
- Botón en un bloque → polvo → bombilla de cobre (cambia de estado con cada pulso).
- Comparador leyendo la bombilla → 15 si está encendida, 0 si apagada.
- Encera la bombilla (panal) si no quieres que se oxide (solo cambia la luz, no la lógica).

## 7. Reloj de antorcha controlable

Vista desde arriba, capa Y=1:

```
        x=-1  x=0  x=1
  z=0:   P     █    *       ← antorcha pegada a la cara este del bloque █
  z=1:   ·     ▲4   ═
  z=2:   ·     ═    ═
```
- Antorcha (cara este de `█`) → polvo → vuelve por el repetidor `▲4`, que apunta al bloque `█`.
- Bloque energizado → antorcha se apaga → el repetidor se apaga 4 ticks después → antorcha se enciende... Periodo = 2 × (1 + retardo del repetidor) = 10 ticks (1 s).
- **Palanca encendida = reloj parado** (energiza el bloque fijo). Para que encendida = funciona, pon un inversor entre la palanca y el bloque.
- No uses retardos menores de 4 en total: la antorcha se puede quemar. Para periodos más largos, añade repetidores en el bucle.
- Salida: toma la señal de cualquier polvo del bucle.

## 8. Puerta de pistones 1 de ancho × 2 de alto

Vista lateral (el pasillo está en x=0):

```
           x=0     x=1      x=2         x=3       x=4
  Y=2:     (paso)  bloque   pistón◀     ═ (polvo encima del bloque de x=3)
  Y=1:     (paso)  bloque   pistón◀     █          ═ ← viene de la palanca
  Y=0:     suelo   suelo    suelo       suelo      suelo
```
- Dos pistones **pegajosos** apilados en x=2, mirando hacia el pasillo, con un bloque pegado delante (x=1).
- La línea de polvo sube al bloque de x=3: el polvo de arriba apunta al pistón superior y energiza el bloque de debajo, que activa el pistón inferior.
- **Palanca encendida = pistones extendidos = puerta cerrada.** Apagada = los bloques se retiran a x=1 = puerta abierta. Para invertirlo, inversor antes de la línea.
- En Java, cuidado con la cuasi-conectividad si pasas polvo por encima de los pistones.

## 9. Retardo largo

- Varios repetidores en fila: 4 ticks cada uno (10 repetidores = 4 s).
- Para minutos, usa un reloj de tolvas o un contador con comparadores; diseñarlo requiere más detalle: explica el principio y verifica en el juego.
