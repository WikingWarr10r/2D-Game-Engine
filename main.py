from engine_core import *
from physics_ui import PhysicsUI

engine = EngineCore()

ui = PhysicsUI(engine, vec2(950, 30))

while engine.looping:
    start = time.time()
    ui.update_simulation()
    ui.object_spawning()

    engine.main_loop()
    ui.update_stats(start)