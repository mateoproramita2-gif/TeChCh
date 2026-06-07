#!/bin/bash
# ============================================================
# TeChCh - Instalador Rapido para Kali Linux
# ============================================================
# Uso en Kali Linux:
#   1. Copia toda la carpeta TccEch a Kali
#   2. chmod +x setup_kali.sh
#   3. sudo ./setup_kali.sh
# ============================================================

set -e

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'
BOLD='\033[1m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}${BOLD}"
echo "  █████████╗ ██████╗  █████╗  ██████╗██╗  ██╗"
echo "  ╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██║ ██╔╝"
echo "     ██║   ██║   ██║███████║██║     █████╔╝ "
echo "     ██║   ██║   ██║██╔══██║██║     ██╔═██╗ "
echo "     ██║   ╚██████╔╝██║  ██║╚██████╗██║  ██╗"
echo "     ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
echo -e "${RESET}"
echo -e "${CYAN}  Instalador para Kali Linux${RESET}"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Ejecute como root: sudo ./setup_kali.sh${RESET}"
    exit 1
fi

echo -e "${CYAN}[1/3] Instalando dependencias del sistema...${RESET}"
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-colorama python3-requests curl git nmap whois dnsutils net-tools 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Dependencias del sistema instaladas"

echo -e "${CYAN}[2/3] Instalando librerias Python...${RESET}"
pip3 install colorama requests pycryptodome 2>/dev/null || true
echo -e "  ${GREEN}[+]${RESET} Librerias Python instaladas"

echo -e "${CYAN}[3/3] Instalando TeChCh...${RESET}"

INSTALL_DIR="/opt/techch"

# Crear directorio
mkdir -p "$INSTALL_DIR"

# Copiar todos los archivos
cp -r "$SCRIPT_DIR/core" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/commands" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/ai" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/animations" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/utils" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/techch.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/" 2>/dev/null || true

# Crear launcher
cat > /usr/local/bin/techch << 'LAUNCHER'
#!/bin/bash
cd /opt/techch
exec python3 techch.py "$@"
LAUNCHER
chmod +x /usr/local/bin/techch
chmod +x "$INSTALL_DIR/techch.py"

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

echo -e "  ${GREEN}[+]${RESET} TeChCh instalado en $INSTALL_DIR"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  TeChCh v2.0 instalado exitosamente en Kali Linux!      ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Para ejecutar:${RESET}"
echo -e "    techch"
echo ""
echo -e "  ${CYAN}O directamente:${RESET}"
echo -e "    python3 $INSTALL_DIR/techch.py"
echo ""
echo -e "  ${CYAN}Para desinstalar:${RESET}"
echo -e "    sudo rm -rf $INSTALL_DIR /usr/local/bin/techch"
echo ""
echo -e "  ${YELLOW}Para instalar Ollama AI:${RESET}"
echo -e "    techch > ollama > [2] Instalar Ollama"
echo ""
