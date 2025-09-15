import pygame
import sys
from engine_math import *

class UINumber:
    def __init__(self, value, pos, label, font, bounds=None):
        self.value = value
        self.pos = pos
        self.label = label
        self.font = font
        self.width = 50
        self.height = 20
        self.bounds = bounds
        if not bounds == None:
            bnds = bounds
            if bounds[0] == "-inf":
                bnds[0] = -sys.maxsize
            if bounds[1] == "inf":
                bnds[1] = sys.maxsize
            self.bounds = bnds

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

                if not self.bounds == None:
                    if self.value < self.bounds[0]:
                        self.value = self.bounds[0]
                    if self.value > self.bounds[1]:
                        self.value = self.bounds[1]



    def set_value(self, val):
        self.value = val
        if not self.bounds == None:
            if self.value < self.bounds[0]:
                self.value = self.bounds[0]
            if self.value > self.bounds[1]:
                self.value = self.bounds[1]

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

    def get_value(self):
        return self.label

    def set_value(self, val):
        self.label = str(val)

class UIVec2:
    def __init__(self, value, pos, label, font):
        self.value = value
        self.pos = pos
        self.label = label
        self.font = font
        self.width = 120
        self.height = 20

        self.box_width = 50
        self.box_height = 20

        self.spacing = 5

    def render(self, screen):
        x_start = self.pos.x

        text_x_label = self.font.render("x:", True, (255, 255, 255))
        screen.blit(text_x_label, (x_start, self.pos.y + (self.box_height - text_x_label.get_height()) / 2))
        x_start += text_x_label.get_width() + 2

        rect_x = pygame.Rect(x_start, self.pos.y, self.box_width, self.box_height)
        pygame.draw.rect(screen, (150, 30, 30), rect_x, border_radius=3)
        text_x = self.font.render(str(self.value.x), True, (255, 255, 255))
        screen.blit(text_x, (x_start + (self.box_width - text_x.get_width()) / 2, self.pos.y + (self.box_height - text_x.get_height()) / 2))
        x_start += self.box_width + self.spacing

        text_y_label = self.font.render("y:", True, (255, 255, 255))
        screen.blit(text_y_label, (x_start, self.pos.y + (self.box_height - text_y_label.get_height()) / 2))
        x_start += text_y_label.get_width() + 2

        rect_y = pygame.Rect(x_start, self.pos.y, self.box_width, self.box_height)
        pygame.draw.rect(screen, (150, 30, 30), rect_y, border_radius=3)
        text_y = self.font.render(str(self.value.y), True, (255, 255, 255))
        screen.blit(text_y, (x_start + (self.box_width - text_y.get_width()) / 2, self.pos.y + (self.box_height - text_y.get_height()) / 2))
        x_start += self.box_width + self.spacing

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = vec2(*pygame.mouse.get_pos())
            x_start = self.pos.x
            text_x_label = self.font.render("x:", True, (255, 255, 255))
            x_start += text_x_label.get_width() + 2

            if (x_start <= mouse_pos.x <= x_start + self.box_width and self.pos.y <= mouse_pos.y <= self.pos.y + self.box_height):
                self.value.x += event.y
            x_start += self.box_width + self.spacing

            text_y_label = self.font.render("y:", True, (255, 255, 255))
            x_start += text_y_label.get_width() + 2

            if (x_start <= mouse_pos.x <= x_start + self.box_width and self.pos.y <= mouse_pos.y <= self.pos.y + self.box_height):
                self.value.y += event.y

    def get_value(self):
        return self.value

    def set_value(self, val):
        self.value = val