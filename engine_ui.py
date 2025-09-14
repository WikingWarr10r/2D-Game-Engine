import pygame
from engine_math import *

class UINumber:
    def __init__(self, value, pos, label, font):
        self.value = value
        self.pos = pos
        self.label = label
        self.font = font
        self.width = 50
        self.height = 20

    def render(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, (150, 30, 30), rect, border_radius=5)

        text_surf = self.font.render(str(self.value), True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x + 5, self.pos.y + (self.height - text_surf.get_height()) / 2))

        text_surf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x + 5 + self.width, self.pos.y + (self.height - text_surf.get_height()) / 2))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = vec2(*pygame.mouse.get_pos())
            if (self.pos.x <= mouse_pos.x <= self.pos.x + self.width and self.pos.y <= mouse_pos.y <= self.pos.y + self.height):
                self.value += event.y

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value
    
class UIButton:
    def __init__(self, value, pos, label, font, hold:bool):
        self.value = value
        self.pos = pos
        self.label = label
        self.font = font
        self.width = 50
        self.height = 20

        self.hold = hold

    def render(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.value:
            pygame.draw.rect(screen, (150, 30, 30), rect, border_radius=5)
        else:
            pygame.draw.rect(screen, (100, 30, 30), rect, border_radius=5)

        text_surf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x + 5 + self.width, self.pos.y + (self.height - text_surf.get_height()) / 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = vec2(*pygame.mouse.get_pos())
            if (self.pos.x <= mouse_pos.x <= self.pos.x + self.width and self.pos.y <= mouse_pos.y <= self.pos.y + self.height):
                if self.hold == True:
                    self.value = True
                else:
                    self.value = not self.value
        else:
            if self.hold == True:
                self.value = False

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value

class UISpacer:
    def __init__(self, pos):
        self.pos = pos

    def render(self, screen):
        pass

    def handle_event(self, event):
        pass

class UILabel:
    def __init__(self, pos, label, font):
        self.pos = pos
        self.label = label
        self.font = font

    def render(self, screen):
        text_surf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(text_surf, (self.pos.x, self.pos.y + (text_surf.get_height()) / 2))

    def handle_event(self, event):
        pass

class UIObject:
    def __init__(self, title, pos, width, height, engine):
        self.title = title
        self.pos = pos
        self.width = width
        self.height = height
        engine.ui.append(self)

        self.elements = []
        self.lookup = {}

        self.dragging = False
        self.drag_offset = vec2(0, 0)

        self.font = pygame.font.Font("font/ProggyClean.ttf", 16)

    def add_number(self, val: int, label):
        num = UINumber(val, vec2(0, 0), label, self.font)
        self.elements.append(num)
        self.lookup[label] = num

    def add_button(self, val: bool, label, hold):
        button = UIButton(val, vec2(0, 0), label, self.font, hold)
        self.elements.append(button)
        self.lookup[label] = button

    def add_spacer(self):
        spacer = UISpacer(vec2(0, 0))
        self.elements.append(spacer)

    def add_label(self, label):
        lab = UILabel(vec2(0,0), label, self.font)
        self.elements.append(lab)
        self.lookup[label] = lab

    def get_value(self, label):
        if label in self.lookup:
            return self.lookup[label].get_value()
        return None

    def handle_event(self, event):
        for elem in self.elements:
            elem.handle_event(event)

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
        self.height = 20 + len(self.elements) * 25

        pygame.draw.rect(screen, (30, 30, 30,), (self.pos.x, self.pos.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, (150, 30, 30), (self.pos.x, self.pos.y, self.width, 15), border_radius=5)
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (self.pos.x + 5, self.pos.y + (15 - title_surf.get_height()) / 2))

        for i, elem in enumerate(self.elements):
            elem.pos = vec2(self.pos.x + 5, self.pos.y + 20 + i * 25)
            elem.render(screen)
