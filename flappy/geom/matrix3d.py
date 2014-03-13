import math

class Matrix3D(object):

    def __init__(self, data=None):
        self.data = None
        if data and len(data) == 16:
            self.data = data
        else:
            self.identity()


    def identity(self):
        self.data = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

    def __getitem__(self, key):
        if key >= len(self.data):
            raise IndexError('')
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        ret = 'Matrix3D:\n'
        for i in range(4):
            ret = ret + '[ %.2f,  %.2f,  %.2f,  %.2f]\n' % \
                                        tuple(self.data[i * 4 : (i + 1) * 4])
        return ret

    def append(self, mat):
        result = []
        for i in range(4):
            for j in range(4):
                nn = 0.0
                for k in range(4):
                    nn += self[i * 4 + k] * mat[k * 4 + j]
                result.append(nn)
        self.data = result

    def transformvec(self, vec):
        ret = []
        for i in range(4):
            nn = 0.0
            for j in range(4):
                nn += self[i * 4 + j] * vec[j]
            ret.append(nn)
        return ret

    def rotate(self, ax, ay, az):
        sinax = math.sin(ax)
        cosax = math.cos(ax)
        sinay = math.sin(ay)
        cosay = math.cos(ay)
        sinaz = math.sin(az)
        cosaz = math.cos(az)

        rx = Matrix3D([
            1.0, 0.0, 0.0, 0.0,
            0.0, cosax, -sinax, 0.0,
            0.0, sinax, cosax, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])
        ry = Matrix3D([
            cosay, 0.0, sinay, 0.0,
            0.0, 1.0, 0.0, 0.0,
            -sinay, 0.0, cosay, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])

        rz = Matrix3D([
            cosaz, -sinaz, 0.0, 0.0,
            sinaz, cosaz, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])

        self.append(rx)
        self.append(ry)
        self.append(rz)

    def translate(self, tx, ty, tz):
        t = Matrix3D([
            1.0, 0.0, 0.0, tx,
            0.0, 1.0, 0.0, ty,
            0.0, 0.0, 1.0, tz,
            0.0, 0.0, 0.0, 1.0
        ])
        self.append(t)    

    def scale(self, sx, sy, sz):
        s = Matrix3D([
            sx, 0.0, 0.0, 0.0,
            0.0, sy, 0.0, 0.0,
            0.0, 0.0, sz, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])
        self.append(s)

    @staticmethod
    def create2D(x, y, scale=1.0, rotation=0.0):
        theta = rotation * math.pi / 180.0
        c = math.cos(theta)
        s = math.sin(theta)
        return Matrix3D([
            c * scale, -s * scale,  0.0,  0.0,
            s * scale,  c* scale,   0.0,  0.0,
            0.0,        0.0,        1.0,  0.0,
            x,          y,          0.0,  1.0,
        ])

    @staticmethod
    def createOrtho(x0, x1, y0, y1, znear, zfar):
        sx = 1.0 / (x1 - x0)
        sy = 1.0 / (y1 - y0)
        sz = 1.0 / (zfar - znear)
        return Matrix3D([
            2.0 * sx,         0.0,              0.0,                   0.0,
            0.0,              2.0 * sy,         0.0,                   0.0,
            0.0,              0.0,              -2.0 * sz,             0.0,
            -(x0 + x1) * sx,  -(y0 + y1) * sy,  -(znear + zfar) * sz,  1.0,
        ])

    @staticmethod
    def createPerspective(fov, aspect, znear, zfar):
        top = znear * math.tan(fov)
        bottom = -top
        right = top * aspect
        left = -right
        return Matrix3D([
                (2.0 * znear) / (right - left), 0.0, 0.0, 0.0,
                0.0, (2.0 * znear) / (top - bottom), 0.0, 0.0,
                0.0, 0.0, -((zfar + znear) / (zfar - znear)),
                                -((2.0 * zfar * znear) / (zfar - znear)),
                0.0, 0.0, -1.0, 0.0 
            ])
