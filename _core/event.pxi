

cdef extern from "Display.h" namespace "lime":
    cdef enum EventType:
        pass

    cdef enum EventFlags:
        pass

    cdef enum EventResult:
        pass

    cdef cppclass Event:
        Event(EventType inType=etUnknown, int inX=0, int inY=0, 
            int inValue=0, int inID=0, int inFlags=0, float inSx=1, float inSy=1)

        EventType type
        int       x,y
        int       value
        int       code
        int       id
        int       flags
        EventResult result
        float       sx,sy

etUnknown           = 0
etKeyDown           = 1
etChar              = 2
etKeyUp             = 3
etMouseMove         = 4
etMouseDown         = 5
etMouseClick        = 6
etMouseUp           = 7
etResize            = 8
etPoll              = 9
etQuit              = 10
etFocus             = 11
etShouldRotate      = 12
etDestroyHandler    = 13
etRedraw            = 14
etTouchBegin        = 15
etTouchMove         = 16
etTouchEnd          = 17
etTouchTap          = 18
etChange            = 19
etActivate          = 20
etDeactivate        = 21
etGotInputFocus     = 22
etLostInputFocus    = 23
etJoyAxisMove       = 24
etJoyBallMove       = 25
etJoyHatMove        = 26
etJoyButtonDown     = 27
etJoyButtonUp       = 28
etSysWM             = 29

efLeftDown          = 0x0001
efShiftDown         = 0x0002
efCtrlDown          = 0x0004
efAltDown           = 0x0008
efCommandDown       = 0x0010
efMiddleDown        = 0x0020
efRightDown         = 0x0040
efLocationRight     = 0x4000
efPrimaryTouch      = 0x8000
efNoNativeClick     = 0x10000

cdef class _Event:
    cdef Event          *thisptr

    def __cinit__(self):
        self.thisptr = NULL

    @property
    def type(self):
        return self.thisptr.type     
    @property
    def x(self):
        return self.thisptr.x    
    @property
    def y(self):
        return self.thisptr.y
    @property
    def value(self):
        return self.thisptr.value
    @property
    def code(self):
        return self.thisptr.code
    @property
    def id(self):
        return self.thisptr.id    
    @property
    def flags(self):
        return self.thisptr.flags    
    @property
    def result(self):
        return self.thisptr.result    
    @property
    def sx(self):
        return self.thisptr.sx    
    @property
    def sy(self):
        return self.thisptr.sy