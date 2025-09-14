import pygame

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

    def setup_screen(self, width=1280, height=720):
        self.screen = pygame.display.set_mode((width,height))
        
    def render(self):
        self.screen.fill("black")
        pygame.draw.line(self.screen, "white", (0, self.floor+15), (1280, self.floor+15), 5)


        for obj in self.objects:
            obj.render(self.screen)

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
            obj.update(self.gravity, self.bounciness, self.air_resistance, self.friction, self.floor)
            
        for ui in self.ui:
            ui.update()

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
    
    def add_object(self, pos: vec2, vel: vec2):
        self.objects.append(Object(pos, vel))