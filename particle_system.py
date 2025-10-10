from engine_core import *
import random

class ParticleSystem:
    def __init__(self, engine: EngineCore, pos, vel):
        self.engine = engine
        self.pos = pos
        self.vel = vel

    def spawn_particles(self):
        self.engine.add_circle(self.pos, self.vel + vec2(random.randint(-5,5),random.randint(-5,5)), random.randint(2,5), False, False)