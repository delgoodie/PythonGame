import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def t(self):
        return math.atan(self.x / self.y)

    @t.setter
    def t(self, v):
        length = self.length
        self.x = length * math.cos(v)
        self.y = length * math.sin(v)

    @property
    def r(self):
        return math.hypot(self.x, self.y)

    @r.setter
    def r(self, v):
        angle = self.t
        self.x = v * math.cos(angle)
        self.y = v * math.sin(angle)

    @property
    def mag(self):
        return math.hypot(self.x, self.y)

    @property
    def tup(self):
        return (self.x, self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        raise Exception("error")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception("error")

    # region Operator Overloads

    def __add__(self, other):
        if type(other) is Vec2:
            return Vec2(self.x + other.x, self.y + other.y)
        elif type(other) is float or type(other) is int:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) is Vec2:
            return Vec2(self.x - other.x, self.y - other.y)
        elif type(other) is float or type(other) is int:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) is Vec2:
            return Vec2(self.x * other.x, self.y * other.y)
        elif type(other) is float or type(other) is int:
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) is Vec2:
            return Vec2(self.x / other.x, self.y / other.y)
        elif type(other) is float or type(other) is int:
            return Vec2(self.x / other, self.y / other)

    def __pow__(self, other):
        if type(other) is Vec2:
            return Vec2(self.x ** other.x, self.y ** other.y)
        elif type(other) is float or type(other) is int:
            return Vec2(self.x ** other, self.y ** other)

    def __eq__(self, other):
        return type(other) is Vec2 and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not type(other) is Vec2 or self.x != other.x or self.y != other.y

    def __iadd__(self, other):
        if type(other) is Vec2:
            self.x += other.x
            self.y += other.y
        elif type(other) is float or type(other) is int:
            self.x += other
            self.y += other

    def __isub__(self, other):
        if type(other) is Vec2:
            self.x -= other.x
            self.y -= other.y
        elif type(other) is float or type(other) is int:
            self.x -= other
            self.y -= other

    def __imul__(self, other):
        if type(other) is Vec2:
            self.x *= other.x
            self.y *= other.y
        elif type(other) is float or type(other) is int:
            self.x *= other
            self.y *= other

    def __idiv__(self, other):
        if type(other) is Vec2:
            self.x /= other.x
            self.y /= other.y
        elif type(other) is float or type(other) is int:
            self.x /= other
            self.y /= other

    def __ipow__(self, other):
        if type(other) is Vec2:
            self.x **= other.x
            self.y **= other.y
        elif type(other) is float or type(other) is int:
            self.x **= other
            self.y **= other

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __pos__(self):
        return Vec2(self.x, self.y)

    # endregion
