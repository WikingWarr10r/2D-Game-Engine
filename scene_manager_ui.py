from ui_container import *
from scene_manager import SceneManager

class SceneManagerUI:
    def __init__(self, engine, pos, physics_ui):
        self.engine = engine
        self.ui = UIObject("Scene Manager", pos, 300, 200, engine)
        self.scene_manager = SceneManager(engine)
        self.physics_ui = physics_ui

        self.ui.add_button(False, "Save Scene", True)
        self.ui.add_button(False, "Load Scene", True)

    def update(self):
        if self.ui.get_value("Save Scene"):
            self.scene_manager.store()

        if self.ui.get_value("Load Scene"):
            self.scene_manager.load()
            self.physics_ui.regenerate()