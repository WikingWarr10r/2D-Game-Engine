from fractions import Fraction

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
    
def decimal_to_fraction(decimal_str):
    return Fraction(decimal_str).limit_denominator()

def smart_number(decimal_str):
    frac = Fraction(decimal_str).limit_denominator()
    dec = str(float(decimal_str))
    
    if len(str(frac)) < len(dec):
        return frac
    else:
        return dec