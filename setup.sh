#!/bin/bash
# ============================================================
# TeChCh - Instalador via APT
# ============================================================
# Ejecutar UNA VEZ:
#   curl -sSL https://mateoproramita2-gif.github.io/TeChCh/setup.sh | sudo bash
#
# Despues:
#   sudo apt install techch
#   sudo apt install --only-upgrade techch
# ============================================================

set -e

REPO_URL="https://mateoproramita2-gif.github.io/TeChCh/repo"
SOURCES_FILE="/etc/apt/sources.list.d/techch.list"
KEYRING="/usr/share/keyrings/techch.gpg"

if [ "$EUID" -ne 0 ]; then
    echo "[!] Ejecute con sudo: sudo bash setup.sh"
    exit 1
fi

echo ""
echo "  █████████╗ ██████╗  █████╗  ██████╗██╗  ██╗"
echo "  ╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██║ ██╔╝"
echo "     ██║   ██║   ██║███████║██║     █████╔╝ "
echo "     ██║   ██║   ██║██╔══██║██║     ██╔═██╗ "
echo "     ██║   ╚██████╔╝██║  ██║╚██████╗██║  ██╗"
echo "     ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
echo ""
echo "  Configurando repositorio APT..."
echo ""

# Instalar dependencias
apt-get install -y -qq curl gpg 2>/dev/null || true

# Agregar clave GPG
echo "[1/3] Agregando clave GPG..."
mkdir -p /usr/share/keyrings
curl -fsSL "$REPO_URL/KEY.gpg" | gpg --dearmor -o "$KEYRING" 2>/dev/null || \
    wget -qO- "$REPO_URL/KEY.gpg" | gpg --dearmor -o "$KEYRING"

# Agregar fuente APT
echo "[2/3] Agregando fuente..."
echo "deb [signed-by=$KEYRING] $REPO_URL ./" > "$SOURCES_FILE"
chmod 644 "$SOURCES_FILE"

# Actualizar
echo "[3/3] Actualizando listas..."
apt-get update -qq 2>/dev/null

echo ""
echo "[+] Repositorio configurado!"
echo ""
echo "  Instalar:     sudo apt install techch"
echo "  Actualizar:   sudo apt install --only-upgrade techch"
echo "  Desinstalar:  sudo apt remove techch"
echo ""
