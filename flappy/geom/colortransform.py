

class ColorTransform(object):

    def __init__(self, redMultiplier=1.0, greenMultiplier=1.0, 
                        blueMultiplier=1.0, alphaMultiplier=1.0, 
                            redOffset=0.0, greenOffset=0.0, 
                                blueOffset=0.0, alphaOffset=0.0):
        self.redMultiplier = redMultiplier
        self.greenMultiplier = greenMultiplier
        self.blueMultiplier = blueMultiplier
        self.alphaMultiplier = alphaMultiplier
        self.redOffset = redOffset
        self.greenOffset = greenOffset
        self.blueOffset = blueOffset
        self.alphaOffset = alphaOffset

    def concat(self, second):
        self.redMultiplier += second.redMultiplier
        self.greenMultiplier += second.greenMultiplier
        self.blueMultiplier += second.blueMultiplier
        self.alphaMultiplier += second.alphaMultiplier

    @property
    def color(self):
        col = int(self.redOffset) << 16
        col |= int(self.greenOffset) << 8
        col |= int(self.blueOffset)
        return col

    @color.setter
    def color(self, value):
        self.redOffset = (value >> 16) & 0xff
        self.greenOffset = (value >> 8) & 0xff
        self.blueOffset = value & 0xff

        self.redMultiplier = 0
        self.greenMultiplier = 0
        self.blueMultiplier = 0

        return self.color
