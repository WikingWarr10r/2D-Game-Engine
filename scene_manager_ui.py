from ui_container import *

class SceneManagerUI:
    def __init__(self, engine, pos):
        self.engine = engine
        self.ui = UIObject("Scene Manager", pos, 300, 200, engine)
        self.ui.add_button(False, "Save Scene", True)
        self.ui.add_button(False, "Load Scene", True)
