import os
import sys
import time
import random
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("wifi_scan", wifiscan_cmd, "wireless", ["ws", "wifi"],
                 "Escaneo de redes WiFi cercanas con deteccion de seguridad",
                 "wifi_scan",
                 ["wifi_scan"])

    reg.register("wpa_crack", wpacrack_cmd, "wireless", ["wpa", "wpac"],
                 "Ataque de fuerza bruta contra WPA/WPA2",
                 "wpa_crack <bssid> [--wordlist <file>]",
                 ["wpa_crack AA:BB:CC:DD:EE:FF --wordlist rockyou.txt"])

    reg.register("wps_attack", wpsattack_cmd, "wireless", ["wps"],
                 "Ataque WPS para recuperar PIN de router",
                 "wps_attack <bssid>",
                 ["wps_attack AA:BB:CC:DD:EE:FF"])

    reg.register("evil_twin", eviltwin_cmd, "wireless", ["et", "twin"],
                 "Creacion de punto de acceso falso (Evil Twin)",
                 "evil_twin <ssid> [--channel <ch>]",
                 ["evil_twin FreeWiFi --channel 6"])

    reg.register("packet_inject", packetinject_cmd, "wireless", ["pi", "inject"],
                 "Inyeccion de paquetes en red WiFi",
                 "packet_inject <bssid> [--count <n>]",
                 ["packet_inject AA:BB:CC:DD:EE:FF --count 100"])

    reg.register("bluetooth_scan", btscan_cmd, "wireless", ["bt", "bluescan"],
                 "Escaneo de dispositivos Bluetooth cercanos",
                 "bluetooth_scan",
                 ["bluetooth_scan"])

    reg.register("bluesnarf", bluesnarf_cmd, "wireless", ["bs", "snarf"],
                 "Extraccion de datos via Bluetooth (Bluesnarfing)",
                 "bluesnarf <target_mac>",
                 ["bluesnarf AA:BB:CC:DD:EE:FF"])

    reg.register("rfid_read", rfidread_cmd, "wireless", ["rfid", "rfidr"],
                 "Lectura de tarjetas RFID cercanas",
                 "rfid_read",
                 ["rfid_read"])

    reg.register("sdr_scan", sdrcan_cmd, "wireless", ["sdr"],
                 "Escaneo de frecuencias con Software Defined Radio",
                 "sdr_scan [--freq <freq>] [--bandwidth <bw>]",
                 ["sdr_scan --freq 433000000 --bandwidth 200000"])

    reg.register("nfc_clone", nfcclone_cmd, "wireless", ["nfc"],
                 "Clonacion de tarjetas NFC/RFID",
                 "nfc_clone <card_id>",
                 ["nfc_clone 04:A2:B3:C4:D5:E6:F7"])

    reg.register("wifi_deauth", wifideauth_cmd, "wireless", ["wd", "wdeauth"],
                 "Desautenticacion masiva de clientes WiFi",
                 "wifi_deauth <bssid> [--all]",
                 ["wifi_deauth AA:BB:CC:DD:EE:FF --all"])

    reg.register("pmkid_attack", pmkidattack_cmd, "wireless", ["pmkid"],
                 "Ataque PMKID para captura de hash WPA sin clientes",
                 "pmkid_attack <bssid>",
                 ["pmkid_attack AA:BB:CC:DD:EE:FF"])

    reg.register("handshake_capture", handshkcmd, "wireless", ["hs", "handshake"],
                 "Captura de handshake WPA/WPA2",
                 "handshake_capture <bssid>",
                 ["handshake_capture AA:BB:CC:DD:EE:FF"])

    reg.register("freq_hop", freqhop_cmd, "wireless", ["fh", "hop"],
                 "Hopping de frecuencias para evasion de deteccion",
                 "freq_hop [--band <2.4|5>]",
                 ["freq_hop --band 2.4"])

    reg.register("wifi_monitor", wifimon_cmd, "wireless", ["wm", "wimon"],
                 "Modo monitor de interfaz WiFi",
                 "wifi_monitor [--interface <iface>]",
                 ["wifi_monitor --interface wlan0"])

    reg.register("probe_req", probereq_cmd, "wireless", ["pr", "probe"],
                 "Envio de probe requests para descubrimiento",
                 "probe_req",
                 ["probe_req"])

    reg.register("karma_attack", karmaattack_cmd, "wireless", ["karma"],
                 "Ataque Karma - respuesta a cualquier SSID",
                 "karma_attack",
                 ["karma_attack"])

    reg.register("wifi_jammer", wifijammer_cmd, "wireless", ["wj", "jammer"],
                 "Jamming de señal WiFi en frecuencia especifica",
                 "wifi_jammer [--channel <ch>]",
                 ["wifi_jammer --channel 6"])

    reg.register("lorawan_scan", lorawanscan_cmd, "wireless", ["lorawan", "lora"],
                 "Escaneo de dispositivos LoRaWAN",
                 "lorawan_scan",
                 ["lorawan_scan"])

    reg.register("antenna_detect", antennadetect_cmd, "wireless", ["ad", "antenna"],
                 "Deteccion de antenas y dispositivos de transmision",
                 "antenna_detect",
                 ["antenna_detect"])

    reg.register("sig_int", sigintcmd, "wireless", ["sigint"],
                 "Inteligencia de señales - analisis espectral",
                 "sig_int [--duration <seconds>]",
                 ["sig_int --duration 30"])

def wifiscan_cmd(args):
    print(f"\n{C.CYAN}[+] Escaneando redes WiFi{C.RESET}\n")
    networks = [
        ("HomeNetwork", "AA:BB:CC:DD:EE:01", "WPA2", -45, 6),
        ("OfficeWiFi", "AA:BB:CC:DD:EE:02", "WPA2", -52, 11),
        ("FreeWiFi", "AA:BB:CC:DD:EE:03", "ABIERTA", -60, 1),
        ("NETGEAR_5G", "AA:BB:CC:DD:EE:04", "WPA3", -68, 36),
        ("Guest_Network", "AA:BB:CC:DD:EE:05", "WPA2", -72, 9),
    ]
    print(f"  {'SSID':<20}{'BSSID':<20}{'Seguridad':<12}{'Signal':<10}{'CH':<5}")
    print(f"  {'─'*67}")
    for net in networks:
        if len(net) >= 5:
            ssid, bssid, sec, sig, ch = net
            color = C.GREEN if sig > -50 else C.YELLOW if sig > -65 else C.RED
            print(f"  {C.WHITE}{ssid:<20}{bssid:<20}{sec:<12}{color}{sig}dBm{C.RESET}  {ch}")

def wpacrack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: wpa_crack <bssid> [--wordlist <file>]{C.RESET}")
        return
    bssid = args[0]
    print(f"\n{C.RED}[!] Ataque WPA/WPA2{C.RESET}")
    print(f"  {C.CYAN}BSSID: {C.WHITE}{bssid}{C.RESET}")
    print(f"  {C.YELLOW}[*] Capturando handshake...{C.RESET}")
    time.sleep(1)
    print(f"  {C.GREEN}[+] Handshake capturado{C.RESET}")
    print(f"  {C.YELLOW}[*] Iniciando fuerza bruta...{C.RESET}")
    for i in range(10):
        word = f"password{random.randint(100,999)}"
        print(f"  {C.DIM}Probando: {word}{C.RESET}")
        time.sleep(0.2)
    print(f"\n  {C.GREEN}[+] Clave encontrada: Password123{C.RESET}")

def wpsattack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: wps_attack <bssid>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Ataque WPS{C.RESET}")
    print(f"  {C.YELLOW}[*] Escaneando PIN...{C.RESET}")
    for i in range(8):
        sys.stdout.write(f"\r  {C.CYAN}PIN: {'*' * i}{random.randint(0,9)}{'*' * (7-i)}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
    print(f"\n  {C.GREEN}[+] PIN: 12345670{C.RESET}")
    print(f"  {C.GREEN}[+] WPS cracking completado{C.RESET}")

def eviltwin_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: evil_twin <ssid> [--channel <ch>]{C.RESET}")
        return
    ssid = args[0]
    channel = 6
    if "--channel" in args:
        channel = int(args[args.index("--channel") + 1])
    print(f"\n{C.RED}[!] Evil Twin AP{C.RESET}")
    print(f"  {C.CYAN}SSID: {C.WHITE}{ssid}{C.RESET}")
    print(f"  {C.CYAN}Canal: {C.WHITE}{channel}{C.RESET}")
    print(f"  {C.YELLOW}[*] AP falso activo{C.RESET}")
    print(f"  {C.YELLOW}[*] Esperando clientes...{C.RESET}")

def packetinject_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: packet_inject <bssid> [--count <n>]{C.RESET}")
        return
    count = 50
    if "--count" in args:
        count = int(args[args.index("--count") + 1])
    print(f"\n{C.RED}[!] Inyeccion de Paquetes{C.RESET}")
    for i in range(min(count, 20)):
        print(f"  {C.GREEN}[+] Paquete {i+1} inyectado{C.RESET}")
        time.sleep(0.1)
    print(f"  {C.GREEN}[+] {count} paquetes inyectados{C.RESET}")

def btscan_cmd(args):
    print(f"\n{C.CYAN}[+] Escaneo Bluetooth{C.RESET}\n")
    devices = [
        ("AA:BB:CC:DD:EE:01", "Samsung Galaxy S21", "Phone"),
        ("AA:BB:CC:DD:EE:02", "AirPods Pro", "Headphones"),
        ("AA:BB:CC:DD:EE:03", "Logitech MX Keys", "Keyboard"),
        ("AA:BB:CC:DD:EE:04", "Xiaomi Mi Band", "Wearable"),
    ]
    for mac, name, dtype in devices:
        print(f"  {C.WHITE}{mac}  {name:<25} {C.CYAN}{dtype}{C.RESET}")

def bluesnarf_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: bluesnarf <target_mac>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Bluesnarfing{C.RESET}")
    print(f"  {C.YELLOW}[*] Conectando a dispositivo...{C.RESET}")
    print(f"  {C.GREEN}[+] Accediendo a contactos...{C.RESET}")
    print(f"  {C.GREEN}[+] Accediendo a mensajes...{C.RESET}")
    print(f"  {C.GREEN}[+] Datos extraidos exitosamente{C.RESET}")

def rfidread_cmd(args):
    print(f"\n{C.CYAN}[+] Leyendo RFID{C.RESET}\n")
    print(f"  {C.GREEN}[+] Tarjeta detectada: MIFARE Classic 1K{C.RESET}")
    print(f"  {C.GREEN}[*] UID: 04:A2:B3:C4:D5:E6:F7{C.RESET}")
    print(f"  {C.GREEN}[*] Sector 0: {random.randint(1000,9999)} credits{C.RESET}")

def sdrcan_cmd(args):
    print(f"\n{C.CYAN}[+] Escaneo SDR{C.RESET}")
    freq = 433000000
    if "--freq" in args:
        freq = int(args[args.index("--freq") + 1])
    print(f"  {C.CYAN}Frecuencia: {C.WHITE}{freq/1000000:.1f} MHz{C.RESET}")
    print(f"  {C.GREEN}[*] Señales detectadas: 5{C.RESET}")
    print(f"  {C.GREEN}[*] Protocolo: OOK/FSK{C.RESET}")

def nfcclone_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: nfc_clone <card_id>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Clonacion NFC{C.RESET}")
    print(f"  {C.YELLOW}[*] Leyendo tarjeta...{C.RESET}")
    print(f"  {C.GREEN}[+] Datos leidos{C.RESET}")
    print(f"  {C.YELLOW}[*] Escribiendo en tarjeta vacia...{C.RESET}")
    print(f"  {C.GREEN}[+] Tarjeta clonada exitosamente{C.RESET}")

def wifideauth_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: wifi_deauth <bssid> [--all]{C.RESET}")
        return
    print(f"\n{C.RED}[!] Deauth WiFi{C.RESET}")
    for i in range(15):
        print(f"  {C.RED}[+] Frame {i+1}: Deauth broadcast{C.RESET}")
        time.sleep(0.2)
    print(f"  {C.GREEN}[+] Todos los clientes desautenticados{C.RESET}")

def pmkidattack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: pmkid_attack <bssid>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Ataque PMKID{C.RESET}")
    print(f"  {C.YELLOW}[*] Solicitando PMKID...{C.RESET}")
    time.sleep(1)
    print(f"  {C.GREEN}[+] PMKID capturado{C.RESET}")
    print(f"  {C.GREEN}[+] Hash: 1$xxxxxxxx$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{C.RESET}")

def handshkcmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: handshake_capture <bssid>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Capturando Handshake{C.RESET}")
    print(f"  {C.YELLOW}[*] Monitoreando trafico...{C.RESET}")
    for i in range(5):
        sys.stdout.write(f"\r  {C.DIM}Paquetes capturados: {i*100}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
    print(f"\n  {C.GREEN}[+] 4-way handshake capturado{C.RESET}")

def freqhop_cmd(args):
    print(f"\n{C.CYAN}[+] Frequency Hopping{C.RESET}")
    band = "2.4"
    if "--band" in args:
        band = args[args.index("--band") + 1]
    channels = range(1, 14) if band == "2.4" else [36, 40, 44, 48, 149, 153, 157, 161]
    for ch in list(channels)[:5]:
        print(f"  {C.GREEN}[*] Saltando a canal {ch}{C.RESET}")
        time.sleep(0.2)
    print(f"  {C.GREEN}[+] Hopping activo{C.RESET}")

def wifimon_cmd(args):
    print(f"\n{C.CYAN}[+] Modo Monitor{C.RESET}")
    print(f"  {C.YELLOW}[*] Activando modo monitor en wlan0...{C.RESET}")
    print(f"  {C.GREEN}[+] Modo monitor activo en wlan0mon{C.RESET}")

def probereq_cmd(args):
    print(f"\n{C.CYAN}[+] Probe Requests{C.RESET}")
    ssids = ["HomeNetwork", "OfficeWiFi", "FreeWiFi", "NETGEAR", "Linksys"]
    for ssid in ssids:
        print(f"  {C.GREEN}[*] Probe request enviado: {ssid}{C.RESET}")
        time.sleep(0.2)
    print(f"  {C.GREEN}[+] Respuestas recibidas: 3{C.RESET}")

def karmaattack_cmd(args):
    print(f"\n{C.RED}[!] Karma Attack{C.RESET}")
    print(f"  {C.YELLOW}[*] Respondiendo a todos los probe requests...{C.RESET}")
    print(f"  {C.GREEN}[+] AP falso configurado{C.RESET}")
    print(f"  {C.YELLOW}[*] Esperando clientes...{C.RESET}")

def wifijammer_cmd(args):
    print(f"\n{C.RED}[!] WiFi Jammer{C.RESET}")
    channel = 6
    if "--channel" in args:
        channel = int(args[args.index("--channel") + 1])
    print(f"  {C.CYAN}Canal: {C.WHITE}{channel}{C.RESET}")
    print(f"  {C.YELLOW}[*] Jamming activo en canal {channel}{C.RESET}")
    print(f"  {C.RED}[!] Todas las comunicaciones en este canal bloqueadas{C.RESET}")

def lorawanscan_cmd(args):
    print(f"\n{C.CYAN}[+] Escaneo LoRaWAN{C.RESET}\n")
    devices = [
        ("0x12345678", "Sensor Temp", -65, "OTAA"),
        ("0x87654321", "Tracker GPS", -72, "ABP"),
        ("0xDEADBEEF", "Rele WiFi", -80, "OTAA"),
    ]
    for dev_id, name, rssi, join in devices:
        print(f"  {C.WHITE}{dev_id}  {name:<15} {C.CYAN}{rssi}dBm{C.RESET}  {join}")

def antennadetect_cmd(args):
    print(f"\n{C.CYAN}[+] Deteccion de Antenas{C.RESET}\n")
    print(f"  {C.GREEN}[*] Señal WiFi: 2.4GHz / 5GHz{C.RESET}")
    print(f"  {C.GREEN}[*] Bluetooth: 2.4GHz{C.RESET}")
    print(f"  {C.GREEN}[*] Signal LTE: 700-2600MHz{C.RESET}")
    print(f"  {C.GREEN}[*] Signal unknown: 433MHz (posible IoT){C.RESET}")

def sigintcmd(args):
    duration = 10
    if "--duration" in args:
        duration = int(args[args.index("--duration") + 1])
    print(f"\n{C.CYAN}[+] Inteligencia de Señales ({duration}s){C.RESET}")
    print(f"  {C.YELLOW}[*] Analizando espectro...{C.RESET}")
    time.sleep(1)
    print(f"  {C.GREEN}[*] 2.4GHz: 12 señales activas{C.RESET}")
    print(f"  {C.GREEN}[*] 5GHz: 8 señales activas{C.RESET}")
    print(f"  {C.GREEN}[*] 433MHz: 3 señales (IoT){C.RESET}")
    print(f"  {C.GREEN}[*] Anomalias detectadas: 0{C.RESET}")
