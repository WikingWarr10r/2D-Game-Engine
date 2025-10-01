from engine_core import *
from physics_ui import PhysicsUI
from profiler_ui import ProfilerUI
from scene_manager_ui import SceneManagerUI
from camera import Camera

engine = EngineCore()

cam = Camera(vec2(0,0), 1)
engine.add_camera(cam)

ui = PhysicsUI(engine, vec2(950, 30))
profiler = ProfilerUI(engine, vec2(30, 30))

scene_manager = SceneManagerUI(engine, vec2(30, 615), ui)

while engine.looping:
    start = time.time()
    ui.update_simulation()
    ui.object_spawning()
    scene_manager.update()

    cam.update()

    engine.main_loop()
    ui.update_stats(start)
    profiler.update_profiler()