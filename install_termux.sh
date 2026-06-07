#!/bin/bash
# TeChCh - Instalador para Termux (Android)

GREEN='\033[92m'
CYAN='\033[96m'
RED='\033[91m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo " _____ _____ ____ _   _  ____ _   _"
echo "|_   _| ____/ ___| | | |/ ___| | | |"
echo "  | | |  _|| |   | |_| | |   | |_| |"
echo "  | | | |__| |___|  _  | |___|  _  |"
echo "  |_| |_____|\\____|_| |_|\\____|_| |_|"
echo ""
echo "  Instalador para Termux"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detectar python
if command -v python3 &>/dev/null; then
    PY="python3"
    PIP="pip3"
elif command -v python &>/dev/null; then
    PY="python"
    PIP="pip"
else
    echo "${RED}[!] Python no encontrado. Instalando...${RESET}"
    pkg update -y
    pkg install -y python
    PY="python"
    PIP="pip"
fi

echo "${CYAN}[1/4] Verificando Python...${RESET}"
$PY --version
echo -e "  ${GREEN}[+]${RESET} Python OK"

echo "${CYAN}[2/4] Instalando librerias...${RESET}"
$PY -m pip install --upgrade pip 2>/dev/null || true
$PY -m pip install colorama requests pycryptodome 2>/dev/null || \
$PIP install colorama requests pycryptodome 2>/dev/null || true

# Verificar
$PY -c "import colorama" 2>/dev/null && echo -e "  ${GREEN}[+]${RESET} colorama OK" || echo -e "  ${RED}[!]${RESET} colorama no se pudo instalar"
$PY -c "import requests" 2>/dev/null && echo -e "  ${GREEN}[+]${RESET} requests OK" || echo -e "  ${RED}[!]${RESET} requests no se pudo instalar"

echo "${CYAN}[3/4] Copiando archivos...${RESET}"
INSTALL_DIR="$HOME/.techch"
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
echo -e "  ${GREEN}[+]${RESET} Archivos copiados"

echo "${CYAN}[4/4] Creando comando techch...${RESET}"
mkdir -p "$HOME/.local/bin"

# Crear launcher con el python correcto
cat > "$HOME/.local/bin/techch" << LAUNCHER
#!/bin/bash
cd $INSTALL_DIR
$PY techch.py
LAUNCHER
chmod +x "$HOME/.local/bin/techch"

# PATH
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo -e "  ${GREEN}[+]${RESET} Listo"

echo ""
echo "════════════════════════════════════════════════════"
echo "  TeChCh v2.0 instalado en Termux!"
echo "════════════════════════════════════════════════════"
echo ""
echo "  Ejecutar:"
echo "    $PY $INSTALL_DIR/techch.py"
echo ""
echo "  Desinstalar:"
echo "    rm -rf $INSTALL_DIR ~/.local/bin/techch"
echo ""
