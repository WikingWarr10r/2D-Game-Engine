import pygame

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x * other.x, self.y * other.y)
        else:
            return vec2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return vec2(self.x / other.x, self.y / other.y)
    
    def __repr__(self):
        return f"{self.x}, {self.y}"
    
class Object:
    def __init__(self, pos: vec2, vel: vec2):
        self.pos = pos
        self.vel = vel
        
        self.mass = 1
        self.radius = 15
        
    def check_collision(self, other):
        distance = ((self.pos.x - other.pos.x) ** 2 + (self.pos.y - other.pos.y) ** 2) ** 0.5
        return distance < (self.radius + other.radius)
    
    def resolve_overlap(self, other):
        delta = vec2(other.pos.x - self.pos.x, other.pos.y - self.pos.y)
        dist = (delta.x**2 + delta.y**2) ** 0.5
        if dist == 0:
            dist = 0.01
        
        overlap = (self.radius + other.radius) - dist
        
        normal = vec2(delta.x / dist, delta.y / dist)
        
        self.pos.x -= normal.x * overlap/2
        self.pos.y -= normal.y * overlap/2
        other.pos.x += normal.x * overlap/2
        other.pos.y += normal.y * overlap/2
    
    def collision_response(self, other):
        delta = other.pos - self.pos
        dist = (delta.x ** 2 + delta.y ** 2) ** 0.5
        if dist == 0:
            dist = 0.01

        normal = delta / vec2(dist, dist)
        
        relative_velocity = other.vel - self.vel
        vel_along_normal = relative_velocity.x * normal.x + relative_velocity.y * normal.y

        if vel_along_normal > 0:
            return

        restitution = 0.7

        impulse_scalar = -(1 + restitution) * vel_along_normal
        impulse_scalar /= (1 / self.mass + 1 / other.mass)

        impulse = normal * impulse_scalar

        self.vel = self.vel - impulse * (1 / self.mass)
        other.vel = other.vel + impulse * (1 / other.mass)            
    def collide(self, lower, bounciness, friction):
        if self.pos.y > lower:
            self.pos.y = lower
            self.vel.y = -self.vel.y*bounciness
            self.vel.x *= friction
        if self.pos.x < 50:
            self.pos.x = 50
            self.vel.x *= -1
        if self.pos.x > 1230:
            self.pos.x = 1230
            self.vel.x *= -1
    
    def update(self, bounciness, air_resistance, friction):
        dt = 1/60
        self.pos = self.pos + (self.vel * vec2(dt, dt))
        self.vel = self.vel + (vec2(0, 10))
        self.vel.x = self.vel.x * air_resistance
        self.collide(600, bounciness, friction)
        
    def render(self, screen):
        pygame.draw.circle(screen, "white", (self.pos.x, self.pos.y), self.radius)

class EngineCore:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.looping = True
        
        self.objects = []

    def setup_screen(self, width=1280, height=720):
        self.screen = pygame.display.set_mode((width,height))
        
    def render(self):
        self.screen.fill("black")
        
        for obj in self.objects:
            obj.render(self.screen)

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        
        for obj in self.objects:
            obj.update(0.7, 0.999, 0.8)
            
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

engine = EngineCore()
engine.setup_screen()

engine.add_object(vec2(50, 500), vec2(1000, 50))
engine.add_object(vec2(50, 450), vec2(1000, 50))
engine.add_object(vec2(50, 400), vec2(1000, 50))
engine.add_object(vec2(1000, 500), vec2(-1000, 50))
engine.add_object(vec2(1000, 450), vec2(-1000, 50))
engine.add_object(vec2(1000, 400), vec2(-1000, 50))

while engine.looping:
    engine.main_loop()