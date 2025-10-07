from engine_core import *
from camera import Camera

from physics_ui import PhysicsUI
from profiler_ui import ProfilerUI
from scene_manager_ui import SceneManagerUI
from object_inspector import InspectorUI

engine = EngineCore()

cam = Camera(vec2(0,0), 1)
engine.add_camera(cam)

ui = PhysicsUI(engine, vec2(950, 30))
profiler = ProfilerUI(engine, vec2(30, 30))

scene_manager = SceneManagerUI(engine, vec2(30, 615), ui)

inspector = InspectorUI(engine, vec2(30, 320), None)

while engine.looping:
    start = time.time()
    ui.update_simulation()
    ui.object_spawning()
    scene_manager.update()
    inspector.update()

    cam.update()

    engine.main_loop()
    ui.update_stats(start)
    profiler.update_profiler()