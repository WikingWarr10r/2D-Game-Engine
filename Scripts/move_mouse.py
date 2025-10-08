# Access the modules in the engine
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pygame
import engine_core
from engine_math import vec2

# Init function called once at the beginning
def init(obj):
    pass

# Update function called every frame
def update(obj):
    obj.pos = vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])