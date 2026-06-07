#!/bin/bash
# ============================================================
# TeChCh - Build .deb Package
# ============================================================
# Ejecutar: chmod +x build_deb.sh && ./build_deb.sh
# Genera: techch_2.0.0_all.deb
# ============================================================

set -e

VERSION=$(grep -oP 'Version: \K.*' "$(dirname "$0")/debian/control" 2>/dev/null || echo "2.0.0")
PKG_NAME="techch"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR=$(mktemp -d)
DEB_NAME="${PKG_NAME}_${VERSION}_all"
DEB_PATH="${BUILD_DIR}/${DEB_NAME}"

echo "[*] Construyendo paquete $DEB_NAME ..."

# Crear estructura
mkdir -p "$DEB_PATH/DEBIAN"
mkdir -p "$DEB_PATH/opt/techch/core"
mkdir -p "$DEB_PATH/opt/techch/commands/recon"
mkdir -p "$DEB_PATH/opt/techch/commands/exploit"
mkdir -p "$DEB_PATH/opt/techch/commands/net"
mkdir -p "$DEB_PATH/opt/techch/commands/crypto"
mkdir -p "$DEB_PATH/opt/techch/commands/forensics"
mkdir -p "$DEB_PATH/opt/techch/commands/system"
mkdir -p "$DEB_PATH/opt/techch/commands/wireless"
mkdir -p "$DEB_PATH/opt/techch/commands/web"
mkdir -p "$DEB_PATH/opt/techch/commands/malware"
mkdir -p "$DEB_PATH/opt/techch/commands/osint"
mkdir -p "$DEB_PATH/opt/techch/ai"
mkdir -p "$DEB_PATH/opt/techch/animations"
mkdir -p "$DEB_PATH/opt/techch/config"
mkdir -p "$DEB_PATH/opt/techch/utils"
mkdir -p "$DEB_PATH/usr/local/bin"
mkdir -p "$DEB_PATH/usr/share/doc/techch"

# Copiar archivos
cp "$SCRIPT_DIR/techch.py" "$DEB_PATH/opt/techch/"
cp "$SCRIPT_DIR/README.md" "$DEB_PATH/usr/share/doc/techch/" 2>/dev/null || true

# Core
cp "$SCRIPT_DIR/core/"*.py "$DEB_PATH/opt/techch/core/"
touch "$DEB_PATH/opt/techch/core/__init__.py"

# Commands
for cat_dir in recon exploit net crypto forensics system wireless web malware osint; do
    cp "$SCRIPT_DIR/commands/$cat_dir/"*.py "$DEB_PATH/opt/techch/commands/$cat_dir/" 2>/dev/null || true
    touch "$DEB_PATH/opt/techch/commands/$cat_dir/__init__.py"
done
touch "$DEB_PATH/opt/techch/commands/__init__.py"

# AI
cp "$SCRIPT_DIR/ai/"*.py "$DEB_PATH/opt/techch/ai/"
touch "$DEB_PATH/opt/techch/ai/__init__.py"

# Animations
cp "$SCRIPT_DIR/animations/"*.py "$DEB_PATH/opt/techch/animations/"
touch "$DEB_PATH/opt/techch/animations/__init__.py"

# Config
cp "$SCRIPT_DIR/config/"*.py "$DEB_PATH/opt/techch/config/" 2>/dev/null || true
touch "$DEB_PATH/opt/techch/config/__init__.py"

# Config por defecto
cat > "$DEB_PATH/opt/techch/config/settings.json" << 'SETTINGS'
{
  "theme": "hacker",
  "ollama_model": "llama3",
  "ollama_auto_connect": false,
  "animations_enabled": true,
  "sound_enabled": false,
  "log_commands": true,
  "max_history": 1000,
  "timeout": 30,
  "verbose": false,
  "language": "es",
  "banner_style": "full"
}
SETTINGS

# Utils
cp "$SCRIPT_DIR/utils/"*.py "$DEB_PATH/opt/techch/utils/" 2>/dev/null || true
touch "$DEB_PATH/opt/techch/utils/__init__.py"

# Calcular tamano
INSTALLED_SIZE=$(du -sk "$DEB_PATH/opt" | cut -f1)

# DEBIAN/control
cat > "$DEB_PATH/DEBIAN/control" << EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-pip
Recommends: nmap, whois, dnsutils, net-tools
Installed-Size: $INSTALLED_SIZE
Maintainer: TeChCh Security Team
Description: TeChCh - Terminal Enhanced Cyber Command Hub
 Sistema de ciberseguridad avanzado con 181+ comandos para
 administracion de sistemas, redes, criptografia, forense digital,
 analisis de malware, OSINT, y mas.
 .
 Incluye integracion con Ollama AI para asistente de ciberseguridad.
 .
 SOLO USO AUTORIZADO - PROFESIONALES DE SEGURIDAD
EOF

# DEBIAN/postinst
cat > "$DEB_PATH/DEBIAN/postinst" << 'POSTINST'
#!/bin/bash
set -e
INSTALL_DIR="/opt/techch"

cat > /usr/local/bin/techch << 'LAUNCHER'
#!/bin/bash
cd /opt/techch
exec python3 techch.py "$@"
LAUNCHER
chmod +x /usr/local/bin/techch
chmod +x "$INSTALL_DIR/techch.py"

pip3 install colorama requests pycryptodome 2>/dev/null || true

mkdir -p "$INSTALL_DIR/config"
if [ ! -f "$INSTALL_DIR/config/settings.json" ]; then
    cat > "$INSTALL_DIR/config/settings.json" << 'SETTINGS'
{
  "theme": "hacker",
  "ollama_model": "llama3",
  "ollama_auto_connect": false,
  "animations_enabled": true,
  "sound_enabled": false,
  "log_commands": true,
  "max_history": 1000,
  "timeout": 30,
  "verbose": false,
  "language": "es",
  "banner_style": "full"
}
SETTINGS
fi
POSTINST
chmod 755 "$DEB_PATH/DEBIAN/postinst"

# DEBIAN/postrm
cat > "$DEB_PATH/DEBIAN/postrm" << 'POSTRM'
#!/bin/bash
set -e
case "$1" in
    remove|purge)
        rm -f /usr/local/bin/techch
        rm -rf /opt/techch
        ;;
esac
POSTRM
chmod 755 "$DEB_PATH/DEBIAN/postrm"

# Compilar
dpkg-deb --build --root-owner-group "$DEB_PATH" "${SCRIPT_DIR}/${DEB_NAME}.deb"

echo ""
echo "[+] Paquete creado: ${SCRIPT_DIR}/${DEB_NAME}.deb"
echo "[+] Instalar con: sudo dpkg -i ${DEB_NAME}.deb"
echo ""

# Limpiar
rm -rf "$BUILD_DIR"
