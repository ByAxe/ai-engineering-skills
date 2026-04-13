#!/usr/bin/env bash
set -euo pipefail

PACKAGES="${1:-./...}"
STATUS=0

if [[ ! -f go.mod ]]; then
  echo "No go.mod found in current directory. Run this from a Go module root." >&2
  exit 2
fi

echo "==> Formatting check (gofmt)"
mapfile -t GOFILES < <(find . -type f -name '*.go'   -not -path './vendor/*'   -not -path './.git/*'   -not -path './node_modules/*')

if ((${#GOFILES[@]} > 0)); then
  UNFORMATTED="$(gofmt -l "${GOFILES[@]}")"
  if [[ -n "${UNFORMATTED}" ]]; then
    echo "Unformatted files:" >&2
    echo "${UNFORMATTED}" >&2
    echo "Run: gofmt -w <files>" >&2
    STATUS=1
  fi
else
  echo "No Go files found."
fi

echo "==> go test ${PACKAGES}"
if ! go test ${PACKAGES}; then
  STATUS=1
fi

if [[ "${GO_SMELLS_ENABLE_RACE:-1}" == "1" ]]; then
  echo "==> go test -race ${PACKAGES}"
  if ! go test -race ${PACKAGES}; then
    echo "Race detector failed or is unsupported on this platform/toolchain." >&2
    STATUS=1
  fi
fi

echo "==> go vet ${PACKAGES}"
if ! go vet ${PACKAGES}; then
  STATUS=1
fi

if command -v staticcheck >/dev/null 2>&1; then
  echo "==> staticcheck ${PACKAGES}"
  if ! staticcheck ${PACKAGES}; then
    STATUS=1
  fi
else
  echo "==> staticcheck not installed; skipping"
fi

if command -v golangci-lint >/dev/null 2>&1; then
  echo "==> golangci-lint run"
  if ! golangci-lint run; then
    STATUS=1
  fi
else
  echo "==> golangci-lint not installed; skipping"
fi

if [[ "${GO_SMELLS_ENABLE_COVER:-0}" == "1" ]]; then
  echo "==> go test -cover ${PACKAGES}"
  if ! go test -cover ${PACKAGES}; then
    STATUS=1
  fi
fi

exit ${STATUS}
