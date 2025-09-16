import pygame
import time
import psutil
import os
from collections import deque

from engine_math import *
from engine_object import *

class EngineCore:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.looping = True
        
        self.objects = []
        self.ui = []

        self.gravity = 10
        self.bounciness = 0.7
        self.air_resistance = 0.999
        self.friction = 0.8
        self.floor = 600
        self.dt = 1/60
        self.gravitational_constant = -10000

        self.sim_type = "Newtonian Gravity"

        self.draw_calls = []

        self.process = psutil.Process(os.getpid())

        self.setup_screen()

    def setup_screen(self, width=1280, height=720):
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Engine")
        
    def draw_circle(self, radius, pos:vec2, colour=(255, 255, 255, 122)):
        self.draw_calls.append(lambda: pygame.draw.circle(self.screen, colour, pos, radius))
    
    def draw_cross(self, centre, colour=(255, 255, 255, 122)):
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (centre.x - 10, centre.y), (centre.x + 10, centre.y)))
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (centre.x, centre.y - 10), (centre.x, centre.y + 10)))

    def draw_line(self, start, end, colour=(255, 255, 255, 122)):
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (start.x, start.y), (end.x, end.y)))

    def render(self):
        self.screen.fill("black")
        pygame.draw.line(self.screen, "white", (0, self.floor), (1280, self.floor), 5)

        for obj in self.objects:
            obj.render(self.screen)

        for draw_call in self.draw_calls:
            draw_call()
        self.draw_calls.clear()

        for ui in self.ui:
            ui.render(self.screen)

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            for ui in self.ui:
                ui.handle_event(event)
        
        for obj in self.objects:
            obj.update(self.gravity, self.bounciness, self.air_resistance, self.friction, self.floor, self.dt, self.sim_type)
            
        for ui in self.ui:
            ui.update()

        if self.sim_type == "Newtonian Gravity":
            for i in range(len(self.objects)):
                for j in range(i+1, len(self.objects)):
                    a = self.objects[i]
                    b = self.objects[j]

                    distance = (a.pos-b.pos).length()
                    force = self.gravitational_constant * ((a.mass*b.mass)/(distance**2))
                    a_force = (vec2(force, force) * ((a.pos - b.pos) / vec2(distance, distance))) * vec2(.5, .5)
                    b_force = (vec2(force, force) * ((b.pos - a.pos) / vec2(distance, distance))) * vec2(.5, .5)
                    
                    print(a_force)

                    a.add_force(a_force)
                    b.add_force(b_force)


        for i in range(len(self.objects)):
            for j in range(i+1, len(self.objects)):
                a = self.objects[i]
                b = self.objects[j]
                if a.check_collision(b):
                    a.resolve_overlap(b)
                    a.collision_response(b)
        
        self.render()

        pygame.display.flip()
        self.clock.tick(60)
    
    def add_object(self, pos: vec2, vel: vec2, radius):
        self.objects.append(Object(pos, vel, radius))