# Bloques musicales (note blocks) — referencia completa

## Contenido
1. Cómo funciona un bloque musical
2. Instrumentos (bloque de debajo) y rangos
3. Tabla de clics por nota
4. Tempo y ritmo
5. Diseño 1: una vez por palanca (línea de tiempo)
6. Diseño 2: acordes y varias voces
7. Diseño 3: bucle mientras la palanca está encendida
8. Diseño 4: timbre / una sola nota o melodía corta con botón
9. Solución de problemas

---

## 1. Cómo funciona

- **Receta**: 8 tablones de madera + 1 polvo de redstone (en el centro).
- **Clic derecho** (usar): sube el tono 1 semitono. Hay **25 tonos (0–24)**; tras el 24 vuelve al 0.
- **Clic izquierdo** (golpear): toca la nota actual sin cambiarla. Útil para probar.
- **Con redstone**: suena una vez cada vez que el bloque pasa de *no energizado* a *energizado* (flanco de subida). Mantener la señal no repite la nota.
- **Necesita aire encima.** Cualquier bloque encima lo silencia (excepción: una **cabeza de mob** encima hace que reproduzca el sonido de ese mob en vez de una nota; Java 1.20+ y versiones recientes de Bedrock).
- Se activa con: un repetidor o comparador apuntándole, polvo que le apunta, una palanca/botón pegados a él, **o estando pegado a un bloque sólido energizado** (también a otro bloque musical energizado). Lo más fiable para la línea principal es **un repetidor apuntando directo al bloque musical**.
- Consecuencia importante: si dos bloques musicales se tocan y uno recibe energía de un repetidor, **el otro también suena**. Útil para acordes (ver Diseño 2), pero por eso las pistas paralelas deben ir separadas por una fila de aire.
- El bloque musical es un bloque sólido conductor: si un repetidor le apunta, queda energizado **fuerte**, y un repetidor colocado al otro lado, mirando hacia fuera, recibe la señal. Esto permite encadenar `repetidor → nota → repetidor → nota`.
- En **Java** el tono se ve con F3 (`note=` en el bloque) y se puede fijar por comando: `note_block[instrument=harp,note=6]`. En **Bedrock** el tono no se puede poner con `/setblock`: hay que dar los clics a mano.

## 2. Instrumentos y rangos

El instrumento depende del **bloque que está debajo** del bloque musical. "Clic 0" es siempre un Fa#; cada instrumento cubre 2 octavas (25 semitonos).

| Instrumento | Bloque de debajo (ejemplos) | Rango (clic 0 → 24) |
|---|---|---|
| Arpa / piano | cualquier otro: tierra, césped, aire, etc. | Fa#3 – Fa#5 |
| Bajo | madera: tablones, troncos, cofres de madera | Fa#1 – Fa#3 |
| Guitarra | lana | Fa#2 – Fa#4 |
| Flauta | bloque de arcilla | Fa#4 – Fa#6 |
| Campana | bloque de oro | Fa#5 – Fa#7 |
| Carillón | hielo compacto | Fa#5 – Fa#7 |
| Xilófono | bloque de hueso | Fa#5 – Fa#7 |
| Vibráfono (xilófono de hierro) | bloque de hierro | Fa#3 – Fa#5 |
| Cencerro | arena de almas | Fa#4 – Fa#6 |
| Didgeridoo | calabaza | Fa#1 – Fa#3 |
| Bit (8 bits) | bloque de esmeralda | Fa#3 – Fa#5 |
| Banjo | fardo de heno | Fa#3 – Fa#5 |
| Pling (piano eléctrico) | piedra luminosa | Fa#3 – Fa#5 |
| **Bombo** (percusión) | piedra, roca, netherrack, obsidiana, cuarzo, ladrillos, arenisca | — |
| **Caja / redoblante** (percusión) | arena, grava, cemento en polvo | — |
| **Platillo / hi-hat** (percusión) | cristal, linterna marina, faro | — |

Notación: Do4 = Do central (C4, MIDI 60). La arena y la grava caen: ponles un bloque sólido debajo.

## 3. Tabla de clics por nota

Para instrumentos que empiezan en **Fa#3** (arpa, vibráfono, bit, banjo, pling):

```
 0 Fa#3   1 Sol3   2 Sol#3  3 La3    4 La#3   5 Si3
 6 Do4    7 Do#4   8 Re4    9 Re#4  10 Mi4   11 Fa4
12 Fa#4  13 Sol4  14 Sol#4 15 La4   16 La#4  17 Si4
18 Do5   19 Do#5  20 Re5   21 Re#5  22 Mi5   23 Fa5
24 Fa#5
```

Para otros instrumentos, los clics son los mismos **desplazados de octava**:
- Bajo y didgeridoo: restar 2 octavas (clic 6 = Do2).
- Guitarra: restar 1 octava (clic 6 = Do3).
- Flauta y cencerro: sumar 1 octava (clic 6 = Do5).
- Campana, carillón y xilófono: sumar 2 octavas (clic 6 = Do6).

Fórmula: `clics = (nota_MIDI) − (MIDI del Fa# inicial del instrumento)`; Fa#1=30, Fa#2=42, Fa#3=54, Fa#4=66, Fa#5=78. Bemoles: Sib = La#, Mib = Re#, etc.

## 4. Tempo y ritmo

- 1 tick de redstone = 0,1 s. Un repetidor da 1–4 ticks.
- El tiempo entre dos notas de la misma pista = suma de los repetidores entre ellas.
- **BPM (negra) = 600 / ticks por negra.**

| Ticks por negra | BPM | Corchea | Semicorchea |
|---|---|---|---|
| 2 | 300 | 1 tick | — |
| 4 | 150 | 2 ticks | 1 tick |
| 5 | 120 | — (2,5) | — |
| 6 | 100 | 3 ticks | — |
| 8 | 75 | 4 ticks | 2 ticks |

El tempo real siempre es "redondeado" a ticks enteros: elige el que más se parezca y avisa al usuario. Una canción conocida suele sonar bien con 2 ticks por corchea (150 BPM) o 3 ticks por corchea (100 BPM).

## 5. Diseño 1 — Una vez por palanca (el clásico)

```
Capa Y=1, vista desde arriba (la señal va →)

  P ═ ▶1 N ▶4 N ▶4 N ▶4 N ▶4▶4 N ...
```

- `P` palanca en el suelo, `═` polvo, `▶n` repetidor mirando → con retardo n, `N` bloque musical.
- Capa Y=0 (debajo): suelo cualquiera bajo los repetidores; bajo cada `N`, el bloque del instrumento.
- Capa Y=2: **aire** sobre cada `N`.

Construcción:
1. Pon el suelo y los bloques de instrumento.
2. Coloca los bloques musicales y afínalos (clics según la tabla). Golpéalos para comprobar.
3. Coloca los repetidores mirando en la dirección de la canción (la flecha/el frente de la antorcha pequeña hacia el siguiente bloque) y ajusta su retardo (clic derecho: 1→2→3→4).
4. Al final, el polvo y la palanca.

Cuando la palanca se enciende, la señal recorre la fila y cada nota suena en su momento. La palanca puede quedar encendida; al apagarla no suena nada.

**Canciones largas**: la fila puede doblar en serpentina. En cada giro: `N ▶` → bloque sólido o repetidor girando 90° (un repetidor puede tomar la señal de un bloque musical energizado fuerte en cualquier lado, siempre que el repetidor mire *alejándose* del bloque). Suma el retardo de los repetidores del giro al tiempo de la siguiente nota.

## 6. Diseño 2 — Acordes y varias voces

**Opción A — acorde compacto (hasta 3 notas a la vez en una sola fila).** El repetidor apunta a un bloque sólido (no transparente) y los bloques musicales van pegados a él: a los dos lados y encima.

```
Vista desde arriba, capa Y=1 (señal →):        Vista lateral:
        N                                              N   ← encima (con aire arriba)
  ▶ ▶   █   ▶ N ...                                ▶  █  ▶
        N
```
- El repetidor energiza fuerte el bloque `█` → los 3 bloques musicales pegados suenan a la vez → el siguiente repetidor sale de `█` y la canción continúa.
- Cada bloque musical lateral necesita su bloque de instrumento debajo y aire encima. El de arriba usa `█` como bloque de instrumento (piedra = bombo; usa por ejemplo tierra o un bloque de madera según el instrumento que quieras).
- Asegúrate de que los bloques musicales laterales no toquen ningún otro bloque energizado.

**Opción B — una pista por voz** (para más de 3 voces o ritmos distintos por voz), en paralelo, separadas por una fila de aire:

```
Capa Y=1 (señal →)

  P
  ═ ▶1 N ▶4 N ▶4 N      ← pista 1 (melodía)
  ═
  ═ ▶1 N ▶4 · ▶4 N      ← pista 2 (armonía; '·▶' = silencio: solo repetidores)
  ═
  ═ ▶1 N ▶4 N ▶4 N      ← pista 3 (bajo, con madera debajo)
```

- La columna de polvo `═` reparte la señal de la palanca a todas las pistas **sin retardo**, así que todas arrancan a la vez.
- Para que una nota suene a la vez en dos pistas, la suma de retardos desde el inicio debe ser igual en ambas.
- El polvo pierde 1 de fuerza por bloque: con pistas separadas por 1 fila caben hasta 8 pistas. Para más, pon un repetidor en la columna (y suma ese tick a todas las pistas que alimenta).
- En la pista 2 de arriba, "silencio" significa que hay repetidores sin bloque musical (dos repetidores seguidos se pasan la señal sin problema).

## 7. Diseño 3 — Bucle mientras la palanca está encendida

Idea: la canción la dispara un **pulso**. Ese mismo pulso entra en una **línea de retorno** de repetidores que tarda exactamente lo que dura la canción y vuelve a disparar el inicio. La palanca abre o cierra esa línea.

Piezas:

**a) Generador de pulso al encender (comparador en modo resta)** — funciona en Java y Bedrock.

```
Capa Y=1, vista desde arriba (x hacia la derecha, z hacia abajo)

        x=0  x=1  x=2  x=3
  z=0:   P    ═   [C→]  ═ → (sale el pulso hacia la línea de alimentación)
  z=1:   ·    ═    ▲1
  z=2:   ·    ═    ═
```

- `P` palanca. `C→` comparador mirando → (entrada por la izquierda) en **modo resta** (clic derecho: se enciende su antorcha delantera).
- La rama de abajo lleva la señal a un repetidor `▲1` que apunta **hacia arriba, al costado del comparador**.
- Al encender la palanca: la entrada trasera recibe 15 al instante y el costado todavía 0 → el comparador emite. Un tick después el repetidor llena el costado → 15 − 15 = 0 → se apaga. Resultado: **un pulso corto solo al encender**. Al apagar, no emite nada.
- Retardo del repetidor = duración del pulso (1 basta para bloques musicales).

**b) Línea de alimentación y pistas** como en el Diseño 1/2, pero alimentadas por la salida del generador de pulso en vez de la palanca.

**c) Línea de retorno con compuerta**:
- Desde la línea de alimentación sale una fila de repetidores (sin notas) que da la vuelta y **vuelve a entrar en la misma línea de alimentación**. Su retardo total debe ser **igual a la duración de la canción** (el script la da como "duración en ticks"). Así el pulso vuelve justo cuando termina la última nota y la canción empieza de nuevo sin desfase.
- Uno de los repetidores de esa línea es la **compuerta**: a su costado le apunta otro repetidor que viene de un **inversor** de la palanca. Inversor: coloca la palanca en la cara de un bloque sólido y una antorcha de redstone en otra cara de ese mismo bloque; antorcha → polvo → repetidor apuntando al costado de la compuerta. (Una antorcha sola al costado no bloquea: tiene que ser un repetidor o comparador.)
- La misma palanca alimenta también el generador de pulso del punto a).
- Palanca encendida → antorcha apagada → compuerta libre → el pulso da vueltas y la canción se repite.
- Palanca apagada → antorcha encendida → la compuerta queda **bloqueada** → el pulso muere al llegar → la canción termina la vuelta actual y se detiene.

Advertencia: si apagas la palanca justo en el tick en que el pulso está dentro de la compuerta, puede quedar bloqueada *encendida*. Es raro; basta con encender y apagar de nuevo.

## 8. Diseño 4 — Timbre con botón

Botón en un bloque → polvo → repetidores y notas como en el Diseño 1. El botón de piedra da un pulso de 1 s (10 ticks) y el de madera 1,5 s; como el bloque musical solo suena en el flanco de subida, ambos sirven. "Ding-dong" típico: Mi5 y Do5 con campana o carillón, separados por 4–6 ticks.

## 9. Solución de problemas

| Síntoma | Causa probable |
|---|---|
| Un bloque no suena | Tiene un bloque encima (¡incluso una losa o el polvo!), o el repetidor anterior está girado |
| Suena con otro instrumento | El bloque de debajo no es el correcto (p. ej. piedra → bombo en vez de arpa) |
| La canción se corta a mitad | Un repetidor mira al revés, o el polvo llega con fuerza 0 (más de 15 bloques) |
| Las notas de un acorde no coinciden | Las pistas no suman el mismo retardo hasta esa nota |
| Va demasiado rápido/lento | Ajusta los retardos; recuerda BPM = 600 / ticks por negra |
| Suena una nota equivocada | Recuenta clics: tras 24 vuelve a 0. En Java mira `note=` con F3 |
| El bucle no se repite | La línea de retorno no vuelve a la línea de alimentación, o la compuerta está bloqueada |
| El bucle se desfasa | El retardo de la línea de retorno no es igual a la duración total de la canción |
