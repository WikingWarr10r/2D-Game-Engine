import pygame
from engine_math import *

class Object:
    def __init__(self, pos: vec2, vel: vec2, radius, lock = False):
        self.pos = pos
        self.initial_pos = pos
        self.vel = vel

        self.lock = lock

        self.density = 0.0014147106
        
        self.radius = radius
        self.mass = (pi * radius * radius) * self.density

    def store(self):
        return f"{self.pos.x},{self.pos.y} {self.initial_pos.x},{self.initial_pos.y} {self.vel.x},{self.vel.y} {self.lock} {self.radius} {self.mass}"

    @staticmethod
    def recreate_obj(stored):
        parts = stored.split(" ")
        pos_x, pos_y = map(float, parts[0].split(","))
        init_x, init_y = map(float, parts[1].split(","))
        vel_x, vel_y = map(float, parts[2].split(","))
        lock = True if parts[3] == "True" else False
        radius = float(parts[4])
        mass = float(parts[5])

        obj = Object(vec2(pos_x, pos_y), vec2(vel_x, vel_y), radius, lock)
        obj.initial_pos = vec2(init_x, init_y)
        obj.mass = mass
        return obj

    def check_collision(self, other):
        distance = ((self.pos.x - other.pos.x) ** 2 + (self.pos.y - other.pos.y) ** 2) ** 0.5
        return distance < (self.radius + other.radius)
    
    def resolve_overlap(self, other):
        delta = vec2(other.pos.x - self.pos.x, other.pos.y - self.pos.y)
        dist = (delta.x**2 + delta.y**2) ** 0.5
        if dist == 0:
            dist = 0.01

        overlap = (self.radius + other.radius) - dist
        if overlap <= 0:
            return

        normal = vec2(delta.x / dist, delta.y / dist)

        if self.lock and other.lock:
            return 
        elif self.lock:
            other.pos.x += normal.x * overlap
            other.pos.y += normal.y * overlap
        elif other.lock:
            self.pos.x -= normal.x * overlap
            self.pos.y -= normal.y * overlap
        else:
            self.pos.x -= normal.x * overlap / 2
            self.pos.y -= normal.y * overlap / 2
            other.pos.x += normal.x * overlap / 2
            other.pos.y += normal.y * overlap / 2
    
    def collision_response(self, other):
        if self.lock and other.lock:
            return 

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
        impulse_scalar /= (0 if self.lock else 1 / self.mass) + (0 if other.lock else 1 / other.mass)

        impulse = normal * impulse_scalar

        if not self.lock:
            self.vel = self.vel - impulse * (1 / self.mass)
        if not other.lock:
            other.vel = other.vel + impulse * (1 / other.mass)

    def collide(self, lower, bounciness, friction):
        if self.pos.y > lower-self.radius:
            self.pos.y = lower-self.radius
            self.vel.y = -self.vel.y*bounciness
            self.vel.x *= friction
        if self.pos.x < 0 + self.radius:
            self.pos.x = 0 + self.radius
            self.vel.x *= -1
        if self.pos.x > 1280 - self.radius:
            self.pos.x = 1280 - self.radius
            self.vel.x *= -1

    def add_force(self, vec):
        self.vel += vec
    
    def update(self, gravity, bounciness, air_density, drag_coefficient, friction, floor, dt, simulation_type):
        if self.lock:
            return

        if simulation_type == "Basic":
            if dt == 0:
                return
            self.pos = self.pos + (self.vel * vec2(dt, dt))
            self.vel = self.vel + (vec2(0, gravity * (dt*60)))
            
            air_res = vec2(-0.5, -0.5) * vec2(air_density, air_density) * self.vel * vec2(drag_coefficient, drag_coefficient) * (2*pi*self.radius/2)
            self.add_force(air_res)

            self.collide(floor, bounciness, friction)
        
        elif simulation_type == "Newtonian Gravity":
            self.pos = self.pos + (self.vel * vec2(dt, dt))

    def render(self, screen):
        pygame.draw.circle(screen, "white", (self.pos.x, self.pos.y), self.radius)


class Rectangle:
    def __init__(self, pos: vec2, vel: vec2, width, height, lock=False):
        self.pos = pos
        self.initial_pos = pos
        self.vel = vel
        self.lock = lock

        self.density = 0.0014147106

        self.width = width
        self.height = height
        self.mass = (width * height) * self.density

    def store(self):
        return f"{self.pos.x},{self.pos.y} {self.initial_pos.x},{self.initial_pos.y} {self.vel.x},{self.vel.y} {self.lock} {self.width} {self.height} {self.mass}"

    @staticmethod
    def recreate_obj(stored):
        parts = stored.split(" ")
        pos_x, pos_y = map(float, parts[0].split(","))
        init_x, init_y = map(float, parts[1].split(","))
        vel_x, vel_y = map(float, parts[2].split(","))
        lock = parts[3] == "True"
        width = float(parts[4])
        height = float(parts[5])
        mass = float(parts[6])

        obj = Rectangle(vec2(pos_x, pos_y), vec2(vel_x, vel_y), width, height, lock)
        obj.initial_pos = vec2(init_x, init_y)
        obj.mass = mass
        return obj
    
    def check_collision(self, other):
        if isinstance(other, Rectangle):
            return (abs(self.pos.x - other.pos.x) < (self.width/2 + other.width/2) and
                    abs(self.pos.y - other.pos.y) < (self.height/2 + other.height/2))

        # Circle (Object) collision
        elif hasattr(other, "radius"):
            closest_x = max(self.pos.x - self.width/2,
                            min(other.pos.x, self.pos.x + self.width/2))
            closest_y = max(self.pos.y - self.height/2,
                            min(other.pos.y, self.pos.y + self.height/2))
            dx = other.pos.x - closest_x
            dy = other.pos.y - closest_y
            return dx*dx + dy*dy < (other.radius * other.radius)

        return False

    def resolve_overlap(self, other):
        if not self.check_collision(other):
            return

        if isinstance(other, Rectangle):
            dx = (self.width/2 + other.width/2) - abs(self.pos.x - other.pos.x)
            dy = (self.height/2 + other.height/2) - abs(self.pos.y - other.pos.y)

            if dx < dy:
                shift = dx if self.pos.x < other.pos.x else -dx
                if self.lock and other.lock:
                    return
                elif self.lock:
                    other.pos.x += shift
                elif other.lock:
                    self.pos.x -= shift
                else:
                    self.pos.x -= shift/2
                    other.pos.x += shift/2
            else:
                shift = dy if self.pos.y < other.pos.y else -dy
                if self.lock and other.lock:
                    return
                elif self.lock:
                    other.pos.y += shift
                elif other.lock:
                    self.pos.y -= shift
                else:
                    self.pos.y -= shift/2
                    other.pos.y += shift/2

        elif hasattr(other, "radius"):  # Circle overlap
            delta = vec2(other.pos.x - self.pos.x, other.pos.y - self.pos.y)
            clamped_x = max(-self.width/2, min(delta.x, self.width/2))
            clamped_y = max(-self.height/2, min(delta.y, self.height/2))
            closest = vec2(self.pos.x + clamped_x, self.pos.y + clamped_y)

            diff = other.pos - closest
            dist = max(0.0001, (diff.x**2 + diff.y**2)**0.5)

            penetration = other.radius - dist
            if penetration > 0:
                normal = vec2(diff.x/dist, diff.y/dist)
                if self.lock and other.lock:
                    return
                elif self.lock:
                    other.pos += normal * penetration
                elif other.lock:
                    self.pos -= normal * penetration
                else:
                    self.pos -= normal * penetration * 0.5
                    other.pos += normal * penetration * 0.5

    def collision_response(self, other):
        if not self.check_collision(other):
            return
        if self.lock and other.lock:
            return

        if isinstance(other, Rectangle):
            delta = vec2(other.pos.x - self.pos.x, other.pos.y - self.pos.y)
            overlap_x = (self.width/2 + other.width/2) - abs(delta.x)
            overlap_y = (self.height/2 + other.height/2) - abs(delta.y)
            normal = vec2(1, 0) if overlap_x < overlap_y and delta.x > 0 else \
                     vec2(-1, 0) if overlap_x < overlap_y else \
                     vec2(0, 1) if delta.y > 0 else vec2(0, -1)

        elif hasattr(other, "radius"):  # Circle response
            delta = other.pos - self.pos
            dist = max(0.0001, (delta.x**2 + delta.y**2)**0.5)
            normal = delta * (1/dist)

        relative_velocity = other.vel - self.vel
        vel_along_normal = relative_velocity.x * normal.x + relative_velocity.y * normal.y
        if vel_along_normal > 0:
            return

        restitution = 0.7
        impulse_scalar = -(1 + restitution) * vel_along_normal
        impulse_scalar /= (0 if self.lock else 1/self.mass) + (0 if other.lock else 1/other.mass)

        impulse = normal * impulse_scalar
        if not self.lock:
            self.vel -= impulse * (1/self.mass)
        if not other.lock:
            other.vel += impulse * (1/other.mass)
    
    def collide(self, lower, bounciness, friction):
        half_w = self.width / 2
        half_h = self.height / 2

        if self.pos.y + half_h > lower:
            self.pos.y = lower - half_h
            self.vel.y = -self.vel.y * bounciness
            self.vel.x *= friction

        if self.pos.x - half_w < 0:
            self.pos.x = half_w
            self.vel.x = -self.vel.x * bounciness

        if self.pos.x + half_w > 1280:
            self.pos.x = 1280 - half_w
            self.vel.x = -self.vel.x * bounciness
    
    def add_force(self, vec):
        self.vel += vec
    
    def update(self, gravity, bounciness, air_density, drag_coefficient, friction, floor, dt, simulation_type):
        if self.lock:
            return

        if simulation_type == "Basic":
            if dt == 0:
                return
            self.pos = self.pos + (self.vel * vec2(dt, dt))
            self.vel = self.vel + (vec2(0, gravity * (dt*60)))
            
            air_res = vec2(-0.5, -0.5) * vec2(air_density, air_density) * self.vel * vec2(drag_coefficient, drag_coefficient)
            self.add_force(air_res)

            self.collide(floor, bounciness, friction)
        
        elif simulation_type == "Newtonian Gravity":
            self.pos = self.pos + (self.vel * vec2(dt, dt))
    
    def render(self, screen):
        pygame.draw.rect(screen, "white", pygame.Rect(self.pos.x - self.width/2, self.pos.y - self.height/2, self.width, self.height))