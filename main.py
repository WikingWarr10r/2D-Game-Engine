from engine_core import *
from engine_ui import *

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(300, 50))
engine.add_object(vec2(50, 450), vec2(600, 50))
engine.add_object(vec2(50, 400), vec2(900, 50))

ui = UIObject("Position Editor", vec2(100, 100), 300, 200, engine)

while engine.looping:
    engine.main_loop()