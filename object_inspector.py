from ui_container import UIObject
from engine_math import vec2

class ProfilerUI:
    def __init__(self, engine, pos):
        self.engine = engine
        self.ui = UIObject("Profiler", pos, 300, 200, engine)

        self.ui.add_vec2(vec2(), "Object Position")
        self.ui.add_vec2(vec2(), "Object Velocity")
        self.ui.add_label("Object Type: ", "obj_type")

    def update(self):
        self.ui.set_value()