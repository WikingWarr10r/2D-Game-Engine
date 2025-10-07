import pygame
import time
import psutil
import os
from collections import deque
from copy import deepcopy

from engine_math import *
from engine_object import *

class EngineCore:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.looping = True
        
        self.objects = []
        self.ui = []

        self.gravity = 10
        self.bounciness = 0.7
        self.air_density = 1.225
        self.drag_coefficient = 0.00001
        self.friction = 0.8
        self.floor = 600
        self.dt = 1/60
        self.gravitational_constant = -10000

        self.sim_type = "Newtonian Gravity"

        self.draw_calls = []

        self.process = psutil.Process(os.getpid())

        self.frame_num = 0

        self.cam = None

        self.future_positions = []
        self.predict_freq = 0.5
        self.gravity_debug = False

        self.obj_render_time = 0.0
        self.draw_call_render_time = 0.0
        self.ui_render_time = 0.0
        self.event_handle_time = 0.0
        self.obj_update_time = 0.0
        self.ui_update_time = 0.0
        self.newtonian_physics_time = 0.0
        self.basic_physics_time = 0.0

        self.setup_screen()

    def setup_screen(self, width=1280, height=720):
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Engine")
        
    def draw_circle(self, radius, pos:vec2, colour=(255, 255, 255, 122)):
        self.draw_calls.append(lambda: pygame.draw.circle(self.screen, colour, (pos.x, pos.y), radius))
    
    def draw_cross(self, centre, colour=(255, 255, 255, 122)):
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (centre.x - 10, centre.y), (centre.x + 10, centre.y)))
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (centre.x, centre.y - 10), (centre.x, centre.y + 10)))

    def draw_line(self, start, end, colour=(255, 255, 255, 122), thickness=1):
        self.draw_calls.append(lambda: pygame.draw.line(self.screen, colour, (start.x, start.y), (end.x, end.y), thickness))

    def render(self):
        start = 0
        self.screen.fill("black")
        if self.sim_type == "Basic":
            floor = self.cam.ws_to_ss_vec((0, self.floor))
            pygame.draw.line(self.screen, "white", (0, floor[1]), (1280, floor[1]), 5)

        start = time.time()
        for draw_call in self.draw_calls:
            draw_call()
        self.draw_calls.clear()

        if self.dt == 0 and self.sim_type == "Newtonian Gravity":
            if self.frame_num % (self.predict_freq * 60) == 0:
                self.future_positions = self.predict_future()
            for obj in self.future_positions:
                if len(obj) > 2:
                    ss_obj = []
                    for point in obj:
                        ss_obj.append(self.cam.ws_to_ss_vec(point))
                    pygame.draw.lines(self.screen, (255, 122, 122, 122), False, ss_obj)
        
        self.draw_call_render_time = time.time() - start

        start = time.time()
        for obj in self.objects:
            obj.render(self.screen)
        self.obj_render_time = time.time() - start

        start = time.time()
        for ui in self.ui:
            ui.render(self.screen)
        self.ui_render_time = time.time() - start

    def main_loop(self):
        self.frame_num += 1
        start = 0
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            for ui in self.ui:
                ui.handle_event(event)
        self.event_handle_time = time.time() - start
        
        start = time.time()
        for obj in self.objects:
            obj.update(self.gravity, self.bounciness, self.air_density, self.drag_coefficient, self.friction, self.floor, self.dt, self.sim_type)
        self.obj_update_time = time.time() - start

        start = time.time()
        for ui in self.ui:
            ui.update()
        self.ui_update_time = time.time() - start

        start = time.time()
        if self.sim_type == "Newtonian Gravity":
            objs = self.objects
            G = self.gravitational_constant

            for i, a in enumerate(objs):
                ax, ay, am = a.pos.x, a.pos.y, a.mass
                for j in range(i + 1, len(objs)):
                    b = objs[j]
                    bx, by, bm = b.pos.x, b.pos.y, b.mass

                    dx = bx - ax
                    dy = by - ay
                    dist2 = dx*dx + dy*dy
                    if dist2 == 0:
                        continue

                    inv_dist = 1.0 / math.sqrt(dist2)

                    kelvin = inv_dist * 500_000
                    col = kelvin_to_col(min(kelvin, 40000))
                    if math.sqrt(dist2) < 200 and self.gravity_debug:
                        self.draw_line(a.pos, b.pos, col, max(1, int(kelvin/3000), int(kelvin/1500)))

                    force = G * am * bm * inv_dist * inv_dist * (self.dt * 60)

                    nx = dx * inv_dist
                    ny = dy * inv_dist

                    ax_force = (force / am) * nx
                    ay_force = (force / am) * ny
                    bx_force = (force / bm) * nx
                    by_force = (force / bm) * ny

                    if not a.lock:
                        a.add_force(vec2(-ax_force, -ay_force))
                    else:
                        a.vel = vec2(0, 0)

                    if not b.lock:
                        b.add_force(vec2(bx_force, by_force))
                    else:
                        b.vel = vec2(0, 0)

        self.newtonian_physics_time = time.time() - start

        start = time.time()
        for i in range(len(self.objects)):
            for j in range(i+1, len(self.objects)):
                a = self.objects[i]
                b = self.objects[j]
                if a.check_collision(b):
                    a.resolve_overlap(b)
                    a.collision_response(b)
                    
        self.basic_physics_time = time.time() - start

        self.render()

        pygame.display.flip()
        self.clock.tick(60)
    
    def add_circle(self, pos: vec2, vel: vec2, radius, lock = False):
        self.objects.append(Object(pos, vel, radius, self.cam, lock))

    def add_rect(self, pos: vec2, vel: vec2, width, height, lock = False):
        self.objects.append(Rectangle(pos, vel, width, height, self.cam, lock))

    def predict_future(self, steps=1000):
        objs = deepcopy(self.objects)
        positions = []
        G = self.gravitational_constant

        for _ in range(steps):
            for i, a in enumerate(objs):
                positions.append([])
                ax, ay, am = a.pos.x, a.pos.y, a.mass
                for j in range(i + 1, len(objs)):
                    positions.append([])
                    b = objs[j]
                    bx, by, bm = b.pos.x, b.pos.y, b.mass

                    dx = bx - ax
                    dy = by - ay
                    dist2 = dx*dx + dy*dy
                    if dist2 == 0:
                        continue

                    inv_dist = 1.0 / math.sqrt(dist2)

                    force = G * am * bm * inv_dist * inv_dist * (1/60 * 60)

                    nx = dx * inv_dist
                    ny = dy * inv_dist

                    ax_force = (force / am) * nx
                    ay_force = (force / am) * ny
                    bx_force = (force / bm) * nx
                    by_force = (force / bm) * ny

                    if not a.lock:
                        a.add_force(vec2(-ax_force, -ay_force))
                    else:
                        a.vel = vec2(0, 0)

                    if not b.lock:
                        b.add_force(vec2(bx_force, by_force))
                    else:
                        b.vel = vec2(0, 0)

                    positions[i].append((a.pos.x, a.pos.y))
                    positions[j].append((b.pos.x, b.pos.y))

            for obj in objs:
                obj.update(self.gravity, self.bounciness, self.air_density, self.drag_coefficient, self.friction, self.floor, 1/60, self.sim_type)

        return positions
    
    def add_camera(self, cam):
        self.cam = cam