

ctypedef void (*RenderFunc)(void *handle, const Rect &inClipRect, const Transform &inTransform)

cdef void _direct_renderer_onrender_proxy(void *handle, const Rect &inClipRect, const Transform &inTransform):
    cdef object obj = <object>handle
    rt = _get_geom_module().Rectangle(inClipRect.x, inClipRect.y, inClipRect.w, inClipRect.h)
    
    try:
        obj._render(rt)
    except Exception as exc:
        print str(exc)
        traceback.print_exc(file=sys.stdout)
        print u'\n    ¯\_(ツ)_/¯    \n'

cdef extern from "Display.h" namespace "lime":

    cdef cppclass DirectRenderer(DisplayObject):
        DirectRenderer(RenderFunc onRender)

        void        *renderHandle
        RenderFunc  onRender



cdef class _DirectRenderer(_DisplayObject):
    cdef DirectRenderer *dr_ptr

    def __init__(self):
        self.dr_ptr = new DirectRenderer(_direct_renderer_onrender_proxy)
        self.do_ptr = <DisplayObject*>self.dr_ptr
        self.do_ptr.IncRef()
        self.created = True

        self.dr_ptr.renderHandle = <void*>self
