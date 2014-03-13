
from flappy import _core
from flappy._core import _Surface

class BitmapData(_Surface):
    
    TRANSPARENT = 1
    HARDWARE    = 2

    @classmethod
    def load(cls, filename, format=0):
        return cls(_file_name=filename)    

    @classmethod
    def loadFromBytes(cls, bytes):
        return cls(_bytes=bytes)

    @staticmethod
    def bindTexture(target):
        assert isinstance(target, BitmapData)
        _core.bindBitmapDataTexture(target)

    def __init__(self, width=0, height=0, transparent=True, 
                    fill_color=0xffffffff, gpu_mode=-1,
                        _file_name=None, _bytes=None):
        _Surface.__init__(self, file_name=_file_name, bytes=_bytes,
                                    width=width, height=height)
        self._file_name = _file_name
        self._bytes = _bytes
        self._width = width
        self._height = height
        self._fill_color = fill_color
        self._transparent = transparent
        self._gpu_mode = gpu_mode
        if _file_name is None and _bytes is None:
            self.clear(fill_color)

    def draw(self, drawable, matrix, color_transform, blend_mode, 
                                                        clip_rect, smoothing):
        drawable._draw_to_surface(self, matrix, color_transform, 
                                                blend_mode, clip_rect)
        
    @property
    def width(self):
        return self.getWidth()

    @property
    def height(self):
        return self.getHeight()
