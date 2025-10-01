from engine_object import Object
from engine_core import EngineCore
import os

class SceneManager:
    def __init__(self, engine: EngineCore):
        self.engine = engine

        self.objects = []
        self.ui = []

        self.gravity = 0
        self.bounciness = 0
        self.air_density = 0
        self.drag_coefficient = 0
        self.friction = 0
        self.floor = 0
        self.dt = 0
        self.gravitational_constant = 0

        self.sim_type = "Newtonian Gravity"

    def store(self):
        self.objects = self.engine.objects
        self.ui = self.engine.ui
        self.gravity = self.engine.gravity
        self.bounciness = self.engine.bounciness
        self.air_density = self.engine.air_density
        self.drag_coefficient = self.engine.drag_coefficient
        self.friction = self.engine.friction
        self.floor = self.engine.floor
        self.dt = self.engine.dt
        self.gravitational_constant = self.engine.gravitational_constant
        self.sim_type = self.engine.sim_type

        objs = ""
        for obj in self.objects:
            objs = objs + obj.store()
            if not obj == self.objects[-1]:
                objs = objs + "#"

        generated_scene = f"{self.gravity}~{self.bounciness}~{self.air_density}~{self.drag_coefficient}~{self.friction}~{self.floor}~{self.dt}~{self.gravitational_constant}~{self.sim_type}~{objs}"
        
        with open("Scenes/main.scene", "w") as scene:
            scene.write(generated_scene)
        scene.close()

    def load(self):
        try:
            generated_scene = ""
            with open("Scenes/main.scene", "r") as scene:
                generated_scene = scene.readline()
            scene.close()
            scn = generated_scene.split("~")
            objs = scn[-1]
            scn.remove(scn[-1])

            objects = objs.split("#")
            final_objects = []
            for stored_obj in objects:
                final_objects.append(Object.recreate_obj(stored_obj, self.engine.cam))

            self.engine.gravity = int(scn[0])
            self.engine.bounciness = float(scn[1])
            self.engine.air_density = float(scn[2])
            self.engine.drag_coefficient = float(scn[3])
            self.engine.friction = float(scn[4])
            self.engine.floor = int(scn[5])
            self.engine.dt = float(scn[6])
            self.engine.gravitational_constant = float(scn[7])
            self.engine.sim_type = str(scn[8])

            self.engine.objects = final_objects
        except:
            if os.path.exists("Scenes/main.scene"):
                print("Save file corrupted or missing, file will be deleted.")
                if os.path.exists("Scenes/main.scene"):
                    os.remove("Scenes/main.scene")
                    print("Corrupted scene succesfully deleted")
                    print("Try saving a new scene")
                else:
                    print("The scene does not exist")
