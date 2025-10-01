from ui_container import *
from scene_manager import SceneManager
import os

class SceneManagerUI:
    def __init__(self, engine, pos, physics_ui):
        self.engine = engine
        self.ui = UIObject("Scene Manager", pos, 300, 200, engine)
        self.scene_manager = SceneManager(engine)
        self.physics_ui = physics_ui

        scenes = os.listdir("Scenes/")

        self.ui.add_button(False, "Save Scene", True)
        self.ui.add_button(False, "Load Scene", True)
        self.ui.add_choice(scenes, "Choose Scene")

    def update(self):
        if self.ui.get_value("Save Scene"):
            self.scene_manager.store()

        if self.ui.get_value("Load Scene"):
            self.scene_manager.load(self.ui.get_value("Choose Scene"))
            self.physics_ui.regenerate()