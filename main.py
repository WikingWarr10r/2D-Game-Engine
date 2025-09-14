from engine_core import *
from engine_ui import *

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(300, 50))
engine.add_object(vec2(50, 450), vec2(600, 50))
engine.add_object(vec2(50, 400), vec2(900, 50))

ui = UIObject("Physics Editor", vec2(100, 100), 300, 200, engine)
ui.add_label("Engine Variables")
ui.add_number(600, "Floor Height")
ui.add_number(10, "Gravity")
ui.add_spacer()

ui.add_label("Position:")
ui.add_number(0, "x")
ui.add_number(0, "y")
ui.add_spacer()
ui.add_button(False, "Add New Object", True)

while engine.looping:
    engine.floor = ui.get_value("Floor Height")
    engine.gravity = ui.get_value("Gravity")

    position = vec2(ui.get_value("x"), ui.get_value("y"))
    engine.draw_cross(position)

    if ui.get_value("Add New Object"):
        engine.add_object(position, vec2(0, 0))

    engine.main_loop()