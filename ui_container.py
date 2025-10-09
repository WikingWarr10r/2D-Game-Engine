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

        self.collapsed = False
        self.min_button_size = 12

        self.font = pygame.font.Font("font/ProggyClean.ttf", 16)

    def add_number(self, val: int, label, bounds=None):
        num = UINumber(val, vec2(0, 0), label, self.font, bounds)
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

    def add_choice(self, choices: list, label):
        choice = UIChoice(choices, vec2(0,0), label, self.font)
        self.elements.append(choice)
        self.lookup[label] = choice

    def add_pie_chart(self, label):
        pie_chart =  UIPieChart(vec2(0, 0), 100, None, self.font)
        self.elements.append(pie_chart)
        self.lookup[label] = pie_chart
        for i in range(8):
            self.add_spacer()

    def get_value(self, label):
        if label in self.lookup:
            return self.lookup[label].get_value()
        return None
    
    def set_value(self, label, val):
        if label in self.lookup:
            self.lookup[label].set_value(val)

    def delete_element(self, label):
        if label in self.lookup:
            elem = self.lookup.pop(label)
            if elem in self.elements:
                self.elements.remove(elem)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = vec2(*event.pos)
            btn_rect = pygame.Rect(
                self.pos.x + self.width - self.min_button_size - 2,
                self.pos.y + 2,
                self.min_button_size,
                self.min_button_size
            )
            if btn_rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self.collapsed = not self.collapsed

        if not self.collapsed:
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

        if self.collapsed:
            self.height = 15
        else:
            self.height = 20 + len(self.elements) * 25

    def render(self, screen):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(
            surf,
            (30, 30, 30, 200) if not self.collapsed else (30, 30, 30, 200),
            (0, 0, self.width, self.height),
            border_radius=5
        )
        pygame.draw.rect(surf, (150, 30, 30, 200), (0, 0, self.width, 15), border_radius=5)

        pygame.draw.rect(
            surf,
            (200, 50, 50, 200),
            (self.width - self.min_button_size - 2, 2, self.min_button_size, self.min_button_size)
        )
        sign = "-" if not self.collapsed else "+"
        sign_surf = self.font.render(sign, True, (255, 255, 255))
        surf.blit(
            sign_surf,
            (
                self.width - self.min_button_size - 2 + (self.min_button_size - sign_surf.get_width()) / 2,
                2 + (self.min_button_size - sign_surf.get_height()) / 2
            )
        )

        screen.blit(surf, (self.pos.x, self.pos.y))

        title_surf = self.font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (self.pos.x + 5, self.pos.y + (15 - title_surf.get_height()) / 2))

        if not self.collapsed:
            for i, elem in enumerate(self.elements):
                elem.pos = vec2(self.pos.x + 5, self.pos.y + 20 + i * 25)
                elem.render(screen)