from engine_core import *
from engine_ui import *

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(300, 50))
engine.add_object(vec2(50, 450), vec2(600, 50))
engine.add_object(vec2(50, 400), vec2(900, 50))

ui = UIObject("Physics Editor", vec2(100, 100), 300, 200, engine)
ui.add_label("Engine Variables:")
ui.add_number(600, "Floor Height")
ui.add_number(10, "Gravity")
ui.add_spacer()

ui.add_label("Position:")
ui.add_vec2(vec2(0, 0), "Position")
ui.add_spacer()
ui.add_button(False, "Add New Object", True)
ui.add_spacer()

ui.add_label("Engine Statistics:")
fps = 0
ui.add_label("FPS: 0", id="fps")
ui.add_label("Number of Objects: 0", id="num_objects")
ui.add_label("Memory Usage: 0MB", id="mem")

while engine.looping:
    start = time.time()

    engine.floor = ui.get_value("Floor Height")
    engine.gravity = ui.get_value("Gravity")

    position = ui.get_value("Position")
    engine.draw_cross(position)

    if ui.get_value("Add New Object"):
        engine.add_object(position, vec2(0, 0))

    engine.main_loop()

    fps = 1/(time.time()-start)
    mem = engine.process.memory_info().rss / 1024**2

    ui.set_value("fps", f"FPS: {int(fps)}")
    ui.set_value("num_objects", f"Number Of Objects: {len(engine.objects)}")
    ui.set_value("mem", f"Memory Usage: {mem:.2f}MB")