
import math

class Point(object):

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = float(x), float(y)

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __mul__(self, p):
        if isinstance(p, Point):
            return Point(self.x * p.x, self.y * p.y)
        elif isinstance(p, float):
            return Point(self.x * p, self.y * p)
        raise ValueError

    def clone(self):
        return Point(self.x, self.y)

    def __eq__(self, p):
        return p.x == self.x and p.y == self.y

    def normalize(self, thickness=1.0):
        if self.x == 0.0 and self.y == 0.0:
            return
        norm = thickness / math.sqrt(self.x * self.x + self.y * self.y)
        self.x *= norm
        self.y *= norm

    def offset(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return  '(x=%f, y=%f)' % (self.x, self.y)

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __getitem__(self, key):
        if key == 0: return self.x
        if key == 1: return self.y
        raise IndexError('')

    @staticmethod
    def distance(p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return math.sqrt(dx * dx + dy * dy)

    @classmethod
    def interpolate(cls, p1, p2, t):
        return cls(p2.x + t * (p1.x - p2.x), p2.y - t * (p1.y - p2.y))

    @classmethod
    def polar(cls, len_, angle):
        return cls(len_ * math.cos(angle), len_ * math.sin(angle))
