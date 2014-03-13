

from flappy.display import DisplayObject
from flappy.geom import Rectangle
from flappy._core import _DirectRenderer


class DirectRenderer(_DirectRenderer, DisplayObject):

    def __init__(self, render_func=None, name='DirectRenderer'):
        DisplayObject.__init__(self, name)
        self._render_func = render_func

    def _native_init(self):
        _DirectRenderer.__init__(self)

    def _render(self, rect):
        if self._render_func:
            self._render_func(Rectangle(*rect))
        else:
            raise AttributeError('You must have to define a rendering '
                                    'function for a DirectRenderer object')

    def setRenderFunc(self, render_func):
        self._render_func = render_func
