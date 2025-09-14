from engine_core import *
from engine_ui import *

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(300, 50))
engine.add_object(vec2(50, 450), vec2(600, 50))
engine.add_object(vec2(50, 400), vec2(900, 50))

ui = UIObject("Floor Editor", vec2(100, 100), 300, 200, engine)
ui.add_number(600)

while engine.looping:
    engine.floor = ui.numbers[0].get_value()
    engine.main_loop()