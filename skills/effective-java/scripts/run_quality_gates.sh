#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: run_quality_gates.sh [options] [-- extra build arguments]

Options:
  --root PATH              Project root (default: .)
  --mode MODE              compile|test|verify|native (default: verify)
  --build TOOL             auto|maven|gradle (default: auto)
  --project NAME           Maven -pl/-am project or Gradle project path
  --dry-run                Print commands without executing
  --allow-system-tool      Permit mvn/gradle when no wrapper exists
  --no-daemon              Add --no-daemon to Gradle
  -h, --help               Show this help

The script is wrapper-first and non-installing. Native commands are conservative
Quarkus defaults; inspect the project's configured native task/profile first.
EOF
}

root="."
mode="verify"
build="auto"
project=""
dry_run=false
allow_system=false
no_daemon=false
extra=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      [[ $# -ge 2 ]] || { echo "error: --root requires a value" >&2; exit 2; }
      root="$2"; shift 2 ;;
    --mode)
      [[ $# -ge 2 ]] || { echo "error: --mode requires a value" >&2; exit 2; }
      mode="$2"; shift 2 ;;
    --build)
      [[ $# -ge 2 ]] || { echo "error: --build requires a value" >&2; exit 2; }
      build="$2"; shift 2 ;;
    --project)
      [[ $# -ge 2 ]] || { echo "error: --project requires a value" >&2; exit 2; }
      project="$2"; shift 2 ;;
    --dry-run)
      dry_run=true; shift ;;
    --allow-system-tool)
      allow_system=true; shift ;;
    --no-daemon)
      no_daemon=true; shift ;;
    -h|--help)
      usage; exit 0 ;;
    --)
      shift
      extra=("$@")
      break ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2 ;;
  esac
done

case "$mode" in
  compile|test|verify|native) ;;
  *) echo "error: unsupported mode: $mode" >&2; exit 2 ;;
esac
case "$build" in
  auto|maven|gradle) ;;
  *) echo "error: unsupported build tool: $build" >&2; exit 2 ;;
esac

root="$(cd "$root" 2>/dev/null && pwd)" || {
  echo "error: root is not a directory" >&2
  exit 2
}

has_maven=false
has_gradle=false
[[ -f "$root/pom.xml" ]] && has_maven=true
[[ -f "$root/build.gradle" || -f "$root/build.gradle.kts" ]] && has_gradle=true

if [[ "$build" == "auto" ]]; then
  if $has_maven && $has_gradle; then
    echo "error: both Maven and Gradle roots detected; pass --build" >&2
    exit 2
  elif $has_maven; then
    build="maven"
  elif $has_gradle; then
    build="gradle"
  else
    echo "error: no root pom.xml or Gradle build file detected" >&2
    exit 2
  fi
fi

quote_command() {
  printf '%q ' "$@"
  printf '\n'
}

run_command() {
  echo "+ $(quote_command "$@")"
  if ! $dry_run; then
    "$@"
  fi
}

contains_quarkus() {
  if [[ -f "$root/pom.xml" ]] && grep -Eq 'io\.quarkus|quarkus-maven-plugin' "$root/pom.xml"; then
    return 0
  fi
  if [[ -f "$root/build.gradle" ]] && grep -Eq 'io\.quarkus' "$root/build.gradle"; then
    return 0
  fi
  if [[ -f "$root/build.gradle.kts" ]] && grep -Eq 'io\.quarkus' "$root/build.gradle.kts"; then
    return 0
  fi
  return 1
}

cd "$root"

echo "Effective Java quality gate"
echo "  root: $root"
echo "  build: $build"
echo "  mode: $mode"
[[ -n "$project" ]] && echo "  project: $project"
$dry_run && echo "  dry-run: true"

if [[ "$build" == "maven" ]]; then
  if [[ -x "$root/mvnw" ]]; then
    tool=("$root/mvnw")
  elif $allow_system && command -v mvn >/dev/null 2>&1; then
    tool=("mvn")
  else
    echo "error: Maven wrapper not executable; use --allow-system-tool only when project policy permits" >&2
    exit 2
  fi
  scope=()
  [[ -n "$project" ]] && scope=("-pl" "$project" "-am")
  case "$mode" in
    compile) goals=("-DskipTests" "compile") ;;
    test) goals=("test") ;;
    verify) goals=("verify") ;;
    native)
      if ! contains_quarkus; then
        echo "error: native mode is only auto-wired for detected Quarkus builds" >&2
        exit 2
      fi
      echo "note: verify that this project/version uses -Dnative before relying on this gate" >&2
      goals=("verify" "-Dnative")
      ;;
  esac
  command_line=("${tool[@]}")
  if (( ${#scope[@]} > 0 )); then
    command_line+=("${scope[@]}")
  fi
  command_line+=("${goals[@]}")
  if (( ${#extra[@]} > 0 )); then
    command_line+=("${extra[@]}")
  fi
  run_command "${command_line[@]}"
else
  if [[ -x "$root/gradlew" ]]; then
    tool=("$root/gradlew")
  elif $allow_system && command -v gradle >/dev/null 2>&1; then
    tool=("gradle")
  else
    echo "error: Gradle wrapper not executable; use --allow-system-tool only when project policy permits" >&2
    exit 2
  fi
  gradle_flags=()
  $no_daemon && gradle_flags+=("--no-daemon")
  prefix=""
  if [[ -n "$project" ]]; then
    prefix=":${project#:}"
    prefix="${prefix%:}"
  fi
  task() {
    local name="$1"
    if [[ -n "$prefix" ]]; then
      printf '%s:%s' "$prefix" "$name"
    else
      printf '%s' "$name"
    fi
  }
  case "$mode" in
    compile) goals=("$(task classes)" "$(task testClasses)") ;;
    test) goals=("$(task test)") ;;
    verify) goals=("$(task check)") ;;
    native)
      if ! contains_quarkus; then
        echo "error: native mode is only auto-wired for detected Quarkus builds" >&2
        exit 2
      fi
      echo "note: verify this Quarkus version's native task/property before relying on this gate" >&2
      goals=("$(task build)" "-Dquarkus.native.enabled=true")
      ;;
  esac
  command_line=("${tool[@]}")
  if (( ${#gradle_flags[@]} > 0 )); then
    command_line+=("${gradle_flags[@]}")
  fi
  command_line+=("${goals[@]}")
  if (( ${#extra[@]} > 0 )); then
    command_line+=("${extra[@]}")
  fi
  run_command "${command_line[@]}"
fi
