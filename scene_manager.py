class SceneManager:
    def __init__(self, engine):
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

        for obj in self.objects:
            obj.store()