#!/usr/bin/env bash
set -euo pipefail

BENCH_PATTERN="${1:-.}"
PACKAGES="${2:-./...}"
OUTDIR="${3:-profiles}"
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${OUTDIR}"
CPU="${OUTDIR}/cpu-${TS}.out"
MEM="${OUTDIR}/mem-${TS}.out"
BENCHTXT="${OUTDIR}/bench-${TS}.txt"

cat <<EOF
Running benchmark profile capture:
  pattern: ${BENCH_PATTERN}
  packages: ${PACKAGES}
  outdir: ${OUTDIR}
EOF

go test -run '^$' -bench "${BENCH_PATTERN}" -benchmem -count=5   -cpuprofile "${CPU}" -memprofile "${MEM}" ${PACKAGES} | tee "${BENCHTXT}"

cat <<EOF

Artifacts:
  benchmark output: ${BENCHTXT}
  CPU profile:      ${CPU}
  memory profile:   ${MEM}

Inspect with:
  go tool pprof ${CPU}
  go tool pprof -http=:0 ${CPU}
  go tool pprof ${MEM}
EOF
