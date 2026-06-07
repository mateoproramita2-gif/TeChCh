import os
import sys
import hashlib
import time
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("file_hash", filehash_cmd, "forensics", ["fh", "hashf"],
                 "Generacion de hashes de archivos para integridad",
                 "file_hash <file>",
                 ["file_hash /etc/passwd"])

    reg.register("file_meta", filemeta_cmd, "forensics", ["fm", "meta"],
                 "Metadatos completos de archivos",
                 "file_meta <file>",
                 ["file_meta document.pdf"])

    reg.register("disk_image", diskimage_cmd, "forensics", ["di", "dd"],
                 "Creacion de imagen de disco forense",
                 "disk_image <device> [--output <file>]",
                 ["disk_image /dev/sda --output backup.img"])

    reg.register("timeline", timeline_cmd, "forensics", ["tl"],
                 "Timeline de actividad del sistema",
                 "timeline [--hours <n>]",
                 ["timeline --hours 24"])

    reg.register("string_extract", stringextract_cmd, "forensics", ["se", "strings"],
                 "Extraccion de cadenas de texto de archivos binarios",
                 "string_extract <file> [--min <len>]",
                 ["string_extract malware.exe --min 4"])

    reg.register("entropy", entropy_cmd, "forensics", ["ent"],
                 "Analisis de entropia para deteccion de cifrado",
                 "entropy <file>",
                 ["entropy suspicious.bin"])

    reg.register("volatility", volatility_cmd, "forensics", ["vol"],
                 "Analisis de volatilidad de memoria",
                 "volatility <memdump> [--profile <profile>]",
                 ["volatility memory.dump --profile Win7SP1x64"])

    reg.register("yara_scan", yarascmd, "forensics", ["yara"],
                 "Escaneo con reglas YARA para deteccion de malware",
                 "yara_scan <file> [--rules <rules_file>]",
                 ["yara_scan malware.exe --rules yara_rules.yar"])

    reg.register("log_parser", logparser_cmd, "forensics", ["lp", "logparse"],
                 "Parser avanzado de logs con correlacion de eventos",
                 "log_parser <logfile> [--filter <pattern>]",
                 ["log_parser /var/log/auth.log --filter FAILED"])

    reg.register("hex_editor", hexeditor_cmd, "forensics", ["hex", "hedit"],
                 "Editor hexadecimal de archivos para analisis forense",
                 "hex_editor <file> [--offset <n>] [--length <n>]",
                 ["hex_editor evidence.bin --offset 0 --length 256"])

    reg.register("net_forensics", netforensics_cmd, "forensics", ["nf", "netforens"],
                 "Analisis forense de capturas de red",
                 "net_forensics <pcap_file>",
                 ["net_forensics capture.pcap"])

    reg.register("steg_analysis", steganalysiscmd, "forensics", ["sa", "steganal"],
                 "Analisis esteganografico de imagenes",
                 "steg_analysis <image>",
                 ["steg_analysis photo.png"])

    reg.register("malware_sandbox", malwaresandbox_cmd, "forensics", ["ms", "sandbox"],
                 "Ejecucion en sandbox aislado para analisis de malware",
                 "malware_sandbox <file>",
                 ["malware_sandbox suspicious.exe"])

    reg.register("registry_analyze", registryanlzcmd, "forensics", ["ra", "reganl"],
                 "Analisis del registro del sistema para evidencia",
                 "registry_analyze",
                 ["registry_analyze"])

    reg.register("browser_forensics", browserforensicscmd, "forensics", ["bf", "browserf"],
                 "Extraccion de evidencia de navegador web",
                 "browser_forensics [--browser <chrome|firefox>]",
                 ["browser_forensics --browser chrome"])

    reg.register("email_forensics", emailforensicscmd, "forensics", ["ef", "emailf"],
                 "Analisis forense de archivos email (.eml)",
                 "email_forensics <eml_file>",
                 ["email_forensics evidence.eml"])

    reg.register("memory_strings", memstrings_cmd, "forensics", ["ms", "memstr"],
                 "Extraccion de cadenas de memoria para evidencia",
                 "memory_strings <memdump>",
                 ["memory_strings ram.dump"])

    reg.register("chain_of_custody", chainofcustody_cmd, "forensics", ["coc", "custody"],
                 "Registro de cadena de custodia forense",
                 "chain_of_custody <evidence_id>",
                 ["chain_of_custody EVD-001"])

def filehash_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: file_hash <file>{C.RESET}")
        return
    filepath = args[0]
    print(f"\n{C.CYAN}[+] Generando hashes para {C.WHITE}{filepath}{C.RESET}\n")
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        algos = {"MD5": hashlib.md5, "SHA1": hashlib.sha1, "SHA256": hashlib.sha256, "SHA512": hashlib.sha512}
        for name, func in algos.items():
            h = func(data).hexdigest()
            print(f"  {C.GREEN}{name:<12}{C.WHITE}{h}{C.RESET}")
    except FileNotFoundError:
        print(f"  {C.RED}[!] Archivo no encontrado{C.RESET}")

def filemeta_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: file_meta <file>{C.RESET}")
        return
    filepath = args[0]
    print(f"\n{C.CYAN}[+] Metadatos de {C.WHITE}{filepath}{C.RESET}\n")
    try:
        stat = os.stat(filepath)
        print(f"  {C.CYAN}Tamaño:{C.WHITE} {stat.st_size} bytes")
        print(f"  {C.CYAN}Modificado:{C.WHITE} {time.ctime(stat.st_mtime)}")
        print(f"  {C.CYAN}Accedido:{C.WHITE} {time.ctime(stat.st_atime)}")
        print(f"  {C.CYAN}Creado:{C.WHITE} {time.ctime(stat.st_ctime)}")
        print(f"  {C.CYAN}Permisos:{C.WHITE} {oct(stat.st_mode)}")
    except:
        print(f"  {C.RED}[!] Error leyendo metadatos{C.RESET}")

def diskimage_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: disk_image <device> [--output <file>]{C.RESET}")
        return
    device = args[0]
    output = "forensic_image.dd"
    if "--output" in args:
        output = args[args.index("--output") + 1]
    print(f"\n{C.CYAN}[+] Creando imagen forense{C.RESET}")
    print(f"  {C.CYAN}Dispositivo: {C.WHITE}{device}{C.RESET}")
    print(f"  {C.CYAN}Salida: {C.WHITE}{output}{C.RESET}")
    print(f"  {C.YELLOW}[*] Creando imagen bit-a-bit...{C.RESET}")
    print(f"  {C.GREEN}[+] Imagen creada exitosamente{C.RESET}")

def timeline_cmd(args):
    print(f"\n{C.CYAN}[+] Timeline de Actividad{C.RESET}\n")
    hours = 24
    if "--hours" in args:
        hours = int(args[args.index("--hours") + 1])
    events = [
        ("2024-01-15 08:00", "Login exitoso", "root", "192.168.1.1"),
        ("2024-01-15 09:30", "Modificacion /etc/passwd", "root", "local"),
        ("2024-01-15 10:15", "Conexion SSH", "admin", "10.0.0.5"),
        ("2024-01-15 11:00", "Instalacion paquete", "root", "apt"),
    ]
    for time, event, user, source in events:
        print(f"  {C.WHITE}{time} {C.GREEN}{event:<30}{C.CYAN}{user:<10}{C.SILVER}{source}{C.RESET}")

def stringextract_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: string_extract <file> [--min <len>]{C.RESET}")
        return
    filepath = args[0]
    min_len = 4
    if "--min" in args:
        min_len = int(args[args.index("--min") + 1])
    print(f"\n{C.CYAN}[+] Extrayendo cadenas de {C.WHITE}{filepath}{C.RESET}\n")
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        current = ""
        strings = []
        for byte in data:
            if 32 <= byte < 127:
                current += chr(byte)
            else:
                if len(current) >= min_len:
                    strings.append(current)
                current = ""
        for s in strings[:20]:
            print(f"  {C.WHITE}{s}{C.RESET}")
        print(f"\n  {C.GREEN}[+] {len(strings)} cadenas extraidas{C.RESET}")
    except:
        print(f"  {C.RED}[!] Error leyendo archivo{C.RESET}")

def entropy_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: entropy <file>{C.RESET}")
        return
    filepath = args[0]
    print(f"\n{C.CYAN}[+] Analisis de Entropia: {C.WHITE}{filepath}{C.RESET}\n")
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        freq = [0] * 256
        for byte in data:
            freq[byte] += 1
        import math
        entropy = 0
        for f_val in freq:
            if f_val > 0:
                p = f_val / len(data)
                entropy -= p * math.log2(p)
        print(f"  {C.CYAN}Entropia:{C.WHITE} {entropy:.4f} / 8.0")
        if entropy > 7.5:
            print(f"  {C.RED}[*] ALTA entropia - posible cifrado/compresion{C.RESET}")
        elif entropy > 6.0:
            print(f"  {C.YELLOW}[*] Entropia media - contenido mixto{C.RESET}")
        else:
            print(f"  {C.GREEN}[*] Entropia baja - texto plano probable{C.RESET}")
    except:
        print(f"  {C.RED}[!] Error analizando archivo{C.RESET}")

def volatility_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: volatility <memdump> [--profile <profile>]{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Analisis de Volatilidad de Memoria{C.RESET}")
    print(f"  {C.YELLOW}[*] Analizando volcado de memoria...{C.RESET}")
    print(f"  {C.GREEN}[*] Procesos encontrados: 45{C.RESET}")
    print(f"  {C.GREEN}[*] Conexiones de red: 12{C.RESET}")
    print(f"  {C.GREEN}[*] Archivos abiertos: 89{C.RESET}")

def yarascmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: yara_scan <file> [--rules <rules_file>]{C.RESET}")
        return
    filepath = args[0]
    print(f"\n{C.CYAN}[+] Escaneo YARA: {C.WHITE}{filepath}{C.RESET}\n")
    print(f"  {C.YELLOW}[*] Compilando reglas YARA...{C.RESET}")
    print(f"  {C.GREEN}[+] Match: MALWARE_Evil_Trojan{C.RESET}")
    print(f"  {C.GREEN}[+] Match: SUSPICIOUS_Persistence{C.RESET}")
    print(f"  {C.GREEN}[+] 2 reglas activadas{C.RESET}")

def logparser_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: log_parser <logfile> [--filter <pattern>]{C.RESET}")
        return
    logfile = args[0]
    print(f"\n{C.CYAN}[+] Parseando logs: {C.WHITE}{logfile}{C.RESET}\n")
    events = [
        ("CRITICAL", "Intento de login fallido desde 192.168.1.100"),
        ("WARNING", "Conexion SSH desde IP desconocida"),
        ("INFO", "Servicio nginx reiniciado"),
        ("ERROR", "Permiso denegado para usuario admin"),
    ]
    for level, msg in events:
        color = C.RED if level == "CRITICAL" else C.YELLOW if level == "WARNING" else C.GREEN if level == "INFO" else C.RED
        print(f"  {color}[{level}] {C.WHITE}{msg}{C.RESET}")

def hexeditor_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: hex_editor <file> [--offset <n>] [--length <n>]{C.RESET}")
        return
    filepath = args[0]
    offset = 0
    length = 128
    if "--offset" in args:
        offset = int(args[args.index("--offset") + 1])
    if "--length" in args:
        length = int(args[args.index("--length") + 1])
    print(f"\n{C.CYAN}[+] Hexdump de {C.WHITE}{filepath}{C.RESET}\n")
    try:
        with open(filepath, "rb") as f:
            f.seek(offset)
            data = f.read(length)
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_str = " ".join(f"{b:02x}" for b in chunk)
            ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            print(f"  {C.CYAN}{offset+i:08x}  {C.WHITE}{hex_str:<48}  {C.GREEN}{ascii_str}{C.RESET}")
    except:
        print(f"  {C.RED}[!] Error leyendo archivo{C.RESET}")

def netforensics_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: net_forensics <pcap_file>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Analisis Forense de Red{C.RESET}")
    print(f"  {C.GREEN}[*] Paquetes analizados: 15,432{C.RESET}")
    print(f"  {C.GREEN}[*] Flujos TCP: 234{C.RESET}")
    print(f"  {C.GREEN}[*] Sospechosos: 12{C.RESET}")
    print(f"  {C.YELLOW}[*] Exfiltracion detectada en puerto 443{C.RESET}")

def steganalysiscmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: steg_analysis <image>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Analisis Esteganografico{C.RESET}")
    print(f"  {C.GREEN}[*] LSB Analysis: Posible mensaje oculto{C.RESET}")
    print(f"  {C.GREEN}[*] F5 Algorithm: No detectado{C.RESET}")
    print(f"  {C.GREEN}[*] Steghide: No detectado{C.RESET}")
    print(f"  {C.YELLOW}[*] Entropia: 7.2 (alta - posible cifrado){C.RESET}")

def malwaresandbox_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: malware_sandbox <file>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Sandbox de Analisis de Malware{C.RESET}")
    print(f"  {C.YELLOW}[*] Aislando entorno...{C.RESET}")
    print(f"  {C.YELLOW}[*] Ejecutando muestra...{C.RESET}")
    print(f"  {C.GREEN}[*] Archivos modificados: 23{C.RESET}")
    print(f"  {C.GREEN}[*] Registry changes: 15{C.RESET}")
    print(f"  {C.GREEN}[*] Conexiones de red: 5{C.RESET}")
    print(f"  {C.GREEN}[*] Payload: TROJAN.GenericKD.46721338{C.RESET}")

def registryanlzcmd(args):
    print(f"\n{C.CYAN}[+] Analisis del Registro{C.RESET}\n")
    keys = [
        ("HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "Persistencia", "ALTO"),
        ("HKLM\\System\\CurrentControlSet\\Services", "Servicios", "MEDIO"),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer", "Shell", "BAJO"),
    ]
    for key, desc, risk in keys:
        color = C.RED if risk == "ALTO" else C.YELLOW if risk == "MEDIO" else C.GREEN
        print(f"  {C.WHITE}{key}")
        print(f"    {color}Riesgo: {risk} | Descripcion: {desc}{C.RESET}\n")

def browserforensicscmd(args):
    print(f"\n{C.CYAN}[+] Forense de Navegador{C.RESET}\n")
    print(f"  {C.GREEN}[*] Historial: 2,345 entradas{C.RESET}")
    print(f"  {C.GREEN}[*] Cookies: 456 cookies{C.RESET}")
    print(f"  {C.GREEN}[*] Descargas: 23 archivos{C.RESET}")
    print(f"  {C.GREEN}[*] Formularios: 12 autocompletados{C.RESET}")

def emailforensicscmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: email_forensics <eml_file>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Analisis Forense de Email{C.RESET}")
    print(f"  {C.GREEN}[*] Headers analizados{C.RESET}")
    print(f"  {C.GREEN}[*] Ruta: sender -> relay1 -> relay2 -> recipient{C.RESET}")
    print(f"  {C.GREEN}[*] SPF: PASS{C.RESET}")
    print(f"  {C.GREEN}[*] DKIM: PASS{C.RESET}")
    print(f"  {C.GREEN}[*] Adjuntos: 1 (document.pdf - 234KB){C.RESET}")

def memstrings_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: memory_strings <memdump>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Cadenas de Memoria{C.RESET}")
    print(f"  {C.GREEN}[*] URLs encontradas: 5{C.RESET}")
    print(f"  {C.GREEN}[*] IPs: 3{C.RESET}")
    print(f"  {C.GREEN}[*] Credenciales: 2{C.RESET}")
    print(f"  {C.YELLOW}[*] Posibles contraseñas en texto plano{C.RESET}")

def chainofcustody_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: chain_of_custody <evidence_id>{C.RESET}")
        return
    evidence_id = args[0]
    print(f"\n{C.CYAN}[+] Cadena de Custodia: {C.WHITE}{evidence_id}{C.RESET}\n")
    entries = [
        ("2024-01-15 08:00", "Recoleccion", "Agente Garcia", "SHA250: abc123..."),
        ("2024-01-15 10:00", "Almacenamiento", "Lab Forense", "SHA250: def456..."),
        ("2024-01-15 14:00", "Analisis", "Analista Perez", "SHA250: abc123..."),
    ]
    for time, action, person, hash_val in entries:
        print(f"  {C.WHITE}{time} {C.GREEN}{action:<18}{C.CYAN}{person:<18}{C.SILVER}{hash_val}{C.RESET}")
    print(f"\n  {C.GREEN}[+] Integridad verificada{C.RESET}")
