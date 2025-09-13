import pygame
from engine_math import *

class UIObject:
    def __init__(self, title, pos, width, height, engine):
        self.title = title
        self.pos = pos
        self.width = width
        self.height = height

        engine.ui.append(self)

        self.dragging = False
        self.drag_offset = vec2(0, 0)

        self.font = pygame.font.Font("Font/ProggyClean.ttf", 16)

    def update(self):
        mouse_pos = vec2(*pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed:
            if not self.dragging:
                if (0 <= mouse_pos.x - self.pos.x <= self.width and 0 <= mouse_pos.y - self.pos.y <= 15):
                    self.dragging = True
                    self.drag_offset = self.pos - mouse_pos
            if self.dragging:
                self.pos = mouse_pos + self.drag_offset
        else:
            self.dragging = False


    def render(self, screen):
        pygame.draw.rect(screen, (30, 30, 30, 122), (self.pos.x, self.pos.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, (150, 30, 30, 122), (self.pos.x, self.pos.y, self.width, 15), border_radius=5)
        text_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x + 5, self.pos.y))
