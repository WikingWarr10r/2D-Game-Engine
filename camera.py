from engine_math import vec2
import pygame

class Camera:
    def __init__(self, pos: vec2, zoom: int):
        self.pos = pos
        self.zoom = zoom

    def ws_to_ss_vec(self, vector):
        if isinstance(vector, vec2):
            return (vector - self.pos) * vec2(self.zoom, self.zoom)
        if isinstance(vector, tuple):
            return ((vector[0] - self.pos.x)*self.zoom, (vector[1] - self.pos.y)*self.zoom)

    def ws_to_ss_num(self, num):
        return num * self.zoom
    
    def ss_to_ws_vec(self, vector):
        if isinstance(vector, vec2):
            return (vector + self.pos) / vec2(self.zoom, self.zoom)
        if isinstance(vector, tuple):
            return ((vector[0] + self.pos.x)/self.zoom, (vector[1] + self.pos.y)/self.zoom)
        
    def centre(self, pos):
        self.pos = vec2(pos.x - 1280/2, pos.y - 720/2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos.x -= 5
        if keys[pygame.K_RIGHT]:
            self.pos.x += 5
        if keys[pygame.K_UP]:
            self.pos.y -= 5
        if keys[pygame.K_DOWN]:
            self.pos.y += 5

        #if keys[pygame.K_q]:
        #    self.zoom += 1/60
        #if keys[pygame.K_e]:
        #    self.zoom -= 1/60

        if self.zoom <= 0:
            self.zoom = 1