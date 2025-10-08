import os, importlib
import ast
from pathlib import Path

def static_check(path: Path) -> bool:    
    BANNED_MODULES = {"subprocess", "socket", "shutil", "requests", "ctypes", "fcntl", "http", "ftplib", "urllib"}

    BANNED_FUNCTIONS = {"system", "popen", "remove", "rmdir", "unlink", "exec", "eval", "compile", "open", "__import__", "globals", "locals", "vars", "input"}

    DANGEROUS_STRINGS = ["rm -rf", "/dev/sda", "dd if=", "mkfs", "/etc/passwd"]

    try:
        text = path.read_text(encoding="utf8", errors="ignore")
        tree = ast.parse(text, filename=str(path))
    except Exception:
        print(f"Static check failed: Cannot parse {path}")
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name.split(".")[0] in BANNED_MODULES:
                    print(f"Static check failed: Banned import {n.name}")
                    return False
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in BANNED_MODULES:
                print(f"Static check failed: Banned import {node.module}")
                return False

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in BANNED_FUNCTIONS:
                    print(f"Static check failed: Banned function {node.func.attr}")
                    return False
            elif isinstance(node.func, ast.Name):
                if node.func.id in BANNED_FUNCTIONS:
                    print(f"Static check failed: Banned function {node.func.id}")
                    return False

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for s in DANGEROUS_STRINGS:
                if s in node.value:
                    print(f"Static check failed: Suspicious string '{s}' found")
                    return False

    return True

class Script:
    def __init__(self, file, obj):
        self.module_name = file[:-3]
        self.obj = obj

        self.safe = static_check(Path(f"Scripts/{file}"))
        if self.safe: 
            print(f"{self.module_name} passed static check")
            self.module = importlib.import_module(f"Scripts.{self.module_name}")
        else:
            self.module = None

    def init(self):
        if hasattr(self.module, "init") and self.safe:
            self.module.init(self.obj)

    def update(self):
        if hasattr(self.module, "update") and self.safe:
            self.module.update(self.obj)

class ScriptSystem:
    def __init__(self):
        self.modules = []
        self.scripts = os.listdir("Scripts")
        for script in self.scripts:
            if script.endswith(".py") and script != "__init__.py":
                s = Script(script, None)
                if s.safe:
                    self.modules.append(s)
                    print(f"Imported {s.module_name}")
                else:
                    print(f"{s.module_name} is unsafe, not importing")

    def init(self):
        for script in self.modules:
            if not script.obj == None:
                script.init()

    def update(self):
        for script in self.modules:
            if not script.obj == None:
                script.update()

    def attach_to_object(self, script, obj):
        self.modules[self.scripts.index(script)].obj = obj

    def detach_from_object(self, script):
        self.modules[self.scripts.index(script)].obj = None

    def detach_all_scripts(self):
        for script in self.modules:
            script.obj = None
