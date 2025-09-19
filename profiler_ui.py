from ui_container import *
import time

class ProfilerUI:
    def __init__(self, engine, pos):
        self.engine = engine
        self.ui = UIObject("Profiler", pos, 300, 200, engine)

        self.ui.add_label("Object Render Time: 0", id="obj_rend")
        self.ui.add_label("Draw Call Render Time: 0", id="draw_call_rend")
        self.ui.add_label("UI Render Time: 0", id="ui_rend")
        self.ui.add_label("Event Handle Time: 0", id="event_handle")
        self.ui.add_label("Object Update Time: 0", id="obj_update")
        self.ui.add_label("UI Update Time: 0", id="ui_update")
        self.ui.add_label("Newtonian Physics Time: 0", id="newton_phys_time")
        self.ui.add_label("Basic Physics Time: 0", id="basic_phys_time")

    def update_profiler(self):
        self.ui.set_value("obj_rend", f"Object Render Time: {self.engine.obj_render_time*1000:.2f}ms")
        self.ui.set_value("draw_call_rend", f"Draw Call Render Time: {self.engine.draw_call_render_time*1000:.2f}ms")
        self.ui.set_value("ui_rend", f"UI Render Time: {self.engine.ui_render_time*1000:.2f}ms")
        self.ui.set_value("event_handle", f"Event Handle Time: {self.engine.event_handle_time*1000:.2f}ms")
        self.ui.set_value("obj_update", f"Object Update Time: {self.engine.obj_update_time*1000:.2f}ms")
        self.ui.set_value("ui_update", f"UI Update Time: {self.engine.ui_update_time*1000:.2f}ms")
        self.ui.set_value("newton_phys_time", f"Newtonian Physics Time: {self.engine.newtonian_physics_time*1000:.2f}ms")
        self.ui.set_value("basic_phys_time", f"Basic Physics Time: {self.engine.basic_physics_time*1000:.2f}ms")