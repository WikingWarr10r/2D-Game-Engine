# Access the modules in the engine
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pygame
from engine_math import vec2, math
from particle_system import ParticleSystem

ps = ParticleSystem(None, vec2(), vec2())

# Init function called once at the beginning
def init(obj, engine):
    pass

# Update function called every frame
def update(obj, engine):
    global ps
    ps.engine = engine
    ps.pos = obj.pos
    ps.vel = vec2(-1, -1) * obj.vel
    force_magnitude = 0
    if engine.keys[pygame.K_w]:
        force_magnitude = 5
        ps.spawn_particles()
    if engine.keys[pygame.K_d]:
        obj.ang_vel += 0.01
    if engine.keys[pygame.K_a]:
        obj.ang_vel -= 0.01
        
    rad = -obj.angle+90
    force = vec2(math.cos(rad), -math.sin(rad)) * force_magnitude
    obj.add_force(force)

    engine.cam.centre(obj.pos)