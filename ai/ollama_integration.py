import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error
from core.ui import C, slow_print, fast_print, spinner, print_loading

OLLAMA_BASE = "http://localhost:11434"

TECHCH_SYSTEM_PROMPT = """Eres TeChCh AI, un asistente de ciberseguridad especializado. Respondes SOLO sobre temas de ciberseguridad, hacking etico, administracion de sistemas, redes, forense digital, y la herramienta TeChCh.

CONOCIMIENTO DE LA HERRAMIENTA TeChCh:
- TeChCh es un sistema de ciberseguridad avanzado con 100+ comandos
- Categorias: recon, exploit, net, crypto, forensics, system, wireless, web, malware, osint
- Se ejecuta via terminal con comandos como: portscan, hash_crack, arp_spoofer, etc.
- Tiene integracion con Ollama para asistente AI
- Modo oscuro hacker con animaciones y efectos visuales
- Totalmente funcional en Linux

COMANDOS PRINCIPALES:
RECON: portscan, serviceid, dnseum, whois_lookup, tracert, subnet_scan, banner_grab, reverse_dns, host_discovery, os_fingerprint, vuln_scan, net_enum, mac_lookup, ssl_scan, http_headers, subdomain_enum, email_harvest, tech_detect, full_recon
NET: net_sniff, arp_spoofer, dns_spof, packet_forge, mitm_attack, net_jam, vlan_hopping, net_map, deauth, tcp_hijack, net_recon, port_knock, net_island, syn_flood, udp_flood, icmp_flood, dhcp_starve, llmnr_spoof, net_serve, capture_hash, wol
CRYPTO: hash_crack, gen_pass, caesar, base64_enc, base64_dec, hex_encode, hex_decode, xor_cipher, aes_encrypt, aes_decrypt, rsa_gen, steg_hide, steg_extract, password_spray, hash_dump, substitution, vigenere, jwt_decode
SYSTEM: proc_list, kill_proc, sys_info, disk_usage, env_dump, user_enum, service_list, file_monitor, log_analyze, cron_list, firewall_rules, open_files, mem_dump, net_connections, startup_list, file_perm, sudo_check, rootkit_check, proc_tree, sys_hardening, scheduled_tasks, kernel_modules, login_history, drive_encryption, reg_check
WIRELESS: wifi_scan, wpa_crack, wps_attack, evil_twin, packet_inject, bluetooth_scan, bluesnarf, rfid_read, sdr_scan, nfc_clone, wifi_deauth, pmkid_attack, handshake_capture, freq_hop, wifi_monitor, probe_req, karma_attack, wifi_jammer, lorawan_scan, antenna_detect, sig_int
WEB: sql_inject, xss_scan, dir_brute, sub_takeover, api_fuzz, jwt_forge, ssrf_scan, xxe_scan, lfi_scan, rfi_scan, cors_scan, graphql_introspect, websocket_test, jwt_decode_web, cookie_analyze, clickjack_test, header_inject, cache_poison, crlf_inject, prototype_polyglot
FORENSICS: file_hash, file_meta, disk_image, timeline, string_extract, entropy, volatility, yara_scan, log_parser, hex_editor, net_forensics, steg_analysis, malware_sandbox, registry_analyze, browser_forensics, email_forensics, memory_strings, chain_of_custody
MALWARE: malware_scan, malware_gen, shellcode_gen, obfuscate, payload_encode, anti_analysis, persistence_check, c2_beacon, evade_test, macro_gen, exploit_gen, rootkit_gen, keylogger, rat_gen, ransomware_sim, process_inject, priv_escalation, coopernight, memory_evasion, dlp_bypass
OSINT: ip_lookup, email_lookup, domain_recon, username_search, phone_lookup, shodan_lookup, cve_lookup, paste_search, breach_check, social_scan, archive_search, dns_history, whois_history, tech_stack, employee_search, darkweb_monitor, geo_track, metadata_extract, subdomain_take, pixel_track, full_osint

INSTRUCCIONES:
- Responde en español y en ingles CUANDO TE LO PIDEN
- Sé preciso y técnico
- Cuando pregunten por comandos, da el nombre exacto y ejemplo de uso
- Para vulnerabilidades, da contexto técnico detallado
- NUNCA uses humor, todo es serio
- Si no sabes algo, di "No tengo información sobre eso"
- Siempre prioriza la seguridad y el uso ético"""

def is_ollama_running():
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
        response = urllib.request.urlopen(req, timeout=3)
        return True
    except:
        return False

def get_models():
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode())
        return data.get("models", [])
    except:
        return []

def install_ollama():
    print(f"\n{C.CYAN}[+] Instalando Ollama...{C.RESET}\n")
    try:
        result = subprocess.run(
            ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
            capture_output=True, text=True, shell=True
        )
        if result.returncode == 0:
            print(f"{C.GREEN}[+] Ollama instalado exitosamente{C.RESET}")
            return True
        else:
            print(f"{C.YELLOW}[*] Intentando metodo alternativo...{C.RESET}")
            subprocess.run(["winget", "install", "Ollama.Ollama"], shell=True)
            return True
    except Exception as e:
        print(f"{C.RED}[!] Error instalando: {e}{C.RESET}")
        return False

def pull_model(model_name):
    print(f"\n{C.CYAN}[+] Descargando modelo: {C.WHITE}{model_name}{C.RESET}\n")
    try:
        data = json.dumps({"name": model_name}).encode()
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/pull",
            data=data,
            method="POST"
        )
        response = urllib.request.urlopen(req, timeout=300)
        print(f"{C.GREEN}[+] Modelo {model_name} descargado{C.RESET}")
        return True
    except Exception as e:
        print(f"{C.RED}[!] Error descargando: {e}{C.RESET}")
        return False

def chat_with_model(model_name, message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    messages = [{"role": "system", "content": TECHCH_SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})

    try:
        data = json.dumps({
            "model": model_name,
            "messages": messages,
            "stream": False
        }).encode()

        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/chat",
            data=data,
            method="POST"
        )

        response = urllib.request.urlopen(req, timeout=120)
        result = json.loads(response.read().decode())

        if "message" in result:
            return result["message"]["content"]
        return "Error: No se pudo obtener respuesta"

    except Exception as e:
        return f"Error de conexion: {e}"

def stream_chat(model_name, message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    messages = [{"role": "system", "content": TECHCH_SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})

    try:
        data = json.dumps({
            "model": model_name,
            "messages": messages,
            "stream": True
        }).encode()

        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/chat",
            data=data,
            method="POST"
        )

        response = urllib.request.urlopen(req, timeout=120)
        full_response = ""

        for line in response:
            try:
                chunk = json.loads(line.decode())
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    sys.stdout.write(f"{C.GREEN}{content}{C.RESET}")
                    sys.stdout.flush()
                    full_response += content
            except:
                pass

        print()
        return full_response

    except Exception as e:
        print(f"\n{C.RED}[!] Error de conexion: {e}{C.RESET}")
        return None

def ollama_chat_session(model_name):
    print(f"\n{C.CYAN}[+] Sesion de chat con {C.WHITE}{model_name}{C.CYAN} iniciada{C.RESET}")
    print(f"{C.DIM}Escribe 'salir' para terminar la sesion{C.RESET}\n")

    conversation = []

    while True:
        try:
            user_input = input(f"{C.GREEN}TechCh [{model_name}]> {C.RESET}").strip()

            if not user_input:
                continue
            if user_input.lower() in ["salir", "exit", "quit"]:
                print(f"\n{C.CYAN}[+] Sesion terminada{C.RESET}")
                break

            response = stream_chat(model_name, user_input, conversation)
            if response:
                conversation.append({"role": "user", "content": user_input})
                conversation.append({"role": "assistant", "content": response})

            print()

        except KeyboardInterrupt:
            print(f"\n\n{C.CYAN}[+] Sesion interrumpida{C.RESET}")
            break
        except EOFError:
            break

def ollama_menu():
    while True:
        print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {C.BOLD}{C.WHITE}[{C.GREEN}Ollama AI{C.WHITE}] Panel de Control                            {C.CYAN}║
╚══════════════════════════════════════════════════════════════╝{C.RESET}

  {C.GREEN}[1]{C.RESET}  Verificar estado de Ollama
  {C.GREEN}[2]{C.RESET}  Instalar Ollama
  {C.GREEN}[3]{C.RESET}  Descargar modelo
  {C.GREEN}[4]{C.RESET}  Listar modelos instalados
  {C.GREEN}[5]{C.RESET}  Iniciar sesion de chat
  {C.GREEN}[6]{C.RESET}  Seleccionar modelo por defecto
  {C.GREEN}[0]{C.RESET}  Volver al menu principal
""")
        choice = input(f"{C.GREEN}TechCh/Ollama> {C.RESET}").strip()

        if choice == "1":
            if is_ollama_running():
                print(f"\n{C.GREEN}[+] Ollama esta activo{C.RESET}")
                models = get_models()
                if models:
                    print(f"  Modelos instalados: {len(models)}")
                    for m in models:
                        print(f"    - {m['name']}")
                else:
                    print(f"  {C.YELLOW}No hay modelos instalados{C.RESET}")
            else:
                print(f"\n{C.RED}[!] Ollama no esta corriendo{C.RESET}")
                print(f"  Ejecute: ollama serve")

        elif choice == "2":
            install_ollama()

        elif choice == "3":
            model = input(f"\n{C.CYAN}Nombre del modelo (ej: llama3, mistral, codellama): {C.RESET}").strip()
            if model:
                pull_model(model)

        elif choice == "4":
            models = get_models()
            if models:
                print(f"\n{C.CYAN}[+] Modelos instalados:{C.RESET}")
                for m in models:
                    print(f"  {C.GREEN}[*] {m['name']}{C.RESET}")
            else:
                print(f"{C.YELLOW}No hay modelos instalados{C.RESET}")

        elif choice == "5":
            models = get_models()
            if not models:
                print(f"{C.YELLOW}No hay modelos. Descargue uno primero.{C.RESET}")
                continue
            print(f"\n{C.CYAN}Modelos disponibles:{C.RESET}")
            for i, m in enumerate(models, 1):
                print(f"  {C.GREEN}[{i}]{C.RESET} {m['name']}")
            model_idx = input(f"\n{C.GREEN}Seleccione modelo: {C.RESET}").strip()
            try:
                idx = int(model_idx) - 1
                if 0 <= idx < len(models):
                    ollama_chat_session(models[idx]['name'])
            except:
                print(f"{C.RED}Seleccion invalida{C.RESET}")

        elif choice == "6":
            models = get_models()
            if not models:
                print(f"{C.YELLOW}No hay modelos instalados{C.RESET}")
                continue
            print(f"\n{C.CYAN}Modelos disponibles:{C.RESET}")
            for i, m in enumerate(models, 1):
                print(f"  {C.GREEN}[{i}]{C.RESET} {m['name']}")
            model_idx = input(f"\n{C.GREEN}Seleccione modelo por defecto: {C.RESET}").strip()
            try:
                idx = int(model_idx) - 1
                if 0 <= idx < len(models):
                    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "settings.json")
                    config = {}
                    if os.path.exists(config_path):
                        with open(config_path) as f:
                            config = json.load(f)
                    config["ollama_model"] = models[idx]['name']
                    with open(config_path, "w") as f:
                        json.dump(config, f, indent=2)
                    print(f"{C.GREEN}[+] Modelo por defecto: {models[idx]['name']}{C.RESET}")
            except:
                print(f"{C.RED}Seleccion invalida{C.RESET}")

        elif choice == "0":
            break
