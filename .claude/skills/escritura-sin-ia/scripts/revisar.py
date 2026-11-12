#!/usr/bin/env python3
"""Revisor de patrones de escritura de IA (basado en Wikipedia: Signs of AI writing).

Uso:
    python revisar.py archivo.txt
    cat archivo.txt | python revisar.py

Marca palabras y construcciones sospechosas con su línea. Sale con código 1 si
encuentra algo. Es una ayuda: hay falsos positivos (sentido literal) y
patrones de fondo (vaguedad) que no puede detectar.
"""
import re
import sys
import unicodedata

# (categoría, lista de expresiones regulares). Se buscan sin distinguir mayúsculas.
PATRONES = [
    ("Vocabulario de IA", [
        r"\bdelv(e|es|ed|ing)\b", r"\btapestr(y|ies)\b", r"\btestament\b", r"\bpivotal\b",
        r"\bcrucial\b", r"\bunderscor(e|es|ed|ing)\b", r"\bshowcas(e|es|ed|ing)\b",
        r"\bhighlight(s|ed|ing)?\b", r"\bfoster(s|ed|ing)?\b", r"\benhanc(e|es|ed|ing)\b",
        r"\bvibrant\b", r"\bmeticulous(ly)?\b", r"\bintricac(y|ies)\b", r"\bintricate\b",
        r"\binterplay\b", r"\bgarner(s|ed|ing)?\b", r"\bbolster(s|ed|ing)?\b", r"\brobust\b",
        r"\bboasts?\b", r"\bdeep dive\b", r"\blandscape\b", r"\bmultifaceted\b",
        r"\bleverag(e|es|ed|ing)\b", r"\balign(s|ed)? with\b", r"\benduring\b",
        r"^\s*additionally\b",
        r"\bcabe (destacar|se[ñn]alar|mencionar)\b", r"\bfundamental(es)?\b",
        r"\bclave\b", r"\bprofundiz(ar|a|amos|ando)\b", r"\badentr(arse|amos|ándonos)\b",
        r"\bsumerg(irse|imos|iéndonos)\b", r"\bpanorama\b", r"\btapiz\b", r"\bentramado\b",
        r"\btestimonio\b", r"\bvibrantes?\b", r"\brobust[oa]s?\b", r"\bmeticulos[oa]s?\b",
        r"\bminucios[oa]s?\b", r"\bintrincad[oa]s?\b", r"\bfoment(ar|a|an|ando|ó|ado|ada)\b",
        r"\bpotenci(ar|a|an|ando|ó|ado|ada)\b", r"\bresalt(ar|a|an|ando|ó|ado|ada)\b",
        r"\bsubray(ar|a|an|ando|ó|ado|ada)\b", r"\bponiendo de relieve\b", r"\bpone de relieve\b",
        r"\bmultifac[eé]tic[oa]s?\b", r"\bsin lugar a dudas\b", r"\ben el mundo actual\b",
        r"\ben la era digital\b", r"\ben constante evoluci[oó]n\b", r"\bun sinf[ií]n de\b",
        r"\buna amplia gama\b", r"\bde vanguardia\b", r"\bsinergias?\b", r"\bhol[ií]stic[oa]\b",
        r"^\s*además\b",
    ]),
    ("Inflar la importancia", [
        r"\b(serves|stands) as\b", r"\bis a (testament|reminder)\b",
        r"\b(crucial|pivotal|vital|significant|key) (role|moment)\b", r"\breflects broader\b",
        r"\bsetting the stage\b", r"\bindelible mark\b", r"\bdeeply rooted\b",
        r"\bevolving landscape\b", r"\bturning point\b", r"\bfocal point\b",
        r"\bpapel (crucial|fundamental|clave|vital|esencial|importante|destacado)\b",
        r"\b(marca|marcó|marcando) un (hito|antes y un después)\b",
        r"\bsent(ar|ó|ando) las bases\b", r"\bhuella imborrable\b",
        r"\bprofundamente arraigad[oa]\b", r"\bpunto de inflexi[oó]n\b",
        r"\btendencias más amplias\b", r"\bes un recordatorio\b",
        r"\b(esta|la) distinci[oó]n (importa|es importante)\b",
    ]),
    ("Evitar 'es/tiene'", [
        r"\bse erige como\b", r"\bsirve como\b", r"\bfunciona como\b", r"\bopera como\b",
        r"\bcuenta con\b", r"\bostenta\b", r"\bse refiere a\b",
    ]),
    ("Análisis superficial / gerundio final", [
        r"[,—–]\s*(destacando|subrayando|resaltando|reflejando|simbolizando|contribuyendo|"
        r"fomentando|garantizando|asegurando|consolidando|evidenciando|demostrando)\b",
        r",\s*lo que (refleja|demuestra|subraya|evidencia|pone de manifiesto)\b",
        r",\s*(highlighting|underscoring|emphasizing|reflecting|symbolizing|contributing|"
        r"ensuring|fostering|showcasing)\b",
        r"\bvaluable insights\b", r"\bvaliosas? (perspectivas?|aportes?)\b",
    ]),
    ("Conexión vaga", [
        r"\b(vinculad|asociad|ligad)[oa]s? (a|con)\b", r"\ben relaci[oó]n con\b",
        r"\b(associated|connected) (with|to)\b", r"\bin connection with\b",
    ]),
    ("Atribución vaga", [
        r"\b(los|algunos|muchos) (expertos|analistas|críticos|especialistas|observadores)\b",
        r"\b(diversas|varias|numerosas) fuentes\b", r"\bse ha (señalado|destacado)\b",
        r"\b(experts|observers|critics) (argue|say|have cited|note)\b",
        r"\bindustry reports\b", r"\bcomo por ejemplo\b",
    ]),
    ("Paralelismo negativo", [
        r"\bno (solo|sólo|solamente|únicamente)\b.{0,80}\bsino\b",
        r"\bno es (solo|sólo|simplemente)?\s*\w+.{0,40}[,;]\s*es\b",
        r"\ben lugar de\b", r"\bmás que\b.{0,40}\bes\b",
        r"\bnot (only|just)\b.{0,80}\bbut\b", r"\bit'?s not\b.{0,40}\bit'?s\b",
        r"\brather than\b",
    ]),
    ("Desafíos y perspectivas", [
        r"\ba pesar de (sus|estos|estas)\b.{0,60}\b(desaf[ií]os|retos)\b",
        r"\bperspectivas futuras\b", r"\bdesaf[ií]os y legado\b",
        r"\bdespite (its|these)\b.{0,60}\bchallenges\b", r"\bfuture (outlook|prospects)\b",
        r"\bpremios y reconocimientos\b", r"\bawards and recognition\b",
    ]),
    ("Hablarle al usuario", [
        r"¡\s*(claro|por supuesto|excelente pregunta|buena pregunta)", r"\bespero que (esto|te)\b",
        r"¿\s*(quer[eé]s|te gustar[ií]a|deseas|quieres) que\b", r"\bno dudes en\b",
        r"\bav[ií]same si\b", r"\ba continuaci[oó]n te (presento|dejo)\b",
        r"\baqu[ií] (ten[eé]s|tienes)\b", r"\bI hope this helps\b", r"\bcertainly!",
        r"\bof course!", r"\bwould you like\b", r"\blet me know\b",
        r"\byou'?re absolutely right\b", r"\bhere is a\b",
    ]),
    ("Avisos / didactismo", [
        r"\bes importante (señalar|destacar|tener en cuenta|mencionar|recordar)\b",
        r"\bdetalles\b.{0,40}\b(son|resultan|siguen siendo) (escasos|limitados)\b",
        r"\b(escasa|limitada) informaci[oó]n\b", r"\bno (está|es) ampliamente\b",
        r"\binformaci[oó]n (p[uú]blica )?disponible\b", r"\bperfil bajo\b",
        r"\bno establece por s[ií] (solo|sola|mism[oa])\b", r"\bno debe confundirse\b",
        r"\bit'?s important to note\b", r"\bspecific details are (limited|scarce)\b",
        r"\bnot widely (available|documented)\b", r"\bbased on available information\b",
        r"\bmaintains? a low profile\b",
    ]),
    ("Cierre de resumen", [
        r"\ben (resumen|conclusi[oó]n|definitiva|s[ií]ntesis|pocas palabras)\b",
        r"\bin (summary|conclusion)\b", r"^\s*overall\b",
    ]),
    ("Tono promocional", [
        r"\benclavad[oa]\b", r"\ben el coraz[oó]n de\b", r"\bimpresionantes?\b",
        r"\brica (herencia|historia|tradici[oó]n)\b", r"\binnovador(a|es)?\b",
        r"\brevolucionari[oa]s?\b", r"\bde renombre\b", r"\bbelleza natural\b",
        r"\bnestled\b", r"\bin the heart of\b", r"\bgroundbreaking\b", r"\brenowned\b",
        r"\bdiverse array\b", r"\bcommitment to\b",
        r"\bpresencia (digital|en redes)\b", r"\bsocial media presence\b",
    ]),
    ("Atención al cliente / IA", [
        r"\blamento (cualquier|las molestias)\b", r"\brevis[eé] cuidadosamente\b",
        r"\bcomo (modelo de lenguaje|IA)\b", r"\bmi [uú]ltima actualizaci[oó]n\b",
        r"\bas an AI\b", r"\bmy last (knowledge|training) update\b",
    ]),
    ("Resumen de cambios genérico", [
        r"\b(mejor[eé]|mejorando) (la )?(claridad|fluidez|legibilidad)\b",
        r"\bpreservando el (significado|sentido)\b", r"\btono (m[aá]s )?(neutral|enciclop[eé]dico)\b",
        r"\bimproved clarity\b", r"\bwhile preserving\b",
    ]),
    ("Plantillas sin completar / restos", [
        r"\[(nombre|año|fecha|empresa|name|year|insert)[^\]]*\]", r"\b20\d\d-(xx|XX)-(xx|XX)\b",
        r"example\.com/", r"INSERT_\w+", r"utm_source=(chatgpt|openai|copilot)",
        r"referrer=grok", r"contentReference\[", r"oaicite", r"↩",
    ]),
]

RAYA = "—"
COMILLAS_CURVAS = "“”‘’"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✨]")


def revisar(texto):
    hallazgos = []
    lineas = texto.splitlines()
    for n, linea in enumerate(lineas, 1):
        for cat, regs in PATRONES:
            for r in regs:
                for m in re.finditer(r, linea, re.IGNORECASE | re.MULTILINE):
                    hallazgos.append((n, cat, m.group(0).strip()))
        if RAYA in linea:
            hallazgos.append((n, "Raya (—)", f"{linea.count(RAYA)} raya(s)"))
        if any(c in linea for c in COMILLAS_CURVAS):
            hallazgos.append((n, "Comillas curvas", "“ ” ‘ ’"))
        if re.search(r"\*\*[^*]+\*\*", linea) and not linea.lstrip().startswith(("#", "|")):
            hallazgos.append((n, "Negritas en prosa/lista", re.search(r"\*\*[^*]+\*\*", linea).group(0)))
        if linea.lstrip().startswith("#") or (linea.lstrip()[:1] in "-*•" and EMOJI.search(linea)):
            if EMOJI.search(linea):
                hallazgos.append((n, "Emoji en título/viñeta", linea.strip()[:40]))
        m = re.match(r"\s*#+\s+(.*)", linea)
        if m:
            palabras = [p for p in m.group(1).split() if p.isalpha() and len(p) > 3]
            if len(palabras) >= 3 and all(p[0].isupper() for p in palabras):
                hallazgos.append((n, "Título en Mayúsculas Iniciales", m.group(1)[:50]))
        # Regla de tres: "a, b y c" con elementos cortos
        for t in re.finditer(r"\b(\w+(?: \w+)?), (\w+(?: \w+)?),? (y|e|and) (\w+(?: \w+)?)\b", linea):
            hallazgos.append((n, "Posible regla de tres", t.group(0)))

    # Ritmo: largo de oraciones
    oraciones = [o for o in re.split(r"(?<=[.!?])\s+", texto.replace("\n", " ")) if len(o.split()) > 2]
    if len(oraciones) >= 6:
        largos = [len(o.split()) for o in oraciones]
        en_rango = sum(1 for l in largos if 8 <= l <= 20) / len(largos)
        if en_rango > 0.85:
            hallazgos.append((0, "Ritmo monótono",
                              f"{en_rango:.0%} de las oraciones tienen 8-20 palabras; variá el largo"))
    return hallazgos


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            texto = f.read()
    else:
        texto = sys.stdin.read()
    texto = unicodedata.normalize("NFC", texto)
    hallazgos = revisar(texto)
    if not hallazgos:
        print("Sin patrones detectados. (Igual releé por vaguedad e importancia inflada.)")
        return 0
    por_cat = {}
    for n, cat, frag in hallazgos:
        por_cat.setdefault(cat, []).append((n, frag))
    print(f"{len(hallazgos)} posibles patrones de IA:\n")
    for cat, items in por_cat.items():
        print(f"[{cat}] ({len(items)})")
        for n, frag in items:
            donde = f"línea {n}" if n else "texto"
            print(f"  {donde}: {frag}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
