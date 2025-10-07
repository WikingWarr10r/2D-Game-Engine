from ui_container import UIObject
from engine_math import vec2
from engine_object import Object, Rectangle
import pygame

class InspectorUI:
    def __init__(self, engine, pos, obj=None):
        self.engine = engine
        self.ui = UIObject("Inspector", pos, 300, 200, engine)
        self.obj = obj

        self.ui.add_label("Object Type: ", "obj_type")
        self.ui.add_label("Position:")
        self.ui.add_vec2(vec2(), "Object Position")
        self.ui.add_label("Velocity:")
        self.ui.add_vec2(vec2(), "Object Velocity")


    def update(self):
        if pygame.mouse.get_pressed()[0] and not self.engine.mouse_over_ui():
            mouse = pygame.mouse.get_pos()
            self.obj = self.engine.find_closest_obj(self.engine.cam.ss_to_ws_vec(vec2(mouse[0], mouse[1])))

        if not self.obj == None:
            obj_type = ""
            if type(self.obj) == Object:
                obj_type = "Circle"
                self.engine.draw_circle(self.obj.radius + 2, self.engine.cam.ws_to_ss_vec(self.obj.pos), (255, 0, 0, 122))
            else:
                obj_type = "Rectangle"
                self.engine.draw_rect(self.engine.cam.ws_to_ss_vec(self.obj.pos), self.obj.width+4, self.obj.height+4, (255, 0, 0, 122))
            self.ui.set_value("obj_type", f"Object Type: {obj_type}")
            self.ui.set_value("Object Position", self.obj.pos)
            self.ui.set_value("Object Velocity", self.obj.vel)
        else:
            self.ui.set_value("obj_type", f"None Selected")
            self.ui.set_value("Object Position", vec2(0,0))
            self.ui.set_value("Object Velocity", vec2(0,0))
