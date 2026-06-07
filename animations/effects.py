import os
import sys
import time
import random

def loading_animation(text="Cargando", duration=2):
    from core.ui import C
    symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C.CYAN}{symbols[i % len(symbols)]} {text}...{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{C.GREEN}[+] {text} completado{C.RESET}\n")

def matrix_effect(duration=3):
    from core.ui import C
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモ"
    end_time = time.time() + duration
    while time.time() < end_time:
        line = ""
        for _ in range(80):
            if random.random() < 0.1:
                line += f"{C.GREEN}{random.choice(chars)}{C.RESET}"
            else:
                line += " "
        sys.stdout.write(f"\r{line}")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def glitch_effect(text, iterations=3):
    from core.ui import C
    glitch_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    original = text
    for _ in range(iterations):
        glitched = ""
        for char in original:
            if random.random() < 0.3:
                glitched += random.choice(glitch_chars)
            else:
                glitched += char
        sys.stdout.write(f"\r{C.RED}{glitched}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f"\r{C.GREEN}{original}{C.RESET}\n")

def scan_animation(target, duration=3):
    from core.ui import C
    end_time = time.time() + duration
    while time.time() < end_time:
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        port = random.randint(1, 65535)
        sys.stdout.write(f"\r{C.CYAN}Escaneando {C.WHITE}{target}{C.CYAN} | IP: {C.WHITE}{ip}{C.CYAN} | Puerto: {C.WHITE}{port}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def progress_animation(text="Procesando", total=20):
    from core.ui import C
    for i in range(total + 1):
        bar = "█" * i + "░" * (total - i)
        pct = int((i / total) * 100)
        sys.stdout.write(f"\r{C.CYAN}{text} {C.GREEN}{bar} {C.WHITE}{pct}%{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def typing_effect(text, delay=0.03):
    from core.ui import C
    for char in text:
        sys.stdout.write(f"{C.GREEN}{char}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def cyber_sweep():
    from core.ui import C
    frames = [
        f"{C.CYAN}╔═══════════════════════════════════╗{C.RESET}",
        f"{C.CYAN}║{C.RESET}  {C.GREEN}[■■■■■■■■■■■■■■■■■■■]{C.RESET}  {C.CYAN}║{C.RESET}",
        f"{C.CYAN}║{C.RESET}  {C.WHITE}INICIALIZANDO SISTEMAS{C.RESET}        {C.CYAN}║{C.RESET}",
        f"{C.CYAN}╚═══════════════════════════════════╝{C.RESET}",
    ]
    for frame in frames:
        print(frame)
        time.sleep(0.3)

def boot_sequence():
    from core.ui import C
    lines = [
        f"{C.DIM}[BIOS] Verificando sistema...{C.RESET}",
        f"{C.DIM}[CPU] Inicializando nucleo...{C.RESET}",
        f"{C.DIM}[RAM] Cargando modulos...{C.RESET}",
        f"{C.DIM}[NET] Configurando interfaz...{C.RESET}",
        f"{C.DIM}[SEC] Verificando permisos...{C.RESET}",
        f"{C.GREEN}[+] TeChCh Engine v2.0 inicializado{C.RESET}",
    ]
    for line in lines:
        print(f"  {line}")
        time.sleep(0.2)
