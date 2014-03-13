
class Transform(object):

    def __init__(self, parent):
        self.obj = parent         
    
    @property 
    def colorTransform(self):
        return self.obj._getColorTransform()

    @colorTransform.setter 
    def colorTransform(self, ct):
        self.obj._setColorTransform(ct)
        return ct

    @property 
    def concatenatedColorTransform(self):
        return self.obj._getColorTransform(True)

    @property 
    def concatenatedMatrix(self):
        return self.obj._getMatrix(True)

    @property 
    def matrix(self):
        return self.obj._getMatrix()

    @matrix.setter
    def matrix(self, m):
        self.obj._setMatrix(m)
        return m

    @property
    def pixelBounds(self):
        return self.obj._getPixelBounds()
