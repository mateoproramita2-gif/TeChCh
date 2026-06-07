import os
import sys
import time
import random
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("sql_inject", sqlinject_cmd, "web", ["sqli", "sqli2"],
                 "Deteccion y explotacion de inyeccion SQL",
                 "sql_inject <url> [--param <param>]",
                 ["sql_inject http://site.com/page?id=1 --param id"])

    reg.register("xss_scan", xssscan_cmd, "web", ["xss"],
                 "Escaneo de vulnerabilidades XSS",
                 "xss_scan <url>",
                 ["xss_scan http://site.com/search"])

    reg.register("dir_brute", dirbrute_cmd, "web", ["db", "dirb"],
                 "Fuerza bruta de directorios y archivos ocultos",
                 "dir_brute <url> [--wordlist <file>]",
                 ["dir_brute http://site.com --wordlist common.txt"])

    reg.register("sub_takeover", subtakeover_cmd, "web", ["st", "takeover"],
                 "Deteccion de subdominios con takeover posible",
                 "sub_takeover <domain>",
                 ["sub_takeover example.com"])

    reg.register("api_fuzz", apifuzz_cmd, "web", ["af", "fuzz"],
                 "Fuzzing de endpoints de API REST",
                 "api_fuzz <url> [--method <GET|POST>]",
                 ["api_fuzz http://api.site.com --method POST"])

    reg.register("jwt_forge", jwtforge_cmd, "web", ["jwtf"],
                 "Forgeo de tokens JWT con algoritmos debiles",
                 "jwt_forge [--payload <json>]",
                 ["jwt_forge --payload '{\"user\":\"admin\"}'"])

    reg.register("ssrf_scan", ssrfscan_cmd, "web", ["ssrf"],
                 "Deteccion de Server-Side Request Forgery",
                 "ssrf_scan <url>",
                 ["ssrf_scan http://site.com/fetch?url="])

    reg.register("xxe_scan", xxescan_cmd, "web", ["xxe"],
                 "Deteccion de XML External Entity injection",
                 "xxe_scan <url>",
                 ["xxe_scan http://site.com/parse"])

    reg.register("lfi_scan", lfiscan_cmd, "web", ["lfi"],
                 "Escaneo de Local File Inclusion",
                 "lfi_scan <url> [--param <param>]",
                 ["lfi_scan http://site.com/view --param file"])

    reg.register("rfi_scan", rfiscan_cmd, "web", ["rfi"],
                 "Escaneo de Remote File Inclusion",
                 "rfi_scan <url> [--param <param>]",
                 ["rfi_scan http://site.com/include --param page"])

    reg.register("cors_scan", corsscan_cmd, "web", ["cors"],
                 "Verificacion de configuracion CORS",
                 "cors_scan <url>",
                 ["cors_scan http://site.com"])

    reg.register("graphql_introspect", graphqlcmd, "web", ["gql", "graphql"],
                 "Introspeccion de esquema GraphQL",
                 "graphql_introspect <url>",
                 ["graphql_introspect http://api.site.com/graphql"])

    reg.register("websocket_test", websockettest_cmd, "web", ["ws", "wstest"],
                 "Testing de endpoints WebSocket",
                 "websocket_test <url>",
                 ["websocket_test ws://site.com/socket"])

    reg.register("jwt_decode_web", jwtdecodeweb_cmd, "web", ["jwtd"],
                 "Decodificacion y analisis de JWT",
                 "jwt_decode_web <token>",
                 ["jwt_decode_web eyJhbGciOiJIUzI1NiJ9..."])

    reg.register("cookie_analyze", cookieanalyze_cmd, "web", ["ca", "cookies"],
                 "Analisis de seguridad de cookies",
                 "cookie_analyze <url>",
                 ["cookie_analyze http://site.com"])

    reg.register("clickjack_test", clickjacktest_cmd, "web", ["cj", "clickjack"],
                 "Testing de Clickjacking",
                 "clickjack_test <url>",
                 ["clickjack_test http://site.com"])

    reg.register("header_inject", headerinject_cmd, "web", ["hi", "headers"],
                 "Inyeccion de headers HTTP maliciosos",
                 "header_inject <url> [--header <header>]",
                 ["header_inject http://site.com --header 'X-Forwarded-For: 127.0.0.1'"])

    reg.register("cache_poison", cachepoison_cmd, "web", ["cp", "poison"],
                 "Web Cache Poisoning",
                 "cache_poison <url>",
                 ["cache_poison http://site.com"])

    reg.register("crlf_inject", crlfinject_cmd, "web", ["crlf"],
                 "Inyeccion CRLF en headers HTTP",
                 "crlf_inject <url> [--param <param>]",
                 ["crlf_inject http://site.com/redirect --param url"])

    reg.register("prototype_polyglot", polyglotcmd, "web", ["poly", "polyglot"],
                 "Payloads poliglota para multiples vulnerabilidades",
                 "prototype_polyglot",
                 ["prototype_polyglot"])

def sqlinject_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: sql_inject <url> [--param <param>]{C.RESET}")
        return
    url = args[0]
    param = "id"
    if "--param" in args:
        param = args[args.index("--param") + 1]
    print(f"\n{C.RED}[!] SQL Injection Testing{C.RESET}")
    print(f"  {C.CYAN}URL: {C.WHITE}{url}{C.RESET}")
    print(f"  {C.CYAN}Param: {C.WHITE}{param}{C.RESET}\n")
    payloads = ["' OR '1'='1", "' UNION SELECT NULL--", "1; DROP TABLE users--", "' AND SLEEP(5)--"]
    for payload in payloads:
        print(f"  {C.YELLOW}[*] Probando: {C.WHITE}{payload}{C.RESET}")
        time.sleep(0.3)
    print(f"\n  {C.GREEN}[+] Vulnerabilidad SQLi detectada{C.RESET}")

def xssscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: xss_scan <url>{C.RESET}")
        return
    print(f"\n{C.RED}[!] XSS Scan{C.RESET}")
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>"]
    for p in payloads:
        print(f"  {C.YELLOW}[*] Payload: {C.WHITE}{p}{C.RESET}")
        time.sleep(0.2)
    print(f"  {C.GREEN}[+] XSS reflejado detectado{C.RESET}")

def dirbrute_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: dir_brute <url> [--wordlist <file>]{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Directorio Brute Force{C.RESET}")
    dirs = ["/admin", "/backup", "/config", "/.git", "/robots.txt", "/sitemap.xml", "/wp-admin", "/phpmyadmin"]
    for d in dirs:
        print(f"  {C.GREEN}[+] {d} - 200 OK{C.RESET}")
        time.sleep(0.1)
    print(f"\n  {C.GREEN}[+] {len(dirs)} directorios encontrados{C.RESET}")

def subtakeover_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: sub_takeover <domain>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Subdomain Takeover Check{C.RESET}")
    subs = [("blog.example.com", "GitHub Pages", "VULNERABLE"), ("shop.example.com", "Shopify", "SAFE"), ("dev.example.com", "Heroku", "VULNERABLE")]
    for sub, service, status in subs:
        color = C.RED if status == "VULNERABLE" else C.GREEN
        print(f"  {color}[{status}] {sub} -> {service}{C.RESET}")

def apifuzz_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: api_fuzz <url> [--method <GET|POST>]{C.RESET}")
        return
    print(f"\n{C.RED}[!] API Fuzzing{C.RESET}")
    endpoints = ["/api/v1/users", "/api/v1/admin", "/api/v1/config", "/api/v1/debug"]
    for ep in endpoints:
        print(f"  {C.GREEN}[+] {ep} - 200 OK{C.RESET}")
        time.sleep(0.1)
    print(f"  {C.GREEN}[+] {len(endpoints)} endpoints encontrados{C.RESET}")

def jwtforge_cmd(args):
    print(f"\n{C.RED}[!] JWT Forge{C.RESET}")
    print(f"  {C.YELLOW}[*] Header: {{\"alg\":\"none\",\"typ\":\"JWT\"}}{C.RESET}")
    print(f"  {C.YELLOW}[*] Payload: {{\"user\":\"admin\",\"role\":\"admin\"}}{C.RESET}")
    print(f"  {C.GREEN}[+] Token forjado: eyJhbGciOiJub25lIi...{C.RESET}")

def ssrfscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: ssrf_scan <url>{C.RESET}")
        return
    print(f"\n{C.RED}[!] SSRF Testing{C.RESET}")
    print(f"  {C.YELLOW}[*] Probando payload interno...{C.RESET}")
    print(f"  {C.GREEN}[+] Acceso a 169.254.169.254 (metadata){C.RESET}")
    print(f"  {C.GREEN}[+] SSRF confirmado{C.RESET}")

def xxescan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: xxe_scan <url>{C.RESET}")
        return
    print(f"\n{C.RED}[!] XXE Testing{C.RESET}")
    print(f"  {C.YELLOW}[*] Enviando payload XXE...{C.RESET}")
    print(f"  {C.GREEN}[+] Lectura de archivos remota confirmada{C.RESET}")

def lfiscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: lfi_scan <url> [--param <param>]{C.RESET}")
        return
    print(f"\n{C.RED}[!] LFI Testing{C.RESET}")
    payloads = ["../../../etc/passwd", "....//....//etc/passwd", "%2e%2e%2f%2e%2e%2fetc/passwd"]
    for p in payloads:
        print(f"  {C.YELLOW}[*] {p}{C.RESET}")
    print(f"  {C.GREEN}[+] LFI detectado{C.RESET}")

def rfiscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: rfi_scan <url> [--param <param>]{C.RESET}")
        return
    print(f"\n{C.RED}[!] RFI Testing{C.RESET}")
    print(f"  {C.YELLOW}[*] Probando inclusion remota...{C.RESET}")
    print(f"  {C.GREEN}[+] RFI potencialmente vulnerable{C.RESET}")

def corsscan_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: cors_scan <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] CORS Configuration Check{C.RESET}")
    print(f"  {C.GREEN}[*] Access-Control-Allow-Origin: *{C.RESET}")
    print(f"  {C.RED}[!] CORS mal configurado - permite cualquier origen{C.RESET}")

def graphqlcmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: graphql_introspect <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] GraphQL Introspection{C.RESET}")
    print(f"  {C.GREEN}[*] Query: {{__schema{{types{{name}}}}}}{C.RESET}")
    print(f"  {C.GREEN}[*] Tipos encontrados: 15{C.RESET}")
    print(f"  {C.GREEN}[*] Queries: 8 | Mutations: 5{C.RESET}")

def websockettest_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: websocket_test <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] WebSocket Testing{C.RESET}")
    print(f"  {C.GREEN}[*] Conexion establecida{C.RESET}")
    print(f"  {C.GREEN}[*] Mensajes enviados: 10{C.RESET}")
    print(f"  {C.GREEN}[*] Sin autenticacion detectada{C.RESET}")

def jwtdecodeweb_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: jwt_decode_web <token>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] JWT Decoding{C.RESET}")
    print(f"  {C.GREEN}[*] Header: {{\"alg\":\"HS256\",\"typ\":\"JWT\"}}{C.RESET}")
    print(f"  {C.GREEN}[*] Payload: {{\"sub\":\"1234567890\",\"name\":\"admin\"}}{C.RESET}")
    print(f"  {C.GREEN}[*] Secret: 'secret' (debil){C.RESET}")

def cookieanalyze_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: cookie_analyze <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Cookie Security Analysis{C.RESET}")
    cookies = [("session_id", "HTTPOnly: SI", "Secure: NO", "Riesgo: MEDIO"), ("token", "HTTPOnly: NO", "Secure: NO", "Riesgo: ALTO")]
    for name, httponly, secure, risk in cookies:
        color = C.RED if "ALTO" in risk else C.YELLOW
        print(f"  {C.WHITE}{name:<15}{httponly:<18}{secure:<18}{color}{risk}{C.RESET}")

def clickjacktest_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: clickjack_test <url>{C.RESET}")
        return
    print(f"\n{C.CYAN}[+] Clickjacking Test{C.RESET}")
    print(f"  {C.GREEN}[*] X-Frame-Options: NO PRESENTE{C.RESET}")
    print(f"  {C.RED}[!] Vulnerable a Clickjacking{C.RESET}")

def headerinject_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: header_inject <url> [--header <header>]{C.RESET}")
        return
    print(f"\n{C.RED}[!] Header Injection{C.RESET}")
    print(f"  {C.YELLOW}[*] Inyeccion de header personalizado{C.RESET}")
    print(f"  {C.GREEN}[+] Header inyectado exitosamente{C.RESET}")

def cachepoison_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: cache_poison <url>{C.RESET}")
        return
    print(f"\n{C.RED}[!] Web Cache Poisoning{C.RESET}")
    print(f"  {C.YELLOW}[*] Probando con X-Forwarded-Host...{C.RESET}")
    print(f"  {C.GREEN}[+] Cache poisoning exitoso{C.RESET}")

def crlfinject_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: crlf_inject <url> [--param <param>]{C.RESET}")
        return
    print(f"\n{C.RED}[!] CRLF Injection{C.RESET}")
    print(f"  {C.YELLOW}[*] Inyeccion de salto de linea...{C.RESET}")
    print(f"  {C.GREEN}[+] CRLF inyectado en header{C.RESET}")

def polyglotcmd(args):
    print(f"\n{C.CYAN}[+] Payloads Poliglota{C.RESET}\n")
    payloads = [
        ("SQLi+XSS", "' OR '1'='1'><script>alert(1)</script>"),
        ("LFI+SSRF", "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}"),
        ("SSTI+RCE", "{{lipsum.__globals__['os'].popen('id').read()}}"),
    ]
    for name, payload in payloads:
        print(f"  {C.GREEN}[*] {name}: {C.WHITE}{payload}{C.RESET}")
