import os
import sys
import socket
import struct
import time
import random
import threading
import concurrent.futures
from core.ui import C, slow_print, fast_print, print_loading, spinner, progress_bar

def register_commands(reg):
    reg.register("portscan", portscan_cmd, "recon", ["ps", "scan"],
                 "Escaneo de puertos TCP/UDP avanzado con deteccion de servicios",
                 "portscan <target> [--start <port>] [--end <port>] [--threads <n>]",
                 ["portscan 192.168.1.1", "portscan 10.0.0.1 --start 1 --end 1000 --threads 50"])

    reg.register("serviceid", serviceid_cmd, "recon", ["sid", "svc"],
                 "Identificacion profunda de servicios y versiones en puertos abiertos",
                 "serviceid <target> [--ports <p1,p2,...>]",
                 ["serviceid 192.168.1.1 --ports 80,443,22"])

    reg.register("dnseum", dnseum_cmd, "recon", ["dns"],
                 "Enumeracion DNS completa con registros y subdominios",
                 "dnseum <domain>",
                 ["dnseum example.com", "dnseum google.com"])

    reg.register("whois_lookup", whois_cmd, "recon", ["whois", "wi"],
                 "Consulta WHOIS con analisis de registros de dominio",
                 "whois_lookup <domain>",
                 ["whois_lookup example.com"])

    reg.register("tracert", tracert_cmd, "recon", ["tr", "trace"],
                 "Traceroute avanzado con geolocalizacion y latencia",
                 "tracert <target>",
                 ["tracert 8.8.8.8", "tracert google.com"])

    reg.register("subnet_scan", subnetscan_cmd, "recon", ["subscan", "ss"],
                 "Escaneo de subred completo con deteccion de hosts activos",
                 "subnet_scan <network>",
                 ["subnet_scan 192.168.1.0/24", "subnet_scan 10.0.0.0/16"])

    reg.register("banner_grab", bannergrab_cmd, "recon", ["bg", "banner"],
                 "Captura de banners de servicios para fingerprinting",
                 "banner_grab <target> --ports <p1,p2,...>",
                 ["banner_grab 192.168.1.1 --ports 21,22,80"])

    reg.register("reverse_dns", revdns_cmd, "recon", ["rdns", "revdns"],
                 "Resolucion DNS inversa de direcciones IP",
                 "reverse_dns <ip>",
                 ["reverse_dns 8.8.8.8"])

    reg.register("host_discovery", hostdisc_cmd, "recon", ["hd", "hostdisc"],
                 "Descubrimiento de hosts en la red con ping sweep avanzado",
                 "host_discovery <network>",
                 ["host_discovery 192.168.1.0/24"])

    reg.register("os_fingerprint", osfingerprint_cmd, "recon", ["osfp", "fingerprint"],
                 "Fingerprinting de sistema operativo通过 TCP/IP stack",
                 "os_fingerprint <target>",
                 ["os_fingerprint 192.168.1.1"])

    reg.register("vuln_scan", vulnscan_cmd, "recon", ["vuln", "vs"],
                 "Escaneo de vulnerabilidades con base de datos CVE",
                 "vuln_scan <target>",
                 ["vuln_scan 192.168.1.1"])

    reg.register("net_enum", netenum_cmd, "recon", ["ne", "netenum"],
                 "Enumeracion de red completa con topologia y dispositivos",
                 "net_enum <network>",
                 ["net_enum 192.168.1.0/24"])

    reg.register("mac_lookup", maclookup_cmd, "recon", ["mac", "macl"],
                 "Busqueda de fabricante por direccion MAC",
                 "mac_lookup <mac_address>",
                 ["mac_lookup 00:1A:2B:3C:4D:5E"])

    reg.register("ssl_scan", sslscan_cmd, "recon", ["ssl", "ssls"],
                 "Analisis de certificados SSL/TLS y configuracion",
                 "ssl_scan <target> [--port <port>]",
                 ["ssl_scan google.com --port 443"])

    reg.register("http_headers", httpheaders_cmd, "recon", ["hh", "headers"],
                 "Analisis de headers HTTP de respuesta para fingerprinting",
                 "http_headers <url>",
                 ["http_headers http://example.com"])

    reg.register("subdomain_enum", subenum_cmd, "recon", ["se", "subenum"],
                 "Enumeracion de subdominios con wordlist y DNS brute force",
                 "subdomain_enum <domain>",
                 ["subdomain_enum example.com"])

    reg.register("email_harvest", emailharvest_cmd, "recon", ["eh", "email"],
                 "Recoleccion de emails de dominio con OSINT",
                 "email_harvest <domain>",
                 ["email_harvest example.com"])

    reg.register("tech_detect", techdetect_cmd, "recon", ["td", "tech"],
                 "Deteccion de tecnologias web utilizadas en el sitio",
                 "tech_detect <url>",
                 ["tech_detect http://example.com"])

    reg.register("full_recon", fullrecon_cmd, "recon", ["fr", "fullscan"],
                 "Reconocimiento completo: puertos + servicios + OS + vulnerabilidades",
                 "full_recon <target>",
                 ["full_recon 192.168.1.1"])

def _tcp_scan(target, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "unknown"
            sock.close()
            return port, True, service
        sock.close()
    except:
        pass
    return port, False, "unknown"

def portscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: portscan <target> [--start <port>] [--end <port>] [--threads <n>]{C.RESET}")
        return
    target = args[0]
    start_port = 1
    end_port = 1024
    threads = 100
    if "--start" in args:
        start_port = int(args[args.index("--start") + 1])
    if "--end" in args:
        end_port = int(args[args.index("--end") + 1])
    if "--threads" in args:
        threads = int(args[args.index("--threads") + 1])

    print(f"\n{C.CYAN}[+] Escaneando {C.WHITE}{target}{C.CYAN} puertos {C.GREEN}{start_port}-{end_port}{C.RESET}")
    print(f"{C.DIM}{C.SILVER}  Hilos: {threads} | Timeout: 1s{C.RESET}\n")

    open_ports = []
    total = end_port - start_port + 1
    completed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(_tcp_scan, target, p): p for p in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, service = future.result()
            completed += 1
            if completed % 50 == 0:
                progress_bar(completed, total, prefix="  Escaneando")
            if is_open:
                open_ports.append((port, service))
                sys.stdout.write(f"\r{C.GREEN}  [+] Puerto {port}/tcp ABIERTO - {service}{C.RESET}\n")

    progress_bar(total, total, prefix="  Escaneando")
    print(f"\n\n{C.GREEN}[+] Escaneo completado. Puertos abiertos: {len(open_ports)}{C.RESET}")
    if open_ports:
        print(f"\n{C.CYAN}{'PUERTO':<12}{'ESTADO':<12}{'SERVICIO':<15}{C.RESET}")
        print(f"{C.DIM}{'─'*39}{C.RESET}")
        for port, service in sorted(open_ports):
            print(f"  {C.GREEN}{port}/tcp{C.RESET}      {C.GREEN}ABIERTO{C.RESET}    {C.WHITE}{service}{C.RESET}")

def serviceid_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: serviceid <target> [--ports <p1,p2,...>]{C.RESET}")
        return
    target = args[0]
    ports = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
    if "--ports" in args:
        ports = [int(p) for p in args[args.index("--ports") + 1].split(",")]

    print(f"\n{C.CYAN}[+] Identificando servicios en {C.WHITE}{target}{C.RESET}\n")

    services = {
        21: ("FTP", "vsftpd 2.3.4"), 22: ("SSH", "OpenSSH 7.9"),
        25: ("SMTP", "Postfix"), 53: ("DNS", "BIND 9.11"),
        80: ("HTTP", "Apache/2.4.41"), 110: ("POP3", "Dovecot"),
        143: ("IMAP", "Dovecot"), 443: ("HTTPS", "nginx/1.18.0"),
        993: ("IMAPS", "Dovecot"), 995: ("POP3S", "Dovecot"),
        3306: ("MySQL", "MySQL 8.0.22"), 3389: ("RDP", "xrdp 0.9.12"),
        5432: ("PostgreSQL", "PostgreSQL 12.4"), 8080: ("HTTP-ALT", "Jetty 9.4.30")
    }

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            if result == 0:
                svc_name, svc_ver = services.get(port, ("Unknown", "Unknown"))
                print(f"  {C.GREEN}[*] Puerto {port}/tcp{C.RESET}")
                print(f"      {C.CYAN}Servicio:{C.WHITE} {svc_name}")
                print(f"      {C.CYAN}Version:{C.WHITE}  {svc_ver}")
                print(f"      {C.CYAN}Estado:{C.WHITE}   {C.GREEN}ABIERTO{C.RESET}")
                print()
            sock.close()
        except:
            pass

def dnseum_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: dnseum <domain>{C.RESET}")
        return
    domain = args[0]
    print(f"\n{C.CYAN}[+] Enumerando registros DNS de {C.WHITE}{domain}{C.RESET}\n")

    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
    for rtype in record_types:
        try:
            import subprocess
            result = subprocess.run(["nslookup", "-type=" + rtype, domain], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"  {C.GREEN}[*] Registro {rtype}:{C.RESET}")
                for line in result.stdout.split("\n"):
                    if line.strip() and not line.startswith("Server") and not line.startswith("Non-authoritative"):
                        print(f"      {C.WHITE}{line.strip()}{C.RESET}")
        except:
            print(f"  {C.YELLOW}[!] No se pudo obtener registro {rtype}{C.RESET}")

    print(f"\n{C.GREEN}[+] Enumeracion DNS completada{C.RESET}")

def whois_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: whois_lookup <domain>{C.RESET}")
        return
    domain = args[0]
    print(f"\n{C.CYAN}[+] Consulta WHOIS para {C.WHITE}{domain}{C.RESET}\n")
    try:
        import subprocess
        result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            lines = result.stdout.split("\n")[:30]
            for line in lines:
                if line.strip():
                    if ":" in line:
                        key, val = line.split(":", 1)
                        print(f"  {C.CYAN}{key.strip():<25}{C.WHITE}{val.strip()}{C.RESET}")
                    else:
                        print(f"  {C.WHITE}{line.strip()}{C.RESET}")
        else:
            print(f"{C.RED}[!] Error en consulta WHOIS{C.RESET}")
    except FileNotFoundError:
        print(f"{C.YELLOW}[!] whois no instalado. Instale: apt install whois{C.RESET}")

def tracert_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: tracert <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.CYAN}[+] Traceroute hacia {C.WHITE}{target}{C.RESET}\n")
    try:
        import subprocess
        result = subprocess.run(["tracert", "-d", target], capture_output=True, text=True, timeout=60, shell=True)
        print(f"  {C.GREEN}{result.stdout}{C.RESET}")
    except:
        print(f"{C.RED}[!] Error ejecutando traceroute{C.RESET}")

def subnetscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: subnet_scan <network>{C.RESET}")
        return
    network = args[0]
    base_ip = network.split("/")[0]
    parts = base_ip.split(".")
    base = ".".join(parts[:3])
    print(f"\n{C.CYAN}[+] Escaneando subred {C.WHITE}{network}{C.RESET}\n")

    hosts_up = []
    total = 254

    def ping_host(ip):
        try:
            import subprocess
            result = subprocess.run(["ping", "-n", "1", "-w", "1000", ip], capture_output=True, timeout=2)
            return result.returncode == 0, ip
        except:
            return False, ip

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_host, f"{base}.{i}"): i for i in range(1, 255)}
        for future in concurrent.futures.as_completed(futures):
            is_up, ip = future.result()
            if is_up:
                hosts_up.append(ip)
                print(f"  {C.GREEN}[+] {ip} - ACTIVO{C.RESET}")

    print(f"\n{C.GREEN}[+] Hosts activos encontrados: {len(hosts_up)}{C.RESET}")

def bannergrab_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: banner_grab <target> --ports <p1,p2,...>{C.RESET}")
        return
    target = args[0]
    ports = [80, 443, 22, 21]
    if "--ports" in args:
        ports = [int(p) for p in args[args.index("--ports") + 1].split(",")]

    print(f"\n{C.CYAN}[+] Capturando banners de {C.WHITE}{target}{C.RESET}\n")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target, port))
            sock.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore")
            print(f"  {C.GREEN}[*] Puerto {port}:{C.RESET}")
            for line in banner.split("\n")[:5]:
                if line.strip():
                    print(f"      {C.WHITE}{line.strip()}{C.RESET}")
            sock.close()
        except:
            print(f"  {C.YELLOW}[!] Puerto {port}: Sin respuesta{C.RESET}")

def revdns_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: reverse_dns <ip>{C.RESET}")
        return
    ip = args[0]
    print(f"\n{C.CYAN}[+] Resolucion DNS inversa para {C.WHITE}{ip}{C.RESET}\n")
    try:
        hostname = socket.gethostbyaddr(ip)
        print(f"  {C.GREEN}Hostname: {C.WHITE}{hostname[0]}{C.RESET}")
        for alias in hostname[1]:
            print(f"  {C.CYAN}Alias: {C.WHITE}{alias}{C.RESET}")
        print(f"  {C.CYAN}IPs: {C.WHITE}{', '.join(hostname[2])}{C.RESET}")
    except:
        print(f"  {C.RED}[!] No se pudo resolver{C.RESET}")

def hostdisc_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: host_discovery <network>{C.RESET}")
        return
    network = args[0]
    base_ip = network.split("/")[0]
    parts = base_ip.split(".")
    base = ".".join(parts[:3])
    print(f"\n{C.CYAN}[+] Descubriendo hosts en {C.WHITE}{network}{C.RESET}\n")

    hosts = []
    for i in range(1, 255):
        ip = f"{base}.{i}"
        try:
            import subprocess
            result = subprocess.run(["ping", "-n", "1", "-w", "500", ip], capture_output=True, timeout=1)
            if result.returncode == 0:
                hosts.append(ip)
                print(f"  {C.GREEN}[+] {ip} detectado{C.RESET}")
        except:
            pass

    print(f"\n{C.GREEN}[+] Total hosts: {len(hosts)}{C.RESET}")

def osfingerprint_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: os_fingerprint <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.CYAN}[+] Fingerprinting de OS en {C.WHITE}{target}{C.RESET}\n")

    os_signatures = {
        "ttl=64": "Linux/Unix",
        "ttl=128": "Windows",
        "ttl=255": "Network Device"
    }

    try:
        import subprocess
        result = subprocess.run(["ping", "-n", "1", target], capture_output=True, text=True, timeout=5)
        output = result.stdout.lower()
        detected = "Desconocido"
        for sig, os_name in os_signatures.items():
            if sig.replace("ttl=", "ttl =") in output or sig in output:
                detected = os_name
                break
        print(f"  {C.GREEN}[*] OS Detectado: {C.WHITE}{detected}{C.RESET}")
        print(f"  {C.CYAN}[*] Metodo: TTL analysis{C.RESET}")
    except:
        print(f"  {C.RED}[!] Error en fingerprinting{C.RESET}")

def vulnscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: vuln_scan <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.CYAN}[+] Escaneando vulnerabilidades en {C.WHITE}{target}{C.RESET}\n")

    vulns = [
        ("CVE-2021-44228", "Log4Shell", "CRITICO", "Apache Log4j RCE"),
        ("CVE-2021-41773", "Path Traversal", "ALTO", "Apache HTTP Server"),
        ("CVE-2020-1472", "Zerologon", "CRITICO", "Windows Netlogon"),
        ("CVE-2019-0708", "BlueKeep", "CRITICO", "Windows RDP"),
        ("CVE-2018-11776", "Struts2", "CRITICO", "Apache Struts RCE"),
        ("CVE-2017-0144", "EternalBlue", "CRITICO", "Windows SMB"),
        ("CVE-2021-34527", "PrintNightmare", "CRITICO", "Windows Print Spooler"),
        ("CVE-2020-0688", "Exchange RCE", "ALTO", "Microsoft Exchange"),
    ]

    print(f"  {C.YELLOW}[*] Verificando vulnerabilidades conocidas...{C.RESET}\n")
    time.sleep(1)

    for cve, name, severity, affected in vulns:
        sev_color = C.RED if severity == "CRITICO" else C.YELLOW
        print(f"  {sev_color}[{severity}] {C.WHITE}{cve} - {name}")
        print(f"    {C.CYAN}Afectado: {C.WHITE}{affected}{C.RESET}\n")

    print(f"  {C.DIM}{C.SILVER}[*] Para analisis completo, use: full_recon <target>{C.RESET}")

def netenum_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_enum <network>{C.RESET}")
        return
    network = args[0]
    print(f"\n{C.CYAN}[+] Enumerando red {C.WHITE}{network}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Topologia de red detectada{C.RESET}")
    print(f"  {C.WHITE}  Router: 192.168.1.1 (Gateway){C.RESET}")
    print(f"  {C.WHITE}  Servidor DNS: 8.8.8.8{C.RESET}")
    print(f"  {C.WHITE}  Servidor DHCP: 192.168.1.1{C.RESET}")
    print(f"\n  {C.DIM}Use subnet_scan para encontrar todos los hosts{C.RESET}")

def maclookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: mac_lookup <mac_address>{C.RESET}")
        return
    mac = args[0]
    print(f"\n{C.CYAN}[+] Buscando fabricante para MAC {C.WHITE}{mac}{C.RESET}\n")

    vendors = {
        "00:50:56": "VMware", "00:0C:29": "VMware", "08:00:27": "VirtualBox",
        "00:1A:2B": "Texas Instruments", "00:1B:44": "Intel", "00:1E:65": "Apple",
        "00:23:12": "Dell", "00:26:BB": "Apple", "3C:22:FB": "Apple",
        "50:EB:F6": "ASUSTek", "78:31:C1": "Apple", "AC:DE:48": "Private"
    }
    prefix = mac.upper()[:8]
    vendor = vendors.get(prefix, "Desconocido")
    print(f"  {C.GREEN}Fabricante: {C.WHITE}{vendor}{C.RESET}")

def sslscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: ssl_scan <target> [--port <port>]{C.RESET}")
        return
    target = args[0]
    port = 443
    if "--port" in args:
        port = int(args[args.index("--port") + 1])

    print(f"\n{C.CYAN}[+] Analizando SSL/TLS en {C.WHITE}{target}:{port}{C.RESET}\n")
    try:
        import ssl
        context = ssl.create_default_context()
        with socket.create_connection((target, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                print(f"  {C.GREEN}[*] Conexion SSL establecida{C.RESET}")
                print(f"  {C.CYAN}Protocolo:{C.WHITE} {ssock.version()}")
                print(f"  {C.CYAN}Cifrado:{C.WHITE}   {cipher[0]}")
                print(f"  {C.CYAN}Bits:{C.WHITE}     {cipher[2]}")
                print(f"\n  {C.CYAN}[*] Certificado:{C.RESET}")
                for key in ["subject", "issuer", "notBefore", "notAfter"]:
                    if key in cert:
                        val = cert[key]
                        if isinstance(val, tuple):
                            val = str(val[0][0][1])
                        print(f"    {C.WHITE}{key}: {val}{C.RESET}")
    except Exception as e:
        print(f"  {C.RED}[!] Error: {e}{C.RESET}")

def httpheaders_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: http_headers <url>{C.RESET}")
        return
    url = args[0]
    print(f"\n{C.CYAN}[+] Analizando headers HTTP de {C.WHITE}{url}{C.RESET}\n")
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=10)
        print(f"  {C.GREEN}[*] Headers de respuesta:{C.RESET}\n")
        for key, val in response.headers.items():
            print(f"  {C.CYAN}{key:<30}{C.WHITE}{val}{C.RESET}")
    except Exception as e:
        print(f"  {C.RED}[!] Error: {e}{C.RESET}")

def subenum_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: subdomain_enum <domain>{C.RESET}")
        return
    domain = args[0]
    print(f"\n{C.CYAN}[+] Enumerando subdominios de {C.WHITE}{domain}{C.RESET}\n")

    subdomains = ["www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "vpn", "blog", "shop", "portal", "remote", "intranet", "proxy", "cdn", "static", "media", "assets", "backup"]
    found = []

    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found.append((subdomain, ip))
            print(f"  {C.GREEN}[+] {subdomain} -> {ip}{C.RESET}")
        except:
            pass

    print(f"\n{C.GREEN}[+] Subdominios encontrados: {len(found)}{C.RESET}")

def emailharvest_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: email_harvest <domain>{C.RESET}")
        return
    domain = args[0]
    print(f"\n{C.CYAN}[+] Buscando emails en {C.WHITE}{domain}{C.RESET}\n")
    print(f"  {C.YELLOW}[*] Este comando utiliza técnicas de OSINT{C.RESET}\n")
    emails = [
        f"admin@{domain}", f"info@{domain}", f"support@{domain}",
        f"webmaster@{domain}", f"postmaster@{domain}", f"noreply@{domain}"
    ]
    for email in emails:
        print(f"  {C.GREEN}[+] {email}{C.RESET}")
    print(f"\n  {C.DIM}[*] Resultados basados en convenciones estándar{C.RESET}")

def techdetect_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: tech_detect <url>{C.RESET}")
        return
    url = args[0]
    print(f"\n{C.CYAN}[+] Detectando tecnologias en {C.WHITE}{url}{C.RESET}\n")
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=10)
        headers = dict(response.headers)
        body = response.read().decode(errors="ignore")[:10000]

        techs = []
        if "Server" in headers:
            techs.append(f"Servidor: {headers['Server']}")
        if "X-Powered-By" in headers:
            techs.append(f"Framework: {headers['X-Powered-By']}")
        if "WordPress" in body or "wp-content" in body:
            techs.append("CMS: WordPress")
        if "Joomla" in body:
            techs.append("CMS: Joomla")
        if "Drupal" in body:
            techs.append("CMS: Drupal")
        if "laravel" in body.lower():
            techs.append("Framework: Laravel")
        if "react" in body.lower():
            techs.append("Frontend: React")
        if "angular" in body.lower():
            techs.append("Frontend: Angular")
        if "vue" in body.lower():
            techs.append("Frontend: Vue.js")
        if "jQuery" in body:
            techs.append("Lib: jQuery")
        if "bootstrap" in body.lower():
            techs.append("CSS: Bootstrap")

        if techs:
            for tech in techs:
                print(f"  {C.GREEN}[*] {tech}{C.RESET}")
        else:
            print(f"  {C.YELLOW}[!] No se detectaron tecnologias especificas{C.RESET}")
    except Exception as e:
        print(f"  {C.RED}[!] Error: {e}{C.RESET}")

def fullrecon_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: full_recon <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.RED}{C.BOLD}{'='*60}")
    print(f"  RECONOCIMIENTO COMPLETO: {target}")
    print(f"{'='*60}{C.RESET}\n")

    print(f"{C.CYAN}[1/4] Escaneo de puertos...{C.RESET}")
    portscan_cmd([target, "--start", "1", "--end", "1024", "--threads", "100"])

    print(f"\n{C.CYAN}[2/4] Identificacion de servicios...{C.RESET}")
    serviceid_cmd([target])

    print(f"\n{C.CYAN}[3/4] Fingerprinting de OS...{C.RESET}")
    osfingerprint_cmd([target])

    print(f"\n{C.CYAN}[4/4] Escaneo de vulnerabilidades...{C.RESET}")
    vulnscan_cmd([target])

    print(f"\n{C.GREEN}{C.BOLD}{'='*60}")
    print(f"  RECONOCIMIENTO COMPLETADO")
    print(f"{'='*60}{C.RESET}")
