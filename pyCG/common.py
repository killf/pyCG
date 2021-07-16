class Point3D:
    """
    点
    """

    def __init__(self, x, y, z):
        """
        三维空间中的点
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """
        点的平移
        """
        if isinstance(other, Vector3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        """
        点的平移和点的减法运算
        """
        if isinstance(other, Point3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Vector3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise NotImplementedError()

    def __neg__(self):
        """
        负号
        """
        return Point3D(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        """
        判断两个点是否是同一个点
        """
        return isinstance(other, Point3D) and self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        """
        可视化
        """
        return f"Point3D({self.x}, {self.y}, {self.z})"


class Vector3D:
    """
    向量
    """

    def __init__(self, x, y, z):
        """
        三维空间中的向量
        """
        self.x = x
        self.y = y
        self.z = z

    def norm(self, p: int = 2):
        """
        向量的模
        """
        x, y, z = abs(self.x), abs(self.y), abs(self.z)
        if p == 0:
            return x + y + z
        elif p > 0:
            s = x ** p + y ** p + z ** p
            return s ** (1.0 / p)
        else:
            raise NotImplementedError()

    def is_zero(self):
        """
        是否是0向量
        """
        return abs(self.x) < 1e-8 and abs(self.y) < 1e-8 and abs(self.z) < 1e-8

    def __add__(self, other):
        """
        向量的加法运算
        """
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Point3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Line):
            return Line(other.p + self, other.v + self)
        elif isinstance(other, Plane):
            return Plane(other.p + self, other.n)
        elif isinstance(other, Triangle):
            return Triangle(other.a + self, other.b + self, other.c + self)
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        """
        向量的减法运算
        """
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x - other, self.y - other, self.z - other)
        elif isinstance(other, Line):
            return Line(other.p - self, other.v - self)
        elif isinstance(other, Plane):
            return Plane(other.p - self, other.n)
        elif isinstance(other, Triangle):
            return Triangle(other.a - self, other.b - self, other.c - self)
        else:
            raise NotImplementedError()

    def __mul__(self, other):
        """
        向量的数乘和内积
        """
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3D):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise NotImplementedError()

    def __matmul__(self, other):
        """
        向量的外积
        """
        if isinstance(other, Vector3D):
            return Vector3D(self.y * other.z - self.z * other.y, self.x * other.z - self.z * other.x, self.x * other.y - self.y * other.x)
        else:
            raise NotImplementedError()

    def __neg__(self):
        """
        负号
        """
        return Vector3D(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        """
        判断两个向量是否相等
        """
        return isinstance(other, Vector3D) and self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        """
        可视化
        """
        return f"Vector3D({self.x}, {self.y}, {self.z})"


class Line:
    """
    直线
    """

    def __init__(self, p: Point3D, v: Point3D):
        """
        使用两个不同的点来描述直线
        """
        assert p != v

        self.p = p
        self.v = v

    def pointAt(self, t: float or int):
        """
        直线上某处的点
        """
        return self.p + t * self.v

    def contain(self, point: Point3D):
        """
        直线上是否包含某个点
        """
        triangle = Triangle(self.p, self.v, point)
        return abs(triangle.area()) < 1e-8

    def coplane(self, other):
        """
        判断两条直线是否共面
        """
        return isinstance(other, Line) and Tetrahedron(self.p, self.v, other.p, other.v).volume() < 1e-8

    def __add__(self, other: Vector3D):
        """
        直线平移
        """
        return Line(self.p + other, self.v + other)

    def __sub__(self, other):
        """
        直线平移
        """
        return Line(self.p - other, self.v - other)

    def __eq__(self, other):
        """
        判断两条直线是否是同一条
        """
        return isinstance(other, Line) and self.contain(other.p) and self.contain(other.v)

    def __repr__(self):
        """
        可视化
        """
        return f"Line({self.p}, {self.v})"


class Plane:
    def __init__(self, p: Point3D, n: Vector3D):
        """
        使用点和法向量来描述一个平面
        """
        self.p = p
        self.n = n

    def contain(self, other):
        """
        判断点或直线是否在平面上
        """
        if isinstance(other, Point3D):
            return self.p == other or abs(self.n * (self.p - other)) < 1e-8
        elif isinstance(other, Line):
            return self.contain(other.p) and self.contain(other.v)
        else:
            raise NotImplementedError()

    def __add__(self, other: Vector3D):
        """
        平面的平移
        """
        return Plane(self.p + other, self.n)

    def __sub__(self, other: Vector3D):
        """
        平面的平移
        """
        return Plane(self.p - other, self.n)

    def __eq__(self, other):
        """
        判断两个平面是否是同一个
        """
        return isinstance(other, Plane) and self.contain(other.p) and (self.n @ other.n).is_zero()

    def __repr__(self):
        """
        可视化
        """
        return f"Plane(p={self.p}, n={self.n})"


class Triangle:
    """
    三角形
    """

    def __init__(self, a: Point3D, b: Point3D, c: Point3D):
        assert a != b and b != c and c != a

        self.a = a
        self.b = b
        self.c = c

    def area(self):
        """
        三角形的面积
        """
        x1, y1 = self.a.x, self.a.y
        x2, y2 = self.b.x, self.b.y
        x3, y3 = self.c.x, self.c.y
        return x1 * y2 - x1 * y3 + x2 * y3 - x2 * y1 + x3 * y1 - x2 * y2

    def contain(self, other):
        """
        判断三角形内部是否包含某个点
        """
        if isinstance(other, Point3D):
            s1 = Triangle(self.a, self.b, other).area()
            s2 = Triangle(self.a, other, self.c).area()
            s3 = Triangle(other, self.b, self.c).area()
            return abs(s1 + s2 + s3 - self.area()) < 1e-8
        else:
            raise NotImplementedError()

    def __add__(self, other: Vector3D):
        """
        三角形的平移
        """
        return Triangle(self.a + other, self.b + other, self.c + other)

    def __sub__(self, other):
        """
        三角形的平移
        """
        return Triangle(self.a - other, self.b - other, self.c - other)

    def __repr__(self):
        """
        可视化
        """
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"


class Tetrahedron:
    """
    四面体
    """

    def __init__(self, a: Point3D, b: Point3D, c: Point3D, d: Point3D):
        """
        使用四个点来表示四面体
        """
        assert a != b and a != c and a != d and b != c and b != d and c != d

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def volume(self):
        """
        求四面体的体积
        """
        a = self.a - self.d
        b = self.b - self.d
        c = self.c - self.d

        x1, y1, z1 = a.x, a.y, a.z
        x2, y2, z2 = b.x, b.y, b.z
        x3, y3, z3 = c.x, c.y, c.z

        v = x1 * (y2 * z3 - y3 * z2) - x2 * (y1 * z3 - y3 * z1) + x3 * (y1 * z2 - y2 * z1)
        return abs(v) / 6

    def __repr__(self):
        """
        可视化
        """
        return f"Tetrahedron(a={self.a}, b={self.b}, c={self.c}, d={self.d})"
