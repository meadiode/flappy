# encoding: utf-8


class ColorMatrixFilter(object):

    def __init__(self, matrix):
        if len(matrix) != 20:
            raise ValueError('The matrix argument must must be an iterable ' 
                                'of 20 elements' )

        self._type = 'ColorMatrixFilter'
        self.matrix = matrix[:]

    def clone(self):
        return ColorMatrixFilter(self.matrix)