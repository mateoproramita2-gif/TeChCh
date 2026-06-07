import os
import sys
import socket
import time
import struct
import random
import threading
import concurrent.futures
from core.ui import C, slow_print, fast_print, progress_bar, spinner

def register_commands(reg):
    reg.register("net_sniff", netsniff_cmd, "net", ["ns", "sniff"],
                 "Captura y analisis de paquetes de red en tiempo real",
                 "net_sniff [--interface <iface>] [--count <n>]",
                 ["net_sniff --count 100"])

    reg.register("arp_spoofer", arpspoof_cmd, "net", ["arp", "arps"],
                 "Ataque ARP spoofing para interceptacion de trafico",
                 "arp_spoofer <target> <gateway>",
                 ["arp_spoofer 192.168.1.100 192.168.1.1"])

    reg.register("dns_spof", dnsspoof_cmd, "net", ["dns", "dnss"],
                 "Envenenamiento DNS para redireccionamiento",
                 "dns_spof <domain> <fake_ip>",
                 ["dns_spof example.com 192.168.1.100"])

    reg.register("packet_forge", packetforge_cmd, "net", ["pf", "forge"],
                 "Forgeo de paquetes IP/ICMP/TCP personalizados",
                 "packet_forge <type> [--src <ip>] [--dst <ip>] [--payload <data>]",
                 ["packet_forge icmp --src 10.0.0.1 --dst 10.0.0.2"])

    reg.register("mitm_attack", mitmcmd, "net", ["mitm"],
                 "Man-in-the-Middle con ARP poisoning y sniffing",
                 "mitm_attack <target>",
                 ["mitm_attack 192.168.1.100"])

    reg.register("net_jam", netjam_cmd, "net", ["nj", "jam"],
                 "Denegacion de servicio por inundacion de paquetes",
                 "net_jam <target> [--port <port>] [--packets <n>]",
                 ["net_jam 192.168.1.1 --port 80 --packets 1000"])

    reg.register("vlan_hopping", vlanhop_cmd, "net", ["vlan", "vh"],
                 "VLAN hopping para acceso a redes segmentadas",
                 "vlan_hopping <target>",
                 ["vlan_hopping 192.168.1.1"])

    reg.register("net_map", netmap_cmd, "net", ["nm", "nmap"],
                 "Mapeo de red con deteccion de servicios y firewalls",
                 "net_map <network>",
                 ["net_map 192.168.1.0/24"])

    reg.register("deauth", deauth_cmd, "net", ["deauth", "da"],
                 "Ataque de desautenticacion WiFi (802.11)",
                 "deauth <bssid> [--client <mac>]",
                 ["deauth AA:BB:CC:DD:EE:FF --client 11:22:33:44:55:66"])

    reg.register("tcp_hijack", tcphijack_cmd, "net", ["tj", "hijack"],
                 "Secuestro de sesiones TCP activas",
                 "tcp_hijack <target> [--port <port>]",
                 ["tcp_hijack 192.168.1.100 --port 80"])

    reg.register("net_recon", netrecon_cmd, "net", ["nr"],
                 "Reconocimiento de red con deteccion de dispositivos",
                 "net_recon <network>",
                 ["net_recon 192.168.1.0/24"])

    reg.register("port_knock", portknock_cmd, "net", ["pk", "knock"],
                 "Port knocking para abrir puertos ocultos",
                 "port_knock <target> --ports <p1,p2,...>",
                 ["port_knock 192.168.1.1 --ports 7000,8000,9000"])

    reg.register("net_island", netisland_cmd, "net", ["ni", "island"],
                 "Aislamiento de red contra dispositivos objetivo",
                 "net_island <target>",
                 ["net_island 192.168.1.100"])

    reg.register("syn_flood", synflood_cmd, "net", ["sf", "syn"],
                 "Ataque SYN flood para denegacion de servicio",
                 "syn_flood <target> [--port <port>] [--packets <n>]",
                 ["syn_flood 192.168.1.1 --port 80 --packets 5000"])

    reg.register("udp_flood", udpflood_cmd, "net", ["uf", "udpfl"],
                 "Ataque UDP flood de alta velocidad",
                 "udp_flood <target> [--port <port>] [--packets <n>]",
                 ["udp_flood 192.168.1.1 --port 53 --packets 10000"])

    reg.register("icmp_flood", icmpflood_cmd, "net", ["if", "icmpfl"],
                 "Ataque ICMP flood (ping flood)",
                 "icmp_flood <target> [--packets <n>]",
                 ["icmp_flood 192.168.1.1 --packets 5000"])

    reg.register("dhcp_starve", dhcpstarve_cmd, "net", ["ds", "dhcp"],
                 "Ataque DHCP starvation para agotar pool de IPs",
                 "dhcp_starve <network>",
                 ["dhcp_starve 192.168.1.0/24"])

    reg.register("llmnr_spoof", llmnrspoof_cmd, "net", ["llmnr"],
                 "Spoofing LLMNR/NBT-NS para captura de hashes",
                 "llmnr_spoof <network>",
                 ["llmnr_spoof 192.168.1.0/24"])

    reg.register("net_serve", netserve_cmd, "net", ["nsv", "serve"],
                 "Servidor HTTP/FTP temporal para exfiltracion",
                 "net_serve [--port <port>] [--type <http|ftp>]",
                 ["net_serve --port 8080 --type http"])

    reg.register("capture_hash", capturehash_cmd, "net", ["ch", "capture"],
                 "Captura de hashes NTLMv2 mediante relay",
                 "capture_hash [--listen <iface>]",
                 ["capture_hash --listen eth0"])

    reg.register("wol", wol_cmd, "net", ["wol", "wake"],
                 "Wake-on-Law para encender equipos remotamente",
                 "wol <mac_address>",
                 ["wol 00:1A:2B:3C:4D:5E"])

def netsniff_cmd(args):
    print(f"\n{C.CYAN}[+] Capturando paquetes de red...{C.RESET}\n")
    count = 10
    if "--count" in args:
        count = int(args[args.index("--count") + 1])

    protocols = ["TCP", "UDP", "ICMP", "ARP", "DNS", "HTTP", "HTTPS"]
    for i in range(count):
        proto = random.choice(protocols)
        src = f"192.168.1.{random.randint(1,254)}"
        dst = f"10.0.0.{random.randint(1,254)}"
        size = random.randint(40, 1500)
        print(f"  {C.GREEN}[{i+1:>4}]{C.RESET} {C.CYAN}{proto:<6}{C.WHITE} {src:<16} -> {dst:<16} {C.YELLOW}{size}B{C.RESET}")
        time.sleep(0.2)

    print(f"\n{C.GREEN}[+] {count} paquetes capturados{C.RESET}")

def arpspoof_cmd(args):
    if len(args) < 2:
        print(f"{C.RED}[!] Uso: arp_spoofer <target> <gateway>{C.RESET}")
        return
    target, gateway = args[0], args[1]
    print(f"\n{C.RED}[!] ARP Spoofing activado{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}{C.RESET}")
    print(f"  {C.CYAN}Gateway: {C.WHITE}{gateway}{C.RESET}")
    for i in range(10):
        print(f"  {C.YELLOW}[*] Enviando paquetes ARP falsificados... ({i+1}/10){C.RESET}")
        time.sleep(0.5)
    print(f"\n{C.GREEN}[+] ARP poisoning activo{C.RESET}")

def dnsspoof_cmd(args):
    if len(args) < 2:
        print(f"{C.RED}[!] Uso: dns_spof <domain> <fake_ip>{C.RESET}")
        return
    domain, fake_ip = args[0], args[1]
    print(f"\n{C.RED}[!] DNS Spoofing configurado{C.RESET}")
    print(f"  {C.CYAN}Dominio: {C.WHITE}{domain}{C.RESET}")
    print(f"  {C.CYAN}IP falsa: {C.WHITE}{fake_ip}{C.RESET}")
    print(f"  {C.GREEN}[*] Envenenamiento DNS activo{C.RESET}")

def packetforge_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: packet_forge <type> [--src <ip>] [--dst <ip>] [--payload <data>]{C.RESET}")
        return
    ptype = args[0].upper()
    src = "10.0.0.1"
    dst = "10.0.0.2"
    payload = "TEST"
    if "--src" in args:
        src = args[args.index("--src") + 1]
    if "--dst" in args:
        dst = args[args.index("--dst") + 1]
    if "--payload" in args:
        payload = args[args.index("--payload") + 1]

    print(f"\n{C.CYAN}[+] Forgeando paquete {ptype}{C.RESET}")
    print(f"  {C.CYAN}Src: {C.WHITE}{src}{C.RESET}")
    print(f"  {C.CYAN}Dst: {C.WHITE}{dst}{C.RESET}")
    print(f"  {C.CYAN}Payload: {C.WHITE}{payload}{C.RESET}")
    print(f"  {C.GREEN}[*] Paquete forjado exitosamente{C.RESET}")

def mitmcmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: mitm_attack <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.RED}[!] MITM Attack activado{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}{C.RESET}")
    print(f"  {C.YELLOW}[*] ARP Poisoning activo{C.RESET}")
    print(f"  {C.YELLOW}[*] Interceptando trafico...{C.RESET}")
    time.sleep(1)
    print(f"  {C.GREEN}[*] Capturando credenciales...{C.RESET}")
    print(f"  {C.GREEN}[+] Sesion interceptada{C.RESET}")

def netjam_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_jam <target> [--port <port>] [--packets <n>]{C.RESET}")
        return
    target = args[0]
    port = 80
    packets = 100
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--packets" in args:
        packets = int(args[args.index("--packets") + 1])

    print(f"\n{C.RED}[!] Network Jamming activado{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}:{port}{C.RESET}")
    print(f"  {C.CYAN}Paquetes: {C.WHITE}{packets}{C.RESET}")

    for i in range(min(packets, 20)):
        progress_bar(i+1, min(packets, 20), prefix="  Enviando")
        time.sleep(0.1)
    print(f"\n{C.GREEN}[+] {packets} paquetes enviados{C.RESET}")

def vlanhop_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: vlan_hopping <target>{C.RESET}")
        return
    print(f"\n{C.RED}[!] VLAN Hopping configurado{C.RESET}")
    print(f"  {C.CYAN}Tag: {C.WHITE}802.1Q{C.RESET}")
    print(f"  {C.CYAN}Modo: {C.WHITE}Double Tagging{C.RESET}")
    print(f"  {C.GREEN}[*] Acceso a VLANs adyacentes{C.RESET}")

def netmap_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_map <network>{C.RESET}")
        return
    network = args[0]
    print(f"\n{C.CYAN}[+] Mapeando red {C.WHITE}{network}{C.RESET}\n")
    devices = [
        ("192.168.1.1", "Router", "Cisco", "Activo"),
        ("192.168.1.10", "Servidor", "Linux", "Activo"),
        ("192.168.1.20", "PC-Windows", "Windows 10", "Activo"),
        ("192.168.1.30", "Impresora", "HP", "Activo"),
        ("192.168.1.50", "Camera", "Hikvision", "Activo"),
    ]
    print(f"  {'IP':<18}{'Tipo':<15}{'SO':<15}{'Estado':<10}")
    print(f"  {'─'*58}")
    for ip, dtype, os, status in devices:
        print(f"  {C.WHITE}{ip:<18}{dtype:<15}{os:<15}{C.GREEN}{status}{C.RESET}")
    print(f"\n  {C.GREEN}[+] {len(devices)} dispositivos detectados{C.RESET}")

def deauth_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: deauth <bssid> [--client <mac>]{C.RESET}")
        return
    bssid = args[0]
    print(f"\n{C.RED}[!] Deauthentication Attack{C.RESET}")
    print(f"  {C.CYAN}BSSID: {C.WHITE}{bssid}{C.RESET}")
    print(f"  {C.YELLOW}[*] Enviando tramas de desautenticacion...{C.RESET}")
    for i in range(10):
        print(f"  {C.RED}  Frame {i+1}: Deauth sent to {bssid}{C.RESET}")
        time.sleep(0.3)
    print(f"\n{C.GREEN}[+] Ataque completado{C.RESET}")

def tcphijack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: tcp_hijack <target> [--port <port>]{C.RESET}")
        return
    target = args[0]
    port = 80
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    print(f"\n{C.RED}[!] TCP Session Hijacking{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}:{port}{C.RESET}")
    print(f"  {C.YELLOW}[*] Interceptando secuencia TCP...{C.RESET}")
    print(f"  {C.YELLOW}[*] SEQ: {random.randint(1000000, 9999999)}{C.RESET}")
    print(f"  {C.GREEN}[+] Sesion secuestrada{C.RESET}")

def netrecon_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_recon <network>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Reconocimiento de red{C.RESET}")
    print(f"  {C.GREEN}[*] Dispositivos activos detectados{C.RESET}")
    print(f"  {C.WHITE}  192.168.1.1   - Gateway/Router{C.RESET}")
    print(f"  {C.WHITE}  192.168.1.10  - Servidor DHCP{C.RESET}")
    print(f"  {C.WHITE}  192.168.1.100 - Estacion de trabajo{C.RESET}")

def portknock_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: port_knock <target> --ports <p1,p2,...>{C.RESET}")
        return
    target = args[0]
    ports = "7000,8000,9000"
    if "--ports" in args:
        ports = args[args.index("--ports") + 1]
    print(f"\n{C.CYAN}[+] Port Knocking en {C.WHITE}{target}{C.RESET}")
    for port in ports.split(","):
        print(f"  {C.GREEN}[*] Knock en puerto {port.strip()}{C.RESET}")
        time.sleep(0.2)
    print(f"  {C.GREEN}[+] Puerto oculto abierto{C.RESET}")

def netisland_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_island <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.RED}[!] Aislamiento de red{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}{C.RESET}")
    print(f"  {C.YELLOW}[*] Bloqueando todo el trafico...{C.RESET}")
    print(f"  {C.GREEN}[+] {target} aislado de la red{C.RESET}")

def synflood_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: syn_flood <target> [--port <port>] [--packets <n>]{C.RESET}")
        return
    target = args[0]
    port = 80
    packets = 1000
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--packets" in args:
        packets = int(args[args.index("--packets") + 1])
    print(f"\n{C.RED}[!] SYN Flood Attack{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}:{port}{C.RESET}")
    print(f"  {C.CYAN}Paquetes: {C.WHITE}{packets}{C.RESET}")
    progress_bar(packets, packets, prefix="  Enviando SYN")
    print(f"\n{C.GREEN}[+] {packets} paquetes SYN enviados{C.RESET}")

def udpflood_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: udp_flood <target> [--port <port>] [--packets <n>]{C.RESET}")
        return
    target = args[0]
    port = 53
    packets = 1000
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--packets" in args:
        packets = int(args[args.index("--packets") + 1])
    print(f"\n{C.RED}[!] UDP Flood Attack{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}:{port}{C.RESET}")
    progress_bar(packets, packets, prefix="  Enviando UDP")
    print(f"\n{C.GREEN}[+] {packets} paquetes UDP enviados{C.RESET}")

def icmpflood_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: icmp_flood <target> [--packets <n>]{C.RESET}")
        return
    target = args[0]
    packets = 100
    if "--packets" in args:
        packets = int(args[args.index("--packets") + 1])
    print(f"\n{C.RED}[!] ICMP Flood Attack{C.RESET}")
    print(f"  {C.CYAN}Target: {C.WHITE}{target}{C.RESET}")
    progress_bar(packets, packets, prefix="  Enviando ICMP")
    print(f"\n{C.GREEN}[+] {packets} paquetes ICMP enviados{C.RESET}")

def dhcpstarve_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: dhcp_starve <network>{C.RESET}")
        return
    print(f"\n{C.RED}[!] DHCP Starvation Attack{C.RESET}")
    print(f"  {C.YELLOW}[*] Solicitando IPs con MACs aleatorios...{C.RESET}")
    for i in range(50):
        mac = ":".join(f"{random.randint(0,255):02x}" for _ in range(6))
        sys.stdout.write(f"\r  {C.DIM}MAC: {mac}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\n{C.GREEN}[+] Pool DHCP agotado{C.RESET}")

def llmnrspoof_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: llmnr_spoof <network>{C.RESET}")
        return
    print(f"\n{C.RED}[!] LLMNR/NBT-NS Spoofing{C.RESET}")
    print(f"  {C.YELLOW}[*] Escuchando consultas LLMNR...{C.RESET}")
    print(f"  {C.YELLOW}[*] Escuchando consultas NBT-NS...{C.RESET}")
    print(f"  {C.GREEN}[+] Responder activo - capturando hashes{C.RESET}")

def netserve_cmd(args):
    port = 8080
    stype = "http"
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--type" in args:
        stype = args[args.index("--type") + 1]
    print(f"\n{C.CYAN}[+] Servidor {stype.upper()} activo en puerto {port}{C.RESET}")
    print(f"  {C.DIM}URL: http://0.0.0.0:{port}{C.RESET}")
    print(f"  {C.DIM}Presione Ctrl+C para detener{C.RESET}")

def capturehash_cmd(args):
    print(f"\n{C.RED}[!] Captura de hashes NTLMv2{C.RESET}")
    print(f"  {C.YELLOW}[*] Escuchando en interfaz de red...{C.RESET}")
    print(f"  {C.YELLOW}[*] Esperando autenticaciones...{C.RESET}")
    print(f"  {C.GREEN}[+] Responder activo - relay listo{C.RESET}")

def wol_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: wol <mac_address>{C.RESET}")
        return
    mac = args[0]
    print(f"\n{C.CYAN}[+] Wake-on-LAN{C.RESET}")
    print(f"  {C.CYAN}MAC: {C.WHITE}{mac}{C.RESET}")
    print(f"  {C.GREEN}[*] Paquete magico enviado{C.RESET}")
    print(f"  {C.GREEN}[+] Dispositivo encendido remotamente{C.RESET}")
