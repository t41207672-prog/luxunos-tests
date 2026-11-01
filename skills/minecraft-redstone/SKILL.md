---
name: minecraft-redstone
description: Diseña y explica circuitos de redstone de Minecraft (Java y Bedrock) paso a paso, con planos por capas, lista de materiales y comandos. Especialista en música con bloques musicales (note blocks) — por ejemplo, una palanca que al activarse toca una canción, cajas de música, timbres, bucles y acordes — y también en puertas, relojes, puertas lógicas, pulsos, granjas y mecanismos automáticos. Úsala siempre que el usuario hable de redstone, palancas, repetidores, comparadores, observadores, pistones, bloques musicales/note blocks, "hacer música en Minecraft", tocar una canción, puertas secretas, relojes de redstone o cualquier mecanismo de Minecraft, aunque no diga la palabra "redstone".
---

# Circuitos de redstone (Minecraft)

Esta skill sirve para que el usuario **construya un circuito que funcione a la primera**. Un circuito de redstone explicado "más o menos" casi nunca funciona: un repetidor girado, un bloque encima de un bloque musical o un polvo que no apunta donde debe lo rompen todo. Por eso la respuesta tiene que ser **concreta, bloque por bloque**, y apoyarse en mecánicas reales del juego.

## 1. Entender el pedido

Antes de diseñar, aclara (pregunta solo lo que no se pueda deducir; si falta algo, usa el valor por defecto y dilo):

| Dato | Por qué importa | Por defecto |
|---|---|---|
| Edición: **Java** o **Bedrock** (consola, móvil, Windows) | Hay mecánicas distintas (cuasi-conectividad, pulsos, comandos) | Diseño que funcione en ambas |
| Modo: supervivencia o creativo / ¿puede usar comandos? | Decide si das comandos `/setblock` o solo pasos manuales | Pasos manuales + comandos opcionales |
| Qué debe hacer exactamente | Una vez / en bucle, qué lo activa, qué lo detiene | — |
| Espacio disponible | Algunos diseños son largos | Compacto si es posible |

Para música, además: **qué canción** (o notas), **tempo**, y si debe sonar **una vez** al encender la palanca o **en bucle mientras esté encendida**.

## 2. Formato de la respuesta

Usa siempre esta estructura (en el idioma del usuario):

1. **Qué hace** — una o dos frases.
2. **Materiales** — lista con cantidades.
3. **Plano** — vista desde arriba, una cuadrícula por cada capa (Y) que tenga algo, con leyenda. Indica el norte o la dirección en la que viaja la señal, y hacia dónde mira cada repetidor/comparador/observador (flechas `→ ← ↑ ↓`).
4. **Construcción paso a paso** — numerada, en el orden en que conviene colocar los bloques (primero el soporte, después los componentes, la fuente de energía al final para que nada se active antes de tiempo).
5. **Cómo probarlo** — qué debe pasar al accionar la palanca/botón.
6. **Si no funciona** — los 3-4 fallos más probables para *ese* circuito.
7. (Opcional) **Comandos** para Java, si el usuario puede usarlos.

Ejemplo de plano:

```
Capa Y=1 (vista desde arriba, la señal va hacia la derecha →)
  P = palanca   ═ = polvo de redstone   ▶2 = repetidor mirando → con 2 ticks
  N = bloque musical   █ = bloque sólido   · = aire

  P ═ ▶1 N ▶2 N ▶2 N
```

Explica los porqués brevemente ("el repetidor va pegado al bloque musical porque así lo **energiza fuerte** y la señal puede seguir al siguiente repetidor"). Así el usuario puede adaptar el diseño.

## 3. Reglas que no se pueden olvidar

Estas son las causas número uno de circuitos que "no funcionan":

- **Polvo de redstone**: la señal dura **15 bloques**; después hace falta un repetidor. El polvo solo energiza el bloque sobre el que está y el bloque hacia el que **apunta**.
- **Repetidor**: retardo de 1 a 4 ticks (**1 tick de redstone = 0,1 s**), refuerza la señal a 15, solo deja pasar en una dirección. Si otro repetidor/comparador encendido le apunta por el costado, queda **bloqueado**.
- **Bloque musical**: necesita **aire justo encima** (si no, no suena; la excepción son las cabezas de mob, que hacen sonar su sonido). El **bloque de debajo** elige el instrumento. Suena **una vez cada vez que pasa de apagado a encendido**, no mientras sigue encendido.
- **Fuerte vs. débil**: un bloque al que le apunta un repetidor queda energizado *fuerte* y activa polvo y repetidores a su lado; uno energizado solo por polvo (débil) no activa polvo vecino. Ambos activan los mecanismos pegados: **un bloque musical pegado a un bloque energizado (o a otro bloque musical energizado) también suena**.
- **Java vs. Bedrock**: en Java existe la *cuasi-conectividad* (pistones, dispensadores y soltadores se activan si se energiza el bloque de encima de ellos); en Bedrock no. En Bedrock los pistones tardan un poco más y algunos circuitos de tick exacto se comportan distinto. Si no sabes la edición, evita diseños que dependan de estas diferencias.

Detalles de cada componente y más diferencias entre ediciones: `references/fundamentos.md`.

## 4. Música con bloques musicales

Este es el caso estrella: "una palanca que al activarla toque una canción".

### Diseño base (una vez por activación)

Una **línea de tiempo**: repetidores y bloques musicales alternados, en fila.

```
P ═ ▶ N ▶ N ▶▶ N ▶ N ...
```

- La palanca energiza el polvo → el primer repetidor → el primer bloque musical suena → ese bloque (energizado fuerte) activa el siguiente repetidor → y así sucesivamente.
- El **tiempo entre dos notas** = suma de los retardos de los repetidores entre ellas. Si hace falta más de 4 ticks, pon varios repetidores seguidos.
- **Silencios**: solo repetidores, sin bloque musical.
- **Acordes** (varias notas a la vez): hasta 3 notas, el repetidor apunta a un bloque sólido con bloques musicales pegados a los lados y encima. Para más voces, una **pista paralela por voz**, todas alimentadas por la misma línea de polvo desde la palanca (el polvo no tiene retardo, así que todas arrancan a la vez). Deja **siempre** una fila de aire entre pistas: si dos bloques musicales de pistas distintas se tocan, sonarán juntos.
- Al **apagar** la palanca no suena nada. Para repetir: apagar, esperar a que termine y volver a encender.

Para **bucle mientras la palanca esté encendida**, para acordes complejos, percusión y trucos de tempo, lee `references/bloques-musicales.md` (incluye el circuito de bucle completo, la tabla de clics por nota y los rangos de cada instrumento).

### Usa el script para calcular la canción

Calcular a mano los clics de cada nota y los retardos es lento y propenso a errores. El script `scripts/cancion_a_redstone.py` lo hace exacto:

```bash
python3 scripts/cancion_a_redstone.py -c "E4:2 E4:2 F4:2 G4:2 G4:2 F4:2 E4:2 D4:2" --ticks-por-paso 2
python3 scripts/cancion_a_redstone.py cancion.txt --mcfunction musica.mcfunction   # + comandos Java
```

- Notación: `C4` (Do central) o `do4`, `F#4`/`fa#4`, `Bb3`/`sib3`, duración con `:2`, acordes con `+` (`C4+E4+G4`), silencio `R`, percusión `bombo`, `caja`, `platillo`, instrumento forzado `G4@flute`. Ejecuta el script con `--help` para ver todo.
- Devuelve: materiales, plano de cada pista, tabla de afinación (posición → clics → bloque de debajo) y la duración total en ticks (necesaria para hacer el bucle).
- `--mcfunction` genera comandos `/fill` y `/setblock` de **Java** (en Bedrock el tono del bloque musical no se puede fijar por comando: hay que dar los clics a mano, así que dale la tabla).
- Si una nota no cabe en el rango de ningún instrumento, el script avisa; usa `--transponer-auto` o elige otro instrumento.
- Ejemplo de archivo de canción: `assets/himno-de-la-alegria.txt`.

Si no puedes ejecutar código, calcula con la tabla de `references/bloques-musicales.md` y revisa cada nota dos veces.

Cuando el usuario no da las notas de una canción conocida, escribe tú la melodía en la notación (en una tonalidad que caiga en Fa#3–Fa#5 para que todo sea arpa) y avisa que es una transcripción aproximada que puede corregir.

### Al entregar una canción, incluye siempre

- La tabla de afinación (cuántos clics por bloque y qué bloque va debajo).
- El recordatorio de dejar aire encima de cada bloque musical.
- El tempo resultante (BPM de la negra = 600 / ticks por negra).
- Cómo probar una sola nota (golpear el bloque con la mano la hace sonar sin cambiar su tono; el clic derecho sí la sube un semitono).

## 5. Otros circuitos

Para puertas lógicas (NOT, OR, AND), relojes, generadores de pulso, memorias, puertas de pistones y otros mecanismos, usa los diseños probados de `references/circuitos-base.md` y combínalos. Prefiere siempre el diseño más simple que cumpla lo pedido: menos componentes = menos sitios donde equivocarse.

Si el usuario pide algo que no está en las referencias, diseña a partir de las reglas de la sección 3, recorre mentalmente la señal tick a tick ("tick 0: la palanca enciende el polvo; tick 1: el repetidor se enciende..."), y si algo depende de un comportamiento que no es seguro en su edición, dilo en lugar de adivinar.
