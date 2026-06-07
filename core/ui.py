import os
import sys
import time
import random
import platform

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[38;5;129m"
    PINK = "\033[38;5;213m"
    NEON_GREEN = "\033[38;5;46m"
    NEON_BLUE = "\033[38;5;21m"
    GOLD = "\033[38;5;220m"
    SILVER = "\033[38;5;250m"
    DARK_GRAY = "\033[38;5;236m"
    MID_GRAY = "\033[38;5;240m"

C = Colors

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def slow_print(text, delay=0.03, color=C.CYAN):
    for char in text:
        sys.stdout.write(f"{color}{char}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def fast_print(text, color=C.GREEN):
    print(f"{color}{text}{C.RESET}")

def glitch_text(text, iterations=3, delay=0.05):
    glitch_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
    original = text
    for _ in range(iterations):
        glitched = ""
        for i, char in enumerate(original):
            if random.random() < 0.3:
                glitched += random.choice(glitch_chars)
            else:
                glitched += char
        sys.stdout.write(f"\r{C.RED}{glitched}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\r{C.GREEN}{original}{C.RESET}\n")
    sys.stdout.flush()

def matrix_rain(duration=2, width=None):
    if width is None:
        width = 80
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    end_time = time.time() + duration
    lines = [" " * width for _ in range(20)]
    line_lists = [list(line) for line in lines]
    while time.time() < end_time:
        output = "\033[H"
        for i in range(20):
            line = ""
            for j in range(width):
                if random.random() < 0.02:
                    line += f"{C.GREEN}{random.choice(chars)}{C.RESET}"
                elif line_lists[i][j] != " ":
                    line += f"{C.DIM}{C.GREEN}{line_lists[i][j]}{C.RESET}"
                    line_lists[i][j] = " "
                else:
                    line += " "
            print(output + line, end="", flush=True)
            time.sleep(0.05)

def print_banner():
    clear()
    banner = f"""
{C.CYAN}{C.BOLD}  ████████╗██╗  ██╗███████╗███╗   ███╗
{C.GREEN}{C.BOLD}  ╚══██╔══╝██║  ██║██╔════╝████╗ ████║
{C.YELLOW}{C.BOLD}     ██║   ███████║█████╗  ██╔████╔██║
{C.RED}{C.BOLD}     ██║   ██╔══██║██╔══╝  ██║╚██╔╝██║
{C.MAGENTA}{C.BOLD}     ██║   ██║  ██║███████╗██║ ╚═╝ ██║
{C.BLUE}{C.BOLD}     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝{C.RESET}

{C.DIM}{C.WHITE}  ╔══════════════════════════════════════════════════╗
  ║  {C.CYAN}TEChCh {C.SILVER}| Terminal Enhanced Cyber Command Hub      {C.WHITE}║
  ║  {C.GREEN}v2.0.0 {C.SILVER}| Sistema de Ciberseguridad Avanzado       {C.WHITE}║
  ║  {C.YELLOW}[!] {C.SILVER}SOLO USO AUTORIZADO - ADMINISTRADORES       {C.WHITE}║
  ╚══════════════════════════════════════════════════╝{C.RESET}

{C.DIM}{C.MAGENTA}  [{C.CYAN}+{C.MAGENTA}] Modulos: {C.GREEN}100+{C.MAGENTA} | {C.CYAN}Comandos: {C.GREEN}Avanzados{C.MAGENTA} | {C.CYAN}Motor: {C.GREEN}TEChCh Engine v2{C.MAGENTA} {C.RESET}
{C.DIM}{C.ORANGE}  [{C.CYAN}*{C.ORANGE}] Ollama AI Integration: {C.GREEN}Activo{C.ORANGE} | {C.CYAN}Modelos: {C.GREEN}Disponibles{C.ORANGE} {C.RESET}
"""
    print(banner)

def print_category_banner(category, description):
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {C.BOLD}{C.WHITE}[{C.GREEN}Category{C.WHITE}] {category}
║  {C.DIM}{C.SILVER}{description}
╚══════════════════════════════════════════════════════════════╝{C.RESET}
""")

def print_command_help(cmd_name, info):
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {C.BOLD}{C.WHITE}Comando: {C.GREEN}{cmd_name}{C.WHITE}
║  {C.DIM}{C.SILVER}Categoria: {C.YELLOW}{info['category']}{C.SILVER}
║  {C.DIM}{C.SILVER}Descripcion: {C.WHITE}{info['description']}{C.SILVER}
║  {C.DIM}{C.SILVER}Sintaxis: {C.CYAN}{info['syntax']}{C.SILVER}
║  {C.DIM}{C.SILVER}Ejemplos:{C.RESET}""")
    for ex in info.get("examples", []):
        print(f"║    {C.GREEN}>>> {ex}{C.RESET}")
    print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")

def print_error(msg):
    print(f"{C.RED}[!] ERROR: {msg}{C.RESET}")

def print_success(msg):
    print(f"{C.GREEN}[+] EXITO: {msg}{C.RESET}")

def print_warning(msg):
    print(f"{C.YELLOW}[!] AVISO: {msg}{C.RESET}")

def print_info(msg):
    print(f"{C.CYAN}[i] INFO: {msg}{C.RESET}")

def print_loading(text="Cargando", duration=2):
    symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C.CYAN}{symbols[i % len(symbols)]} {text}...{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{C.GREEN}[+] {text} completado{C.RESET}\n")

def progress_bar(current, total, prefix="Progreso", suffix="Completado", length=50, fill="█", empty="░"):
    pct = current / total
    filled = int(length * pct)
    bar = fill * filled + empty * (length - filled)
    sys.stdout.write(f"\r{C.CYAN}{prefix} {C.GREEN}{bar} {C.WHITE}{pct*100:.1f}% {C.CYAN}{suffix}{C.RESET}")
    sys.stdout.flush()

def print_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows) if rows else 0) + 2 for i, h in enumerate(headers)]
    header_line = "│".join(f" {C.BOLD}{C.WHITE}{h:^{col_widths[i]}}{C.RESET} " for i, h in enumerate(headers))
    sep_line = "┼".join("─" * w for w in col_widths)
    print(f"┌{'┬'.join('─' * w for w in col_widths)}┐")
    print(f"│{header_line}│")
    print(f"├{sep_line}┤")
    for row in rows:
        row_line = "│".join(f" {C.GREEN}{str(row[i]):^{col_widths[i]}}{C.RESET} " for i in range(len(headers)))
        print(f"│{row_line}│")
    print(f"└{'┴'.join('─' * w for w in col_widths)}┘")

def spinner(text="Procesando", duration=1.5):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C.CYAN}{chars[i % len(chars)]} {C.WHITE}{text}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")

def hex_dump(data, length=16):
    result = []
    for i in range(0, len(data), length):
        chunk = data[i:i+length]
        hex_str = " ".join(f"{b:02x}" for b in chunk)
        ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        result.append(f"{C.CYAN}{i:08x}  {C.WHITE}{hex_str:<{length*3}}  {C.GREEN}{ascii_str}{C.RESET}")
    return "\n".join(result)

def print_status_bar(registry):
    stats = registry.get_stats()
    print(f"{C.DIM}{C.MAGENTA}┌{'─'*60}┐")
    print(f"│{C.CYAN} Cmds: {C.GREEN}{stats['total_commands']}{C.MAGENTA} │ {C.CYAN}Ejecutados: {C.GREEN}{stats['total_executed']}{C.MAGENTA} │ {C.CYAN}Uptime: {C.GREEN}{stats['session_uptime']}{C.MAGENTA} │{C.RESET}{C.DIM}{C.MAGENTA} │{C.RESET}{C.DIM}{C.MAGENTA} └{'─'*60}┘{C.RESET}")
