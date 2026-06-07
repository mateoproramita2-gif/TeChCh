# TeChCh - Terminal Enhanced Cyber Command Hub

Sistema de Ciberseguridad Avanzado para Linux

## Instalacion

```bash
chmod +x install.sh
./install.sh
```

## Ejecucion

```bash
techch
```

O directamente con Python:
```bash
python3 techch.py
```

## Comandos Principales (100+)

### RECON (Reconocimiento)
- `portscan` - Escaneo de puertos TCP/UDP avanzado
- `serviceid` - Identificacion de servicios y versiones
- `dnseum` - Enumeracion DNS completa
- `whois_lookup` - Consulta WHOIS de dominios
- `tracert` - Traceroute con geolocalizacion
- `subnet_scan` - Escaneo de subred completo
- `banner_grab` - Captura de banners de servicios
- `reverse_dns` - Resolucion DNS inversa
- `host_discovery` - Descubrimiento de hosts
- `os_fingerprint` - Fingerprinting de OS
- `vuln_scan` - Escaneo de vulnerabilidades
- `net_enum` - Enumeracion de red
- `mac_lookup` - Busqueda de fabricante MAC
- `ssl_scan` - Analisis SSL/TLS
- `http_headers` - Analisis de headers HTTP
- `subdomain_enum` - Enumeracion de subdominios
- `email_harvest` - Recoleccion de emails
- `tech_detect` - Deteccion de tecnologias
- `full_recon` - Reconocimiento completo

### NET (Red)
- `net_sniff` - Captura de paquetes
- `arp_spoofer` - ARP spoofing
- `dns_spof` - DNS spoofing
- `packet_forge` - Forgeo de paquetes
- `mitm_attack` - Man-in-the-Middle
- `net_jam` - Denegacion de servicio
- `vlan_hopping` - VLAN hopping
- `net_map` - Mapeo de red
- `deauth` - Desautenticacion WiFi
- `tcp_hijack` - Secuestro TCP
- `syn_flood` - SYN flood attack
- `udp_flood` - UDP flood attack
- `icmp_flood` - ICMP flood attack
- `dhcp_starve` - DHCP starvation
- `wol` - Wake-on-LAN

### CRYPTO (Criptografia)
- `hash_crack` - Fuerza bruta de hashes
- `gen_pass` - Generador de contrasenas
- `caesar` - Cifrado Caesar
- `base64_enc/dec` - Base64 encode/decode
- `hex_encode/dec` - Hexadecimal encode/decode
- `xor_cipher` - Cifrado XOR
- `aes_encrypt/dec` - AES-256-CBC
- `rsa_gen` - Generacion de claves RSA
- `steg_hide/extract` - Steganography
- `hash_dump` - Generacion de hashes
- `vigenere` - Cifrado Vigenere
- `jwt_decode` - Decodificacion JWT

### SYSTEM (Sistema)
- `proc_list` - Lista de procesos
- `kill_proc` - Terminar procesos
- `sys_info` - Informacion del sistema
- `disk_usage` - Uso de disco
- `env_dump` - Variables de entorno
- `user_enum` - Enumeracion de usuarios
- `service_list` - Lista de servicios
- `file_monitor` - Monitoreo de archivos
- `log_analyze` - Analisis de logs
- `firewall_rules` - Reglas de firewall
- `rootkit_check` - Deteccion de rootkits
- `sys_hardening` - Verificacion de hardening

### WIRELESS (Inalambrico)
- `wifi_scan` - Escaneo de redes WiFi
- `wpa_crack` - Ataque WPA/WPA2
- `wps_attack` - Ataque WPS
- `evil_twin` - Punto de acceso falso
- `bluetooth_scan` - Escaneo Bluetooth
- `rfid_read` - Lectura RFID
- `nfc_clone` - Clonacion NFC
- `pmkid_attack` - Ataque PMKID

### WEB (Aplicaciones Web)
- `sql_inject` - SQL Injection testing
- `xss_scan` - XSS scanning
- `dir_brute` - Directory brute force
- `api_fuzz` - API fuzzing
- `ssrf_scan` - SSRF detection
- `xxe_scan` - XXE detection
- `cors_scan` - CORS verification

### FORENSICS (Forense Digital)
- `file_hash` - Hashes de archivos
- `file_meta` - Metadatos de archivos
- `disk_image` - Imagen de disco
- `timeline` - Timeline de actividad
- `string_extract` - Extraccion de strings
- `entropy` - Analisis de entropia
- `yara_scan` - Escaneo YARA
- `hex_editor` - Editor hexadecimal

### MALWARE
- `malware_scan` - Escaneo de malware
- `shellcode_gen` - Generador de shellcode
- `obfuscate` - Ofuscacion de codigo
- `keylogger` - Keylogger para testing
- `ransomware_sim` - Simulador ransomware
- `priv_escalation` - Deteccion de privesc

### OSINT
- `ip_lookup` - Geolocalizacion de IP
- `email_lookup` - Busqueda por email
- `domain_recon` - Reconocimiento de dominio
- `username_search` - Busqueda de usuario
- `breach_check` - Verificacion de filtraciones
- `social_scan` - Escaneo de redes sociales
- `darkweb_monitor` - Monitoreo dark web
- `full_osint` - OSINT completo

## Integracion Ollama AI

1. Instalar Ollama: `ollama` en el menu
2. Descargar modelo: `ollama` > `[3] Descargar modelo`
3. Iniciar chat: `ai <mensaje>` o `ollama` > `[5] Chat`

## Comandos Especiales

- `help` - Ayuda completa
- `categories` - Lista de categorias
- `stats` - Estadisticas de sesion
- `history` - Historial de comandos
- `matrix` - Efecto Matrix
- `all` - Listar todos los comandos
- `search <query>` - Buscar comandos
- `settings` - Ver configuracion
- `set <key> <value>` - Cambiar configuracion

## Licencia

Uso exclusivo para administradores y profesionales de seguridad autorizados.
