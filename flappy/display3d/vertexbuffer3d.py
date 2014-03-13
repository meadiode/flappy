

from flappy import _gl as gl

class VertexBuffer3DFormat(object):
    BYTES_4 = 0
    FLOAT_1 = 1
    FLOAT_2 = 2
    FLOAT_3 = 3
    FLOAT_4 = 4

class VertexBuffer3D(object):

    def __init__(self, data32_per_vertex, data=None):
        self.gl_buffer = gl.createBuffer()
        self.data32_per_vertex = data32_per_vertex
        if data:
            self.upload(data)

    def __del__(self):
        gl.deleteBuffer(self.gl_buffer)

    def upload(self, data):
        gl.bindBuffer(gl.ARRAY_BUFFER, self.gl_buffer)
        gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW)