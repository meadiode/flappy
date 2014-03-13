
cdef class _DisplayObject

cdef extern from "Graphics.h" namespace "lime":

    cdef enum StrokeCaps:
        scRound, 
        scNone, 
        scSquare

    cdef enum StrokeJoints:
        sjRound, 
        sjMiter, 
        sjBevel

    cdef enum StrokeScaleMode:
        ssmNormal, 
        ssmNone, 
        ssmVertical, 
        ssmHorizontal, 
        ssmOpenGL

    cdef enum SpreadMethod:
        smPad, 
        smRepeat, 
        smReflect

    cdef enum InterpolationMethod:
        imRGB,
        imLinearRGB

    enum RenderPhase:
        rpBitmap, 
        rpRender, 
        rpHitTest, 
        rpCreateMask

    cdef cppclass Transform:
        Transform() 
        
        const Matrix  *mMatrix


    cdef cppclass ColorTransform:
        ColorTransform()

        double redMultiplier, redOffset
        double greenMultiplier, greenOffset
        double blueMultiplier, blueOffset
        double alphaMultiplier, alphaOffset

    cdef cppclass GraphicsGradientFill:
        GraphicsGradientFill()
        GraphicsGradientFill(bool linear, const Matrix mat, 
                                SpreadMethod spread, InterpolationMethod interp,
                                double focal)

        void AddStop(int rgb, float alpha, float ratio)
        void setIsSolidStyle(bool solid)
        Object *IncRef()
        void DecRef()


    cdef cppclass Graphics:
        Graphics()

        void clear()
        void beginFill(unsigned int color, float alpha)
        void endFill()
        void beginBitmapFill(Surface *bitmapData, Matrix &inMatrix,
                        bool inRepeat, bool inSmooth)
        void lineStyle(double thickness, unsigned int color, double alpha,
                      bool pixelHinting, StrokeScaleMode scaleMode,
                      StrokeCaps caps, StrokeJoints joints, double miterLimit)

        void lineTo(float x, float y)
        void moveTo(float x, float y)
        void curveTo(float cx,float cy,float x, float y)
        void arcTo(float cx,float cy,float x, float y)

        void drawEllipse(float x, float y, float width, float height)
        void drawCircle(float x, float y, float radius)
        void drawRect(float x, float y, float width, float height)
        void drawRoundRect(float x, float y,float width, float height,
                            float ellipseWidth, float ellipseHeight)

        void drawGraphicsDatum(GraphicsGradientFill *inData)

        void beginTiles(Surface *inSurface, bool inSmooth, int inBlendMode)
        void endTiles()
        void tile(float x, float y, const Rect &inTileRect, float *inTrans, float *inColour)


cdef class _Graphics:
    cdef Graphics *thisptr

    def __init__(self, _DisplayObject owner):
        self.thisptr = &owner.do_ptr.GetGraphics()

    def clear(self):
        self.thisptr.clear()

    def beginFill(self, unsigned int color, float alpha=1.0):
        self.thisptr.beginFill(color, alpha)

    def beginBitmapFill(self, _Surface bitmap, matrix=None, bool repeat=True, bool smooth=False):
        mat = matrix
        if matrix == None:
            mat = _get_geom_module().Matrix()
        cdef Matrix m
        m.m00 = mat.a 
        m.m01 = mat.b 
        m.m10 = mat.c 
        m.m11 = mat.d
        m.mtx = mat.tx
        m.mty = mat.ty
        self.thisptr.beginBitmapFill(bitmap.surf_ptr, m, repeat, smooth)

    def endFill(self):
        self.thisptr.endFill()

    def lineStyle(self, double thickness, unsigned int color = 0, double alpha=1.0,
                      bool pixelHinting=False, StrokeScaleMode scaleMode=ssmNormal,
                      StrokeCaps caps=scNone, StrokeJoints joints=sjMiter, double miterLimit=3.0):
        self.thisptr.lineStyle(thickness, color, alpha, 
            pixelHinting, scaleMode, caps, joints, miterLimit)

    def lineTo(self, float x, float y):
        self.thisptr.lineTo(x, y)

    def moveTo(self, float x, float y):
        self.thisptr.moveTo(x, y)

    def curveTo(self, float cx, float cy, float x, float y):
        self.thisptr.curveTo(cx, cy, x, y)

    def arcTo(self, float cx, float cy, float x, float y):
        self.thisptr.arcTo(cx, cy, x, y)

    def drawEllipse(self, float x, float y, float width, float height):
        self.thisptr.drawEllipse(x, y, width, height)

    def drawCircle(self, float x, float y, float radius):
        self.thisptr.drawEllipse(x - radius, y - radius, radius * 2.0, radius * 2.0)
    
    def drawRect(self, float x, float y, float width, float height):
        self.thisptr.drawRect(x, y, width, height)

    def drawRoundRect(self, float x, float y,float width, float height,
                            float ellipseWidth, float ellipseHeight):
        self.thisptr.drawRoundRect(x, y, width, height, ellipseWidth, ellipseHeight)

    def _beginGradientFill(self, bool linear, colors, alphas, ratios, matrix,
                             SpreadMethod spread_method, 
                                InterpolationMethod interpolation_method, 
                                    float focal_point_ratio, bool for_solid):
        cdef Matrix m
        m.m00 = matrix.a 
        m.m01 = matrix.b 
        m.m10 = matrix.c 
        m.m11 = matrix.d
        m.mtx = matrix.tx
        m.mty = matrix.ty

        cdef GraphicsGradientFill *grad = new GraphicsGradientFill(
                                                                linear, 
                                                                m, 
                                                                spread_method,
                                                                interpolation_method,
                                                                focal_point_ratio)
        n = min(len(colors), len(alphas), len(ratios))

        for i in range(n):
            grad.AddStop(colors[i], alphas[i], ratios[i])

        grad.setIsSolidStyle(for_solid)
        grad.IncRef()
        self.thisptr.drawGraphicsDatum(grad)
        grad.DecRef()

    def drawTiles(self, _Tilesheet sheet, tiles_data, flags):
        cdef BlendMode blend = bmNormal

        if (flags & TILE_BLEND_MASK) == TILE_BLEND_ADD:
            blend = bmAdd

        cdef bool smooth = ((flags & TILE_SMOOTH) != 0)
        self.thisptr.beginTiles(&sheet.thisptr.GetSurface(), smooth, blend)

        cdef int components = 3
        cdef int scale_pos = 3
        cdef int rot_pos = 3

        if flags & TILE_TRANS_2x2:
            components += 4
        else:
            scale_pos = components
            if flags & TILE_SCALE:
                components += 1
            rot_pos = components
            if flags & TILE_ROTATION:
                components += 1
        if flags & TILE_RGB:
            components += 3
        if flags & TILE_ALPHA:
            components += 1

        cdef float *trans_2x2 = [1.0, 0.0, 0.0, 1.0]
        cdef float *rgba = [1.0, 1.0, 1.0, 1.0]

        cdef int n = len(tiles_data) / components
        cdef int tmax = sheet.thisptr.Tiles() 
        cdef int tid
        cdef double x
        cdef double y
        
        cdef const Tile *tile
        cdef double ox
        cdef double _ox
        cdef double oy
        cdef double scale
        cdef double cos_theta
        cdef double sin_theta
        cdef const Rect *rt
        cdef int pos = 0

        cdef int i
        for i in range(n):
            x = tiles_data[pos + 0]
            y = tiles_data[pos + 1]
            tid = tiles_data[pos + 2]
            pos += 3

            if 0 <= tid < tmax:
                tile = &sheet.thisptr.GetTile(tid)
                ox = tile.mOx
                oy = tile.mOy
                rt = &tile.mRect

                if flags & (TILE_TRANS_2x2 | TILE_SCALE | TILE_ROTATION):
                    if flags & TILE_TRANS_2x2:
                        trans_2x2[0] = tiles_data[pos + 0]
                        trans_2x2[1] = tiles_data[pos + 1]
                        trans_2x2[2] = tiles_data[pos + 2]
                        trans_2x2[3] = tiles_data[pos + 3]
                        pos += 4
                    else:
                        scale = 1.0
                        cos_theta = 1.0
                        sin_theta = 1.0

                        if flags & TILE_SCALE:
                            scale = tiles_data[pos]
                            pos += 1

                        if flags & TILE_ROTATION:
                            cos_theta = math.cos(tiles_data[pos])
                            sin_theta = math.sin(tiles_data[pos])
                            pos += 1

                        trans_2x2[0] = scale * cos_theta
                        trans_2x2[1] = scale * sin_theta
                        trans_2x2[2] = -trans_2x2[1]
                        trans_2x2[3] = trans_2x2[0]

                    _ox = ox * trans_2x2[0] + oy * trans_2x2[2]
                    oy  = ox * trans_2x2[1] + oy * trans_2x2[3]
                    ox = _ox

                if flags & TILE_RGB:
                    rgba[0] = tiles_data[pos + 0]
                    rgba[1] = tiles_data[pos + 1]
                    rgba[2] = tiles_data[pos + 2]
                    pos += 3

                if flags & TILE_ALPHA:
                    rgba[3] = tiles_data[pos]
                    pos += 1

                self.thisptr.tile(x - ox, y - oy, deref(rt), trans_2x2, rgba)