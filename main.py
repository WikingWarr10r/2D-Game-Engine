from engine_core import *
from camera import Camera
from script_system import ScriptSystem

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

script_system = ScriptSystem()
script_system.init()
inspector = InspectorUI(engine, script_system, vec2(30, 320))

while engine.looping:
    start = time.time()

    # UI
    ui.update_simulation()
    ui.object_spawning()
    scene_manager.update()
    inspector.update()

    # Script System
    script_system.update()

    # Camera
    cam.update()

    # Engine Main Loop
    engine.main_loop()

    # Extra UI
    ui.update_stats(start)
    profiler.update_profiler()