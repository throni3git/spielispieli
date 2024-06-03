
class Vec2:
    """ two-dimensional vector class """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self._x + other._x, self._y + other._y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self._x - other._x, self._y - other._y)

    def __iadd__(self, other: "Vec2") -> "Vec2":
        self._x += other._x
        self._y += other._y
        return self

    def __isub__(self, other: "Vec2") -> "Vec2":
        self._x -= other._x
        self._y -= other._y
        return self
