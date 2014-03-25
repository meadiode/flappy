# encoding: utf-8

class BlurFilter(object):

    def __init__(self, blurX=4.0, blurY=4.0, quality=1):
        self._type = 'BlurFilter'
        self.blurX = blurX
        self.blurY = blurY
        self.quality = quality

    def clone(self):
        return BlurFilter(blurX=self.blurX, blurY=self.blurY, 
                                                quality=self.quality)