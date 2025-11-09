#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-/dev/cu.usbmodem83101}"


if ! command -v mpremote >/dev/null 2>&1; then
    echo "This script requires the mpremote command. You can install it with:"
    echo "pip3 install --user mpremote"
    exit 1
fi

if ! command -v mpy-cross >/dev/null 2>&1; then
    echo "This script requires the mpy-cross command. You can install it with:"
    echo "pip3 install --user mpy-cross"
    exit 1
fi

upload_fonts () {
    cd romfonts
    rm -f *.mpy
    for font in *.py
    do
        mpy-cross $font
    done
    cd ..
    mpremote cp romfonts/*.mpy :
}

mpremote connect "$PORT" mip install "github:russhughes/st7789py_mpy/lib/st7789py.py" || true

upload_fonts
for file in src/*.py; do
    echo "==> Uploading $file"
    mpremote connect "$PORT" fs cp "$file" :
done

echo "==> Resetting board"
mpremote connect "$PORT" reset
echo "Done."

