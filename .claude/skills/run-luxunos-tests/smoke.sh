#!/usr/bin/env bash
# CLI smoke test for skills/minecraft-redstone/scripts/cancion_a_redstone.py.
# Runs representative invocations, checks exit codes and key output lines.
# Usage (from repo root):  bash .claude/skills/run-luxunos-tests/smoke.sh [outdir]
set -u
cd "$(dirname "$0")/../../.." || exit 1
S=skills/minecraft-redstone/scripts/cancion_a_redstone.py
OUT=${1:-/tmp/redstone-smoke}
mkdir -p "$OUT"
fail=0
check() { # name, expected-exit, grep-pattern, command...
  local name=$1 want=$2 pat=$3; shift 3
  local log="$OUT/$name.log"
  "$@" >"$log" 2>&1; local got=$?
  if [ "$got" -ne "$want" ]; then echo "FAIL $name: exit $got (want $want) - see $log"; fail=1; return; fi
  if ! grep -q -- "$pat" "$log"; then echo "FAIL $name: missing '$pat' - see $log"; fail=1; return; fi
  echo "ok   $name"
}

check example-song 0 "30 bloques musicales" \
  python3 $S skills/minecraft-redstone/assets/himno-de-la-alegria.txt
check chord-perc-solfege 0 "Pistas: 3" \
  python3 $S -c "C4+E4+G4:2 R sol#4@flute caja bombo=3 Bb2 do6:1.5 fa#3"
check mcfunction 0 "comandos guardados" \
  python3 $S -c "E4 E4 F4 G4" --mcfunction "$OUT/musica.mcfunction" --json "$OUT/diseno.json"
check mcfunction-content 0 "repeater\[facing=west,delay=1\]" cat "$OUT/musica.mcfunction"
check out-of-range 1 "fuera del rango" python3 $S -c "C9"
check transpose 0 "Do7 .*Campana" python3 $S -c "C9" --transponer-auto
check bad-duration 1 "no es entero" python3 $S -c "C4:0.3"

[ $fail -eq 0 ] && echo "ALL OK (logs in $OUT)" || { echo "SMOKE FAILED"; exit 1; }
