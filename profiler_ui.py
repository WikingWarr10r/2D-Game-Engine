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
        self.ui.add_pie_chart("Profiler Times")

    def update_profiler(self): 
        profiler_times = [self.engine.obj_render_time, self.engine.draw_call_render_time, self.engine.ui_render_time, self.engine.event_handle_time, self.engine.obj_update_time, self.engine.ui_update_time, self.engine.newtonian_physics_time, self.engine.basic_physics_time]

        profiler_dict = {
            "Object Render Time": profiler_times[0],
            "Draw Call Render Time": profiler_times[1],
            "UI Render Time": profiler_times[2],
            "Event Handle Time": profiler_times[3],
            "Object Update Time": profiler_times[4],
            "UI Update Time": profiler_times[5],
            "Newtonian Physics Time": profiler_times[6],
            "Basic Physics Time": profiler_times[7]
        }

        self.ui.set_value("obj_rend", f"Object Render Time: {profiler_times[0]*1000:.2f}ms")
        self.ui.set_value("draw_call_rend", f"Draw Call Render Time: {profiler_times[1]*1000:.2f}ms")
        self.ui.set_value("ui_rend", f"UI Render Time: {profiler_times[2]*1000:.2f}ms")
        self.ui.set_value("event_handle", f"Event Handle Time: {profiler_times[3]*1000:.2f}ms")
        self.ui.set_value("obj_update", f"Object Update Time: {profiler_times[4]*1000:.2f}ms")
        self.ui.set_value("ui_update", f"UI Update Time: {profiler_times[5]*1000:.2f}ms")
        self.ui.set_value("newton_phys_time", f"Newtonian Physics Time: {profiler_times[6]*1000:.2f}ms")
        self.ui.set_value("basic_phys_time", f"Basic Physics Time: {profiler_times[7]*1000:.2f}ms")
        self.ui.set_value("Profiler Times", profiler_dict)