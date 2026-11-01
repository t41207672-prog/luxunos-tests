# Fundamentos de redstone

## Contenido
1. Unidades de tiempo
2. Fuentes de energía
3. Transmisión: polvo, repetidor, comparador
4. Energía fuerte y débil
5. Componentes que reaccionan (salidas)
6. Diferencias Java / Bedrock
7. Cómo comprobar un diseño "tick a tick"

---

## 1. Tiempo

- **1 tick de redstone = 2 ticks de juego = 0,1 s.** Todo retardo de este documento está en ticks de redstone salvo que se diga lo contrario.
- 10 ticks de redstone = 1 segundo.

## 2. Fuentes de energía

| Fuente | Señal | Notas |
|---|---|---|
| Palanca | 15 continua | Se queda encendida/apagada. Energiza fuerte el bloque al que está pegada |
| Botón de piedra | 15, pulso de 10 ticks (1 s) | Botón de madera: 15 ticks (1,5 s); también lo activan flechas |
| Placa de presión | 15 (de peso: según cantidad de entidades) | Madera: cualquier entidad; piedra: mobs y jugadores |
| Antorcha de redstone | 15 | Se **apaga** si el bloque al que está pegada recibe energía (inversor). 1 tick de retardo |
| Bloque de redstone | 15 permanente | Se puede mover con pistones |
| Sensor de luz solar | 0–15 según la luz | Clic derecho: modo nocturno |
| Observador | pulso de 1 tick | Detecta cambios en el bloque que mira; emite por detrás |
| Bloque diana | según dónde acierte el proyectil | |
| Cable trampa (tripwire) | 15 | Con dos ganchos |

## 3. Transmisión

**Polvo de redstone**
- Pierde 1 de fuerza por bloque: con una fuente de 15 llega a 15 bloques.
- Energiza el bloque de debajo y el bloque hacia el que **apunta**. Una línea recta apunta en sus dos extremos.
- Sube y baja escalones de 1 bloque (si no hay un bloque sólido que corte la diagonal).
- No tiene retardo.
- En Java, un polvo suelto con forma de cruz energiza en las 4 direcciones; clic derecho lo cambia a punto (no energiza a los lados).

**Repetidor**
- Retardo 1–4 ticks (clic derecho para cambiarlo). Refuerza la señal a 15.
- Solo deja pasar en un sentido: entra por detrás, sale por delante (el lado de la antorcha simple).
- Energiza **fuerte** el bloque que tiene delante.
- **Bloqueo**: si un repetidor o comparador encendido apunta a su costado, el repetidor se congela en su estado actual.
- Alarga los pulsos más cortos que su retardo hasta igualar su retardo.

**Comparador** (1 tick de retardo)
- **Modo comparar** (antorcha delantera apagada): salida = entrada trasera si es ≥ que la lateral más fuerte; si no, 0.
- **Modo restar** (antorcha delantera encendida): salida = trasera − lateral más fuerte (mínimo 0).
- Lee contenedores (cofre, tolva, horno, barril, soltador...): da una señal proporcional a lo lleno que está. También lee atriles, marcos (rotación del objeto), pasteles, bloques de compostaje, la bombilla de cobre (15 si está encendida), etc.

## 4. Energía fuerte y débil

- Un bloque sólido está **fuertemente energizado** si le apunta un repetidor/comparador, si tiene una palanca/botón pegados o una antorcha debajo. Un bloque fuerte activa: polvo a su lado, repetidores que salen de él y mecanismos vecinos.
- Está **débilmente energizado** si solo le llega polvo (encima o apuntándole). Un bloque débil activa los mecanismos pegados a él (pistones, lámparas, bloques musicales, puertas...) y los repetidores/comparadores que salen de él, pero **no** activa polvo vecino.
- Los bloques no transparentes conducen; cristal, losas (salvo dobles), escaleras, hojas y otros transparentes **no** conducen energía.
- Un bloque energizado **no** energiza a otro bloque sólido pegado a él, pero **sí activa los mecanismos pegados** (un bloque musical pegado a un bloque energizado suena).

## 5. Componentes que reaccionan

| Componente | Comportamiento |
|---|---|
| Pistón / pistón pegajoso | Empuja hasta 12 bloques. No mueve obsidiana, bloques con inventario (en Java), etc. El pegajoso tira del bloque al retraerse |
| Lámpara de redstone | Se enciende con energía; se apaga con 2 ticks de retraso |
| Puerta / trampilla / puerta de valla | Se abre con energía |
| Bloque musical | Suena una vez al recibir energía (necesita aire encima) |
| Dispensador / soltador | Dispara / suelta un objeto por cada pulso |
| Tolva | Con energía se **bloquea** (deja de mover objetos) |
| TNT | Se enciende |
| Raíl propulsor / activador | Se activa |
| Bombilla de cobre (1.21+) | **Cambia** de encendida a apagada en cada pulso (es un biestable T); un comparador la lee como 15 si está encendida |
| Crafteador (1.21+) | Fabrica un objeto por pulso |

## 6. Diferencias Java / Bedrock

| Tema | Java | Bedrock |
|---|---|---|
| Cuasi-conectividad | Pistones, dispensadores y soltadores se activan si se energiza el espacio de **encima** de ellos (aunque no se actualicen hasta recibir otra actualización) | No existe |
| Pulsos de 0 ticks y "trucos" de tick exacto | Habituales | No funcionan igual |
| Pistones | Tiempos fijos y deterministas | Tardan algo más; circuitos muy ajustados pueden fallar |
| Mover bloques con inventario | No | Sí (los pistones pueden mover cofres, etc.) |
| Tono del bloque musical por comando | `note_block[note=N,instrument=...]` | No: hay que dar los clics a mano |
| Quemado de antorchas | Una antorcha que cambia muy rápido (≈8 veces en 3 s) se quema temporalmente | Comportamiento parecido; no abuses de relojes de 1 tick |

Si el usuario no ha dicho la edición, diseña sin depender de nada de esta tabla.

## 7. Comprobar un diseño tick a tick

Antes de entregar un circuito, recórrelo así:

1. Lista los componentes en el camino de la señal.
2. Escribe una línea de tiempo: `tick 0: palanca ON → polvo 15 → entrada del repetidor A`, `tick 1: A ON → bloque musical 1 suena y energiza fuerte → entrada de B`, ...
3. Comprueba en cada paso: ¿la señal llega con fuerza ≥ 1? ¿el repetidor mira hacia el lado correcto? ¿hay algo que bloquee (repetidor lateral, bloque transparente, bloque encima del bloque musical)?
4. Haz lo mismo para el apagado: ¿se apaga todo bien o queda algo "enganchado"?
5. Busca conexiones no deseadas: polvo que se conecta a un componente vecino que no debería, pistones activados por un bloque energizado al lado, y (en Java) cuasi-conectividad.
