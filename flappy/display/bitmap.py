
from flappy.display import BitmapData, DisplayObject


class PixelSnapping(object):
   NEVER    = 0
   AUTO     = 1
   ALWAYS   = 2


class Bitmap(DisplayObject):

    def __init__(self, bitmap_data=None, 
                        pixel_snapping=PixelSnapping.AUTO,
                                            smoothing=False):
        DisplayObject.__init__(self, 'Bitmap')
        self.pixelSnapping = pixel_snapping
        self._smoothing = smoothing
        self._bitmapData = bitmap_data
        self._rebuild()

    def _rebuild(self):
        if self._bitmapData:
            g = self.graphics
            g.clear()
            g.beginBitmapFill(self._bitmapData, repeat=False, smooth=True)
            g.drawRect(0.0, 0.0, 
                        self._bitmapData.width, self._bitmapData.height)
            g.endFill()

    @property
    def smoothing(self):
        return self._smoothing
    
    @smoothing.setter
    def smoothing(self, value):
        self._smoothing = value
        self._rebuild()

    @property
    def bitmapData(self):
        return self._bitmapData
    
    @bitmapData.setter
    def bitmapData(self, value):
        self._bitmapData = value
        self._rebuild()
