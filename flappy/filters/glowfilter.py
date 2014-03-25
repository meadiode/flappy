# encoding: utf-8


class GlowFilter(object):

    def __init__(self, color=0x0, alpha=1.0, blurX=4.0, blurY=4.0, 
                    strength=1.0, quality=1, inner=False, knockout=False):
        self._type = 'DropShadowFilter'

        self.distance = 0
        self.angle = 0
        self.color = color
        self.alpha = alpha
        self.blurX = blurX
        self.blurY = blurY
        self.strength = strength
        self.quality = quality
        self.inner = inner
        self.knockout = knockout
        self.hideObject = False

    def clone(self):
        return GlowFilter(self.color, self.alpha, self.blurX, self.blurY, 
                            self.strength, self.quality, self.inner, 
                                self.knockout)
