#!/bin/bash
# ============================================================
# TeChCh - Generar Repositorio APT completo
# ============================================================
# Uso: ./build_repo.sh
# Genera: repo/ listo para subir a GitHub Pages
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION=$(grep -oP 'Version: \K.*' "$SCRIPT_DIR/debian/control" 2>/dev/null || echo "2.0.0")
DEB_NAME="techch_${VERSION}_all"
DEB_FILE="$SCRIPT_DIR/${DEB_NAME}.deb"
REPO_DIR="$SCRIPT_DIR/repo"

echo "[*] Construyendo TeChCh v${VERSION}..."

# Paso 1: Build .deb
bash "$SCRIPT_DIR/build_deb.sh"

# Paso 2: Generar repositorio
echo "[*] Generando repositorio APT..."
rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"

cp "$DEB_FILE" "$REPO_DIR/"

# Generar clave GPG si no existe
if [ ! -f "$SCRIPT_DIR/KEY.gpg" ]; then
    echo "[*] Generando clave GPG..."
    gpg --batch --gen-key 2>/dev/null << GPGKEY || true
Key-Type: RSA
Key-Length: 2048
Name-Real: TeChCh
Name-Email: techch@security.local
Expire-Date: 0
%no-protection
%commit
GPGKEY
    gpg --export --armor "TeChCh" > "$SCRIPT_DIR/KEY.gpg" 2>/dev/null || \
    gpg --export --armor > "$SCRIPT_DIR/KEY.gpg" 2>/dev/null || true
fi

cp "$SCRIPT_DIR/KEY.gpg" "$REPO_DIR/" 2>/dev/null || true

# Generar Packages
cd "$REPO_DIR"
dpkg-scanpackages --multiversion . /dev/null > Packages 2>/dev/null
gzip -9c Packages > Packages.gz

# Generar Release
cat > Release << EOF
Origin: TeChCh
Label: TeChCh Security Tool
Suite: stable
Codename: stable
Architectures: all
Components: main
Description: TeChCh - Terminal Enhanced Cyber Command Hub Repository
Date: $(date -R)
SHA256:
 $(sha256sum Packages | cut -d' ' -f1) $(wc -c < Packages) Packages
 $(sha256sum Packages.gz | cut -d' ' -f1) $(wc -c < Packages.gz) Packages.gz
EOF

echo ""
echo "[+] Repositorio generado: $REPO_DIR/"
echo "[+] Paquete: techch_${VERSION}_all.deb"
echo ""
echo "Para publicar:"
echo "  1. Sube la carpeta repo/ a GitHub Pages"
echo "  2. Edite setup.sh con su usuario de GitHub"
echo "  3. Los usuarios ejecutan: curl -sSL URL/setup.sh | sudo bash"
echo ""
