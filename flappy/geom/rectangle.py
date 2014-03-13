
from flappy.geom import Point, Matrix

class Rectangle(object):

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def clone(self):
        return Rectangle(self.x, self.y, self.width, self.height)

    def contains(self, x, y):
        return (self.x <= x < self.right) and (self.y <= y < self.bottom)

    def containsPoint(self, p):
        return self.contains(p.x, p.y)

    def containsRect(self, rect):
        if self.contains(rect.x, rect.y):
            if self.containsPoint(rect.bottomRight):
                return True
        return False

    def __eq__(self, rect):
        return self.x == rect.x and self.y == rect.y and \
                self.width == rect.width and self.height == rect.height

    def extendBounds(self, r):
        dx = self.x - r.x;
        if dx > 0.0: 
            self.x -= dx
            self.width += dx

        dy = self.y - r.y
        if dy > 0:
            self.y -= dy
            self.height += dy

        if r.right > self.right:
            self.right = r.right;

        if r.bottom > self.bottom:     
            self.bottom = r.bottom;

    def inflate(self, dx , dy):
        self.x -= dx
        self.width += dx * 2.0
        self.y -= dy
        self.height += dy * 2.0

    def inflatePoint(self, p):
        self.inflate(p.x, p.y)

    def intersection(self, rect):
        x0 = rect.x if self.x < rect.x else self.x
        x1 = rect.right if self.right > rect.right else self.right
        if x1 <= x0:
            return Rectangle()

        y0 = rect.y if self.y < rect.y else self.y
        y1 = rect.bottom if self.bottom > rect.bottom else self.bottom
        if y1 <= y0:
            return Rectangle()
            
        return Rectangle(x0, y0, x1 - x0, y1 - y0)    

    def intersects(self, rect):
        x0 = rect.x if self.x < rect.x else self.x
        x1 = rect.right if self.right > rect.right else self.right
        if x1 <= x0:
            return False

        y0 = rect.y if self.y < rect.y else self.y
        y1 = rect.bottom if self.bottom > rect.bottom else self.bottom
        return y1 > y0

    def isEmpty(self):
        return self.width == 0.0 and self.height == 0.0

    def offset(self, dx, dy):
        self.x += dx
        self.y += dy

    def offstePoint(self, p):
        self.x += p.x
        self.y += p.y

    def setEmpty(self):
        self.x = self.y = self.width = self.height = 0

    def transform(self, m):
        tx0 = m.a * self.x + m.c * self.y;
        tx1 = tx0;
        ty0 = m.b * self.x + m.d * self.y;
        ty1 = tx0;

        tx = m.a * (self.x + self.width) + m.c * self.y
        ty = m.b * (self.x + self.width) + m.d * self.y
        if tx < tx0: tx0 = tx
        if ty < ty0: ty0 = ty
        if tx > tx1: tx1 = tx
        if ty > ty1: ty1 = ty

        tx = m.a * (self.x + self.width) + m.c * (self.y + self.height)
        ty = m.b * (self.x + self.width) + m.d * (self.y + self.height)
        if tx < tx0: tx0 = tx
        if ty < ty0: ty0 = ty
        if tx > tx1: tx1 = tx
        if ty > ty1: ty1 = ty

        tx = m.a * self.x + m.c * (self.y + self.height)
        ty = m.b * self.x + m.d * (self.y + self.height)
        if tx < tx0: tx0 = tx
        if ty < ty0: ty0 = ty
        if tx > tx1: tx1 = tx
        if ty > ty1: ty1 = ty

        return Rectangle(tx0 + m.tx, ty0 + m.ty, tx1 - tx0, ty1 - ty0)

    def union(self, rect):
        x0 = rect.x if self.x > rect.x else self.x
        x1 = rect.right if self.right < rect.right else self.right
        y0 = rect.y if self.y > rect.y  else self.y
        y1 = rect.bottom if self.bottom < rect.bottom else self.bottom
        return Rectangle(x0, y0, x1 - x0, y1 - y0)

    def __getitem__(self, key):
        its = (self.x, self.y, self.width, self.height)
        if key >= len(its):
            raise IndexError('')
        return its[key]

    def __len__(self):
        return 4

    def __str__(self):
        return 'Rectangle (x: %.2f, y: %.2f, width: %.2f, height: %.2f)' % \
                    (self.x, self.y, self.width, self.height)              

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, b):
        self.height = b - self.y
        return b

    @property
    def bottomRight(self):
        return Point(self.x + self.width, self.y + self.height)

    @bottomRight.setter
    def bottomRight(self, p):
        self.width = p.x - self.x
        self.height = p.y - self.y 
        return p.clone()

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, l):
        self.width -= l - self.x
        self.x = l
        return l

    @property 
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, r):
        self.width = r - self.x
        return r

    @property 
    def size(self):
        return Point(self.width, self.height)

    @size.setter
    def size(self, p):
        self.width = p.x
        self.height = p.y
        return p.clone()

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, t):
        self.height -= t - self.y
        self.y = t
        return t

    @property 
    def topLeft(self):
        return Point(self.x ,self.y)

    @topLeft.setter
    def topLeft(self, p):
        self.x = p.x
        self.y = p.y
        return p.clone()
