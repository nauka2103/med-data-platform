#!/bin/sh
set -eu

diagram_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

if ! command -v dot >/dev/null 2>&1; then
  printf '%s\n' 'Graphviz is required: install it from https://graphviz.org/download/' >&2
  exit 1
fi

for name in 01-system-context 02-use-cases 03-components; do
  dot -Kdot -Tsvg "$diagram_dir/$name.dot" -o "$diagram_dir/$name.svg"
  dot -Kdot -Tpng -Gdpi=160 "$diagram_dir/$name.dot" -o "$diagram_dir/$name.png"
  printf 'Rendered %s.svg and %s.png\n' "$name" "$name"
done
