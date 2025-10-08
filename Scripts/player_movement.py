# Access the modules in the engine
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pygame
from engine_math import vec2

# Init function called once at the beginning
def init(obj, engine):
    pass

# Update function called every frame
def update(obj, engine):
    force = vec2()
    if engine.keys[pygame.K_w] and engine.floor - obj.pos.y < obj.radius + 10:
        force.y = -50
    if engine.keys[pygame.K_d] and obj.vel.x < 200:
        force.x = 20
    if engine.keys[pygame.K_a] and obj.vel.x > -200:
        force.x = -20
    
    obj.add_force(force)