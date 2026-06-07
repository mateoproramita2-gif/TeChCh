#!/bin/bash
# ============================================================
# TeChCh - Instalador para Termux (Android)
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

echo -e "${CYAN}[1/4] Instalando dependencias...${RESET}"
pkg update -y
pkg install -y python
echo -e "  ${GREEN}[+]${RESET} Python instalado"

echo -e "${CYAN}[2/4] Instalando librerias...${RESET}"
python -m pip install colorama requests pycryptodome
echo -e "  ${GREEN}[+]${RESET} Librerias instaladas"

echo -e "${CYAN}[3/4] Copiando archivos...${RESET}"
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

echo -e "${CYAN}[4/4] Creando acceso directo...${RESET}"
mkdir -p "$HOME/.local/bin"

cat > "$HOME/.local/bin/techch" << 'EOF'
#!/bin/bash
cd $HOME/.techch
python techch.py
EOF
chmod +x "$HOME/.local/bin/techch"

# Verificar que python funciona
python -c "import colorama; print('colorama OK')" 2>/dev/null || echo "Instalando colorama..."
python -c "import requests; print('requests OK')" 2>/dev/null || echo "Instalando requests..."
python -c "import Crypto; print('pycryptodome OK')" 2>/dev/null || echo "Instalando pycryptodome..."

# PATH
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo -e "  ${GREEN}[+]${RESET} Listo"

echo ""
echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}  TeChCh v2.0 instalado en Termux!${RESET}"
echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${CYAN}Ejecutar ahora:${RESET}"
echo "    python $INSTALL_DIR/techch.py"
echo ""
echo -e "  ${CYAN}Para desinstalar:${RESET}"
echo "    rm -rf $INSTALL_DIR ~/.local/bin/techch"
echo ""
