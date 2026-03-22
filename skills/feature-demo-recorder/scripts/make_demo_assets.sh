#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 || $# -gt 6 ]]; then
  echo "Usage: $0 <input-video> <output-base> <start-seconds> <end-seconds> [gif-fps=6] [gif-width=420]" >&2
  exit 1
fi

input_video="$1"
output_base="$2"
start_seconds="$3"
end_seconds="$4"
gif_fps="${5:-6}"
gif_width="${6:-420}"

if [[ ! -f "$input_video" ]]; then
  echo "Input video not found: $input_video" >&2
  exit 1
fi

output_dir="$(dirname "$output_base")"
mkdir -p "$output_dir"

mp4_output="${output_base}.mp4"
gif_output="${output_base}.gif"
palette_file="${output_base}.palette.png"

ffmpeg -y \
  -i "$input_video" \
  -vf "trim=start=${start_seconds}:end=${end_seconds},setpts=PTS-STARTPTS,fps=${gif_fps}" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -an \
  "$mp4_output"

ffmpeg -y \
  -i "$mp4_output" \
  -vf "fps=${gif_fps},scale=${gif_width}:-1:flags=lanczos,palettegen" \
  "$palette_file"

ffmpeg -y \
  -i "$mp4_output" \
  -i "$palette_file" \
  -lavfi "fps=${gif_fps},scale=${gif_width}:-1:flags=lanczos[x];[x][1:v]paletteuse" \
  "$gif_output"

rm -f "$palette_file"

echo "Created:"
echo "  $mp4_output"
echo "  $gif_output"
