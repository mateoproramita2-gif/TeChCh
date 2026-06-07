#!/bin/bash
# ============================================================
# TeChCh - Instalador de Repositorio APT para Kali Linux
# ============================================================
# Ejecutar UNA VEZ en Kali Linux:
#   sudo chmod +x install_repo.sh
#   sudo ./install_repo.sh
#
# Despues de esto, siempre podras hacer:
#   sudo apt install techch
#   sudo apt remove techch
#   sudo apt update techch
# ============================================================

set -e

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
WHITE='\033[97m'
RESET='\033[0m'
BOLD='\033[1m'

VERSION="2.0.0"
PKG_NAME="techch"
REPO_DIR="/var/www/html/techch-repo"
DEB_POOL="$REPO_DIR/pool/main"
DEB_DIST="$REPO_DIR/dists/stable"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Ejecute como root: sudo ./install_repo.sh${RESET}"
    exit 1
fi

echo -e "${CYAN}${BOLD}"
echo " _____ _____ ____ _   _  ____ _   _"
echo "|_   _| ____/ ___| | | |/ ___| | | |"
echo "  | | |  _|| |   | |_| | |   | |_| |"
echo "  | | | |__| |___|  _  | |___|  _  |"
echo "  |_| |_____|\\____|_| |_|\\____|_| |_|"
echo -e "${RESET}"
echo -e "${CYAN}  Configurador de Repositorio APT v${VERSION}${RESET}"
echo ""

# ============================================================
# PASO 1: Instalar dependencias
# ============================================================
echo -e "${CYAN}[1/7] Instalando dependencias del sistema...${RESET}"
apt-get update -qq
apt-get install -y -qq dpkg-dev apt-utils python3 python3-pip curl wget 2>/dev/null
pip3 install colorama requests pycryptodome 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Dependencias instaladas"

# ============================================================
# PASO 2: Crear estructura del .deb
# ============================================================
echo -e "${CYAN}[2/7] Creando paquete .deb...${RESET}"

BUILD_DIR=$(mktemp -d)
DEB_NAME="${PKG_NAME}_${VERSION}_all"
DEB_PATH="${BUILD_DIR}/${DEB_NAME}"

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

# Copiar archivos del proyecto
cp "$SCRIPT_DIR/techch.py" "$DEB_PATH/opt/techch/"
cp "$SCRIPT_DIR/install.sh" "$DEB_PATH/opt/techch/" 2>/dev/null || true
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

echo -e "  ${GREEN}[+]${RESET} Archivos copiados"

# ============================================================
# PASO 3: Crear scripts DEBIAN
# ============================================================
echo -e "${CYAN}[3/7] Creando scripts de empaquetado...${RESET}"

INSTALLED_SIZE=$(du -sk "$DEB_PATH/opt" | cut -f1)

cat > "$DEB_PATH/DEBIAN/control" << EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-pip
Recommends: nmap, whois, dnsutils, net-tools
Installed-Size: $INSTALLED_SIZE
Maintainer: TeChCh Security Team <techch@security.local>
Homepage: https://github.com/techch/techch
Description: TeChCh - Terminal Enhanced Cyber Command Hub
 Sistema de ciberseguridad avanzado con 181+ comandos para
 administracion de sistemas, redes, criptografia, forense digital,
 analisis de malware, OSINT, y mas.
 .
 Incluye integracion con Ollama AI para asistente de ciberseguridad.
 .
 SOLO USO AUTORIZADO - PROFESIONALES DE SEGURIDAD
EOF

cat > "$DEB_PATH/DEBIAN/postinst" << 'POSTINST'
#!/bin/bash
set -e
INSTALL_DIR="/opt/techch"

# Crear launcher
cat > /usr/local/bin/techch << 'LAUNCHER'
#!/bin/bash
cd /opt/techch
exec python3 techch.py "$@"
LAUNCHER
chmod +x /usr/local/bin/techch
chmod +x "$INSTALL_DIR/techch.py"

# Instalar dependencias Python
pip3 install colorama requests pycryptodome 2>/dev/null || true

# Config por defecto
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
echo "[+] TeChCh instalado. Ejecute: techch"
POSTINST
chmod 755 "$DEB_PATH/DEBIAN/postinst"

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

cat > "$DEB_PATH/DEBIAN/conffiles" << 'CONFFILES'
/opt/techch/config/settings.json
CONFFILES

echo -e "  ${GREEN}[+]${RESET} Scripts DEBIAN creados"

# ============================================================
# PASO 4: Compilar el .deb
# ============================================================
echo -e "${CYAN}[4/7] Compilando paquete .deb...${RESET}"
dpkg-deb --build --root-owner-group "$DEB_PATH" "${BUILD_DIR}/${DEB_NAME}.deb"
echo -e "  ${GREEN}[+]${RESET} Paquete compilado: ${DEB_NAME}.deb"

# ============================================================
# PASO 5: Crear repositorio APT local
# ============================================================
echo -e "${CYAN}[5/7] Creando repositorio APT local...${RESET}"

rm -rf "$REPO_DIR"
mkdir -p "$DEB_POOL"
mkdir -p "$DEB_DIST/binary-all"

cp "${BUILD_DIR}/${DEB_NAME}.deb" "$DEB_POOL/"

# Crear Packages.gz
cd "$DEB_DIST/binary-all"
dpkg-scanpackages --multiversion "$DEB_POOL/" /dev/null | gzip -9c > Packages.gz
dpkg-scanpackages --multiversion "$DEB_POOL/" /dev/null > Packages

# Crear Release
cd "$DEB_DIST"
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
 $(sha256sum binary-all/Packages | cut -d' ' -f1) $(wc -c < binary-all/Packages) Packages
 $(sha256sum binary-all/Packages.gz | cut -d' ' -f1) $(wc -c < binary-all/Packages.gz) Packages.gz
EOF

echo -e "  ${GREEN}[+]${RESET} Repositorio creado en $REPO_DIR"

# ============================================================
# PASO 6: Configurar APT para usar el repo local
# ============================================================
echo -e "${CYAN}[6/7] Configurando fuente APT...${RESET}"

# Copiar el .deb a una ubicacion estatica
mkdir -p /opt/techch-deb
cp "${BUILD_DIR}/${DEB_NAME}.deb" /opt/techch-deb/

# Crear script de instalacion rapida
cat > /usr/local/bin/install-techch << 'INSTALLER'
#!/bin/bash
set -e
DEB="/opt/techch-deb/techch_2.0.0_all.deb"
if [ ! -f "$DEB" ]; then
    echo "[!] Paquete no encontrado"
    exit 1
fi
echo "[*] Instalando TeChCh..."
dpkg -i "$DEB" 2>/dev/null || apt-get install -f -y
echo "[+] TeChCh instalado. Ejecute: techch"
INSTALLER
chmod +x /usr/local/bin/install-techch

# Crear script de desinstalacion
cat > /usr/local/bin/uninstall-techch << 'UNINSTALLER'
#!/bin/bash
echo "[*] Desinstalando TeChCh..."
apt-get remove -y techch 2>/dev/null || rm -rf /opt/techch /usr/local/bin/techch
rm -f /usr/local/bin/install-techch /usr/local/bin/uninstall-techch
echo "[+] TeChCh desinstalado"
UNINSTALLER
chmod +x /usr/local/bin/uninstall-techch

echo -e "  ${GREEN}[+]${RESET} Scripts de instalacion creados"

# ============================================================
# PASO 7: Limpiar e instalar
# ============================================================
echo -e "${CYAN}[7/7] Instalando TeChCh...${RESET}"

dpkg -i "${BUILD_DIR}/${DEB_NAME}.deb" 2>/dev/null || apt-get install -f -y

# Limpiar
rm -rf "$BUILD_DIR"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  TeChCh v${VERSION} instalado y configurado!                      ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Para ejecutar:${RESET}"
echo -e "    techch"
echo ""
echo -e "  ${CYAN}Para reinstalar:${RESET}"
echo -e "    sudo install-techch"
echo ""
echo -e "  ${CYAN}Para desinstalar:${RESET}"
echo -e "    sudo uninstall-techch"
echo -e "    ${DIM}o${RESET}"
echo -e "    sudo apt remove techch"
echo ""
echo -e "  ${CYAN}Paquete .deb guardado en:${RESET}"
echo -e "    /opt/techch-deb/${DEB_NAME}.deb"
echo ""
