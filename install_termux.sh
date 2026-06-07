#!/bin/bash
# ============================================================
# TeChCh - Instalador para Termux (Android)
# ============================================================
# Uso en Termux:
#   pkg install git python
#   git clone https://github.com/mateoproramita2-gif/TeChCh.git
#   cd TeChCh
#   bash install_termux.sh
# ============================================================

set -e

GREEN='\033[92m'
CYAN='\033[96m'
RED='\033[91m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${CYAN}{BOLD}"
echo " _____ _____ ____ _   _  ____ _   _"
echo "|_   _| ____/ ___| | | |/ ___| | | |"
echo "  | | |  _|| |   | |_| | |   | |_| |"
echo "  | | | |__| |___|  _  | |___|  _  |"
echo "  |_| |_____|\\____|_| |_|\\____|_| |_|"
echo -e "${RESET}"
echo -e "${CYAN}  Instalador para Termux${RESET}"
echo ""

# Detectar directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Instalar dependencias
echo -e "${CYAN}[1/3] Instalando dependencias...${RESET}"
pkg update -y -qq 2>/dev/null || true
pkg install -y python git 2>/dev/null || true
pip install colorama requests pycryptodome 2>/dev/null || \
pip3 install colorama requests pycryptodome 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Dependencias instaladas"

# Crear directorio de instalacion
echo -e "${CYAN}[2/3] Instalando TeChCh...${RESET}"
INSTALL_DIR="$HOME/.techch"
mkdir -p "$INSTALL_DIR"

# Copiar archivos
cp -r "$SCRIPT_DIR/core" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/commands" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/ai" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/animations" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/utils" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/techch.py" "$INSTALL_DIR/"

# Crear comando global
cat > "$HOME/.local/bin/techch" << LAUNCHER
#!/bin/bash
cd "$INSTALL_DIR"
exec python techch.py "\$@"
LAUNCHER
chmod +x "$HOME/.local/bin/techch"

# Agregar al PATH si no esta
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

mkdir -p "$HOME/.local/bin"

echo -e "  ${GREEN}[+]${RESET} TeChCh instalado en $INSTALL_DIR"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  TeChCh v2.0 instalado en Termux!               ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Para ejecutar:${RESET}"
echo -e "    source ~/.bashrc"
echo -e "    techch"
echo ""
echo -e "  ${CYAN}O directamente:${RESET}"
echo -e "    python $INSTALL_DIR/techch.py"
echo ""
echo -e "  ${CYAN}Para desinstalar:${RESET}"
echo -e "    rm -rf $INSTALL_DIR ~/.local/bin/techch"
echo ""
