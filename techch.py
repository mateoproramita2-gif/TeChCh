#!/usr/bin/env python3
"""
TeChCh - Terminal Enhanced Cyber Command Hub
Sistema de Ciberseguridad Avanzado v2.0
"""

import os
import sys
import json
import time
import random
import signal
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core.ui import (
    C, clear, slow_print, fast_print, print_banner, print_category_banner,
    print_command_help, print_error, print_success, print_warning, print_info,
    print_loading, progress_bar, spinner, print_table, print_status_bar,
    glitch_text, matrix_rain
)
from animations.effects import matrix_effect, boot_sequence
from core.engine import CommandRegistry
from config.settings import load_settings, save_settings, print_settings, set_setting, get_setting
from ai.ollama_integration import (
    ollama_menu, is_ollama_running, get_models, chat_with_model,
    stream_chat, ollama_chat_session, TECHCH_SYSTEM_PROMPT
)

registry = CommandRegistry()

def load_all_commands():
    commands_dir = os.path.join(BASE_DIR, "commands")
    for category in os.listdir(commands_dir):
        cat_path = os.path.join(commands_dir, category)
        if os.path.isdir(cat_path) and not category.startswith("_"):
            for filename in os.listdir(cat_path):
                if filename.endswith("_commands.py"):
                    module_name = f"commands.{category}.{filename[:-3]}"
                    try:
                        import importlib
                        module = importlib.import_module(module_name)
                        if hasattr(module, "register_commands"):
                            module.register_commands(registry)
                    except Exception as e:
                        print(f"{C.RED}[!] Error cargando {module_name}: {e}{C.RESET}")

def show_help():
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {C.BOLD}{C.WHITE}TeChCh - Comandos Disponibles                             {C.CYAN}║
╚══════════════════════════════════════════════════════════════╝{C.RESET}

  {C.GREEN}[CATEGORIES]{C.RESET}
""")
    for cat, cmds in sorted(registry.categories.items()):
        print(f"    {C.CYAN}{cat.upper():<15}{C.WHITE}({len(cmds)} comandos){C.RESET}")
    print(f"""
  {C.GREEN}[COMANDOS ESPECIALES]{C.RESET}
    {C.GREEN}help{C.RESET}              Mostrar esta ayuda
    {C.GREEN}categories{C.RESET}         Listar categorias
    {C.GREEN}category <name>{C.RESET}     Ver comandos de una categoria
    {C.GREEN}info <cmd>{C.RESET}          Ver info de un comando
    {C.GREEN}search <query>{C.RESET}      Buscar comandos
    {C.GREEN}ollama{C.RESET}             Panel de control Ollama AI
    {C.GREEN}ai <message>{C.RESET}        Consultar al asistente AI
    {C.GREEN}settings{C.RESET}           Configuracion del sistema
    {C.GREEN}stats{C.RESET}              Estadisticas de sesion
    {C.GREEN}clear{C.RESET}              Limpiar pantalla
    {C.GREEN}exit{C.RESET}              Salir del sistema
""")

def show_categories():
    print(f"\n{C.CYAN}[+] Categorias disponibles:{C.RESET}\n")
    for cat, cmds in sorted(registry.categories.items()):
        print(f"  {C.GREEN}{cat.upper():<15}{C.WHITE}{len(cmds)} comandos{C.RESET}")

def show_category(name):
    cmds = registry.get_category(name)
    if not cmds:
        print(f"{C.RED}[!] Categoria '{name}' no encontrada{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Comandos en {name.upper()}:{C.RESET}\n")
    for cmd in sorted(cmds):
        info = registry.commands[cmd]
        print(f"  {C.GREEN}{cmd:<25}{C.WHITE}{info['description'][:60]}{C.RESET}")

def show_stats():
    stats = registry.get_stats()
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {C.BOLD}{C.WHITE}Estadisticas de Sesion                                     {C.CYAN}║
╚══════════════════════════════════════════════════════════════╝{C.RESET}

  {C.CYAN}Total comandos:{C.WHITE}     {stats['total_commands']}
  {C.CYAN}Categorias:{C.WHITE}         {stats['total_categories']}
  {C.CYAN}Ejecutados:{C.WHITE}         {stats['total_executed']}
  {C.CYAN}Tiempo activo:{C.WHITE}       {stats['session_uptime']}
  {C.CYAN}Historial:{C.WHITE}          {stats['history_size']} entradas
""")

def show_history():
    if not registry.history:
        print(f"{C.YELLOW}[*] No hay historial en esta sesion{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Historial de comandos:{C.RESET}\n")
    for entry in registry.history[-20:]:
        time_str = entry['timestamp'].strftime("%H:%M:%S")
        print(f"  {C.DIM}{time_str}{C.RESET} {C.GREEN}{entry['command']}{C.RESET} {C.DIM}({entry['time']:.2f}s){C.RESET}")

def handle_ai_query(query):
    settings = load_settings()
    model = settings.get("ollama_model", "llama3")

    if not is_ollama_running():
        print(f"{C.RED}[!] Ollama no esta corriendo. Inicie con: ollama serve{C.RESET}")
        return

    print(f"\n{C.CYAN}[AI - {model}]{C.RESET}")
    response = stream_chat(model, query)
    print()

def execute_command(cmd_name, args):
    start_time = time.time()
    result, error = registry.execute(cmd_name, args)
    elapsed = time.time() - start_time

    if error:
        print_error(error)
    elif result is not None:
        if isinstance(result, str):
            print(result)

    return result, error

def main():
    settings = load_settings()

    signal.signal(signal.SIGINT, lambda s, f: None)

    clear()
    if settings.get("animations_enabled", True):
        try:
            matrix_effect(1.5)
        except:
            pass

    print_banner()

    if settings.get("animations_enabled", True):
        print_loading("Cargando modulos", 1.5)

    load_all_commands()

    print_success(f"{len(registry.commands)} comandos cargados en {len(registry.categories)} categorias")
    print()

    while True:
        try:
            stats = registry.get_stats()
            prompt = f"{C.GREEN}TechCh{C.CYAN}({C.WHITE}{stats['total_executed']}{C.CYAN}){C.GREEN}>{C.RESET} "
            user_input = input(prompt).strip()

            if not user_input:
                continue

            parts = user_input.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ["exit", "quit", "salir"]:
                print(f"\n{C.CYAN}[+] Cerrando TeChCh...{C.RESET}")
                print(f"{C.DIM}Sesion finalizada. Total comandos ejecutados: {stats['total_executed']}{C.RESET}")
                break

            elif cmd == "help":
                show_help()

            elif cmd == "categories":
                show_categories()

            elif cmd == "category":
                if args:
                    show_category(args[0])
                else:
                    print_error("Uso: category <nombre>")

            elif cmd == "info":
                if args:
                    info = registry.get_command_info(args[0])
                    if info:
                        print_command_help(args[0], info)
                    else:
                        print_error(f"Comando '{args[0]}' no encontrado")
                else:
                    print_error("Uso: info <comando>")

            elif cmd == "search":
                if args:
                    query = " ".join(args)
                    results = registry.search(query)
                    if results:
                        print(f"\n{C.CYAN}[+] Resultados para '{query}':{C.RESET}\n")
                        for name, info in results:
                            print(f"  {C.GREEN}{name:<25}{C.WHITE}{info['description'][:50]}{C.RESET}")
                    else:
                        print_warning("No se encontraron resultados")
                else:
                    print_error("Uso: search <termino>")

            elif cmd == "ollama":
                ollama_menu()

            elif cmd == "ai":
                if args:
                    handle_ai_query(" ".join(args))
                else:
                    print_error("Uso: ai <mensaje>")

            elif cmd == "settings":
                print_settings()

            elif cmd == "set":
                if len(args) >= 2:
                    key = args[0]
                    value = " ".join(args[1:])
                    if value.lower() in ["true", "yes", "on"]:
                        value = True
                    elif value.lower() in ["false", "no", "off"]:
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    set_setting(key, value)
                    print_success(f"Configuracion '{key}' actualizada a '{value}'")
                else:
                    print_error("Uso: set <key> <value>")

            elif cmd == "stats":
                show_stats()

            elif cmd == "history":
                show_history()

            elif cmd == "clear":
                clear()
                print_banner()

            elif cmd == "matrix":
                if args and args[0].isdigit():
                    matrix_effect(int(args[0]))
                else:
                    matrix_effect(3)

            elif cmd == "all":
                all_cmds = registry.get_all_commands()
                print(f"\n{C.CYAN}[+] Todos los comandos ({len(all_cmds)}):{C.RESET}\n")
                for i, c in enumerate(all_cmds):
                    print(f"  {C.GREEN}{c:<25}{C.RESET}", end="")
                    if (i + 1) % 3 == 0:
                        print()

            elif cmd == "glitch":
                text = " ".join(args) if args else "TECHCH"
                glitch_text(text)

            else:
                result, error = execute_command(cmd, args)

        except KeyboardInterrupt:
            print(f"\n{C.DIM}Use 'exit' para salir{C.RESET}")
        except EOFError:
            break
        except Exception as e:
            print_error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
