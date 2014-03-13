
_geom_module = None

def _get_geom_module():
    global _geom_module
    if _geom_module is None:
        import flappy.geom
        _geom_module = flappy.geom
    return _geom_module

cdef extern from "Geom.h" namespace "lime":
    cdef cppclass TRect[T]:
        TRect() 
        TRect(T inX,T inY,T inW,T inH) 

        T x, y
        T w, h

    ctypedef TRect[int]         Rect
    ctypedef TRect[double]      DRect


cdef extern from "Geom.h" namespace "lime":
    cdef cppclass Point2D[T]:
        Point2D() 
        Point2D(T x, T y) 

        T x
        T y

    ctypedef Point2D[float]     UserPoint
    ctypedef Point2D[int]       ImagePoint


cdef extern from "Geom.h" namespace "lime":
    cdef cppclass Extent2D[T]:
        Extent2D()
        
        bool GetRect(Rect &outRect, double inExtraX=0, double inExtraY=0)
        bool Contains(UserPoint &inOther)
        
        T mMinX, mMaxX
        T mMinY, mMaxY
        bool mValidX, mValidY

    ctypedef Extent2D[int] Extent2DI
    ctypedef Extent2D[float] Extent2DF