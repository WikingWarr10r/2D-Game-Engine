from ui_container import *
import time

class PhysicsUI:
    def __init__(self, engine, pos):
        self.engine = engine
        self.held = False

        self.ui = UIObject("Physics Editor", pos, 300, 200, engine)
        self.ui.add_label("Engine Variables:")
        self.ui.add_choice(["Basic", "Newtonian"], "Simulation Type")
        self.ui.add_number(600, "Floor Height")
        self.ui.add_number(10, "Gravity")
        self.ui.add_spacer()

        self.ui.add_label("Spawn Position:")
        self.ui.add_vec2(vec2(0, 0), "Position")
        self.ui.add_label("Spawn Velocity:")
        self.ui.add_vec2(vec2(0, 0), "Velocity")
        self.ui.add_number(15, "Object Radius", [1, "inf"])
        self.ui.add_spacer()
        self.ui.add_button(False, "Add New Object", True)
        self.ui.add_button(False, "Mouse Mode", False)
        self.ui.add_button(False, "Fast Spawn", False)
        self.ui.add_button(False, "Locked", False)
        self.ui.add_spacer()
        
        self.ui.add_label("Simulation:")
        self.ui.add_button(False, "Pause Simulation", False)
        self.ui.add_button(False, "Clear Objects", True)
        self.ui.add_number(1, "Delta Time Divisor", [1, "inf"])
        self.ui.add_spacer()

        self.ui.add_label("Engine Statistics:")

        self.ui.add_label("FPS: 0", id="fps")
        self.ui.add_label("Number of Objects: 0", id="num_objects")
        self.ui.add_label("Fixed Timestep: 0", id="dt")
        self.ui.add_label("Memory Usage: 0MB", id="mem")
    
    def update_simulation(self):
        if self.ui.get_value("Simulation Type") == "Newtonian":
            self.engine.sim_type = "Newtonian Gravity"
        else:
            self.engine.sim_type = "Basic"

        self.engine.floor = self.ui.get_value("Floor Height")
        self.engine.gravity = self.ui.get_value("Gravity")
        if self.ui.get_value("Pause Simulation") == True:
            self.engine.dt = 0
        else:
            self.engine.dt = 1/60

        self.engine.dt /= self.ui.get_value("Delta Time Divisor")

        if self.ui.get_value("Clear Objects"):
            self.engine.objects = []

    def object_spawning(self):
        position = self.ui.get_value("Position")
        velocity = self.ui.get_value("Velocity")
        radius = self.ui.get_value("Object Radius")
        lock = self.ui.get_value("Locked")
        mouse_pos = vec2(*pygame.mouse.get_pos())
        
        ui_rect = pygame.Rect(self.ui.pos.x, self.ui.pos.y, self.ui.width, self.ui.height)

        if self.ui.get_value("Fast Spawn"):
            self.held = False

        if self.ui.get_value("Mouse Mode"):
            self.ui.set_value("Position", mouse_pos)
            if pygame.mouse.get_pressed()[0] and not ui_rect.collidepoint(mouse_pos.x, mouse_pos.y) and self.held == False:
                self.engine.add_object(position, velocity, radius, lock)
                self.held = True
            if not pygame.mouse.get_pressed()[0]:
                self.held = False
            if pygame.mouse.get_pressed()[2]:
                for obj in self.engine.objects:
                    length = (mouse_pos - obj.pos).length()
                    obj.add_force(((mouse_pos - obj.pos) / vec2(length, length)) * 50)

        if self.ui.get_value("Add New Object"):
            if self.held == False:
                self.engine.add_object(position, velocity, radius, lock)
                self.held = True
        else:
            if not self.ui.get_value("Mouse Mode"):
                self.held = False

        self.engine.draw_cross(position)
        self.engine.draw_line(position, position + (velocity/vec2(10, 10)), (255, 0, 0, 122))
    
    def update_stats(self, start):
        self.ui.set_value("fps", f"FPS: {int(1/(time.time()-start))}")
        self.ui.set_value("num_objects", f"Number Of Objects: {len(self.engine.objects)}")
        self.ui.set_value("dt", f"Fixed Timestep: {smart_number(self.engine.dt)}")
        self.ui.set_value("mem", f"Memory Usage: {self.engine.process.memory_info().rss / 1024**2:.2f}MB")