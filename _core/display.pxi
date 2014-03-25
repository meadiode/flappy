
cdef extern from "Display.h" namespace "lime":

    cdef enum BlendMode:
        bmNormal,
        bmLayer,
        bmMultiply,
        bmScreen,
        bmLighten,
        bmDarken,
        bmDifference,
        bmAdd,
        bmSubtract,
        bmInvert,
        bmAlpha,
        bmErase,
        bmOverlay,
        bmHardLight,
        bmCopy,
        bmInner,
        bmTinted,
        bmTintedInner,
        bmTintedAdd,

    cdef enum FocusSource:
        fsProgram,
        fsMouse,
        fsKey

    cdef enum StageQuality:
        sqLow,
        sqMedium,
        sqHigh,
        sqBest
    
    cdef enum StageScaleMode:
            ssmShowAll,
            ssmNoScale,
            ssmNoBorder,
            ssmExactFit
    
    cdef cppclass DisplayObject(Object):
        DisplayObject()

        double          getX()
        void            setX(double inValue)
        double          getY()
        void            setY(double inValue)
        double          getHeight()
        void            setHeight(double inValue)
        double          getWidth()
        void            setWidth(double inValue)
        double          getRotation()
        void            setRotation(double inValue)
        double          getScaleX()
        void            setScaleX(double inValue)
        double          getScaleY()
        void            setScaleY(double inValue)
        double          getMouseX()
        double          getMouseY()

        void            setScale9Grid(const DRect &inRect)
        void            setScrollRect(const DRect &inRect)
        void            setMask(DisplayObject *inMask)
        DisplayObject   *getMask()

        void            setOpaqueBackground(unsigned int inBG)
        unsigned int    getOpaqueBackground()
        bool            getMouseEnabled()
        void            setMouseEnabled(bool inVal)
        bool            getNeedsSoftKeyboard()
        void            setNeedsSoftKeyboard(bool inVal)
        bool            getMovesForSoftKeyboard()
        void            setMovesForSoftKeyboard(bool inVal)
        bool            getCacheAsBitmap()
        void            setCacheAsBitmap(bool inVal)
        bool            getVisible()
        void            setVisible(bool inVal)

        const wchar_t   *getName()
        void            setName(const WString &inName)
        void            setMatrix(const Matrix &inMatrix)
        void            setColorTransform(const ColorTransform &inTransform)

        double          getAlpha()
        void            setAlpha(double inAlpha)
        BlendMode       getBlendMode()
        void            setBlendMode(int inMode)

        int             getID()

        DisplayObject   *getParent()
        DisplayObject   *getRoot()

        Stage           *getStage()

        void            GetExtent(const Transform &inTrans, Extent2DF &outExt, bool inForBitmap, bool inIncludeStroke)

        void            Render( const RenderTarget &inTarget, const RenderState &inState )

        void            DirtyUp(unsigned int inFlags)
        void            DirtyCache(bool inParentOnly)
        bool            NonNormalBlendChild()

        UserPoint       GlobalToLocal(const UserPoint &inPoint)
        UserPoint       LocalToGlobal(const UserPoint &inPoint)

        Graphics        &GetGraphics()
        Matrix          GetFullMatrix(bool inWithStageScaling)
        Matrix          &GetLocalMatrix()
        ColorTransform  &GetLocalColorTransform()
        ColorTransform  GetFullColorTransform()
        void            setFilters(QuickVec[Filter*] &inFilters)

    cdef cppclass DisplayObjectContainer(DisplayObject):
        DisplayObjectContainer()

        void            addChild(DisplayObject *inChild)
        void            swapChildrenAt(int inChild1, int inChild2)
        void            removeChild(DisplayObject *inChild)
        void            removeChildAt(int inIndex)
        void            setChildIndex(DisplayObject *inChild, int inNewIndex)
        DisplayObject   *getChildAt(int index)
        void            hackAddChild(DisplayObject *inObj)
        void            hackRemoveChildren()

        void            RemoveChildFromList(DisplayObject *inChild)

        bool            getMouseChildren()
        void            setMouseChildren(bool inVal)

    ctypedef void (*EventHandler)(Event &ioEvent, void *inUserData)

    cdef cppclass Stage(DisplayObjectContainer):
        Stage()

        void            Flip()
        void            GetMouse()
        # Surface         *GetPrimarySurface()
        void            PollNow()
        void            RenderStage()
        bool            isOpenGL()

        void          SetEventHandler(EventHandler inHander, void *inUserData)
        void            SetNominalSize(int inWidth,int inHeight)
        DisplayObject   *HitTest(UserPoint inPoint, DisplayObject *inRoot, bool inRecurse)
        void            SetFullscreen(bool inFullscreen)
        void            ShowCursor(bool inShow)
        # void            SetCursor(Cursor inCursor)
        void            EnablePopupKeyboard(bool inEnable)
        double          GetNextWake()
        void            SetNextWakeDelay(double inNextWake)

        bool            getMultitouchSupported()
        void            setMultitouchActive(bool inActive)
        bool            getMultitouchActive()

        bool            FinishEditOnEnter()

        void            setFocusRect(bool inVal)
        bool            getFocusRect()
        UserPoint       getMousePos()
        double          getStageWidth()
        double          getStageHeight()
        double          getDPIScale()
        int             getScaleMode()
        void            setScaleMode(int inMode)
        int             getAlign()
        void            setAlign(int inAlign)
        int             getQuality()
        void            setQuality(int inQuality)
        int             getDisplayState()
        void            setDisplayState(int inDisplayState)
        int             GetAA()

        void            RemovingFromStage(DisplayObject *inObject)

        DisplayObject   *GetFocusObject()
        void            SetFocusObject(DisplayObject *inObj, FocusSource inSource, int inKey)

    cdef cppclass ManagedStage(Stage):
        ManagedStage(int inW,int inH,int inFlags)

    cdef cppclass Frame(Object):
        Frame()
        Stage *GetStage()

    cdef enum WindowFlags:
        wfFullScreen     = 0x00000001,
        wfBorderless     = 0x00000002,
        wfResizable      = 0x00000004,
        wfHardware       = 0x00000008,
        wfVSync          = 0x00000010,
        wfHW_AA          = 0x00000020,
        wfHW_AA_HIRES    = 0x00000060,
        wfAllowShaders   = 0x00000080,
        wfRequireShaders = 0x00000100,
        wfDepthBuffer    = 0x00000200,
        wfStencilBuffer  = 0x00000400

    ctypedef void (*FrameCreationCallback)(Frame*)

    void StartAnimation()
    void PauseAnimation()
    void ResumeAnimation()
    void StopAnimation()

    void CreateMainFrame(FrameCreationCallback inOnFrame, int inWidth,int inHeight,
                            unsigned int inFlags, const char *inTitle, Surface *inIcon)

IF PLATFORM == 'IOS':
    cdef extern from "Display.h" namespace "lime":
        Stage *IPhoneGetStage()


cdef extern from "Display.h" namespace "lime::Stage":
    Stage *GetCurrent()


cdef class _DisplayObject:
    cdef DisplayObject *do_ptr
    cdef bool created
 
    def __init__(self):
        self.do_ptr = new DisplayObject()
        self.do_ptr.IncRef()
        self.created = True
        self._filters = []

    def __dealloc__(self):
        if self.created:
            self.do_ptr.DecRef()

#TODO: refactor method names
    def setName(self, char *name):
        cdef WString nm = UTF8ToWide(name)
        self.do_ptr.setName(nm)

    def getName(self):
        cdef WString nm = WString(self.do_ptr.getName())
        cdef string ret = WideToUTF8(nm)
        return ret.c_str()

    def getID(self):
        return self.do_ptr.getID()

    def _getBounds(self, _DisplayObject target, bool strokes):
        cdef Matrix ref = target.do_ptr.GetFullMatrix(False)
        cdef Matrix inv_ref = ref.Inverse()

        cdef Matrix m = self.do_ptr.GetFullMatrix(False)
        m = inv_ref.Mult(m)

        cdef Transform trans
        trans.mMatrix = &m

        cdef Extent2DF ext
        self.do_ptr.GetExtent(trans, ext, False, strokes)

        cdef Rect rect
        ext.GetRect(rect)

        return _get_geom_module().Rectangle(rect.x, rect.y, rect.w, rect.h)

    def _getColorTransform(self, bool full=False):
        cdef ColorTransform ct
        if full:
            ct = self.do_ptr.GetFullColorTransform()
        else:
            ct = self.do_ptr.GetLocalColorTransform()
        return _get_geom_module().ColorTransform(
            ct.redMultiplier, ct.greenMultiplier, ct.blueMultiplier, ct.alphaMultiplier,
            ct.redOffset, ct.greenOffset, ct.blueOffset, ct.alphaOffset)

    def _setColorTransform(self, ctrans):
        cdef ColorTransform ct
        ct.redMultiplier = ctrans.redMultiplier
        ct.greenMultiplier = ctrans.greenMultiplier
        ct.blueMultiplier = ctrans.blueMultiplier
        ct.alphaMultiplier = ctrans.alphaMultiplier
        ct.redOffset = ctrans.redOffset
        ct.greenOffset = ctrans.greenOffset
        ct.blueOffset = ctrans.blueOffset
        ct.alphaOffset = ctrans.alphaOffset
        self.do_ptr.setColorTransform(ct)

    def _getMatrix(self, bool full=False):
        cdef Matrix m
        if full:
            m = self.do_ptr.GetFullMatrix(False)
        else:
            m = self.do_ptr.GetLocalMatrix()
        return _get_geom_module().Matrix(m.m00, m.m10, m.m01, m.m11, m.mtx, m.mty)

    def _setMatrix(self, mat):
        cdef Matrix m
        m.m00 = mat.a 
        m.m10 = mat.b 
        m.m01 = mat.c 
        m.m11 = mat.d
        m.mtx = mat.tx
        m.mty = mat.ty
        self.do_ptr.setMatrix(m)

    def _hitTestPoint(self, float x, float y, bool shapeFlag, bool recurse):
        cdef UserPoint pos = UserPoint(x, y)
        cdef Stage *stage
        
        if shapeFlag:
            stage = self.do_ptr.getStage()
            if stage != NULL:
                return (stage.HitTest(pos, self.do_ptr, recurse) != NULL)
            else:
                return False

        cdef Matrix m = self.do_ptr.GetFullMatrix(False)
        cdef Transform trans
        trans.mMatrix = &m
        cdef Extent2DF ext
        self.do_ptr.GetExtent(trans, ext, True, True)
        return ext.Contains(pos)

    def _drawToSurface(self, _Surface surf, mat, color_trans, blend_mode, clip_rect):
        cdef Rect r = Rect(0, 0, surf.surf_ptr.Width(), surf.surf_ptr.Height())

        if clip_rect != None:
            r.x = clip_rect.x
            r.y = clip_rect.y
            r.w = clip_rect.width
            r.h = clip_rect.height

        cdef AutoSurfaceRender *rend = new AutoSurfaceRender(surf.surf_ptr, r)
        cdef Matrix m
        m.m00 = mat.a 
        m.m10 = mat.b 
        m.m01 = mat.c 
        m.m11 = mat.d
        m.mtx = mat.tx
        m.mty = mat.ty

        cdef int aa = 4
        cdef Stage *stage = GetCurrent()
        if stage != NULL:
            aa = {
                sqLow       : 1,
                sqMedium    : 2,
                sqHigh      : 4,
                sqBest      : 4,
            }[stage.getQuality()]

        cdef RenderState state = RenderState(surf.surf_ptr, aa)
        state.mTransform.mMatrix = &m

        cdef ColorTransform ctrans, t
        ctrans.redMultiplier    = color_trans.redMultiplier
        ctrans.greenMultiplier  = color_trans.greenMultiplier
        ctrans.blueMultiplier   = color_trans.blueMultiplier
        ctrans.alphaMultiplier  = color_trans.alphaMultiplier
        ctrans.redOffset        = color_trans.redOffset
        ctrans.greenOffset      = color_trans.greenOffset
        ctrans.blueOffset       = color_trans.blueOffset
        ctrans.alphaOffset      = color_trans.alphaOffset
        state.CombineColourTransform(state, &t, &ctrans)
        
        state.mRoundSizeToPOW2 = False
        state.mPhase = rpBitmap

        cdef Matrix objmat = self.do_ptr.GetLocalMatrix()

        cdef float m00 = objmat.m00
        cdef float m01 = objmat.m01
        cdef float m10 = objmat.m10
        cdef float m11 = objmat.m11
        cdef float mtx = objmat.mtx
        cdef float mty = objmat.mty
        objmat.m00 = 1.0
        objmat.m01 = 0.0
        objmat.m10 = 0.0
        objmat.m11 = 1.0
        objmat.mtx = 0.0
        objmat.mty = 0.0
        self.do_ptr.setMatrix(objmat)

        cdef objalpha = self.do_ptr.getAlpha()
        self.do_ptr.setAlpha(1.0)

        cdef DisplayObjectContainer *dummy = new DisplayObjectContainer()
        dummy.IncRef()
        dummy.hackAddChild(self.do_ptr)
        dummy.Render(rend.Target(), state)
        
        state.mPhase = rpRender
        dummy.Render(rend.Target(), state)
        dummy.hackRemoveChildren()
        dummy.DecRef()

        objmat.m00 = m00
        objmat.m01 = m01
        objmat.m10 = m10
        objmat.m11 = m11
        objmat.mtx = mtx
        objmat.mty = mty
        self.do_ptr.setMatrix(objmat)
        self.do_ptr.setAlpha(objalpha)

    def setScrollRect(self, rect):
        cdef DRect rt = DRect(rect.x, rect.y, rect.width, rect.height)
        self.do_ptr.setScrollRect(rt)

    def setScale9Grid(self, rect):
        cdef DRect rt = DRect(rect.x, rect.y, rect.width, rect.height)
        self.do_ptr.setScale9Grid(rt)

    def globalToLocal(self, point):
        cdef UserPoint pt = UserPoint(point.x, point.y)
        cdef UserPoint ret = self.do_ptr.GlobalToLocal(pt)
        return _get_geom_module().Point(ret.x, ret.y)    

    def localToGlobal(self, point):
        cdef UserPoint pt = UserPoint(point.x, point.y)
        cdef UserPoint ret = self.do_ptr.LocalToGlobal(pt)
        return _get_geom_module().Point(ret.x, ret.y)

    def getX(self): 
        return self.do_ptr.getX()    

    def setX(self, x): 
        self.do_ptr.setX(x)
    
    def getY(self): 
        return self.do_ptr.getY()

    def setY(self, y): 
        self.do_ptr.setY(y)    

    def getWidth(self): 
        return self.do_ptr.getWidth()

    def setWidth(self, double width): 
        self.do_ptr.setWidth(width)    

    def getHeight(self): 
        return self.do_ptr.getHeight()

    def setHeight(self, double height): 
        self.do_ptr.setHeight(height)    

    def getRotation(self): 
        return self.do_ptr.getRotation()

    def setRotation(self, double rot): 
        self.do_ptr.setRotation(rot)    

    def getScaleX(self): 
        return self.do_ptr.getScaleX()

    def setScaleX(self, double scale_x): 
        self.do_ptr.setScaleX(scale_x)    

    def getScaleY(self): 
        return self.do_ptr.getScaleY()

    def setScaleY(self, double scale_y): 
        self.do_ptr.setScaleY(scale_y)

    def getMouseX(self):
        return self.do_ptr.getMouseX()    

    def getMouseY(self):
        return self.do_ptr.getMouseY()

    def setOpaqueBackground(self, color):
        self.do_ptr.setOpaqueBackground(color)    

    def getOpaqueBackground(self):
        return self.do_ptr.getOpaqueBackground()

    def setMouseEnabled(self, bool val):
        self.do_ptr.setMouseEnabled(val)

    def getMouseEnabled(self):
        return self.do_ptr.getMouseEnabled()

    def setNeedsSoftKeyboard(self, bool val):
        self.do_ptr.setNeedsSoftKeyboard(val)

    def getNeedsSoftKeyboard(self):
        return self.do_ptr.getNeedsSoftKeyboard()    

    def setMovesForSoftKeyboard(self, bool val):
        self.do_ptr.setMovesForSoftKeyboard(val)

    def getMovesForSoftKeyboard(self):
        return self.do_ptr.getMovesForSoftKeyboard()    

    def setCacheAsBitmap(self, bool val):
        self.do_ptr.setCacheAsBitmap(val)

    def getCacheAsBitmap(self):
        return self.do_ptr.getCacheAsBitmap()

    def setVisible(self, bool val):
        self.do_ptr.setVisible(val)

    def getVisible(self):
        return self.do_ptr.getVisible()

    def setAlpha(self, double alpha):
        self.do_ptr.setAlpha(alpha)

    def getAlpha(self):
        return self.do_ptr.getAlpha()

    def setBlendMode(self, int mode):
        self.do_ptr.setBlendMode(mode)

    def getBlendMode(self):
        return self.do_ptr.getBlendMode()

    def getGraphics(self):
        return _Graphics(self)

    def _set_filters(self, filter_list):
        cdef QuickVec[Filter*] cfilter_list
        _to_native_filter_list(cfilter_list, filter_list)
        self.do_ptr.setFilters(cfilter_list)
        self._filters = filter_list

cdef class _DisplayObjectContainer(_DisplayObject):
    cdef DisplayObjectContainer *doc_ptr

    def __init__(self):
        self.doc_ptr = new DisplayObjectContainer()
        self.do_ptr = <DisplayObject*>self.doc_ptr
        self.do_ptr.IncRef()
        self.created = True

    def addChild(self, _DisplayObject obj):
        self.doc_ptr.addChild(obj.do_ptr)

    def swapChildrenAt(self, int child1, int child2):
        self.doc_ptr.swapChildrenAt(child1, child2)

    def removeChild(self, _DisplayObject obj):
        self.doc_ptr.removeChild(obj.do_ptr)

    def removeChildAt(self, int child):
        self.doc_ptr.removeChildAt(child)

    def setChildIndex(self, _DisplayObject obj, int new_index):
        self.doc_ptr.setChildIndex(obj.do_ptr, new_index)

    def setMouseChildren(self, bool value):
        self.doc_ptr.setMouseChildren(value)    

    def getMouseChildren(self):
        return self.doc_ptr.getMouseChildren()


cdef class _Stage(_DisplayObjectContainer):
    cdef Stage         *stage_ptr
    
    def __init__(self):
        self.stage_ptr = GetCurrent()
        self.doc_ptr = <DisplayObjectContainer*>self.stage_ptr
        self.do_ptr = <DisplayObject*>self.stage_ptr
        self.created = False

    def getStageWidth(self):
        return self.stage_ptr.getStageWidth()

    def getStageHeight(self):
        return self.stage_ptr.getStageHeight()

    def getQuality(self):
        return self.stage_ptr.getQuality()

    def setQuality(self, int quality):
        self.stage_ptr.setQuality(quality)

    def showCursor(self, bool show_cursor):
        self.stage_ptr.ShowCursor(show_cursor)

    def _render_stage(self):
        self.stage_ptr.RenderStage()

    def _set_next_wake_delay(self, double next_wake):
        self.stage_ptr.SetNextWakeDelay(next_wake)

    def _get_focus_id(self):
        cdef DisplayObject *focus_obj
        focus_obj = self.stage_ptr.GetFocusObject()
        if focus_obj != NULL:
            return focus_obj.getID()
        return 0;

    def _set_focus(self, _DisplayObject focus_obj):
        if focus_obj is None:
            self.stage_ptr.SetFocusObject(NULL, fsProgram, 0)
        else:
            self.stage_ptr.SetFocusObject(focus_obj.do_ptr, fsProgram, 0)