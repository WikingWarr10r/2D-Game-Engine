import os, importlib

class Script:
    def __init__(self, file):
        self.module_name = file[:-3]
        self.module = importlib.import_module(f"Scripts.{self.module_name}")

    def init(self):
        if hasattr(self.module, "init"):
            self.module.init()

    def update(self):
        if hasattr(self.module, "update"):
            self.module.update()

class ScriptSystem:
    def __init__(self):
        self.modules = []
        self.scripts = os.listdir("Scripts")
        for script in self.scripts:
            if script.endswith(".py") and script != "__init__.py":
                s = Script(script)
                self.modules.append(s)
                print(f"Imported {s.module_name}")

    def init(self):
        for script in self.modules:
            script.init()

    def update(self):
        for script in self.modules:
            script.update()