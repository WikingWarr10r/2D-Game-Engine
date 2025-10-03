import pygame
from engine_math import *
from camera import Camera

class Object:
    def __init__(self, pos: vec2, vel: vec2, radius, cam: Camera, lock = False):
        self.pos = pos
        self.initial_pos = pos
        self.vel = vel

        self.cam = cam

        self.ss_pos = cam.ws_to_ss_vec(self.pos)

        self.lock = lock

        self.density = 0.0014147106
        
        self.radius = radius
        self.mass = (pi * radius * radius) * self.density

    def store(self):
        return f"Circle {self.pos.x},{self.pos.y} {self.initial_pos.x},{self.initial_pos.y} {self.vel.x},{self.vel.y} {self.lock} {self.radius} {self.mass}"

    @staticmethod
    def recreate_obj(parts, camera):
        pos_x, pos_y = map(float, parts[0].split(","))
        init_x, init_y = map(float, parts[1].split(","))
        vel_x, vel_y = map(float, parts[2].split(","))
        lock = True if parts[3] == "True" else False
        radius = float(parts[4])
        mass = float(parts[5])

        obj = Object(vec2(pos_x, pos_y), vec2(vel_x, vel_y), radius, camera, lock)
        obj.initial_pos = vec2(init_x, init_y)
        obj.mass = mass
        return obj

    def check_collision(self, other):
        if hasattr(other, "radius"):
            distance = ((self.pos.x - other.pos.x) ** 2 + (self.pos.y - other.pos.y) ** 2) ** 0.5
            return distance < (self.radius + other.radius)
        elif isinstance(other, Rectangle):
            verts = other.get_vertices()
            pen, axis = sat_poly_circle(verts, self.pos, self.radius)
            return pen is not None
        else:
            return False
        
    def resolve_overlap(self, other):
        if hasattr(other, "radius"):
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
        elif isinstance(other, Rectangle):
            pen, axis = other.compute_mtv(self)
            if pen is None:
                return
            if self.lock and other.lock:
                return
            if self.lock:
                other.pos = other.pos + axis * pen
            elif other.lock:
                self.pos = self.pos - axis * pen
            else:
                self.pos = self.pos - axis * (pen * 0.5)
                other.pos = other.pos + axis * (pen * 0.5)
  
    def collision_response(self, other):
        if self.lock and getattr(other, "lock", False):
            return 

        if hasattr(other, "radius"):
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
        elif isinstance(other, Rectangle):
            other.collision_response(self)

    def collide(self, floor_rect, bounciness, friction):
        if self.check_collision(floor_rect):
            self.resolve_overlap(floor_rect)
            self.collision_response(floor_rect)

    def add_force(self, vec):
        self.vel += vec
    
    def update(self, gravity, bounciness, air_density, drag_coefficient, friction, floor_rect, dt, simulation_type):
        if self.lock:
            return

        if simulation_type == "Basic":
            if dt == 0:
                return
            self.pos = self.pos + (self.vel * vec2(dt, dt))
            self.vel = self.vel + (vec2(0, gravity * (dt*60)))
            
            air_res = vec2(-0.5, -0.5) * vec2(air_density, air_density) * self.vel * vec2(drag_coefficient, drag_coefficient) * (2*pi*self.radius/2)
            self.add_force(air_res)

            self.collide(floor_rect, bounciness, friction)
        
        elif simulation_type == "Newtonian Gravity":
            self.pos = self.pos + (self.vel * vec2(dt, dt))

    def render(self, screen):
        self.ss_pos = self.cam.ws_to_ss_vec(self.pos)

        pygame.draw.circle(screen, "white", (self.ss_pos.x, self.ss_pos.y), self.cam.ws_to_ss_num(self.radius))

def rotate_point(local: vec2, angle: float) -> vec2:
    ca = math.cos(angle)
    sa = math.sin(angle)
    return vec2(local.x * ca - local.y * sa, local.x * sa + local.y * ca)

def rect_get_vertices(center: vec2, w: float, h: float, angle: float):
    hw = w * 0.5
    hh = h * 0.5
    local = [vec2(-hw, -hh), vec2(hw, -hh), vec2(hw, hh), vec2(-hw, hh)]
    return [center + rotate_point(c, angle) for c in local]

def project_polygon(axis: vec2, verts):
    dots = [axis.dot(v) for v in verts]
    return min(dots), max(dots)

def project_circle(axis: vec2, center: vec2, radius: float):
    c = axis.dot(center)
    return c - radius, c + radius

def interval_overlap(minA, maxA, minB, maxB):
    return min(maxA, maxB) - max(minA, minB)

def polygon_axes(verts):
    axes = []
    n = len(verts)
    for i in range(n):
        p1 = verts[i]
        p2 = verts[(i+1) % n]
        edge = p2 - p1
        axis = vec2(-edge.y, edge.x)
        axis = axis.normalized()
        axes.append(axis)
    return axes

def sat_poly_poly(vertsA, vertsB):
    smallest_pen = float('inf')
    smallest_axis = None
    for axis in polygon_axes(vertsA) + polygon_axes(vertsB):
        minA, maxA = project_polygon(axis, vertsA)
        minB, maxB = project_polygon(axis, vertsB)
        pen = interval_overlap(minA, maxA, minB, maxB)
        if pen <= 0:
            return None, None
        if pen < smallest_pen:
            smallest_pen = pen
            smallest_axis = axis
    return smallest_pen, smallest_axis

def closest_point_on_segment(a: vec2, b: vec2, p: vec2):
    ab = b - a
    denom = ab.x*ab.x + ab.y*ab.y
    t = 0.0
    if denom != 0:
        t = ((p.x - a.x) * ab.x + (p.y - a.y) * ab.y) / denom
        t = max(0.0, min(1.0, t))
    return a + ab * t

def sat_poly_circle(verts, center: vec2, radius: float):
    smallest_pen = float('inf')
    smallest_axis = None
    for axis in polygon_axes(verts):
        minP, maxP = project_polygon(axis, verts)
        minC, maxC = project_circle(axis, center, radius)
        pen = interval_overlap(minP, maxP, minC, maxC)
        if pen <= 0:
            return None, None
        if pen < smallest_pen:
            smallest_pen = pen
            smallest_axis = axis

    closest = None
    best_d = float('inf')
    for i in range(len(verts)):
        a = verts[i]
        b = verts[(i+1) % len(verts)]
        proj = closest_point_on_segment(a, b, center)
        d = (center - proj).length()
        if d < best_d:
            best_d = d
            closest = proj

    if closest is not None:
        axis = (center - closest)
        if axis.length() == 0:
            axis = vec2(1,0)
        else:
            axis = axis.normalized()
        minP, maxP = project_polygon(axis, verts)
        minC, maxC = project_circle(axis, center, radius)
        pen = interval_overlap(minP, maxP, minC, maxC)
        if pen <= 0:
            return None, None
        if pen < smallest_pen:
            smallest_pen = pen
            smallest_axis = axis

    return smallest_pen, smallest_axis

class Rectangle:
    def __init__(self, pos: vec2, vel: vec2, width, height, cam, lock=False, angle=0.0, ang_vel=0.0):
        self.pos = pos
        self.initial_pos = vec2(pos.x, pos.y)
        self.vel = vel
        self.cam = cam
        self.ss_pos = cam.ws_to_ss_vec(self.pos)
        self.lock = lock
        self.density = 0.0014147106
        self.width = width
        self.height = height
        self.mass = (width * height) * self.density
        self.angle = angle
        self.ang_vel = ang_vel
        self.inertia = self.mass * (self.width*self.width + self.height*self.height) / 12.0 if self.mass != 0 else float('inf')

    def store(self):
        return f"Rect {self.pos.x},{self.pos.y} {self.initial_pos.x},{self.initial_pos.y} {self.vel.x},{self.vel.y} {self.lock} {self.width} {self.height} {self.mass} {self.angle} {self.ang_vel}"

    @staticmethod
    def recreate_obj(parts, camera):
        pos_x, pos_y = map(float, parts[0].split(","))
        init_x, init_y = map(float, parts[1].split(","))
        vel_x, vel_y = map(float, parts[2].split(","))
        lock = parts[3] == "True"
        width = float(parts[4])
        height = float(parts[5])
        mass = float(parts[6])
        angle = float(parts[7]) if len(parts) > 7 else 0.0
        ang_vel = float(parts[8]) if len(parts) > 8 else 0.0
        obj = Rectangle(vec2(pos_x, pos_y), vec2(vel_x, vel_y), width, height, camera, lock, angle, ang_vel)
        obj.initial_pos = vec2(init_x, init_y)
        obj.mass = mass
        obj.inertia = obj.mass * (obj.width*obj.width + obj.height*obj.height) / 12.0 if obj.mass != 0 else float('inf')
        return obj

    def get_vertices(self):
        return rect_get_vertices(self.pos, self.width, self.height, self.angle)

    def check_collision(self, other):
        if isinstance(other, Rectangle):
            vertsA = self.get_vertices()
            vertsB = other.get_vertices()
            pen, axis = sat_poly_poly(vertsA, vertsB)
            return pen is not None
        elif hasattr(other, "radius"):
            verts = self.get_vertices()
            pen, axis = sat_poly_circle(verts, other.pos, other.radius)
            return pen is not None
        return False

    def compute_mtv(self, other):
        if isinstance(other, Rectangle):
            vertsA = self.get_vertices()
            vertsB = other.get_vertices()
            pen, axis = sat_poly_poly(vertsA, vertsB)
            if pen is None:
                return None, None
            dir = other.pos - self.pos
            if axis.dot(dir) < 0:
                axis = axis * -1
            return pen, axis
        elif hasattr(other, "radius"):
            verts = self.get_vertices()
            pen, axis = sat_poly_circle(verts, other.pos, other.radius)
            if pen is None:
                return None, None
            dir = other.pos - self.pos
            if axis.dot(dir) < 0:
                axis = axis * -1
            return pen, axis
        return None, None

    def resolve_overlap(self, other):
        res = self.compute_mtv(other)
        if res[0] is None:
            return
        pen, axis = res
        if self.lock and getattr(other, "lock", False):
            return
        if self.lock:
            other.pos = other.pos + axis * pen
        elif getattr(other, "lock", False):
            self.pos = self.pos - axis * pen
        else:
            self.pos = self.pos - axis * (pen * 0.5)
            other.pos = other.pos + axis * (pen * 0.5)

    def collision_response(self, other):
        if not self.check_collision(other):
            return
        if self.lock and getattr(other, "lock", False):
            return

        pen, axis = self.compute_mtv(other)
        if pen is None:
            return

        contact = None
        if isinstance(other, Rectangle):
            verts = self.get_vertices()
            best = float('inf')
            for v in verts:
                d = (v - other.pos).length()
                if d < best:
                    best = d
                    contact = v
        else:
            verts = self.get_vertices()
            best = float('inf')
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i+1) % len(verts)]
                proj = closest_point_on_segment(a, b, other.pos)
                d = (other.pos - proj).length()
                if d < best:
                    best = d
                    contact = proj

        if contact is None:
            contact = (self.pos + other.pos) * 0.5

        rA = contact - self.pos
        rB = contact - other.pos

        velA = self.vel + vec2.cross_scalar_vec(self.ang_vel, rA)
        velB = other.vel + vec2.cross_scalar_vec(getattr(other, "ang_vel", 0.0), rB)
        rel_vel = velB - velA

        n = axis.normalized()
        vel_along = rel_vel.dot(n)
        if vel_along > 0:
            return

        restitution = 0.7
        invMassA = 0.0 if self.lock else (1.0 / self.mass if self.mass != 0 else 0.0)
        invMassB = 0.0 if getattr(other, "lock", False) else (1.0 / getattr(other, "mass", float('inf')) if getattr(other, "mass", 0) != 0 else 0.0)
        invInertiaA = 0.0 if self.lock else (1.0 / self.inertia if self.inertia != 0 else 0.0)
        invInertiaB = 0.0 if getattr(other, "lock", False) else (1.0 / getattr(other, "inertia", float('inf')) if getattr(other, "inertia", 0) != 0 else 0.0)

        ra_cross_n = rA.cross(n)
        rb_cross_n = rB.cross(n)
        denom = invMassA + invMassB + (ra_cross_n*ra_cross_n) * invInertiaA + (rb_cross_n*rb_cross_n) * invInertiaB
        if denom == 0:
            return

        j = -(1 + restitution) * vel_along
        j /= denom
        impulse = n * j

        if not self.lock:
            self.vel = self.vel - impulse * invMassA
            self.ang_vel -= ra_cross_n * j * invInertiaA
        if not getattr(other, "lock", False):
            other.vel = other.vel + impulse * invMassB
            if hasattr(other, "ang_vel"):
                other.ang_vel += rb_cross_n * j * invInertiaB

        tangent = rel_vel - n * rel_vel.dot(n)
        tlen = tangent.length()
        if tlen > 1e-6:
            tdir = tangent / tlen
            mu = 0.3
            jt = -rel_vel.dot(tdir)
            jt /= denom
            jt = max(-j * mu, min(j * mu, jt))
            tang_imp = tdir * jt
            if not self.lock:
                self.vel = self.vel - tang_imp * invMassA
                self.ang_vel -= rA.cross(tang_imp) * invInertiaA
            if not getattr(other, "lock", False):
                other.vel = other.vel + tang_imp * invMassB
                if hasattr(other, "ang_vel"):
                    other.ang_vel += rB.cross(tang_imp) * invInertiaB

    def collide(self, floor_rect, bounciness, friction):
        if self.check_collision(floor_rect):
            self.resolve_overlap(floor_rect)
            self.collision_response(floor_rect)

    def add_force(self, v: vec2):
        self.vel = self.vel + v

    def add_torque(self, torque: float):
        if self.lock:
            return
        ang_acc = torque / self.inertia if self.inertia != 0 else 0.0
        self.ang_vel += ang_acc

    def update(self, gravity, bounciness, air_density, drag_coefficient, friction, floor_rect, dt, simulation_type):
        if self.lock:
            return

        self.vel += vec2(0, gravity * dt * 60)
        self.pos += self.vel * dt

        self.vel *= (1 - drag_coefficient * air_density * dt)
        self.ang_vel *= (1 - 0.01 * drag_coefficient * air_density)

        self.collide(floor_rect, bounciness, friction)

        self.angle += self.ang_vel * dt

    def render(self, screen):
        self.ss_pos = self.cam.ws_to_ss_vec(self.pos)
        ss_h = self.cam.ws_to_ss_num(self.height)
        ss_w = self.cam.ws_to_ss_num(self.width)
        surf = pygame.Surface((int(ss_w), int(ss_h)), pygame.SRCALPHA)
        pygame.draw.rect(surf, "white", pygame.Rect(0, 0, int(ss_w), int(ss_h)))
        rot = pygame.transform.rotate(surf, -math.degrees(self.angle))
        rrect = rot.get_rect(center=(self.ss_pos.x, self.ss_pos.y))
        screen.blit(rot, rrect.topleft)

def recreate_object(stored, camera):
    parts = stored.split(" ")
    obj_type = parts.pop(0)
    if obj_type == "Circle":
        return Object.recreate_obj(parts, camera)
    elif obj_type == "Rect":
        return Rectangle.recreate_obj(parts, camera)
    else:
        print("Invalid Object Type")
        raise TypeError