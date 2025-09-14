from engine_core import *
from engine_ui import *

engine = EngineCore()

ui = PhysicsUI(engine, vec2(950, 30))

while engine.looping:
    start = time.time()
    ui.update_simulation()
    ui.object_spawning()

    engine.main_loop()
    ui.update_stats(start)