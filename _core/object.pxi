

cdef extern from "Object.h" namespace "lime":
    
    cdef cppclass Object:
        Object()
        Object *IncRef()
        void DecRef()
        int GetRefCount()


cdef class _Object:
    cdef Object *thisptr
    def __cinit__(self):
        self.thisptr = new Object()
        self.thisptr.IncRef()

    def __dealloc__(self):
        self.thisptr.DecRef()