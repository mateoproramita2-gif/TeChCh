import os
import sys
import json
import socket
import struct
import time
import random
import threading
import hashlib
from core.ui import C, slow_print, fast_print, spinner

def register_commands(reg):
    reg.register("hash_crack", hashcrack_cmd, "crypto", ["hc", "hash"],
                 "Fuerza bruta de hashes con diccionario y reglas",
                 "hash_crack <hash> [--wordlist <file>] [--mode <md5|sha1|sha256>]",
                 ["hash_crack 5d41402abc4b2a76b9719d911017c592 --mode md5"])

    reg.register("gen_pass", genpass_cmd, "crypto", ["gp", "passgen"],
                 "Generador de contraseñas seguras con patron personalizado",
                 "gen_pass [--length <n>] [--count <n>] [--charset <type>]",
                 ["gen_pass --length 20 --count 5 --charset complex"])

    reg.register("caesar", caesar_cmd, "crypto", ["ca", "rot"],
                 "Cifrado Caesar con fuerza bruta automatica de 25 rotaciones",
                 "caesar <text> [--shift <n>]",
                 ["caesar HelloWorld --shift 13"])

    reg.register("base64_enc", b64enc_cmd, "crypto", ["b64e", "b64"],
                 "Codificacion Base64 de texto o archivos",
                 "base64_enc <text>",
                 ["base64_enc 'Hello World'"])

    reg.register("base64_dec", b64dec_cmd, "crypto", ["b64d"],
                 "Decodificacion Base64",
                 "base64_dec <encoded>",
                 ["base64_dec SGVsbG8gV29ybGQ="])

    reg.register("hex_encode", hexenc_cmd, "crypto", ["he", "hexe"],
                 "Codificacion hexadecimal de texto",
                 "hex_encode <text>",
                 ["hex_encode 'Hello World'"])

    reg.register("hex_decode", hexdec_cmd, "crypto", ["hd", "hexd"],
                 "Decodificacion hexadecimal",
                 "hex_decode <hex>",
                 ["hex_decode 48656c6c6f"])

    reg.register("xor_cipher", xorcmd, "crypto", ["xor"],
                 "Cifrado XOR con clave personalizada",
                 "xor_cipher <text> [--key <key>]",
                 ["xor_cipher 'Secret' --key 'mykey'"])

    reg.register("aes_encrypt", aesenc_cmd, "crypto", ["aese"],
                 "Cifrado AES-256-CBC con passphrase",
                 "aes_encrypt <text> [--pass <password>]",
                 ["aes_encrypt 'SecretData' --pass 'mypass'"])

    reg.register("aes_decrypt", aesdec_cmd, "crypto", ["aesd"],
                 "Descifrado AES-256-CBC",
                 "aes_decrypt <encrypted> [--pass <password>]",
                 ["aes_decrypt 'encrypted_data' --pass 'mypass'"])

    reg.register("rsa_gen", rsagen_cmd, "crypto", ["rsag"],
                 "Generacion de pares de claves RSA",
                 "rsa_gen [--bits <2048|4096>]",
                 ["rsa_gen --bits 4096"])

    reg.register("steg_hide", steghide_cmd, "crypto", ["steg", "stgh"],
                 "Ocultamiento de mensajes en imagenes (steganography)",
                 "steg_hide <image> [--message <text>]",
                 ["steg_hide photo.png --message 'Hidden message'"])

    reg.register("steg_extract", stegextract_cmd, "crypto", ["ste", "stge"],
                 "Extraccion de mensajes ocultos en imagenes",
                 "steg_extract <image>",
                 ["steg_extract photo.png"])

    reg.register("password_spray", passspray_cmd, "crypto", ["ps", "spray"],
                 "Ataque de password spraying contra servicios",
                 "password_spray <target> [--users <file>] [--pass <password>]",
                 ["password_spray 192.168.1.1 --users users.txt --pass 'Password123'"])

    reg.register("hash_dump", hashdump_cmd, "crypto", ["hd", "hashd"],
                 "Generacion de hashes para diferentes algoritmos",
                 "hash_dump <text>",
                 ["hash_dump 'password123'"])

    reg.register("substitution", subcmd, "crypto", ["sub", "subst"],
                 "Cifrado por sustitucion con alfabeto personalizado",
                 "substitution <text> [--map <mapping>]",
                 ["substitution 'HELLO' --map 'ABC...Z'"])

    reg.register("vigenere", vigenere_cmd, "crypto", ["vig"],
                 "Cifrado Vigenere con palabra clave",
                 "vigenere <text> [--key <key>]",
                 ["vigenere 'HELLO' --key 'KEY'"])

    reg.register("jwt_decode", jwtdecode_cmd, "crypto", ["jwt"],
                 "Decodificacion de tokens JWT",
                 "jwt_decode <token>",
                 ["jwt_decode eyJhbGciOiJIUzI1NiJ9..."])

def hashcrack_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: hash_crack <hash> [--wordlist <file>] [--mode <md5|sha1|sha256>]{C.RESET}")
        return
    target_hash = args[0].lower()
    mode = "md5"
    wordlist = None
    if "--mode" in args:
        mode = args[args.index("--mode") + 1]
    if "--wordlist" in args:
        wordlist = args[args.index("--wordlist") + 1]

    print(f"\n{C.CYAN}[+] Analizando hash: {C.WHITE}{target_hash}{C.RESET}")
    print(f"  {C.CYAN}Algoritmo:{C.WHITE} {mode.upper()}{C.RESET}")

    common_passwords = ["password", "123456", "admin", "root", "toor", "pass", "test", "guest", "master", "qwerty", "abc123", "12345678", "letmein", "welcome", "monkey", "dragon", "login", "princess", "football", "shadow", "sunshine", "trustno1", "iloveyou", "batman", "access", "hello", "charlie", "donald", "password1", "qwerty123"]

    print(f"\n  {C.YELLOW}[*] Iniciando ataque de fuerza bruta...{C.RESET}\n")
    time.sleep(0.5)

    for i, word in enumerate(common_passwords):
        if mode == "md5":
            computed = hashlib.md5(word.encode()).hexdigest()
        elif mode == "sha1":
            computed = hashlib.sha1(word.encode()).hexdigest()
        elif mode == "sha256":
            computed = hashlib.sha256(word.encode()).hexdigest()
        else:
            computed = hashlib.md5(word.encode()).hexdigest()

        if computed == target_hash:
            print(f"  {C.GREEN}[+] HASH CRACKED!{C.RESET}")
            print(f"  {C.GREEN}[*] Hash: {C.WHITE}{target_hash}{C.GREEN}")
            print(f"  {C.GREEN}[*] Texto: {C.WHITE}{word}{C.GREEN}")
            print(f"  {C.GREEN}[*] Intentos: {i+1}{C.RESET}")
            return
        sys.stdout.write(f"\r  {C.DIM}Probando: {word:<20}{C.RESET}")
        sys.stdout.flush()

    print(f"\n\n  {C.RED}[!] Hash no encontrado en diccionario basico{C.RESET}")
    print(f"  {C.DIM}Use --wordlist para un diccionario personalizado{C.RESET}")

def genpass_cmd(args):
    length = 16
    count = 1
    charset_type = "complex"
    if "--length" in args:
        length = int(args[args.index("--length") + 1])
    if "--count" in args:
        count = int(args[args.index("--count") + 1])
    if "--charset" in args:
        charset_type = args[args.index("--charset") + 1]

    charsets = {
        "simple": "abcdefghijklmnopqrstuvwxyz",
        "medium": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "complex": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+",
        "numeric": "0123456789",
        "hex": "0123456789abcdef",
        "symbols": "!@#$%^&*()-_=+[]{}|;:',.<>?"
    }

    charset = charsets.get(charset_type, charsets["complex"])
    print(f"\n{C.CYAN}[+] Generando {count} contraseñas de {length} caracteres{C.RESET}\n")

    passwords = []
    for _ in range(count):
        pwd = "".join(random.SystemRandom().choice(charset) for _ in range(length))
        passwords.append(pwd)
        print(f"  {C.GREEN}[+] {pwd}{C.RESET}")

    print(f"\n{C.GREEN}[+] {len(passwords)} contraseñas generadas{C.RESET}")

def caesar_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: caesar <text> [--shift <n>]{C.RESET}")
        return
    text = args[0]
    shift = None
    if "--shift" in args:
        shift = int(args[args.index("--shift") + 1])

    if shift is not None:
        result = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base + shift) % 26 + base)
            else:
                result += c
        print(f"\n{C.GREEN}[+] Cifrado Caesar (shift={shift}): {C.WHITE}{result}{C.RESET}")
    else:
        print(f"\n{C.CYAN}[+] Analisis de 25 rotaciones para: {C.WHITE}{text}{C.RESET}\n")
        for s in range(1, 26):
            result = ""
            for c in text:
                if c.isalpha():
                    base = ord('A') if c.isupper() else ord('a')
                    result += chr((ord(c) - base + s) % 26 + base)
                else:
                    result += c
            print(f"  {C.GREEN}Shift {s:>2}: {C.WHITE}{result}{C.RESET}")

def b64enc_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: base64_enc <text>{C.RESET}")
        return
    import base64
    text = " ".join(args)
    encoded = base64.b64encode(text.encode()).decode()
    print(f"\n{C.GREEN}[+] Base64: {C.WHITE}{encoded}{C.RESET}")

def b64dec_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: base64_dec <encoded>{C.RESET}")
        return
    import base64
    encoded = args[0]
    try:
        decoded = base64.b64decode(encoded).decode()
        print(f"\n{C.GREEN}[+] Decodificado: {C.WHITE}{decoded}{C.RESET}")
    except:
        print(f"{C.RED}[!] Error decodificando Base64{C.RESET}")

def hexenc_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: hex_encode <text>{C.RESET}")
        return
    text = " ".join(args)
    encoded = text.encode().hex()
    print(f"\n{C.GREEN}[+] Hexadecimal: {C.WHITE}{encoded}{C.RESET}")

def hexdec_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: hex_decode <hex>{C.RESET}")
        return
    hex_str = args[0]
    try:
        decoded = bytes.fromhex(hex_str).decode()
        print(f"\n{C.GREEN}[+] Decodificado: {C.WHITE}{decoded}{C.RESET}")
    except:
        print(f"{C.RED}[!] Error decodificando hexadecimal{C.RESET}")

def xorcmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: xor_cipher <text> [--key <key>]{C.RESET}")
        return
    text = args[0]
    key = "default_key"
    if "--key" in args:
        key = args[args.index("--key") + 1]

    encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(text.encode())])
    print(f"\n{C.GREEN}[+] XOR Cifrado: {C.WHITE}{encrypted.hex()}{C.RESET}")
    print(f"{C.GREEN}[+] XOR Decodificado: {C.WHITE}{encrypted.decode(errors='ignore')}{C.RESET}")

def aesenc_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: aes_encrypt <text> [--pass <password>]{C.RESET}")
        return
    text = args[0]
    password = "default_password"
    if "--pass" in args:
        password = args[args.index("--pass") + 1]

    key = hashlib.sha256(password.encode()).digest()
    iv = os.urandom(16)
    print(f"\n{C.GREEN}[+] AES-256-CBC Cifrado{C.RESET}")
    print(f"  {C.CYAN}Texto: {C.WHITE}{text}{C.RESET}")
    print(f"  {C.CYAN}IV: {C.WHITE}{iv.hex()}{C.RESET}")
    print(f"  {C.CYAN}Key Hash: {C.WHITE}{key.hex()[:32]}...{C.RESET}")
    print(f"  {C.YELLOW}[*] Nota: Instale pycryptodome para cifrado real{C.RESET}")

def aesdec_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: aes_decrypt <encrypted> [--pass <password>]{C.RESET}")
        return
    print(f"\n{C.YELLOW}[*] Descifrado AES requiere pycryptodome: pip install pycryptodome{C.RESET}")

def rsagen_cmd(args):
    bits = 2048
    if "--bits" in args:
        bits = int(args[args.index("--bits") + 1])
    print(f"\n{C.CYAN}[+] Generando par de claves RSA-{bits}{C.RESET}\n")
    try:
        from Crypto.PublicKey import RSA
        key = RSA.generate(bits)
        print(f"  {C.GREEN}[*] Clave privada generada{C.RESET}")
        print(f"  {C.GREEN}[*] Clave publica generada{C.RESET}")
    except ImportError:
        print(f"  {C.YELLOW}[*] Instale pycryptodome: pip install pycryptodome{C.RESET}")
        print(f"  {C.DIM}Generando clave simulada...{C.RESET}")
        print(f"  {C.GREEN}[*] RSA-{bits} key pair (simulado){C.RESET}")

def steghide_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: steg_hide <image> [--message <text>]{C.RESET}")
        return
    image = args[0]
    message = ""
    if "--message" in args:
        message = args[args.index("--message") + 1]
    print(f"\n{C.CYAN}[+] Ocultando mensaje en {C.WHITE}{image}{C.RESET}")
    print(f"  {C.CYAN}Mensaje: {C.WHITE}{message}{C.RESET}")
    print(f"  {C.GREEN}[*] Steganography aplicada (simulado){C.RESET}")

def stegextract_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: steg_extract <image>{C.RESET}")
        return
    image = args[0]
    print(f"\n{C.CYAN}[+] Extrayendo mensaje oculto de {C.WHITE}{image}{C.RESET}")
    print(f"  {C.GREEN}[*] Mensaje extraido (simulado){C.RESET}")

def passspray_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: password_spray <target> [--users <file>] [--pass <password>]{C.RESET}")
        return
    target = args[0]
    password = "Password123"
    users = ["admin", "root", "user", "test"]
    if "--pass" in args:
        password = args[args.index("--pass") + 1]
    print(f"\n{C.CYAN}[+] Password spraying contra {C.WHITE}{target}{C.RESET}\n")
    for user in users:
        print(f"  {C.DIM}Probando {user}:{password}...{C.RESET}")
        time.sleep(0.3)
        print(f"  {C.YELLOW}[*] {user} - Credencial no verificada{C.RESET}")
    print(f"\n{C.DIM}[*] Simulacion completada. Use herramientas reales para auditorias autorizadas{C.RESET}")

def hashdump_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: hash_dump <text>{C.RESET}")
        return
    text = args[0]
    print(f"\n{C.CYAN}[+] Generando hashes para: {C.WHITE}{text}{C.RESET}\n")
    algos = {
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA224": hashlib.sha224,
        "SHA256": hashlib.sha256,
        "SHA384": hashlib.sha384,
        "SHA512": hashlib.sha512
    }
    for name, func in algos.items():
        h = func(text.encode()).hexdigest()
        print(f"  {C.GREEN}{name:<12}{C.WHITE}{h}{C.RESET}")

def subcmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: substitution <text> [--map <mapping>]{C.RESET}")
        return
    text = args[0]
    print(f"\n{C.CYAN}[+] Cifrado por sustitucion: {C.WHITE}{text}{C.RESET}")
    mapping = {chr(i): chr((i - 65 + 3) % 26 + 65) if i < 91 else chr((i - 97 + 3) % 26 + 97) for i in range(65, 123)}
    result = "".join(mapping.get(c, c) for c in text)
    print(f"  {C.GREEN}Resultado: {C.WHITE}{result}{C.RESET}")

def vigenere_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: vigenere <text> [--key <key>]{C.RESET}")
        return
    text = args[0]
    key = "KEY"
    if "--key" in args:
        key = args[args.index("--key") + 1].upper()
    result = ""
    key_idx = 0
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(key[key_idx % len(key)]) - ord('A')
            result += chr((ord(c.upper()) - ord('A') + shift) % 26 + base)
            key_idx += 1
        else:
            result += c
    print(f"\n{C.GREEN}[+] Vigenere (key={key}): {C.WHITE}{result}{C.RESET}")

def jwtdecode_cmd(args):
    if not args:
        print(f"{C.RED}[!] Uso: jwt_decode <token>{C.RESET}")
        return
    token = args[0]
    print(f"\n{C.CYAN}[+] Decodificando JWT{C.RESET}\n")
    try:
        import base64
        parts = token.split(".")
        if len(parts) >= 2:
            header = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
            print(f"  {C.GREEN}[*] Header:{C.RESET}")
            for k, v in header.items():
                print(f"    {C.CYAN}{k}: {C.WHITE}{v}{C.RESET}")
            print(f"\n  {C.GREEN}[*] Payload:{C.RESET}")
            for k, v in payload.items():
                print(f"    {C.CYAN}{k}: {C.WHITE}{v}{C.RESET}")
    except Exception as e:
        print(f"  {C.RED}[!] Error decodificando JWT: {e}{C.RESET}")
