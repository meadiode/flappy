# encoding: utf-8


class DropShadowFilter(object):

    def __init__(self, distance=4.0, angle=45.0, color=0, alpha=1.0, 
                    blurX=4.0, blurY=4.0, strength=1.0, quality=1, 
                        inner=False, knockout=False, hideObject=False):
        self._type = 'DropShadowFilter'
        self.distance = distance
        self.angle = angle
        self.color = color
        self.alpha = alpha
        self.blurX = blurX
        self.blurY = blurY
        self.strength = strength
        self.quality = quality
        self.inner = inner
        self.knockout = knockout
        self.hideObject = hideObject

    def clone(self):
        return DropShadowFilter(self.distance, self.angle, self.color, 
                                    self.alpha, self.blurX, self.blurY, 
                                        self.strength, self.quality, 
                                            self.inner, self.knockout, 
                                                self.hideObject)