import math

from flappy.geom import Point

class Matrix(object):
    _GRADIENT_DIMENSION = 1638.4

    def __init__(self, a=1.0, b=0.0, c=0.0, d=1.0, tx=0.0, ty=0.0):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.tx = float(tx)
        self.ty = float(ty)

    def clone(self):
        return Matrix(self.a, self.b, self.c, self.d, self.tx, self.ty)

    def concat(self, m):
        a1 = self.a * m.a + self.b * m.c
        self.b = self.a * m.b + self.b * m.d
        self.a = a1

        c1 = self.c * m.a + self.d * m.c
        self.d = self.c * m.b + self.d * m.d

        self.c = c1

        tx1 = self.tx * m.a + self.ty * m.c + m.tx
        self.ty = self.tx * m.b + self.ty * m.d + m.ty
        self.tx = tx1

    def createBox(self, scalex, scaley, rotation=0.0, tx=0.0, ty=0.0):
        self.a = float(scalex)
        self.d = float(scaley)
        self.b = float(rotation)
        self.tx = float(tx)
        self.ty = float(ty)

    def createGradientBox(self, width, height, rotation=0.0, tx=0.0, ty=0.0):
        theta = rotation * (math.pi / 180.0)
        self.a = width / self._GRADIENT_DIMENSION
        self.d = height / self._GRADIENT_DIMENSION

        if float(theta) != 0.0:
            cos = math.cos(theta);
            sin = math.sin(theta);
            self.b = -sin * self.a;
            self.c = sin * self.d;
            self.a *= cos;
            self.d *= cos;
        else:
            self.b = self.c = 0;

        self.tx = tx + width / 2.0
        self.ty = ty + height / 2.0

    def deltaTransformPoint(self, p):
        return Point(p.x * self.a + p.y * self.c, p.x * self.b, p.y * self.d)

    def identity(self):
        self.a = 1.0
        self.b = 0.0
        self.c = 0.0
        self.d = 1.0
        self.tx = 0.0
        self.ty = 0.0

    def invert(self):
        norm = self.a * self.d - self.b * self.c;

        if norm == 0.0:
            self.a = self.b = self.c = self.d = 0.0
            self.tx = -self.tx
            self.ty = -self.ty
        else: 
            norm = 1.0 / norm
            a1 = self.d * norm
            self.d = self.a * norm
            self.a = a1
            self.b *= -norm
            self.c *= -norm

            tx1 = -self.a * self.tx - self.c * self.ty
            self.ty = -self.b * self.tx - self.d * self.ty
            self.tx = tx1

        return self

    def __mul__(self, m):
        ret = Matrix()

        ret.a = self.a * m.a + self.b * m.c
        ret.b = self.a * m.b + self.b * m.d
        ret.c = self.c * m.a + self.d * m.c
        ret.d = self.c * m.b + self.d * m.d

        ret.tx = self.tx * m.a + self.ty * m.c + m.tx
        ret.ty = self.tx * m.b + self.ty * m.d + m.ty

        return ret

    def rotate(self, deg):
        theta = deg * (math.pi / 180.0)
        cos = math.cos(theta)
        sin = math.sin(theta)

        a1 = self.a * cos - self.b * sin
        self.b = self.a * sin + self.b * cos
        self.a = a1

        c1 = self.c * cos - self.d * sin
        self.d = self.c * sin + self.d * cos
        self.c = c1

        tx1 = self.tx * cos - self.ty * sin
        self.ty = self.tx * sin + self.ty * cos
        self.tx = tx1

    def scale(self, sx, sy):
        self.a *= sx
        self.b *= sy

        self.c *= sx
        self.d *= sy

        self.tx *= sx
        self.ty *= sy

    def setRotation(self, theta, scale=1.0):
        self.a = math.cos(theta) * scale
        self.c = math.sin(theta) * scale
        self.b = -self.c
        self.d = self.a

    def transformPoint(self, p):
        return Point(p.x * self.a + p.y * self.c + self.tx, 
                        p.x * self.b + p.y * self.d + self.ty)

    def translate(self, dx, dy):
        self.tx += dx
        self.ty += dy

    def __getitem__(self, key):
        its = (self.a, self.b, self.c, self.d, self.tx, self.ty)
        if key >= len(its):
            raise IndexError('')
        return its[key]          
    