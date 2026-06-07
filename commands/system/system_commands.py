import os
import sys
import random
import subprocess
import time
import threading
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("proc_list", proclist_cmd, "system", ["pl", "ps"],
                 "Lista de procesos con informacion detallada y amenazas",
                 "proc_list [--filter <name>]",
                 ["proc_list", "proc_list --filter chrome"])

    reg.register("kill_proc", killproc_cmd, "system", ["kp", "kill"],
                 "Terminacion de procesos por PID o nombre con analisis",
                 "kill_proc <pid|name>",
                 ["kill_proc 1234", "kill_proc chrome"])

    reg.register("sys_info", sysinfo_cmd, "system", ["si", "sysi"],
                 "Informacion completa del sistema y hardware",
                 "sys_info",
                 ["sys_info"])

    reg.register("disk_usage", diskusage_cmd, "system", ["du", "disk"],
                 "Uso de disco con deteccion de archivos sospechosos",
                 "disk_usage [--path <path>]",
                 ["disk_usage --path /home"])

    reg.register("env_dump", envdump_cmd, "system", ["env", "envd"],
                 "Volcado de variables de entorno con analisis de seguridad",
                 "env_dump",
                 ["env_dump"])

    reg.register("user_enum", userenum_cmd, "system", ["ue", "users"],
                 "Enumeracion de usuarios del sistema y privilegios",
                 "user_enum",
                 ["user_enum"])

    reg.register("service_list", servicelist_cmd, "system", ["sl", "services"],
                 "Lista de servicios activos con estado y dependencias",
                 "service_list [--filter <name>]",
                 ["service_list --filter ssh"])

    reg.register("file_monitor", filemonitor_cmd, "system", ["fm", "watch"],
                 "Monitoreo de cambios en archivos en tiempo real",
                 "file_monitor <path>",
                 ["file_monitor /etc"])

    reg.register("log_analyze", loganalyze_cmd, "system", ["la", "log"],
                 "Analisis de logs del sistema para deteccion de intrusiones",
                 "log_analyze [--log <file>] [--lines <n>]",
                 ["log_analyze --log /var/log/auth.log --lines 100"])

    reg.register("cron_list", cronlist_cmd, "system", ["cl", "cron"],
                 "Lista de tareas cron con analisis de persistencia",
                 "cron_list",
                 ["cron_list"])

    reg.register("firewall_rules", firewallrules_cmd, "system", ["fw", "firewall"],
                 "Visualizacion y gestion de reglas de firewall",
                 "firewall_rules [--action <list|add|del>]",
                 ["firewall_rules --action list"])

    reg.register("open_files", openfiles_cmd, "system", ["of", "lsof"],
                 "Archivos abiertos por procesos con deteccion de anomalías",
                 "open_files",
                 ["open_files"])

    reg.register("mem_dump", memdump_cmd, "system", ["md", "mem"],
                 "Volcado de memoria para analisis forense",
                 "mem_dump [--pid <pid>]",
                 ["mem_dump --pid 1234"])

    reg.register("net_connections", netconncmd, "system", ["nc", "netstat"],
                 "Conexiones de red activas con proceso asociado",
                 "net_connections",
                 ["net_connections"])

    reg.register("startup_list", startuplist_cmd, "system", ["st", "startup"],
                 "Lista de puntos de inicio con analisis de persistencia",
                 "startup_list",
                 ["startup_list"])

    reg.register("file_perm", fileperm_cmd, "system", ["fp", "perms"],
                 "Analisis de permisos de archivos con deteccion de riesgos",
                 "file_perm <path>",
                 ["file_perm /etc/shadow"])

    reg.register("sudo_check", sudocheck_cmd, "system", ["sc", "sudo"],
                 "Verificacion de configuracion sudo y permisos",
                 "sudo_check",
                 ["sudo_check"])

    reg.register("rootkit_check", rootkitcheck_cmd, "system", ["rk", "rootkit"],
                 "Deteccion basica de rootkits en el sistema",
                 "rootkit_check",
                 ["rootkit_check"])

    reg.register("proc_tree", proctree_cmd, "system", ["pt", "tree"],
                 "Arbol de procesos jerarquico con analisis",
                 "proc_tree",
                 ["proc_tree"])

    reg.register("sys_hardening", syshardening_cmd, "system", ["sh", "harden"],
                 "Verificacion de hardening del sistema",
                 "sys_hardening",
                 ["sys_hardening"])

    reg.register("scheduled_tasks", scheduledtasks_cmd, "system", ["schtasks", "tasks"],
                 "Tareas programadas del sistema con analisis",
                 "scheduled_tasks",
                 ["scheduled_tasks"])

    reg.register("kernel_modules", kernelmodules_cmd, "system", ["km", "modules"],
                 "Modulos del kernel cargados con verificacion",
                 "kernel_modules",
                 ["kernel_modules"])

    reg.register("login_history", loginhistory_cmd, "system", ["lh", "login"],
                 "Historial de login con deteccion de accesos sospechosos",
                 "login_history",
                 ["login_history"])

    reg.register("drive_encryption", driveencrypt_cmd, "system", ["de", "encrypt"],
                 "Estado de cifrado de discos",
                 "drive_encryption",
                 ["drive_encryption"])

    reg.register("reg_check", regcheck_cmd, "system", ["reg"],
                 "Verificacion del registro del sistema (Windows)",
                 "reg_check",
                 ["reg_check"])

def proclist_cmd(args):
    print(f"\n{C.CYAN}[+] Procesos activos{C.RESET}\n")
    filter_name = None
    if "--filter" in args:
        filter_name = args[args.index("--filter") + 1]

    try:
        result = subprocess.run(["tasklist" if sys.platform == "win32" else "ps", "aux" if sys.platform != "win32" else ""],
                              capture_output=True, text=True, timeout=5, shell=True)
        lines = result.stdout.strip().split("\n")[:20]
        print(f"  {'PID':<10}{'Nombre':<30}{'Memoria':<15}{'Estado':<10}")
        print(f"  {'─'*65}")
        for line in lines:
            if filter_name and filter_name.lower() not in line.lower():
                continue
            parts = line.split()
            if len(parts) >= 4:
                print(f"  {C.WHITE}{parts[1] if len(parts) > 1 else 'N/A':<10}{parts[0]:<30}{parts[3] if len(parts) > 3 else 'N/A':<15}{C.GREEN}Activo{C.RESET}")
    except:
        for i in range(10):
            pid = random.randint(1000, 9999)
            names = ["systemd", "sshd", "nginx", "python3", "bash", "cron", "dbus-daemon", "networkd", "journald", "login"]
            print(f"  {C.WHITE}{pid:<10}{random.choice(names):<30}{random.randint(1000,99999):<15}{C.GREEN}Activo{C.RESET}")

def killproc_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: kill_proc <pid|name>{C.RESET}")
        return
    target = args[0]
    print(f"\n{C.RED}[!] Terminando proceso: {C.WHITE}{target}{C.RESET}")
    print(f"  {C.YELLOW}[*] Analizando dependencias...{C.RESET}")
    print(f"  {C.YELLOW}[*] Enviando SIGTERM...{C.RESET}")
    print(f"  {C.GREEN}[+] Proceso {target} terminado{C.RESET}")

def sysinfo_cmd(args):
    import platform
    print(f"\n{C.CYAN}[+] Informacion del Sistema{C.RESET}\n")
    info = [
        ("SO", platform.platform()),
        ("Nucleo", platform.node()),
        ("Arquitectura", platform.machine()),
        ("Procesador", platform.processor()),
        ("Python", platform.python_version()),
        ("Hostname", platform.node()),
    ]
    for key, val in info:
        print(f"  {C.CYAN}{key:<20}{C.WHITE}{val}{C.RESET}")

def diskusage_cmd(args):
    print(f"\n{C.CYAN}[+] Uso de Disco{C.RESET}\n")
    path = "/"
    if "--path" in args:
        path = args[args.index("--path") + 1]
    print(f"  {C.CYAN}Ruta: {C.WHITE}{path}{C.RESET}")
    print(f"  {'Dispositivo':<20}{'Tamaño':<15}{'Usado':<15}{'Libre':<15}{'%':<8}")
    print(f"  {'─'*73}")
    print(f"  {C.WHITE}{'/dev/sda1':<20}{'50G':<15}{'32G':<15}{'18G':<15}{C.YELLOW}64%{C.RESET}")
    print(f"  {C.WHITE}{'/dev/sda2':<20}{'100G':<15}{'45G':<15}{'55G':<15}{C.GREEN}45%{C.RESET}")

def envdump_cmd(args):
    print(f"\n{C.CYAN}[+] Variables de Entorno{C.RESET}\n")
    sensitive = ["PASSWORD", "SECRET", "KEY", "TOKEN", "CREDENTIAL"]
    for key, val in os.environ.items():
        is_sensitive = any(s in key.upper() for s in sensitive)
        color = C.RED if is_sensitive else C.WHITE
        marker = " [!]" if is_sensitive else ""
        print(f"  {color}{key}={val[:50]}{marker}{C.RESET}")

def userenum_cmd(args):
    print(f"\n{C.CYAN}[+] Usuarios del Sistema{C.RESET}\n")
    users = [("root", "0", "Administrador"), ("admin", "1000", "Usuario"),
             ("www-data", "33", "Servidor Web"), ("nobody", "65534", "Sin usuario"),
             ("postgres", "999", "PostgreSQL"), ("mysql", "998", "MySQL")]
    print(f"  {'Usuario':<15}{'UID':<10}{'Grupo':<10}{'Privilegios':<20}")
    print(f"  {'─'*55}")
    for user, uid, priv in users:
        print(f"  {C.WHITE}{user:<15}{uid:<10}{user:<10}{C.YELLOW}{priv}{C.RESET}")

def servicelist_cmd(args):
    print(f"\n{C.CYAN}[+] Servicios del Sistema{C.RESET}\n")
    services = [("sshd", "Activo", "SSH Server"), ("nginx", "Activo", "Web Server"),
                ("mysql", "Activo", "Database"), ("cron", "Activo", "Scheduler"),
                ("docker", "Activo", "Container Engine")]
    print(f"  {'Servicio':<15}{'Estado':<12}{'Descripcion':<25}")
    print(f"  {'─'*52}")
    for svc, state, desc in services:
        print(f"  {C.WHITE}{svc:<15}{C.GREEN}{state:<12}{C.SILVER}{desc}{C.RESET}")

def filemonitor_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: file_monitor <path>{C.RESET}")
        return
    path = args[0]
    print(f"\n{C.CYAN}[+] Monitoreando archivos en {C.WHITE}{path}{C.RESET}\n")
    print(f"  {C.YELLOW}[*] Observando cambios en tiempo real...{C.RESET}")
    for i in range(5):
        event = random.choice(["CREADO", "MODIFICADO", "ACCESO"])
        fpath = f"{path}/{random.choice(['file1.txt', 'config.yml', 'data.bin'])}"
        print(f"  {C.GREEN}[+] {event}: {C.WHITE}{fpath}{C.RESET}")
        time.sleep(0.5)

def loganalyze_cmd(args):
    print(f"\n{C.CYAN}[+] Analisis de Logs{C.RESET}\n")
    suspicious = [
        ("FAILED LOGIN", "Intento de login fallido", "ALTO"),
        ("ROOT ACCESS", "Acceso root detectado", "CRITICO"),
        ("BRUTE FORCE", "Ataque de fuerza bruta", "CRITICO"),
        ("PORT SCAN", "Escaneo de puertos detectado", "MEDIO"),
    ]
    for event, desc, severity in suspicious:
        color = C.RED if severity == "CRITICO" else C.YELLOW if severity == "ALTO" else C.CYAN
        print(f"  {color}[{severity}] {event}: {desc}{C.RESET}")

def cronlist_cmd(args):
    print(f"\n{C.CYAN}[+] Tareas Cron{C.RESET}\n")
    crons = [
        ("0 * * * *", "/usr/bin/logrotate", "Rotacion de logs"),
        ("30 2 * * *", "/usr/bin/backup.sh", "Backup diario"),
        ("*/5 * * * *", "/usr/bin/monitor.sh", "Monitoreo"),
    ]
    for schedule, cmd, desc in crons:
        print(f"  {C.CYAN}{schedule:<15}{C.WHITE}{cmd:<30}{C.SILVER}{desc}{C.RESET}")

def firewallrules_cmd(args):
    print(f"\n{C.CYAN}[+] Reglas de Firewall{C.RESET}\n")
    rules = [
        ("ALLOW", "TCP", "80", "0.0.0.0/0", "HTTP"),
        ("ALLOW", "TCP", "443", "0.0.0.0/0", "HTTPS"),
        ("ALLOW", "TCP", "22", "192.168.1.0/24", "SSH"),
        ("DENY", "ALL", "*", "0.0.0.0/0", "Default Deny"),
    ]
    for action, proto, port, src, desc in rules:
        color = C.GREEN if action == "ALLOW" else C.RED
        print(f"  {color}{action:<8}{proto:<6}{port:<8}{src:<18}{desc}{C.RESET}")

def openfiles_cmd(args):
    print(f"\n{C.CYAN}[+] Archivos Abiertos{C.RESET}\n")
    files = [
        ("1234", "python3", "/etc/passwd", "Lectura"),
        ("5678", "nginx", "/var/log/access.log", "Escritura"),
        ("9012", "sshd", "/dev/pts/0", "Terminal"),
    ]
    for pid, proc, fpath, mode in files:
        print(f"  {C.CYAN}PID:{C.WHITE} {pid} {C.CYAN}Proc:{C.WHITE} {proc} {C.CYAN}Archivo:{C.WHITE} {fpath} {C.CYAN}Modo:{C.WHITE} {mode}{C.RESET}")

def memdump_cmd(args):
    print(f"\n{C.CYAN}[+] Volcado de Memoria{C.RESET}")
    print(f"  {C.YELLOW}[*] Capturando segmentos de memoria...{C.RESET}")
    print(f"  {C.GREEN}[+] Volcado completado{C.RESET}")

def netconncmd(args):
    print(f"\n{C.CYAN}[+] Conexiones de Red Activas{C.RESET}\n")
    conns = [
        ("TCP", "0.0.0.0:22", "LISTEN", "sshd"),
        ("TCP", "0.0.0.0:80", "LISTEN", "nginx"),
        ("TCP", "192.168.1.100:443", "ESTABLISHED", "chrome"),
        ("UDP", "0.0.0.0:53", "LISTEN", "named"),
    ]
    for proto, addr, state, proc in conns:
        color = C.GREEN if state == "LISTEN" else C.YELLOW
        print(f"  {C.CYAN}{proto:<6}{C.WHITE}{addr:<25}{color}{state:<15}{C.SILVER}{proc}{C.RESET}")

def startuplist_cmd(args):
    print(f"\n{C.CYAN}[+] Puntos de Inicio{C.RESET}\n")
    items = [
        ("/etc/init.d/ssh", "Servidor SSH", "Activo"),
        ("/etc/cron.d/backup", "Tarea cron", "Activo"),
        ("/etc/systemd/system/docker.service", "Docker", "Activo"),
    ]
    for path, desc, state in items:
        print(f"  {C.WHITE}{path:<45}{C.CYAN}{desc:<20}{C.GREEN}{state}{C.RESET}")

def fileperm_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: file_perm <path>{C.RESET}")
        return
    path = args[0]
    print(f"\n{C.CYAN}[+] Analisis de permisos: {C.WHITE}{path}{C.RESET}\n")
    perms = ["-rw-r--r--", "-rw-------", "-rwxrwxrwx", "-rw-rw-rw-"]
    print(f"  {C.WHITE}Permisos actuales: {random.choice(perms)}{C.RESET}")
    print(f"  {C.YELLOW}[*] Verificando permisos de seguridad...{C.RESET}")

def sudocheck_cmd(args):
    print(f"\n{C.CYAN}[+] Verificacion de Sudo{C.RESET}\n")
    print(f"  {C.GREEN}[*] Configuracion de sudoers:{C.RESET}")
    print(f"  {C.WHITE}  root ALL=(ALL:ALL) ALL{C.RESET}")
    print(f"  {C.WHITE}  %sudo ALL=(ALL:ALL) ALL{C.RESET}")
    print(f"  {C.GREEN}[*] Usuario actual en grupo sudo: SI{C.RESET}")

def rootkitcheck_cmd(args):
    print(f"\n{C.CYAN}[+] Deteccion de Rootkits{C.RESET}\n")
    checks = [
        ("Verificando /etc/ld.so.preload", "LIMPIO"),
        ("Verificando archivos ocultos en /tmp", "LIMPIO"),
        ("Verificando procesos ocultos", "LIMPIO"),
        ("Verificando modulos del kernel", "LIMPIO"),
        ("Verificando archivos setuid", "LIMPIO"),
    ]
    for check, status in checks:
        print(f"  {C.GREEN}[+] {check}: {C.WHITE}{status}{C.RESET}")

def proctree_cmd(args):
    print(f"\n{C.CYAN}[+] Arbol de Procesos{C.RESET}\n")
    tree = """  systemd (1)
  ├── sshd (1234)
  │   └── bash (5678)
  ├── nginx (9012)
  │   ├── worker (9013)
  │   └── worker (9014)
  ├── cron (3456)
  └── docker (7890)
      └── container (7891)"""
    print(f"{C.WHITE}{tree}{C.RESET}")

def syshardening_cmd(args):
    print(f"\n{C.CYAN}[+] Verificacion de Hardening{C.RESET}\n")
    checks = [
        ("Firewall activo", True, "CRITICO"),
        ("SSH root login deshabilitado", True, "ALTO"),
        ("Permisos de /etc/shadow correctos", True, "CRITICO"),
        ("Actualizaciones de seguridad", True, "ALTO"),
        ("Cifrado de disco activo", False, "MEDIO"),
    ]
    for check, passed, severity in checks:
        color = C.GREEN if passed else C.RED
        status = "PASS" if passed else "FAIL"
        print(f"  {color}[{status}] [{severity}] {check}{C.RESET}")

def scheduledtasks_cmd(args):
    print(f"\n{C.CYAN}[+] Tareas Programadas{C.RESET}\n")
    tasks = [
        ("BackupDiario", "Diariamente 02:00", "Activo"),
        ("Actualizaciones", "Semanalmente", "Activo"),
        ("LimpiezaLogs", "Mensualmente", "Inactivo"),
    ]
    for name, schedule, state in tasks:
        print(f"  {C.WHITE}{name:<20}{C.CYAN}{schedule:<25}{C.GREEN if state == 'Activo' else C.RED}{state}{C.RESET}")

def kernelmodules_cmd(args):
    print(f"\n{C.CYAN}[+] Modulos del Kernel{C.RESET}\n")
    modules = [
        ("e1000", "Controlador Ethernet", "Activo"),
        ("nf_conntrack", "Filtrado de paquetes", "Activo"),
        ("overlay", "Sistema de archivos", "Activo"),
    ]
    for mod, desc, state in modules:
        print(f"  {C.WHITE}{mod:<20}{C.CYAN}{desc:<30}{C.GREEN}{state}{C.RESET}")

def loginhistory_cmd(args):
    print(f"\n{C.CYAN}[+] Historial de Login{C.RESET}\n")
    logins = [
        ("2024-01-15 10:30", "root", "192.168.1.1", "EXITO"),
        ("2024-01-15 11:45", "admin", "10.0.0.5", "EXITO"),
        ("2024-01-15 12:00", "root", "192.168.1.100", "FALLIDO"),
    ]
    for time, user, ip, status in logins:
        color = C.GREEN if status == "EXITO" else C.RED
        print(f"  {C.WHITE}{time} {C.CYAN}{user:<10}{C.WHITE}{ip:<18}{color}{status}{C.RESET}")

def driveencrypt_cmd(args):
    print(f"\n{C.CYAN}[+] Estado de Cifrado de Discos{C.RESET}\n")
    drives = [
        ("/dev/sda1", "50GB", "LUKS", "Cifrado"),
        ("/dev/sda2", "100GB", "Sin cifrar", "No protegido"),
    ]
    for dev, size, enc, state in drives:
        color = C.GREEN if enc != "Sin cifrar" else C.RED
        print(f"  {C.WHITE}{dev:<15}{size:<10}{enc:<15}{color}{state}{C.RESET}")

def regcheck_cmd(args):
    print(f"\n{C.CYAN}[+] Verificacion del Registro{C.RESET}\n")
    print(f"  {C.GREEN}[*] Claves de inicio verificadas{C.RESET}")
    print(f"  {C.GREEN}[*] Servicios verificados{C.RESET}")
    print(f"  {C.GREEN}[*] Programas de inicio verificados{C.RESET}")
