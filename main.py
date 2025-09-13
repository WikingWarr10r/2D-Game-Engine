from engine_core import *

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(1000, 50))
engine.add_object(vec2(50, 450), vec2(1000, 50))
engine.add_object(vec2(50, 400), vec2(1000, 50))
engine.add_object(vec2(1000, 500), vec2(-1000, 50))
engine.add_object(vec2(1000, 450), vec2(-1000, 50))
engine.add_object(vec2(1000, 400), vec2(-1000, 50))

while engine.looping:
    engine.main_loop()