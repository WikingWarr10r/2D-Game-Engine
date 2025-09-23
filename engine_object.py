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