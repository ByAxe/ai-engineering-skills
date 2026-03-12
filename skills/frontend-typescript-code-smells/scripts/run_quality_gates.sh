#!/usr/bin/env bash
set -euo pipefail

# Run common frontend quality gates if they exist.
# Intended usage: run from repository root.
#
# This script is intentionally defensive:
# - It only runs scripts that exist in package.json
# - It provides reasonable fallbacks for typecheck and build where possible

if [[ ! -f "package.json" ]]; then
  echo "run_quality_gates.sh: package.json not found. Run this from a Node/TypeScript project root."
  exit 1
fi

has_script () {
  node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$1'] ? 0 : 1)"
}

run_script () {
  local name="$1"
  echo ""
  echo "==> npm run $name"
  npm run -s "$name"
}

# Lint
if has_script "lint"; then
  run_script "lint"
else
  echo "==> Skipping lint (no script named 'lint')"
fi

# Typecheck
if has_script "typecheck"; then
  run_script "typecheck"
else
  if [[ -f "tsconfig.json" ]]; then
    echo ""
    echo "==> npx tsc --noEmit (fallback typecheck)"
    npx -y tsc --noEmit
  else
    echo "==> Skipping typecheck (no typecheck script and no tsconfig.json)"
  fi
fi

# Unit tests
if has_script "test"; then
  run_script "test"
else
  echo "==> Skipping tests (no script named 'test')"
fi

# Build
if has_script "build"; then
  run_script "build"
else
  echo "==> Skipping build (no script named 'build')"
fi

echo ""
echo "All requested quality gates completed."
