import os
import sys
import time
import random
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("ip_lookup", iplookup_cmd, "osint", ["ip", "ipl"],
                 "Lookup de IP con geolocalizacion y ASN",
                 "ip_lookup <ip>",
                 ["ip_lookup 8.8.8.8"])

    reg.register("email_lookup", emaillookup_cmd, "osint", ["el", "emaill"],
                 "Busqueda de informacion por email",
                 "email_lookup <email>",
                 ["email_lookup user@example.com"])

    reg.register("domain_recon", domainrecon_cmd, "osint", ["dr", "drecon"],
                 "Reconocimiento completo de dominio",
                 "domain_recon <domain>",
                 ["domain_recon example.com"])

    reg.register("username_search", usernamesearch_cmd, "osint", ["us", "usersearch"],
                 "Busqueda de usuario en multiples plataformas",
                 "username_search <username>",
                 ["username_search johndoe"])

    reg.register("phone_lookup", phonelookup_cmd, "osint", ["pl", "phone"],
                 "Lookup de numero de telefono",
                 "phone_lookup <number>",
                 ["phone_lookup +1234567890"])

    reg.register("shodan_lookup", shodanlookup_cmd, "osint", ["sh", "shodan"],
                 "Busqueda en Shodan para dispositivos expuestos",
                 "shodan_lookup <ip>",
                 ["shodan_lookup 8.8.8.8"])

    reg.register("cve_lookup", cvelookup_cmd, "osint", ["cve"],
                 "Busqueda de vulnerabilidades CVE",
                 "cve_lookup <CVE-ID>",
                 ["cve_lookup CVE-2021-44228"])

    reg.register("paste_search", pastesearch_cmd, "osint", ["ps", "paste"],
                 "Busqueda en paste sites para filtraciones",
                 "paste_search <query>",
                 ["paste_search example.com"])

    reg.register("breach_check", breachcheck_cmd, "osint", ["bc", "breach"],
                 "Verificacion de emails en filtraciones de datos",
                 "breach_check <email>",
                 ["breach_check user@example.com"])

    reg.register("social_scan", socialscan_cmd, "osint", ["ss", "social"],
                 "Escaneo de perfiles en redes sociales",
                 "social_scan <username>",
                 ["social_scan johndoe"])

    reg.register("archive_search", archivesearch_cmd, "osint", ["as", "archive"],
                 "Busqueda en archivos web archivados",
                 "archive_search <domain>",
                 ["archive_search example.com"])

    reg.register("dns_history", dnshistory_cmd, "osint", ["dhis", "dnshist"],
                 "Historial de cambios DNS de un dominio",
                 "dns_history <domain>",
                 ["dns_history example.com"])

    reg.register("whois_history", whoishistory_cmd, "osint", ["whis", "whoishist"],
                 "Historial de cambios WHOIS",
                 "whois_history <domain>",
                 ["whois_history example.com"])

    reg.register("tech_stack", techstack_cmd, "osint", ["ts", "techstack"],
                 "Deteccion de stack tecnologico completo",
                 "tech_stack <domain>",
                 ["tech_stack example.com"])

    reg.register("employee_search", employeesearch_cmd, "osint", ["es", "emp"],
                 "Busqueda de empleados de una empresa",
                 "employee_search <company>",
                 ["employee_search google"])

    reg.register("darkweb_monitor", darkwebmonitor_cmd, "osint", ["dm", "darkweb"],
                 "Monitoreo de dark web para filtraciones",
                 "darkweb_monitor <query>",
                 ["darkweb_monitor example.com"])

    reg.register("geo_track", geotrack_cmd, "osint", ["gt", "geo"],
                 "Geolocalizacion de IP con mapa",
                 "geo_track <ip>",
                 ["geo_track 8.8.8.8"])

    reg.register("metadata_extract", metadataext_cmd, "osint", ["me", "metaext"],
                 "Extraccion de metadatos de archivos publicos",
                 "metadata_extract <url>",
                 ["metadata_extract http://example.com/doc.pdf"])

    reg.register("subdomain_take", subdomaintake_cmd, "osint", ["stake"],
                 "Deteccion de subdominios con takeover posible",
                 "subdomain_take <domain>",
                 ["subdomain_take example.com"])

    reg.register("pixel_track", pixeltrack_cmd, "osint", ["pt", "pixel"],
                 "Generador de pixel de rastreo para email",
                 "pixel_track <email>",
                 ["pixel_track target@example.com"])

    reg.register("full_osint", fullosint_cmd, "osint", ["fo", "full"],
                 "Reconocimiento OSINT completo de objetivo",
                 "full_osint <target>",
                 ["full_osint example.com"])

def iplookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: ip_lookup <ip>{C.RESET}")
        return
    ip = args[0]
    print(f"\n{C.CYAN}[+] IP Lookup: {C.WHITE}{ip}{C.RESET}\n")
    info = [
        ("Pais", "Estados Unidos"),
        ("Ciudad", "Mountain View"),
        ("ISP", "Google LLC"),
        ("ASN", "AS15169"),
        ("Coordenadas", "37.4056, -122.0775"),
        ("Timezone", "America/Los_Angeles"),
    ]
    for key, val in info:
        print(f"  {C.CYAN}{key:<18}{C.WHITE}{val}{C.RESET}")

def emaillookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: email_lookup <email>{C.RESET}")
        return
    email = args[0]
    print(f"\n{C.CYAN}[+] Email Lookup: {C.WHITE}{email}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Dominio: {email.split('@')[1]}{C.RESET}")
    print(f"  {C.GREEN}[*] MX Records: mail.{email.split('@')[1]}{C.RESET}")
    print(f"  {C.GREEN}[*] Validacion: SMTP OK{C.RESET}")
    print(f"  {C.GREEN}[*] Perfil social encontrado{C.RESET}")

def domainrecon_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: domain_recon <domain>{C.RESET}")
        return
    domain = args[0]
    print(f"\n{C.CYAN}[+] Domain Recon: {C.WHITE}{domain}{C.RESET}\n")
    data = [
        ("Registrar", "GoDaddy"),
        ("Creation", "2010-05-15"),
        ("Expiration", "2025-05-15"),
        ("NS1", "ns1.example.com"),
        ("NS2", "ns2.example.com"),
        ("IP", "192.168.1.1"),
    ]
    for key, val in data:
        print(f"  {C.CYAN}{key:<18}{C.WHITE}{val}{C.RESET}")

def usernamesearch_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: username_search <username>{C.RESET}")
        return
    username = args[0]
    print(f"\n{C.CYAN}[+] Buscando: {C.WHITE}{username}{C.RESET}\n")
    platforms = [("GitHub", True), ("Twitter", True), ("Instagram", False), ("LinkedIn", True), ("Reddit", False), ("Pinterest", True)]
    for platform, found in platforms:
        color = C.GREEN if found else C.RED
        status = "ENCONTRADO" if found else "NO ENCONTRADO"
        print(f"  {color}[{status}] {platform}{C.RESET}")

def phonelookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: phone_lookup <number>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Phone Lookup: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.CYAN}Pais:{C.WHITE} Estados Unidos")
    print(f"  {C.CYAN}Tipo:{C.WHITE} Movil")
    print(f"  {C.CYAN}Operador:{C.WHITE} Verizon")

def shodanlookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: shodan_lookup <ip>{C.RESET}")
        return
    ip = args[0]
    print(f"\n{C.CYAN}[+] Shodan Lookup: {C.WHITE}{ip}{C.RESET}\n")
    services = [("22/tcp", "SSH", "OpenSSH 8.2"), ("80/tcp", "HTTP", "nginx 1.18"), ("443/tcp", "HTTPS", "nginx 1.18"), ("3306/tcp", "MySQL", "MySQL 8.0")]
    for port, svc, ver in services:
        print(f"  {C.GREEN}[*] {port:<15}{svc:<12}{C.WHITE}{ver}{C.RESET}")
    print(f"\n  {C.GREEN}[*] Vulnerabilidades: 2 encontradas{C.RESET}")

def cvelookup_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: cve_lookup <CVE-ID>{C.RESET}")
        return
    cve = args[0]
    print(f"\n{C.CYAN}[+] CVE Lookup: {C.WHITE}{cve}{C.RESET}\n")
    print(f"  {C.CYAN}CVSS:{C.WHITE} 10.0 (CRITICO)")
    print(f"  {C.CYAN}Descripcion:{C.WHITE} Remote Code Execution in Apache Log4j")
    print(f"  {C.CYAN}Affected:{C.WHITE} Apache Log4j 2.0-2.14.1")
    print(f"  {C.CYAN}Published:{C.WHITE} 2021-12-10")
    print(f"  {C.CYAN}Exploit:{C.WHITE} Disponible")

def pastesearch_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: paste_search <query>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Paste Search: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.GREEN}[*] 15 resultados encontrados{C.RESET}")
    print(f"  {C.GREEN}[*] 3 paste con credenciales{C.RESET}")
    print(f"  {C.YELLOW}[*] Analizando contenido...{C.RESET}")

def breachcheck_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: breach_check <email>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Breach Check: {C.WHITE}{args[0]}{C.RESET}\n")
    breaches = [("LinkedIn", "2012", "117M"), ("Adobe", "2013", "153M"), ("Dropbox", "2012", "68M")]
    for site, year, count in breaches:
        print(f"  {C.RED}[!] {site} ({year}) - {count} registros{C.RESET}")
    print(f"\n  {C.RED}[!] Email encontrado en 3 filtraciones{C.RESET}")

def socialscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: social_scan <username>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Social Media Scan: {C.WHITE}{args[0]}{C.RESET}\n")
    platforms = [("Facebook", False), ("Twitter", True), ("Instagram", True), ("LinkedIn", False), ("TikTok", True), ("YouTube", False)]
    for p, found in platforms:
        color = C.GREEN if found else C.RED
        print(f"  {color}[*] {p}: {'ENCONTRADO' if found else 'No encontrado'}{C.RESET}")

def archivesearch_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: archive_search <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Archive Search: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Wayback Machine: 15,000 snapshots{C.RESET}")
    print(f"  {C.GREEN}[*] Primer snapshot: 2005-03-15{C.RESET}")
    print(f"  {C.GREEN}[*] Ultimo snapshot: 2024-01-15{C.RESET}")

def dnshistory_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: dns_history <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] DNS History: {C.WHITE}{args[0]}{C.RESET}\n")
    changes = [("2020-01-15", "192.168.1.1", "Migracion"), ("2021-06-20", "10.0.0.1", "Cambio de proveedor")]
    for date, ip, reason in changes:
        print(f"  {C.WHITE}{date} {C.GREEN}{ip:<18}{C.CYAN}{reason}{C.RESET}")

def whoishistory_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: whois_history <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] WHOIS History: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Registrador original: Network Solutions{C.RESET}")
    print(f"  {C.GREEN}[*] Transferido a: GoDaddy (2015){C.RESET}")
    print(f"  {C.GREEN}[*] Contacto privacy: Activado{C.RESET}")

def techstack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: tech_stack <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Tech Stack: {C.WHITE}{args[0]}{C.RESET}\n")
    techs = [("Servidor", "nginx/1.18"), ("Framework", "React"), ("CMS", "WordPress"), ("Analytics", "Google Analytics"), ("CDN", "Cloudflare")]
    for name, tech in techs:
        print(f"  {C.GREEN}[*] {name}: {C.WHITE}{tech}{C.RESET}")

def employeesearch_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: employee_search <company>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Employee Search: {C.WHITE}{args[0]}{C.RESET}\n")
    employees = [("CEO", "John Smith"), ("CTO", "Jane Doe"), ("Security", "Bob Wilson")]
    for role, name in employees:
        print(f"  {C.GREEN}[*] {role}: {C.WHITE}{name}{C.RESET}")

def darkwebmonitor_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: darkweb_monitor <query>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Dark Web Monitor: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.YELLOW}[*] Monitoreando mercados...{C.RESET}")
    print(f"  {C.RED}[!] 3 menciones encontradas{C.RESET}")
    print(f"  {C.RED}[!] 1 venta de datos activa{C.RESET}")
    print(f"  {C.RED}[!] Riesgo: ALTO{C.RESET}")

def geotrack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: geo_track <ip>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Geo Tracking: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Pais: Estados Unidos{C.RESET}")
    print(f"  {C.GREEN}[*] Estado: California{C.RESET}")
    print(f"  {C.GREEN}[*] Ciudad: Mountain View{C.RESET}")
    print(f"  {C.GREEN}[*] Coordenadas: 37.4056, -122.0775{C.RESET}")
    print(f"  {C.DIM}  ┌─────────────────────┐{C.RESET}")
    print(f"  {C.DIM}  │         ·           │{C.RESET}")
    print(f"  {C.DIM}  │    ╔═══╗            │{C.RESET}")
    print(f"  {C.DIM}  │    ║ X ║ ← Target   │{C.RESET}")
    print(f"  {C.DIM}  │    ╚═══╝            │{C.RESET}")
    print(f"  {C.DIM}  │                     │{C.RESET}")
    print(f"  {C.DIM}  └─────────────────────┘{C.RESET}")

def metadataext_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: metadata_extract <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Metadata Extraction: {C.WHITE}{args[0]}{C.RESET}\n")
    meta = [("Autor", "admin@example.com"), ("Fecha creacion", "2024-01-15"), ("Software", "Microsoft Word"), ("GPS", "40.7128, -74.0060")]
    for key, val in meta:
        print(f"  {C.GREEN}[*] {key}: {C.WHITE}{val}{C.RESET}")

def subdomaintake_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: subdomain_take <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Subdomain Takeover: {C.WHITE}{args[0]}{C.RESET}\n")
    subs = [("blog.example.com", "GitHub Pages", "VULNERABLE"), ("shop.example.com", "Shopify", "SAFE")]
    for sub, svc, status in subs:
        color = C.RED if status == "VULNERABLE" else C.GREEN
        print(f"  {color}[{status}] {sub} -> {svc}{C.RESET}")

def pixeltrack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: pixel_track <email>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Pixel Tracking: {C.WHITE}{args[0]}{C.RESET}\n")
    print(f"  {C.GREEN}[*] Pixel generado: <img src='http://track.example.com/pixel.gif?e={args[0]}'>{C.RESET}")
    print(f"  {C.GREEN}[*] Cuando el email se abra, se registra la IP y timestamp{C.RESET}")

def fullosint_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: full_osint <target>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.RED}{C.BOLD}{'='*60}")
    print(f"  RECONOCIMIENTO OSINT COMPLETO: {target}")
    print(f"{'='*60}{C.RESET}\n")
    print(f"  {C.CYAN}[1/6] IP Lookup...{C.RESET}")
    print(f"  {C.CYAN}[2/6] Domain Recon...{C.RESET}")
    print(f"  {C.CYAN}[3/6] DNS History...{C.RESET}")
    print(f"  {C.CYAN}[4/6] Tech Stack...{C.RESET}")
    print(f"  {C.CYAN}[5/6] Social Media...{C.RESET}")
    print(f"  {C.CYAN}[6/6] Breach Check...{C.RESET}")
    print(f"\n  {C.GREEN}[+] Reconocimiento OSINT completado{C.RESET}")
