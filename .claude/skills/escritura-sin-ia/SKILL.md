---
name: escritura-sin-ia
description: >-
  Escribe y reescribe textos sin los patrones típicos de la escritura de IA catalogados por Wikipedia (WP:Signs of AI writing): vocabulario de IA (crucial, fundamental, tapiz, profundizar, delve, underscore, showcase), "no solo X sino Y", regla de tres, gerundios de análisis superficial ("destacando su importancia"), inflar la relevancia, atribuciones vagas ("los expertos señalan"), rayas/em dashes, negritas y listas de más, emojis en títulos, cierres tipo "En resumen" o "¿Querés que...?". Usala siempre que el usuario pida redactar, reescribir, corregir o "humanizar" un texto (artículo, post, mail, ensayo, bio, descripción, README, comentario), que diga que algo "suena a ChatGPT/IA/robot", que pida "escribir natural" o "sin que parezca IA", o que pegue un texto para revisar su estilo, aunque no mencione Wikipedia ni la IA.
---

# Escritura sin patrones de IA

Esta skill se basa en la página de Wikipedia **"Signs of AI writing"** (WikiProject AI Cleanup), leída completa en noviembre de 2026. Esa página junta los rasgos que delatan un texto generado por chatbots. Acá se usan al revés: como lista de cosas que no hay que escribir.

La idea de fondo, según la propia página: los modelos tienden a la media estadística. Cambian el dato raro y concreto ("inventor del primer enganche de vagones") por una frase genérica y elogiosa ("un titán revolucionario de la industria"). El texto queda a la vez más vago y más exagerado. Casi todos los patrones de abajo son síntomas de eso. Por eso el arreglo real casi nunca es cambiar una palabra por un sinónimo: es poner el dato concreto o borrar la frase.

## Cómo trabajar

1. **Escribí primero el contenido, después el estilo.** Juntá los hechos concretos (nombres, fechas, cifras, qué pasó). Si no tenés un dato, no lo rellenes con generalidades ni con avisos sobre su falta: preguntalo o dejalo afuera.
2. **Redactá evitando los patrones de la tabla.** El detalle de cada uno, con ejemplos en inglés y español, está en `references/patrones.md`. Leelo la primera vez que uses la skill en una conversación, o cuando dudes sobre un caso.
3. **Pasá el revisor automático** sobre el borrador:
   ```bash
   python scripts/revisar.py borrador.txt
   ```
   (También acepta texto por stdin.) Marca palabras y construcciones sospechosas con número de línea. No es infalible: hay falsos positivos ("subrayar" una palabra en sentido literal) y patrones que no puede detectar (vaguedad, análisis superficial). Usalo como checklist, no como juez.
4. **Releé en voz alta mentalmente.** ¿Una persona que sabe del tema lo diría así? ¿Cada oración dice algo que la anterior no dijo?
5. Entregá el texto final limpio. No le agregues al usuario un resumen de "qué patrones evité" salvo que lo pida.

## Los patrones a evitar (resumen)

| # | Patrón | En vez de eso |
|---|--------|---------------|
| 1 | **Inflar la importancia**: "desempeña un papel crucial", "es un testimonio de", "marca un hito", "refleja tendencias más amplias", "deja una huella imborrable" | Decí qué hizo, cuándo y con qué resultado medible. Si no tiene importancia especial, no se la inventes. |
| 2 | **Insistir en la notoriedad o la cobertura**: "ha sido destacado en medios nacionales", "cuenta con cobertura independiente" | Contá qué dijeron esas fuentes, no que existen. |
| 3 | **"Según X, Y figura como..."**: énfasis en que una base de datos o web "identifica/lista/describe" algo | Decí el hecho directamente y citá la fuente al costado. |
| 4 | **"Mantiene una sólida presencia en redes"** | Omitilo, o da el dato concreto si importa. |
| 5 | **Análisis superficial con gerundio** al final de la oración: "..., destacando su compromiso con la calidad", "..., lo que refleja...", "contribuyendo a..." | Cortá la oración en el hecho. Si el análisis importa, argumentalo con datos y atribuilo. |
| 6 | **Conexiones vagas**: "vinculado a", "asociado con", "en relación con" | Decí la relación exacta: "fue director de", "enseñó química en". |
| 7 | **Atribuciones vagas**: "los expertos señalan", "algunos críticos sostienen", "diversas fuentes", "como por ejemplo" ante una lista completa | Nombrá a quién lo dijo. Si es uno solo, decí que es uno. |
| 8 | **Cierre formulaico de "desafíos y perspectivas"**: "A pesar de sus logros, enfrenta desafíos...", secciones "Desafíos y legado", "Perspectivas futuras" | Mencioná problemas concretos donde corresponden, sin fórmula ni final optimista. |
| 9 | **Títulos "X y Y"**, sobre todo "Premios y reconocimientos" | Un título simple y concreto, o ninguno. |
| 10 | **Vocabulario de IA** (ver lista en `references/patrones.md`): crucial, fundamental, clave, profundizar, panorama, tapiz, vibrante, robusto, meticuloso, fomentar, potenciar, resaltar, subrayar, multifacético, aprovechar... | La palabra común: "importante" si hace falta, "tiene", "usa", "muestra", o nada. |
| 11 | **Evitar "es/tiene"**: "sirve como", "se erige como", "funciona como", "cuenta con", "ofrece", "se refiere a" | Usá "es" y "tiene" sin miedo. |
| 12 | **Paralelismos negativos**: "no solo X, sino también Y", "no es X, es Y", "en lugar de X, Y", "no..., no..., solo..." | Afirmá lo que es. Sin contraste fabricado contra una idea que nadie dijo. |
| 13 | **Regla de tres**: tríadas de adjetivos o frases ("rápido, seguro y eficiente") | Usá la cantidad de elementos que el contenido tenga: uno, dos, cuatro. |
| 14 | **Variación elegante**: cambiar de sinónimo cada vez para no repetir ("la empresa... la compañía... la firma... la organización") | Repetí la palabra correcta. La repetición clara es mejor que el sinónimo forzado. |
| 15 | **Formato de chatbot**: Título En Mayúsculas Iniciales, **negritas** en medio de la prosa, listas con "**Encabezado:** texto", emojis en títulos o viñetas, comillas curvas “ ” cuando el resto usa rectas, Markdown donde no corresponde | Prosa corrida. Mayúscula solo en la primera palabra del título. Listas solo cuando el contenido es de verdad una lista. |
| 16 | **Hablarle al usuario dentro del texto**: "¡Claro!", "¡Por supuesto!", "Espero que esto te sirva", "¿Querés que...?", "aquí tenés un...", "revisalo antes de publicar" | El texto empieza con el contenido y termina con el contenido. |
| 17 | **Avisos de falta de información**: "si bien los detalles son escasos", "no hay información pública disponible", "mantiene un perfil bajo", "esto no establece por sí solo...", "debe tomarse como... más que como...", "no debe confundirse con..." | Si no sabés algo, no lo escribas. Nada de especular sobre lo que "probablemente" sea. |
| 18 | **"Es importante señalar/destacar"** y consejos didácticos no pedidos | Decilo y listo, o borralo. |
| 19 | **Plantillas sin completar**: "[Nombre]", "[Año]", "2026-XX-XX", example.com, INSERT_URL | Nunca dejes huecos. Preguntá el dato. |
| 20 | **Citas inventadas o vagas**: URLs que no verificaste, DOI/ISBN dudosos, libros sin página, `utm_source=chatgpt.com` | Citá solo lo que verificaste, con página o enlace. Limpiá parámetros de rastreo. |
| 21 | **Resúmenes al final**: "En resumen", "En conclusión", "En definitiva", "En síntesis" | Terminá cuando terminaste. |
| 22 | **Rayas (—) de más**, sobre todo con espacios alrededor y para dar énfasis "publicitario" | Coma, paréntesis o dos puntos. Una raya ocasional está bien si el idioma la pide (diálogos o incisos en español), pero no como muletilla. |
| 23 | **Ritmo monótono**: todas las oraciones de 8 a 20 palabras, solo comas y puntos (la página lo marca como señal de los modelos de 2026, que dejaron la raya y quedaron planos) | Variá: alguna oración corta, alguna larga, un punto y coma, un paréntesis, una pregunta si viene al caso. |
| 24 | **Tono publicitario o de folleto turístico**: "enclavado en el corazón de", "rica herencia cultural", "impresionante", "de vanguardia", "innovador", "una amplia gama de" | Neutral y concreto. |
| 25 | **Disculpas y frases de atención al cliente**: "lamento cualquier inconveniente", "revisé cuidadosamente", "si hay algún problema específico, indicámelo" | Directo. |
| 26 | **Referencias al propio corte de conocimiento o a ser IA**: "según mi última actualización", "como modelo de lenguaje" | Nunca. |
| 27 | **Resúmenes de cambios procedimentales**: "mejoré la claridad, la fluidez y el tono, preservando el significado original" | Decí qué cambiaste en concreto ("saqué el párrafo de premios, corregí la fecha de fundación"). |

## Lo que la página dice que SÍ es humano

Wikipedia observó que estos rasgos son más comunes en textos escritos por personas. Usalos con naturalidad:

- Frases simples con "es", "hay", "tiene".
- La palabra corta en vez de la rebuscada: "escribió" (no "redactó"), "se mudó" (no "se trasladó/reubicó"), "usó" (no "utilizó"), "intentó" (no "procuró"), "murió" (no "falleció").
- Afirmaciones definitivas cuando son verdad: "fue el primero", "es el único".
- Matices e intensificadores comunes: "muy", "quizás", "suele".
- Alguna construcción algo larga ("como resultado de", "el hecho de que") sin obsesionarse.

## Equilibrio

El objetivo es buena escritura, no un texto que esquive una lista. La propia página advierte que tratar los síntomas sin arreglar el fondo solo esconde el problema: si un párrafo es vago, cambiarle "crucial" por "importante" no lo mejora. Y advierte también que evitar algo de forma mecánica crea un patrón nuevo (los modelos que eliminaron la raya ahora abusan de comas y puntos). Entonces:

- No reemplaces cada palabra prohibida por el mismo sinónimo de siempre. Reformulá.
- Si el usuario pide explícitamente un formato (lista, negritas, tres puntos, un título concreto), respetalo: la skill gobierna el estilo por defecto, no anula pedidos expresos.
- Las palabras de la lista están bien en su sentido literal ("el paisaje del valle", "subrayar con lápiz", "una clave de acceso").
- Adaptá el registro al usuario (voseo rioplatense si escribe así, tuteo, usted) y al género del texto: un mail informal no se escribe como un artículo.
