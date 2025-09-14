from ui_elements import *

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

    def add_label(self, text, id=None):
        lab = UILabel(vec2(0,0), text, self.font)
        self.elements.append(lab)
        if id:
            self.lookup[id] = lab

    def add_vec2(self, val: vec2, label):
        vec = UIVec2(val, vec2(0, 0), label, self.font)
        self.elements.append(vec)
        self.lookup[label] = vec

    def get_value(self, label):
        if label in self.lookup:
            return self.lookup[label].get_value()
        return None
    
    def set_value(self, label, val):
        if label in self.lookup:
            self.lookup[label].set_value(val)

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