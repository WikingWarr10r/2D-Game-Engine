import pygame
from engine_math import *

class UINumber:
    def __init__(self, value, pos, font):
        self.value = value
        self.pos = pos
        self.font = font
        self.width = 50
        self.height = 20

    def render(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, (150, 30, 30), rect, border_radius=5)

        text_surf = self.font.render(str(self.value), True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x + 5, self.pos.y + (self.height - text_surf.get_height()) / 2))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = vec2(*pygame.mouse.get_pos())
            if (self.pos.x <= mouse_pos.x <= self.pos.x + self.width and self.pos.y <= mouse_pos.y <= self.pos.y + self.height):
                self.value += event.y

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value


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
        num = UINumber(val, vec2(0, 0), self.font)
        self.numbers.append(num)

    def handle_event(self, event):
        for num in self.numbers:
            num.handle_event(event)

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
        self.height = 20 + len(self.numbers) * 25

        pygame.draw.rect(screen, (30, 30, 30), (self.pos.x, self.pos.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, (150, 30, 30), (self.pos.x, self.pos.y, self.width, 15), border_radius=5)
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (self.pos.x + 5, self.pos.y + (15 - title_surf.get_height()) / 2))

        for i, num in enumerate(self.numbers):
            num.pos = vec2(self.pos.x + 5, self.pos.y + 20 + i * 25)
            num.render(screen)
