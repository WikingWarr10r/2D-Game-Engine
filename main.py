from engine_core import *
from physics_ui import PhysicsUI
from profiler_ui import ProfilerUI

engine = EngineCore()

ui = PhysicsUI(engine, vec2(950, 30))
profiler = ProfilerUI(engine, vec2(30, 30))

while engine.looping:
    start = time.time()
    ui.update_simulation()
    ui.object_spawning()

    engine.main_loop()
    ui.update_stats(start)
    profiler.update_profiler()