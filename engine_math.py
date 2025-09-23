from fractions import Fraction
import math

pi = 3.14159265359

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
        if other.x == 0:
            other.x += 0.00001
        if other.y == 0:
            other.y += 0.00001
        return vec2(self.x / other.x, self.y / other.y)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __repr__(self):
        return f"{self.x}, {self.y}"
    
def decimal_to_fraction(decimal_str):
    return Fraction(decimal_str).limit_denominator()

def smart_number(decimal_str):
    frac = Fraction(decimal_str).limit_denominator()
    dec = str(float(decimal_str))
    
    if len(str(frac)) < len(dec):
        return frac
    else:
        return dec

def kelvin_to_col(temp):
    temperature = temp / 100

    if temperature <= 66:
        red = 255
    else:
        red = temperature - 60
        red = 329.698727446 * (red ** -0.1332047592)
        if red < 0: red = 0
        if red > 255: red = 255

    if temperature <= 66:
        green = temperature
        green = 99.4708025861 * math.log(green) - 161.1195681661
        if green < 0: green = 0
        if green > 255: green = 255
    else:
        green = temperature - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        if green < 0: green = 0
        if green > 255: green = 255

    if temperature >= 66:
        blue = 255
    else:
        if temperature <= 19:
            blue = 0
        else:
            blue = temperature - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
            if blue < 0: blue = 0
            if blue > 255: blue = 255
    
    return (red, green, blue)