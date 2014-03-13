

from flappy import _gl as gl

class Texture(object):

    def __init__(self, width, height):
        self.gl_texture = gl.createTexture()
        self.width = width
        self.height = height

        gl.bindTexture(gl.TEXTURE_2D, self.gl_texture)
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, 0)

#TODO: upload from bytes, upload from BitmapData 