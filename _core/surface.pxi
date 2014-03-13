

cdef extern from "Graphics.h" namespace "lime":
    cdef cppclass HardwareContext:
        int Width()
        int Height()

    cdef extern HardwareContext *gDirectRenderContext

    cdef cppclass RenderTarget:
        pass

    cdef cppclass RenderState:
        RenderState()
        RenderState(Surface *surf, int aa)

        void CombineColourTransform(const RenderState &inState,
                                        const ColorTransform *inObjTrans,
                                            ColorTransform *inBuf)

        Transform mTransform

        RenderPhase    mPhase
        bool           mRoundSizeToPOW2
        bool           mRecurse



cdef extern from "Graphics.h" namespace "lime::HardwareContext":
    cdef HardwareContext *current

cdef extern from "SimpleSurface.h" namespace "lime":
    cdef cppclass Surface:
        Surface()
        int             Width()
        int             Height()
        void            Clear(unsigned int color, Rect *rect)
        unsigned int    getPixel(int x, int y)
        void            setPixel(int x, int y, unsigned int color, bool alpha_too)
        void            scroll(int dx, int dy)
        Texture         *GetOrCreateTexture(HardwareContext &inHardware)


        Object*         IncRef()
        void            DecRef()

    cdef cppclass SimpleSurface(Surface):
        SimpleSurface(int width, int height, PixelFormat format, 
                        int byte_align, int gpu_format)
    
    cdef enum PixelFormat:
        pfXRGB         = 0x00
        pfARGB         = 0x01

cdef extern from "Texture.h" namespace "lime":
    cdef cppclass Texture:
        void Bind(Surface *inSurface, int inSlot)

cdef extern from "AutoSurfaceRender.h" namespace "lime":
    cdef cppclass AutoSurfaceRender:
        AutoSurfaceRender(Surface *surf)
        AutoSurfaceRender(Surface *surf, Rect &rt)

        RenderTarget &Target()

cdef extern from "Surface.h" namespace "lime::Surface":
    Surface* Load(OSChar *file_name)
    Surface* LoadFromBytes(uint8 *bytes, int length)


cdef class _Surface:
    cdef Surface *surf_ptr

    def __init__(self, file_name=None, bytes=None, int width=0, int height=0):
        if file_name is not None:
            IF PLATFORM == 'WINDOWS':
                self.surf_ptr = Load(UTF8ToWide(<char*>file_name).c_str())
            ELSE:
                self.surf_ptr = Load(<char*>file_name)              
        elif bytes is not None:
            val = str(bytes)
            self.surf_ptr = LoadFromBytes(<uint8*>val, len(bytes))
        elif width > 0 and height > 0:
            self.surf_ptr = new SimpleSurface(width, height, pfARGB, 4, -1)
        else:
            raise ValueError('Wrong _Surface constructor parametres')

        if self.surf_ptr == NULL:
            raise RuntimeError("Could not create a surface")

        self.surf_ptr.IncRef()

    def __dealloc__(self):
        self.surf_ptr.DecRef()

    def clear(self, unsigned int color):
        self.surf_ptr.Clear(color, NULL)

    def getPixel(self, int x, int y):
        return self.surf_ptr.getPixel(x, y)

    def setPixel(self, int x, int y, unsigned int color):
        self.surf_ptr.setPixel(x, y, color, False)

    def scroll(self, int dx, int dy):
        self.surf_ptr.scroll(dx, dy)

    def getWidth(self):
        return self.surf_ptr.Width()    

    def getHeight(self):
        return self.surf_ptr.Height()


from cython.operator cimport dereference as deref

def bindBitmapDataTexture(_Surface bitmapdata):
    cdef Surface *surf = bitmapdata.surf_ptr
    cdef HardwareContext *ctx = gDirectRenderContext
    cdef Texture *tex

    if surf != NULL:
        if ctx == NULL:
            ctx = current
        if ctx != NULL:
            tex = surf.GetOrCreateTexture(deref(ctx))
            if tex != NULL:
                tex.Bind(surf, -1)