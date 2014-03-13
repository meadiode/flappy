

class GLObject(object):

    def __init__(self, version, obj_id):
        self.version = version
        self.obj_id = obj_id

    def getType(self):
        return 'GLObject'

    def invalidate(self):
        self.obj_id = None

    def isValid(self):
        return self.obj_id != None and self.version == GL.version

    def __str__(self):
        return '%s(%i)' % (self.getType(), self.obj_id)

    @property
    def valid(self):
        return self.isValid()

    @property
    def invalidatet(self):
        return not self.valid


class GLShader(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)

    def getType(self):
        return 'Shader'


class GLProgram(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)
        self.shaders = []

    def attach(self, shader):
        self.shaders.append(shader)

    def getShaders(self):
        return self.shaders[:]

    def getType(self):
        return 'Program'


class GLBuffer(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)

    def getType(self):
        return 'Buffer'

class GLRenderBuffer(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)

    def getType(self):
        return 'RenderBuffer'

class GLFrameBuffer(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)

    def getType(self):
        return 'FrameBuffer' 


class GLTexture(GLObject):

    def __init__(self, version, obj_id):
        GLObject.__init__(self, version, obj_id)

    def getType(self):
        return 'Texture'

class GLContextAttributes(object):
    def __init__(self):
        self.alpha = False
        self.depth = False
        self.stencil = False
        self.antialias = False
        self.premultipliedAlpha = False
        self.preserveDrawingBuffer = False


class GLActiveInfo(object):
    def __init__(self):
        self.size = 0
        self.type = 0
        self.name = ""