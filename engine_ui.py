import pygame
from engine_math import *

class UIObject:
    def __init__(self, title, pos, width, height, engine):
        self.title = title
        self.pos = pos
        self.width = width
        self.height = height
        engine.ui.append(self)

        self.numbers = []
        self.dragging = False
        self.drag_offset = vec2(0, 0)

        self.font = pygame.font.Font("font/ProggyClean.ttf", 16)

    def add_number(self, val):
        self.numbers.append(val)

    def update(self):
        mouse_pos = vec2(*pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed:
            if not self.dragging:
                if (0 <= mouse_pos.x - self.pos.x <= self.width and
                    0 <= mouse_pos.y - self.pos.y <= 15):
                    self.dragging = True
                    self.drag_offset = self.pos - mouse_pos
            if self.dragging:
                self.pos = mouse_pos + self.drag_offset
        else:
            self.dragging = False

    def render(self, screen):
        self.height = 20 + len(self.numbers) * 25

        pygame.draw.rect(screen, (30, 30, 30), (self.pos.x, self.pos.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, (150, 30, 30), (self.pos.x, self.pos.y, self.width, 15), border_radius=5)
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (self.pos.x + 5, self.pos.y + (15 - title_surf.get_height()) / 2))

        for i, val in enumerate(self.numbers):
            x = self.pos.x + 5
            y = self.pos.y + 20 + i * 25
            pygame.draw.rect(screen, (150, 30, 30), (x, y, 50, 20), border_radius=5)
            text_surf = self.font.render(str(val), True, (255, 255, 255))
            screen.blit(text_surf, (x + 5, y + (20 - text_surf.get_height()) / 2))
