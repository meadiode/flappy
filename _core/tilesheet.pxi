

cdef extern from "Tilesheet.h" namespace "lime":
    
    cdef cppclass Tile:
        float     mOx
        float     mOy
        Rect      mRect
        Surface   *mSurface

    cdef cppclass Tilesheet:
        Tilesheet(int width, int height, PixelFormat fmormat, bool initref=False)
        Tilesheet(Surface *surf, bool initref=False)

        Tilesheet   *IncRef()
        void        DecRef()
        int         AllocRect(int w, int h, int x, int y)
        int         addTileRect(const Rect &rect, float x, float y)
        const Tile  &GetTile(int inID)
        Surface     &GetSurface()
        int         Tiles()


cdef enum TileFlags:
    TILE_SCALE          = 0x0001
    TILE_ROTATION       = 0x0002
    TILE_RGB            = 0x0004
    TILE_ALPHA          = 0x0008
    TILE_TRANS_2x2      = 0x0010
    TILE_SMOOTH         = 0x1000
    TILE_BLEND_ADD      = 0x10000
    TILE_BLEND_MASK     = 0xf0000

cdef class _Tilesheet:
    cdef Tilesheet *thisptr
    cdef _Surface _surf
    
    def __init__(self, _Surface surf):
        self._surf = surf

        surf.surf_ptr.IncRef()
        self.thisptr = new Tilesheet(surf.surf_ptr)
        self.thisptr.IncRef()
        surf.surf_ptr.DecRef()

    def __dealloc__(self):
        self.thisptr.DecRef()

    def addTileRect(self, rect, center_point=None):
        cdef Rect rt = Rect(rect.x, rect.y, rect.width, rect.height)
        cdef UserPoint pt = UserPoint(0, 0)
        if center_point != None:
            pt.x = center_point.x
            pt.y = center_point.y

        cdef int ret = self.thisptr.addTileRect(rt, pt.x, pt.y)
        return ret