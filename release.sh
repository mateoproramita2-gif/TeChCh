#!/bin/bash
# ============================================================
# TeChCh - Script de Release
# ============================================================
# Uso: ./release.sh [patch|minor|major]
#   patch: 2.0.0 -> 2.0.1
#   minor: 2.0.0 -> 2.1.0
#   major: 2.0.0 -> 3.0.0
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUMP="${1:-patch}"

# Leer version actual
CURRENT=$(grep -oP 'Version: \K.*' "$SCRIPT_DIR/debian/control")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# Calcular nueva version
case "$BUMP" in
    major) MAJOR=$((MAJOR+1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR+1)); PATCH=0 ;;
    patch) PATCH=$((PATCH+1)) ;;
    *) echo "[!] Uso: ./release.sh [patch|minor|major]"; exit 1 ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"

echo "[*] Release: $CURRENT -> $NEW_VERSION"
echo ""

# Actualizar version en debian/control
sed -i "s/^Version: .*/Version: $NEW_VERSION/" "$SCRIPT_DIR/debian/control"

# Actualizar version en setup.sh
sed -i "s/^VERSION=.*/VERSION=\"$NEW_VERSION\"/" "$SCRIPT_DIR/build_deb.sh" 2>/dev/null || true

# Actualizar version en techch.py si existe
sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v${NEW_VERSION}/g" "$SCRIPT_DIR/techch.py" 2>/dev/null || true

# Build
echo "[*] Construyendo paquete..."
bash "$SCRIPT_DIR/build_deb.sh"

# Generar repo
echo "[*] Generando repositorio..."
bash "$SCRIPT_DIR/build_repo.sh"

echo ""
echo "[+] Release v${NEW_VERSION} listo!"
echo ""
echo "Siguientes pasos:"
echo "  1. git add -A && git commit -m 'v${NEW_VERSION}'"
echo "  2. git push origin main"
echo "  3. Los usuarios ejecutan: sudo apt install --only-upgrade techch"
echo ""
