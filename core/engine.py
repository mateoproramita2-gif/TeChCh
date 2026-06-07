import os
import sys
import importlib
import pkgutil
import traceback
from datetime import datetime

class CommandRegistry:
    def __init__(self):
        self.commands = {}
        self.categories = {}
        self.aliases = {}
        self.history = []
        self.session_start = datetime.now()
        self.total_executed = 0
        self.last_cmd_time = 0

    def register(self, name, func, category="general", aliases=None, description="", syntax="", examples=None):
        self.commands[name] = {
            "func": func,
            "category": category,
            "description": description,
            "syntax": syntax,
            "examples": examples or [],
            "registered_at": datetime.now(),
            "executions": 0
        }
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        if aliases:
            for alias in aliases:
                self.aliases[alias] = name

    def execute(self, name, args=None):
        import time
        cmd_name = self.aliases.get(name, name)
        if cmd_name not in self.commands:
            return None, f"[!] Comando no encontrado: {name}"
        start = time.time()
        try:
            result = self.commands[cmd_name]["func"](args)
            elapsed = time.time() - start
            self.commands[cmd_name]["executions"] += 1
            self.total_executed += 1
            self.last_cmd_time = elapsed
            self.history.append({
                "command": cmd_name,
                "args": args,
                "time": elapsed,
                "timestamp": datetime.now()
            })
            return result, None
        except Exception as e:
            return None, f"[!] Error ejecutando {cmd_name}: {str(e)}\n{traceback.format_exc()}"

    def get_category(self, category):
        return self.categories.get(category, [])

    def search(self, query):
        results = []
        query_lower = query.lower()
        for name, info in self.commands.items():
            if query_lower in name.lower() or query_lower in info["description"].lower():
                results.append((name, info))
        return results

    def load_modules(self, base_path):
        package = importlib.import_module("commands")
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=os.path.join(base_path, "commands"),
            prefix="commands."
        ):
            try:
                module = importlib.import_module(modname)
                if hasattr(module, "register_commands"):
                    module.register_commands(self)
            except Exception as e:
                print(f"[!] Error cargando {modname}: {e}")

    def get_stats(self):
        uptime = datetime.now() - self.session_start
        return {
            "total_commands": len(self.commands),
            "total_categories": len(self.categories),
            "total_executed": self.total_executed,
            "session_uptime": str(uptime).split(".")[0],
            "history_size": len(self.history)
        }

    def get_all_commands(self):
        return sorted(self.commands.keys())

    def get_command_info(self, name):
        cmd_name = self.aliases.get(name, name)
        return self.commands.get(cmd_name)
