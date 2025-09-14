from engine_core import *
from engine_ui import *

engine = EngineCore()

ui = PhysicsUI(engine)

while engine.looping:
    start = time.time()
    ui.update_variables()
    ui.object_spawning()

    engine.main_loop()
    ui.update_stats(start)