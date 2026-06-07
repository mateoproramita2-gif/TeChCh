#!/bin/bash
# TeChCh - Instalador para Linux
# Terminal Enhanced Cyber Command Hub

set -e

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
WHITE='\033[97m'
RESET='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'

INSTALL_DIR="/opt/techch"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}${BOLD}"
echo "  ████████╗██╗  ██╗███████╗███╗   ███╗"
echo "  ╚══██╔══╝██║  ██║██╔════╝████╗ ████║"
echo "     ██║   ███████║█████╗  ██╔████╔██║"
echo "     ██║   ██╔══██║██╔══╝  ██║╚██╔╝██║"
echo "     ██║   ██║  ██║███████╗██║ ╚═╝ ██║"
echo "     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝"
echo -e "${RESET}"
echo -e "${DIM}  Instalador de TeChCh v2.0 - Terminal Enhanced Cyber Command Hub${RESET}"
echo ""

echo -e "${CYAN}[1/4] Verificando dependencias...${RESET}"

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[*] python3 no encontrado. Instalando...${RESET}"
    sudo apt-get update -qq
    sudo apt-get install -y python3 python3-pip
fi
echo -e "  ${GREEN}[+]${RESET} Python3 encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}[*] pip no encontrado. Instalando...${RESET}"
    sudo apt-get install -y python3-pip
fi
echo -e "  ${GREEN}[+]${RESET} pip encontrado"

echo ""
echo -e "${CYAN}[2/4] Instalando dependencias de Python...${RESET}"
pip3 install --user colorama requests 2>/dev/null || pip install --user colorama requests 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Dependencias instaladas"

echo ""
echo -e "${CYAN}[3/4] Instalando TeChCh...${RESET}"

# Crear directorio de instalacion
sudo mkdir -p "$INSTALL_DIR"

# Copiar archivos
sudo cp -r "$SCRIPT_DIR"/core "$INSTALL_DIR/"
sudo cp -r "$SCRIPT_DIR"/commands "$INSTALL_DIR/"
sudo cp -r "$SCRIPT_DIR"/ai "$INSTALL_DIR/"
sudo cp -r "$SCRIPT_DIR"/animations "$INSTALL_DIR/"
sudo cp -r "$SCRIPT_DIR"/config "$INSTALL_DIR/"
sudo cp -r "$SCRIPT_DIR"/utils "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR"/techch.py "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR"/install.sh "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR"/README.md "$INSTALL_DIR/"

# Permisos
sudo chmod +x "$INSTALL_DIR/techch.py"
sudo chmod +x "$INSTALL_DIR/install.sh"

echo -e "  ${GREEN}[+]${RESET} Archivos copiados a $INSTALL_DIR"

echo ""
echo -e "${CYAN}[4/4] Creando comando global...${RESET}"

sudo tee /usr/local/bin/techch > /dev/null << 'EOF'
#!/bin/bash
cd /opt/techch
exec python3 techch.py "$@"
EOF

sudo chmod +x /usr/local/bin/techch
echo -e "  ${GREEN}[+]${RESET} Comando 'techch' creado"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  TeChCh v2.0 instalado exitosamente!            ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Ejecutar:${RESET} techch"
echo -e "  ${CYAN}O:${RESET} python3 $INSTALL_DIR/techch.py"
echo ""
echo -e "${DIM}  Para instalar Ollama AI: techch > ollama > [2] Instalar${RESET}"
echo -e "${DIM}  Documentacion: $INSTALL_DIR/README.md${RESET}"
echo ""
