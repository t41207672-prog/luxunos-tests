#!/usr/bin/env python3
"""
cancion_a_redstone.py — Convierte una canción escrita en texto en un circuito
de redstone con bloques musicales (note blocks) que se activa con una palanca.

Calcula, para cada nota:
  * cuántos clics hay que darle al bloque musical (0-24),
  * qué bloque poner DEBAJO para elegir el instrumento,
  * cuántos repetidores y con qué retardo (1-4 ticks) van entre notas.

Y genera:
  * una lista de construcción y un plano visto desde arriba (texto),
  * opcionalmente, comandos /setblock y /fill de Minecraft Java (.mcfunction),
  * opcionalmente, un JSON con todo el diseño.

NOTACIÓN DE LA CANCIÓN (tokens separados por espacios o saltos de línea):
  C4        nota Do4 (Do central), dura 1 paso
  do4       lo mismo en solfeo (do re mi fa sol la si)
  F#4  Bb3  sostenidos (#) y bemoles (b)  ->  fa#4, sib3 también valen
  E4:2      la nota dura 2 pasos
  C4+E4+G4  acorde (varias notas a la vez; cada una va a su propia pista)
  G4@flute  fuerza un instrumento para esa nota
  R:2  -    silencio (R o -), con duración opcional
  bombo caja platillo   percusión (también basedrum, snare, hat);
  caja=5    percusión con 5 clics (cambia un poco el tono)
  # ...     comentario hasta el final de la línea
  |         barra de compás opcional (se ignora)

Un "paso" dura --ticks-por-paso ticks de redstone (1 tick = 0,1 s).
Ejemplo: con 2 ticks por paso y corcheas = 1 paso, la negra (2 pasos) dura
0,4 s  ->  150 BPM.  Fórmula: BPM(negra) = 600 / ticks_por_negra.

Uso:
  python3 cancion_a_redstone.py cancion.txt
  python3 cancion_a_redstone.py -c "E4 E4 F4 G4 G4 F4 E4 D4" --ticks-por-paso 3
  python3 cancion_a_redstone.py cancion.txt --mcfunction musica.mcfunction
  python3 cancion_a_redstone.py cancion.txt --json diseno.json
"""

import argparse
import json
import math
import re
import sys

# ---------------------------------------------------------------------------
# Datos de instrumentos (Java y Bedrock comparten instrumentos y rangos).
# midi_base = nota MIDI que suena con 0 clics (siempre un Fa#). Rango = base..base+24
# ---------------------------------------------------------------------------
INSTRUMENTOS = {
    "harp":           {"base": 54, "bloque": "dirt",          "es": "Arpa/piano",       "debajo": "cualquier otro bloque (tierra, césped, aire...)"},
    "bass":           {"base": 30, "bloque": "oak_planks",    "es": "Bajo",             "debajo": "madera (tablones, troncos)"},
    "guitar":         {"base": 42, "bloque": "white_wool",    "es": "Guitarra",         "debajo": "lana"},
    "flute":          {"base": 66, "bloque": "clay",          "es": "Flauta",           "debajo": "bloque de arcilla"},
    "bell":           {"base": 78, "bloque": "gold_block",    "es": "Campana",          "debajo": "bloque de oro"},
    "chime":          {"base": 78, "bloque": "packed_ice",    "es": "Carillón",         "debajo": "hielo compacto"},
    "xylophone":      {"base": 78, "bloque": "bone_block",    "es": "Xilófono",         "debajo": "bloque de hueso"},
    "iron_xylophone": {"base": 54, "bloque": "iron_block",    "es": "Vibráfono",        "debajo": "bloque de hierro"},
    "cow_bell":       {"base": 66, "bloque": "soul_sand",     "es": "Cencerro",         "debajo": "arena de almas"},
    "didgeridoo":     {"base": 30, "bloque": "pumpkin",       "es": "Didgeridoo",       "debajo": "calabaza"},
    "bit":            {"base": 54, "bloque": "emerald_block", "es": "Bit (8 bits)",     "debajo": "bloque de esmeralda"},
    "banjo":          {"base": 54, "bloque": "hay_block",     "es": "Banjo",            "debajo": "fardo de heno"},
    "pling":          {"base": 54, "bloque": "glowstone",     "es": "Pling (piano eléctrico)", "debajo": "piedra luminosa"},
    "basedrum":       {"base": None, "bloque": "stone",       "es": "Bombo",            "debajo": "piedra (o cualquier bloque de piedra)"},
    "snare":          {"base": None, "bloque": "sand",        "es": "Caja/redoblante",  "debajo": "arena o grava"},
    "hat":            {"base": None, "bloque": "glass",       "es": "Platillo/hi-hat",  "debajo": "cristal"},
}

ALIAS_INSTRUMENTO = {
    "arpa": "harp", "piano": "harp", "bajo": "bass", "guitarra": "guitar",
    "flauta": "flute", "campana": "bell", "carillon": "chime", "carillón": "chime",
    "xilofono": "xylophone", "xilófono": "xylophone", "vibrafono": "iron_xylophone",
    "vibráfono": "iron_xylophone", "cencerro": "cow_bell", "bit": "bit",
    "banjo": "banjo", "pling": "pling", "didgeridoo": "didgeridoo",
}

PERCUSION = {
    "bombo": "basedrum", "basedrum": "basedrum", "kick": "basedrum",
    "caja": "snare", "redoblante": "snare", "snare": "snare",
    "platillo": "hat", "hihat": "hat", "hat": "hat",
}

# Orden de preferencia para elegir instrumento automáticamente (cubre MIDI 30..102).
AUTO = ["harp", "bass", "bell"]

NOMBRES = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
SOLFEO = {"do": "c", "re": "d", "mi": "e", "fa": "f", "sol": "g", "la": "a", "si": "b"}
NOMBRES_SALIDA = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]

RE_NOTA = re.compile(r"^(do|re|mi|fa|sol|la|si|[a-g])([#b]?)(-?\d)$", re.IGNORECASE)

MAX_PISTAS = 8  # con 2 bloques de separación, la línea de polvo llega con señal >= 1


class ErrorCancion(Exception):
    pass


def nombre_midi(m):
    return f"{NOMBRES_SALIDA[m % 12]}{m // 12 - 1}"


def normalizar_instrumento(nombre):
    n = nombre.lower()
    n = ALIAS_INSTRUMENTO.get(n, n)
    if n not in INSTRUMENTOS:
        raise ErrorCancion(f"Instrumento desconocido: '{nombre}'. Opciones: {', '.join(INSTRUMENTOS)}")
    return n


def parse_nota(txt):
    m = RE_NOTA.match(txt)
    if not m:
        return None
    letra, alter, octava = m.group(1).lower(), m.group(2), int(m.group(3))
    letra = SOLFEO.get(letra, letra)
    semitono = NOMBRES[letra] + (1 if alter == "#" else -1 if alter == "b" else 0)
    return (octava + 1) * 12 + semitono  # C4 = 60


def elegir_instrumento(midi, forzado, por_defecto):
    candidatos = [forzado] if forzado else ([por_defecto] if por_defecto != "auto" else AUTO)
    for inst in candidatos:
        base = INSTRUMENTOS[inst]["base"]
        if base is not None and base <= midi <= base + 24:
            return inst, midi - base
    return None, None


def parse_parte(txt, inst_defecto, transponer_auto, linea):
    """Devuelve dict {instrumento, clics, midi, etiqueta}."""
    inst_forzado = None
    if "@" in txt:
        txt, inst_txt = txt.split("@", 1)
        inst_forzado = normalizar_instrumento(inst_txt)

    # Percusión
    clics_perc = None
    base_perc = txt
    if "=" in txt:
        base_perc, c = txt.split("=", 1)
        if not c.isdigit() or not 0 <= int(c) <= 24:
            raise ErrorCancion(f"Línea {linea}: clics inválidos en '{txt}' (0-24)")
        clics_perc = int(c)
    if base_perc.lower() in PERCUSION:
        inst = PERCUSION[base_perc.lower()]
        return {"instrumento": inst, "clics": clics_perc or 0, "midi": None,
                "etiqueta": INSTRUMENTOS[inst]["es"]}

    midi = parse_nota(txt)
    if midi is None:
        raise ErrorCancion(f"Línea {linea}: no entiendo '{txt}'. Ejemplos válidos: C4, F#3, Bb4, sol4, R, caja")

    inst, clics = elegir_instrumento(midi, inst_forzado, inst_defecto)
    if inst is None and transponer_auto:
        for desplaz in (12, -12, 24, -24, 36, -36):
            inst, clics = elegir_instrumento(midi + desplaz, inst_forzado, inst_defecto)
            if inst is not None:
                midi += desplaz
                break
    if inst is None:
        quien = inst_forzado or inst_defecto
        raise ErrorCancion(
            f"Línea {linea}: {txt} ({nombre_midi(midi)}) está fuera del rango de '{quien}'. "
            f"Usa otra octava, otro @instrumento o --transponer-auto.")
    return {"instrumento": inst, "clics": clics, "midi": midi, "etiqueta": nombre_midi(midi)}


def parse_cancion(texto, inst_defecto, transponer_auto):
    """Devuelve (eventos, duracion_total_pasos). eventos = [(paso, [partes])]."""
    eventos = []
    t = 0.0
    for n_linea, linea in enumerate(texto.splitlines(), 1):
        # Un comentario empieza con '#' al inicio o tras un espacio (F#4 no es comentario)
        linea = re.sub(r"(^|\s)#.*$", "", linea)
        for token in linea.split():
            if token == "|":
                continue
            dur = 1.0
            if ":" in token:
                token, d = token.rsplit(":", 1)
                try:
                    dur = float(d)
                except ValueError:
                    raise ErrorCancion(f"Línea {n_linea}: duración inválida en '{token}:{d}'")
                if dur <= 0:
                    raise ErrorCancion(f"Línea {n_linea}: la duración debe ser mayor que 0")
            if token.upper() in ("R", "-", "SILENCIO"):
                t += dur
                continue
            partes = [parse_parte(p, inst_defecto, transponer_auto, n_linea) for p in token.split("+") if p]
            eventos.append((t, partes))
            t += dur
    if not eventos:
        raise ErrorCancion("La canción no tiene notas.")
    return eventos, t


def a_ticks(pasos, tpp):
    ticks = pasos * tpp
    if abs(ticks - round(ticks)) > 1e-9:
        raise ErrorCancion(
            f"Una duración de {pasos} pasos con {tpp} ticks/paso da {ticks} ticks (no es entero). "
            f"Sube --ticks-por-paso o usa duraciones enteras.")
    return int(round(ticks))


def repartir_retardo(d):
    """Divide d ticks en repetidores de 1-4 ticks (los menos posibles)."""
    n = math.ceil(d / 4)
    base, resto = divmod(d, n)
    return [base + 1] * resto + [base] * (n - resto)


def disenar(eventos, total_pasos, tpp):
    n_pistas = max(len(p) for _, p in eventos)
    if n_pistas > MAX_PISTAS:
        raise ErrorCancion(f"Hay acordes de {n_pistas} notas; el diseño admite hasta {MAX_PISTAS} pistas.")

    pistas = [[] for _ in range(n_pistas)]  # (tick, parte)
    for paso, partes in eventos:
        tick = a_ticks(paso, tpp)
        # La voz más aguda va en la pista 1 (melodía); la percusión al final.
        orden = sorted(partes, key=lambda p: -(p["midi"] if p["midi"] is not None else -1))
        for i, parte in enumerate(orden):
            pistas[i].append((tick, parte))

    diseno = {"ticks_por_paso": tpp, "duracion_ticks": a_ticks(total_pasos, tpp), "pistas": []}
    for i, notas in enumerate(pistas):
        componentes = []  # cada uno ocupa 1 bloque en x, empezando en x=1
        tick_prev = -1    # la palanca cuenta como "tick -1": la primera nota tarda t+1
        for tick, parte in notas:
            for r in repartir_retardo(tick - tick_prev):
                componentes.append({"tipo": "repetidor", "retardo": r})
            componentes.append({"tipo": "nota", "tick": tick, **parte})
            tick_prev = tick
        diseno["pistas"].append({"z": 2 * i, "componentes": componentes})
    diseno["largo"] = 1 + max(len(p["componentes"]) for p in diseno["pistas"])
    return diseno


# ---------------------------------------------------------------------------
# Salidas
# ---------------------------------------------------------------------------
def texto_resumen(d):
    out = []
    n = len(d["pistas"])
    dur_s = d["duracion_ticks"] / 10
    out.append("=== CIRCUITO MUSICAL CON PALANCA ===")
    out.append(f"Pistas: {n}   Largo: {d['largo']} bloques   Ancho: {2 * n - 1} bloques (+1 de la palanca)")
    out.append(f"Duración: {d['duracion_ticks']} ticks de redstone = {dur_s:.1f} s   ({d['ticks_por_paso']:g} ticks por paso)")
    out.append(f"(Para un bucle, la línea de retorno debe sumar exactamente {d['duracion_ticks']} ticks)")
    out.append("")

    # Materiales
    n_notas = sum(1 for p in d["pistas"] for c in p["componentes"] if c["tipo"] == "nota")
    n_rep = sum(1 for p in d["pistas"] for c in p["componentes"] if c["tipo"] == "repetidor")
    bloques = {}
    for p in d["pistas"]:
        for c in p["componentes"]:
            if c["tipo"] == "nota":
                bloques[c["instrumento"]] = bloques.get(c["instrumento"], 0) + 1
    out.append("MATERIALES")
    out.append(f"  {n_notas} bloques musicales (note blocks)")
    out.append(f"  {n_rep} repetidores")
    out.append(f"  {2 * n - 1} polvo de redstone (línea de alimentación)")
    out.append("  1 palanca")
    for inst, cant in bloques.items():
        info = INSTRUMENTOS[inst]
        out.append(f"  {cant} x {info['debajo']}  (debajo de las notas de {info['es']})")
    out.append("")

    # Plano
    out.append("PLANO VISTO DESDE ARRIBA (las señales viajan hacia la derecha = Este, +X)")
    out.append("  L = palanca   | = polvo de redstone   1-4 = repetidor con ese retardo (mirando →)")
    out.append("  N = bloque musical (ver tabla)   . = vacío")
    filas = {-1: ["L"] + ["." for _ in range(d["largo"] - 1)]}
    for z in range(0, 2 * n - 1):
        filas[z] = ["|"] + ["." for _ in range(d["largo"] - 1)]
    for p in d["pistas"]:
        for x, c in enumerate(p["componentes"], start=1):
            filas[p["z"]][x] = str(c["retardo"]) if c["tipo"] == "repetidor" else "N"
    ancho_bloque = 80
    for ini in range(0, d["largo"], ancho_bloque):
        if d["largo"] > ancho_bloque:
            out.append(f"  -- columnas x={ini}..{min(ini + ancho_bloque, d['largo']) - 1} --")
        for z in sorted(filas):
            etiqueta = "palanca" if z == -1 else (f"pista {z // 2 + 1}" if z % 2 == 0 else "")
            out.append(f"  {etiqueta:>8} z={z:<3}" + "".join(filas[z][ini:ini + ancho_bloque]))
    out.append("")

    # Tabla de afinación
    out.append("TABLA DE NOTAS (clic derecho = +1 clic; tras 24 vuelve a 0)")
    for i, p in enumerate(d["pistas"], 1):
        out.append(f"  Pista {i} (z={p['z']}):")
        for x, c in enumerate(p["componentes"], start=1):
            if c["tipo"] == "nota":
                info = INSTRUMENTOS[c["instrumento"]]
                out.append(f"    x={x:<4} {c['etiqueta']:<16} {c['clics']:>2} clics   "
                           f"{info['es']} -> debajo: {info['debajo']}   (suena en el tick {c['tick'] + 1})")
    out.append("")
    out.append("RECUERDA: deja AIRE encima de cada bloque musical, o no sonará.")
    out.append("Para volver a tocarla: apaga la palanca, espera a que termine y enciéndela otra vez.")
    return "\n".join(out)


def comandos_java(d, origen):
    """Comandos /fill y /setblock para Minecraft Java 1.13+ (formato .mcfunction).

    Coordenadas relativas a 'origen' (por defecto ~ ~ ~, es decir, quien ejecuta
    la función). El suelo se coloca en y+0 y los componentes en y+1.
    """
    ox, oy, oz = origen

    def pos(x, y, z):
        if ox is None:
            return f"~{x} ~{y} ~{z}"
        return f"{ox + x} {oy + y} {oz + z}"

    n = len(d["pistas"])
    zmax = 2 * (n - 1)
    largo = d["largo"]
    cmds = ["# Generado por cancion_a_redstone.py — circuito musical con palanca",
            f"# {n} pistas, {largo} bloques de largo, {d['duracion_ticks']} ticks"]
    # Limpiar espacio y poner suelo, en trozos para no pasar el límite de /fill (32768 bloques)
    for x0 in range(0, largo, 64):
        x1 = min(x0 + 63, largo - 1)
        cmds.append(f"fill {pos(x0, 1, -1)} {pos(x1, 3, zmax)} air")
        cmds.append(f"fill {pos(x0, 0, -1)} {pos(x1, 0, zmax)} smooth_stone")
    # Bloques de instrumento y notas
    for p in d["pistas"]:
        z = p["z"]
        for x, c in enumerate(p["componentes"], start=1):
            if c["tipo"] == "nota":
                bloque = INSTRUMENTOS[c["instrumento"]]["bloque"]
                if bloque in ("sand", "gravel"):
                    cmds.append(f"setblock {pos(x, -1, z)} stone")  # la arena necesita apoyo
                cmds.append(f"setblock {pos(x, 0, z)} {bloque}")
                cmds.append(f"setblock {pos(x, 1, z)} note_block[instrument={c['instrumento']},note={c['clics']}]")
    # Repetidores: facing=west -> entrada por el oeste, salida hacia el este (+X)
    for p in d["pistas"]:
        z = p["z"]
        for x, c in enumerate(p["componentes"], start=1):
            if c["tipo"] == "repetidor":
                cmds.append(f"setblock {pos(x, 1, z)} repeater[facing=west,delay={c['retardo']}]")
    # Línea de alimentación (polvo) en x=0 con conexiones explícitas
    for z in range(0, zmax + 1):
        norte = "side"  # z=0 conecta con la palanca
        sur = "side" if z < zmax else "none"
        este = "side" if z % 2 == 0 else "none"
        cmds.append(f"setblock {pos(0, 1, z)} redstone_wire[north={norte},south={sur},east={este},west=none]")
    cmds.append(f"setblock {pos(0, 1, -1)} lever[face=floor,facing=east]")
    return cmds


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convierte una canción en un circuito de bloques musicales con palanca.")
    ap.add_argument("archivo", nargs="?", help="archivo de texto con la canción")
    ap.add_argument("-c", "--cancion", help="la canción directamente como texto")
    ap.add_argument("-t", "--ticks-por-paso", type=float, default=2,
                    help="ticks de redstone por paso (1 tick = 0,1 s). Por defecto 2")
    ap.add_argument("-i", "--instrumento", default="auto",
                    help="instrumento por defecto (auto, harp, bass, flute, bell...). Por defecto auto")
    ap.add_argument("--transponer-auto", action="store_true",
                    help="sube/baja octavas las notas que no caben en el instrumento")
    ap.add_argument("--mcfunction", help="guarda comandos de Minecraft Java en este archivo")
    ap.add_argument("--origen", help="coordenadas absolutas X,Y,Z del suelo bajo la palanca+1 en Z (por defecto relativas ~ ~ ~)")
    ap.add_argument("--json", help="guarda el diseño completo en JSON")
    ap.add_argument("-q", "--silencioso", action="store_true", help="no imprime el resumen")
    a = ap.parse_args(argv)

    if a.cancion:
        texto = a.cancion
    elif a.archivo:
        with open(a.archivo, encoding="utf-8") as f:
            texto = f.read()
    else:
        ap.error("indica un archivo o --cancion")

    try:
        inst = a.instrumento if a.instrumento == "auto" else normalizar_instrumento(a.instrumento)
        if inst != "auto" and INSTRUMENTOS[inst]["base"] is None:
            raise ErrorCancion("El instrumento por defecto no puede ser de percusión.")
        tpp = a.ticks_por_paso
        if tpp <= 0:
            raise ErrorCancion("--ticks-por-paso debe ser mayor que 0")
        eventos, total = parse_cancion(texto, inst, a.transponer_auto)
        d = disenar(eventos, total, tpp)
    except ErrorCancion as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    origen = (None, None, None)
    if a.origen:
        try:
            origen = tuple(int(v) for v in a.origen.split(","))
            assert len(origen) == 3
        except (ValueError, AssertionError):
            print("ERROR: --origen debe ser X,Y,Z (enteros)", file=sys.stderr)
            return 1

    if not a.silencioso:
        print(texto_resumen(d))
    if a.mcfunction:
        cmds = comandos_java(d, origen)
        with open(a.mcfunction, "w", encoding="utf-8") as f:
            f.write("\n".join(cmds) + "\n")
        print(f"\n{len(cmds) - 2} comandos guardados en {a.mcfunction}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Diseño guardado en {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
