
from flappy import _core
from flappy.geom import Matrix

class SpreadMethod(object):
    PAD     = 'pad'
    REPEAT  = 'repeat'
    REFLECT = 'reflect'

    _INT_MAP = {
        PAD         : 0,
        REPEAT      : 1,
        REFLECT     : 2,
    }


class InterpolationMethod(object):
    RGB         = 'rgb'
    LINEAR_RGB  = 'linear_rgb'

    _INT_MAP = {
        RGB         : 0,
        LINEAR_RGB  : 1,
    }


class GradientType(object):
    LINEAR = 'linear'
    RADIAL = 'radial'


class GraphicsPathWinding(object):
    EVEN_ODD = "evenOdd"
    NON_ZERO = "nonZero"

    _INT_MAP = {
        EVEN_ODD    : 0,
        NON_ZERO    : 1,
    }


class GraphicsPathCommand(object):
    NO_OP           = 0
    MOVE_TO         = 1
    LINE_TO         = 2
    CURVE_TO        = 3
    WIDE_MOVE_TO    = 4
    WIDE_LINE_TO    = 5
    CUBIC_CURVE_TO  = 6


class TriangleCulling(object):
    POSITIVE    = 0
    NONE        = 1
    NEGATIVE    = 2


class LineScaleMode(object):
    NORMAL      = 0
    NONE        = 1
    VERTICAL    = 2
    HORIZONTAL  = 3
    OPENGL      = 4


class CapsStyle(object):
    ROUND   = 0
    NONE    = 1
    SQUARE  = 2


class JointStyle(object):
    ROUND   = 0
    MITER   = 1
    BEVEL   = 2


class BlendMode(object):
    NORMAL      = 0
    LAYER       = 1
    MULTIPLY    = 2
    SCREEN      = 3
    LIGHTEN     = 4
    DARKEN      = 5
    DIFFERENCE  = 6
    ADD         = 7
    SUBTRACT    = 8
    INVERT      = 9
    ALPHA       = 10
    ERASE       = 11
    OVERLAY     = 12
    HARDLIGHT   = 13


class Graphics(_core._Graphics):

    def __init__(self, owner):
        _core._Graphics.__init__(self, owner)
        
    def beginBitmapFill(self, bitmap, m=None, repeat=True, smooth=False):
        mat = m if m else Matrix()
        _core._Graphics.beginBitmapFill(self, bitmap, 
                                                mat, repeat, smooth)

    def beginGradientFill(self, gtype, colors, alphas, ratios, 
                            matrix=None, spread_method=SpreadMethod.PAD, 
                                interpolation_method=InterpolationMethod.RGB, 
                                    focal_point_ratio=0.0):
        linear = (gtype == GradientType.LINEAR)
        mat = matrix if matrix else Matrix()
        spread = SpreadMethod._INT_MAP[spread_method]
        interp = InterpolationMethod._INT_MAP[interpolation_method]

        _core._Graphics._beginGradientFill(
                                        self, linear, colors, 
                                            alphas, ratios, mat, 
                                                spread, interp,
                                                    focal_point_ratio, True)

    def drawPath(self, commands, data, winding=GraphicsPathWinding.EVEN_ODD):
        _core._Graphics.drawPath(self, commands, data, 
                                        GraphicsPathWinding._INT_MAP[winding])


    @staticmethod
    def RGBA(rgb, a=0xff):
        return rgb | (a << 24)

