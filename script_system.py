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
    def __init__(self, file, objs, engine):
        self.module_name = file[:-3]
        self.objs = objs
        self.engine = engine

        self.safe = static_check(Path(f"Scripts/{file}"))
        if self.safe: 
            print(f"{self.module_name} passed static check")
            self.module = importlib.import_module(f"Scripts.{self.module_name}")
        else:
            self.module = None

    def check_for_duplicates(self):
        self.objs = list(set(self.objs))

    def init(self):
        if len(self.objs) > 0:
            for obj in self.objs:
                if hasattr(self.module, "init") and self.safe:
                    self.module.init(obj, self.engine)

    def update(self):
        if len(self.objs) > 0:
            for obj in self.objs:
                if hasattr(self.module, "update") and self.safe:
                    self.module.update(obj, self.engine)

class ScriptSystem:
    def __init__(self, engine):
        self.modules = []
        self.scripts = os.listdir("Scripts")
        self.engine = engine
        for script in self.scripts:
            if script.endswith(".py") and script != "__init__.py":
                s = Script(script, [], self.engine)
                if s.safe:
                    self.modules.append(s)
                    print(f"Imported {s.module_name}")
                else:
                    print(f"{s.module_name} is unsafe, not importing")

    def init(self):
        for script in self.modules:
            script.init()

    def update(self):
        for script in self.modules:
            script.update()
            script.check_for_duplicates()

    def attach_to_object(self, script, obj):
        self.modules[self.scripts.index(script)].objs.append(obj)

    def detach_all_scripts(self):
        for script in self.modules:
            script.objs = []

    def detach_all_scripts_from_obj(self, obj):
        for script in self.modules:
            if obj in script.objs:
                script.objs.remove(obj)