#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CHECKOUT_DIR="${MXZTAR_CHECKOUT:-$(cd -- "$SCRIPT_DIR/.." && pwd)}"
HOME_DIR="${MXZTAR_HOME:-$HOME}"

RUNNER="$CHECKOUT_DIR/run_mxztar_forge.sh"
ICON="$CHECKOUT_DIR/assets/icons/mxztar-forge-star.svg"
APPS_DIR="$HOME_DIR/.local/share/applications"
DESKTOP_DIR="$HOME_DIR/Desktop"
APP_LAUNCHER="$APPS_DIR/mxztar-forge-v2.desktop"
DESKTOP_LAUNCHER="$DESKTOP_DIR/MXZTAR-Forge-v2.0.desktop"
STAMP="$(date +%Y%m%d-%H%M%S)"

if [ ! -x "$RUNNER" ]; then
    echo "STOP: executable repository launcher not found: $RUNNER" >&2
    exit 1
fi

if [ ! -f "$ICON" ]; then
    echo "STOP: star icon not found: $ICON" >&2
    exit 1
fi

mkdir -p "$APPS_DIR" "$DESKTOP_DIR"

backup_existing() {
    local target="$1"
    if [ -e "$target" ]; then
        cp --preserve=mode,timestamps -- "$target" "$target.before-v2.0-$STAMP"
        echo "Backup: $target.before-v2.0-$STAMP"
    fi
}

write_launcher() {
    local target="$1"
    local temporary
    temporary="$(mktemp "${target}.tmp.XXXXXX")"

    {
        printf '%s\n' '[Desktop Entry]'
        printf '%s\n' 'Type=Application'
        printf '%s\n' 'Version=1.0'
        printf '%s\n' 'Name=MXZTAR Forge v2.0'
        printf '%s\n' 'Comment=Local-first creative concept-engineering forge'
        printf 'Exec=%s\n' "$RUNNER"
        printf 'Path=%s\n' "$CHECKOUT_DIR"
        printf 'Icon=%s\n' "$ICON"
        printf '%s\n' 'Terminal=false'
        printf '%s\n' 'Categories=Graphics;Development;'
        printf '%s\n' 'StartupNotify=true'
    } > "$temporary"

    chmod 755 "$temporary"
    mv -- "$temporary" "$target"
    echo "Installed: $target"
}

backup_existing "$APP_LAUNCHER"
backup_existing "$DESKTOP_LAUNCHER"
write_launcher "$APP_LAUNCHER"
write_launcher "$DESKTOP_LAUNCHER"

if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate "$APP_LAUNCHER"
    desktop-file-validate "$DESKTOP_LAUNCHER"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

echo "PASS: My Apps launcher installed"
echo "PASS: Desktop launcher installed"
echo "PASS: both launchers use the MXZTAR Forge star icon"
