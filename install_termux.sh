#!/bin/bash
# ============================================================
# TeChCh - Instalador para Termux (Android)
# ============================================================
# Uso en Termux:
#   pkg install git python -y
#   git clone https://github.com/mateoproramita2-gif/TeChCh.git
#   cd TeChCh
#   bash install_termux.sh
# ============================================================

GREEN='\033[92m'
CYAN='\033[96m'
RED='\033[91m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${CYAN}${BOLD}"
echo " _____ _____ ____ _   _  ____ _   _"
echo "|_   _| ____/ ___| | | |/ ___| | | |"
echo "  | | |  _|| |   | |_| | |   | |_| |"
echo "  | | | |__| |___|  _  | |___|  _  |"
echo "  |_| |_____|\\____|_| |_|\\____|_| |_|"
echo -e "${RESET}"
echo -e "${CYAN}  Instalador para Termux${RESET}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paso 1: Dependencias
echo -e "${CYAN}[1/4] Instalando dependencias...${RESET}"
pkg update -y 2>/dev/null
pkg install -y python 2>/dev/null
pkg install -y git 2>/dev/null
echo -e "  ${GREEN}[+]${RESET} Python y Git instalados"

# Paso 2: Librerias Python
echo -e "${CYAN}[2/4] Instalando librerias Python...${RESET}"
pip install colorama 2>/dev/null || pip3 install colorama 2>/dev/null || true
pip install requests 2>/dev/null || pip3 install requests 2>/dev/null || true
pip install pycryptodome 2>/dev/null || pip3 install pycryptodome 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Librerias instaladas"

# Paso 3: Copiar archivos
echo -e "${CYAN}[3/4] Instalando TeChCh...${RESET}"
INSTALL_DIR="$HOME/.techch"

# Limpiar instalacion anterior
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

cp -r "$SCRIPT_DIR/core" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/commands" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/ai" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/animations" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/utils" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/techch.py" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/techch.py"

echo -e "  ${GREEN}[+]${RESET} Archivos copiados a $INSTALL_DIR"

# Paso 4: Crear comando global
echo -e "${CYAN}[4/4] Creando comando 'techch'...${RESET}"
mkdir -p "$HOME/.local/bin"

cat > "$HOME/.local/bin/techch" << 'LAUNCHER'
#!/bin/bash
cd "$HOME/.techch"
exec python techch.py "$@"
LAUNCHER
chmod +x "$HOME/.local/bin/techch"

# PATH
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Alias
if ! grep -q 'alias techch' "$HOME/.bashrc" 2>/dev/null; then
    echo 'alias techch="python ~/.techch/techch.py"' >> "$HOME/.bashrc"
fi

echo -e "  ${GREEN}[+]${RESET} Comando 'techch' creado"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  TeChCh v2.0 instalado en Termux!               ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Ejecutar ahora:${RESET}"
echo -e "    python ~/.techch/techch.py"
echo ""
echo -e "  ${CYAN}Despues de reiniciar Termux:${RESET}"
echo -e "    techch"
echo ""
echo -e "  ${CYAN}Para desinstalar:${RESET}"
echo -e "    rm -rf ~/.techch ~/.local/bin/techch"
echo ""
