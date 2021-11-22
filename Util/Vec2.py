import math


class Vec2:

    g = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vec2(self.x, self.y)

    # region getters & setters

    @property
    def t(self):
        if self.x == 0:
            return math.pi / 2 if self.y > 0 else 3 * math.pi / 2
        atan = math.atan(self.y / self.x)
        return (atan + 2 * math.pi) % (2 * math.pi) if self.x > 0 else atan + math.pi

    @t.setter
    def t(self, v):
        length = self.r
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

    def normalized(self):
        length = self.r
        if length > 0:
            return Vec2(self.x / length, self.y / length)
        else:
            return Vec2.zero()

    def set(self, a, b=0):
        if type(a) is Vec2:
            self.x = a.x
            self.y = a.y
        elif type(a) in [int, float] and type(b) in [int, float]:
            self.x = a
            self.y = b

    @property
    def tup(self):
        return (self.x, self.y)

    @tup.setter
    def tup(self, value):
        self.x = value[0]
        self.y = value[1]

    # endregion

    # region static vectors

    def zero():
        return Vec2(0, 0)

    def one():
        return Vec2(1, 1)

    def up():
        return Vec2(0, 1)

    def down():
        return Vec2(0, -1)

    def left():
        return Vec2(-1, 0)

    def right():
        return Vec2(1, 0)

    # endregion

    # region python functions

    def __iter__(self):
        yield self.x
        yield self.y

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

    def __str__(self):
        return f"<{self.x}, {self.y}>"

    def __bool__(self):
        return self.x or self.y

    # endregion

    # region operator overloads

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
        return self

    def __isub__(self, other):
        if type(other) is Vec2:
            self.x -= other.x
            self.y -= other.y
        elif type(other) is float or type(other) is int:
            self.x -= other
            self.y -= other
        return self

    def __imul__(self, other):
        if type(other) is Vec2:
            self.x *= other.x
            self.y *= other.y
        elif type(other) is float or type(other) is int:
            self.x *= other
            self.y *= other
        return self

    def __idiv__(self, other):
        if type(other) is Vec2:
            self.x /= other.x
            self.y /= other.y
        elif type(other) is float or type(other) is int:
            self.x /= other
            self.y /= other
        return self

    def __ipow__(self, other):
        if type(other) is Vec2:
            self.x **= other.x
            self.y **= other.y
        elif type(other) is float or type(other) is int:
            self.x **= other
            self.y **= other
        return self

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __pos__(self):
        return Vec2(self.x, self.y)

    # endregion
