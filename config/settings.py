import os
import json
import sys
from core.ui import C

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")
DEFAULT_SETTINGS = {
    "theme": "hacker",
    "ollama_model": "llama3",
    "ollama_auto_connect": False,
    "animations_enabled": True,
    "sound_enabled": False,
    "log_commands": True,
    "max_history": 1000,
    "default_wordlist": "common.txt",
    "timeout": 30,
    "verbose": False,
    "language": "es",
    "banner_style": "full",
    "prompt_style": "hacker",
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                settings = json.load(f)
            for key, val in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = val
            return settings
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def get_setting(key, default=None):
    settings = load_settings()
    return settings.get(key, default)

def set_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)

def print_settings():
    settings = load_settings()
    print(f"\n{C.CYAN}[+] Configuracion actual:{C.RESET}\n")
    for key, val in settings.items():
        print(f"  {C.CYAN}{key:<25}{C.WHITE}{val}{C.RESET}")
