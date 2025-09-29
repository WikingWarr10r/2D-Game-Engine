from engine_math import vec2

class Camera:
    def __init__(self, pos: vec2, zoom: int):
        self.pos = pos
        self.zoom = zoom

    def update_vector(self, vector):
        return (vector - self.pos) * vec2(self.zoom, self.zoom)

    def update_num(self, num):
        return num * self.zoom