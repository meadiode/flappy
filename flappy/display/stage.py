# encoding: utf-8

import time

import flappy
from flappy import _core
from flappy.events import Event, KeyboardEvent, MouseEvent, TouchEvent
from flappy.events import FocusEvent
from flappy.geom import Point
from flappy.display import DisplayObject, DisplayObjectContainer


class StageQuality(object):
    LOW      = 'low'
    MEDIUM   = 'medium'
    HIGH     = 'high'
    BEST     = 'best'
    _ENUM    = [LOW, MEDIUM, HIGH, BEST]


class Stage(DisplayObjectContainer, _core._Stage):

#public constants
    DOUBLE_CLICK_INTERVAL = 0.25
    
#public methods
    def invalidate(self):
        self._invalid = True

#public properties
    @property
    def frameRate(self):
        return self._frame_rate

    @frameRate.setter
    def frameRate(self, value):
        self._frame_rate = value
        self._frame_period = value if value <= 0 else 1.0 / value

    @property
    def stage(self):
        return self

    @property
    def stageWidth(self):
        return self.getStageWidth()

    @property
    def stageHeight(self):
        return self.getStageHeight()

    @property
    def focus(self):
        obj_id = self._get_focus_id()
        return self._find_by_id(obj_id)

    @focus.setter
    def focus(self, focus_obj):
        self._set_focus(focus_obj)

    @property
    def quality(self):
        return StageQuality._ENUM[self.getQuality()]

    @quality.setter
    def quality(self, quality):
        self.setQuality(StageQuality._ENUM.index(quality))

    @property
    def color(self):
        return self.opaqueBackground

    @color.setter
    def color(self, color):
        self.opaqueBackground = color

#private constants
    _EF_LEFT_DOWN       = 0x0001
    _EF_SHIFT_DOWN      = 0x0002
    _EF_CTRL_DOWN       = 0x0004
    _EF_ALT_DOWN        = 0x0008
    _EF_COMMAND_DOWN    = 0x0010
    _EF_LOCATION_RIGHT  = 0x4000
    _EF_NO_NATIVE_CLICK = 0x10000

    _MOUSE_CHANGES = (
        MouseEvent.MOUSE_OUT,
        MouseEvent.MOUSE_OVER,
        MouseEvent.ROLL_OUT,
        MouseEvent.ROLL_OVER
    )

    _TOUCH_CHANGES = (
        TouchEvent.TOUCH_OUT,
        TouchEvent.TOUCH_OVER,
        TouchEvent.TOUCH_ROLL_OUT,
        TouchEvent.TOUCH_ROLL_OVER
    )

    _S_CLICK_EVENTS = (
        MouseEvent.CLICK,
        MouseEvent.MIDDLE_CLICK,
        MouseEvent.RIGHT_CLICK
    )

    _S_DOWN_EVENTS = (
        MouseEvent.MOUSE_DOWN,
        MouseEvent.MIDDLE_MOUSE_DOWN,
        MouseEvent.RIGHT_MOUSE_DOWN
    )

    _S_UP_EVENTS = (
        MouseEvent.MOUSE_UP,
        MouseEvent.MIDDLE_MOUSE_UP,
        MouseEvent.RIGHT_MOUSE_UP
    )

    _EARLY_WAKE_UP = 0.005

#private class variables
    _current_stage = None

#private methods
    @classmethod
    def _get_instance(cls):
        if not cls._current_stage:
            cls._current_stage = cls()
        return cls._current_stage

    def _native_init(self):
        _core._Stage.__init__(self)

    def __init__(self):
        DisplayObjectContainer.__init__(self, "Stage")
        _core._set_event_handler(self._process_stage_event)

        self._mouse_over_objects = []
        self._focus_over_objects = []
        self.active = True

        self._invalid = False
        self._last_render = 0.0
        self._last_down = [None, None, None]
        self._last_click_time = 0.0
        self._touch_info = {}
        self._joy_axis_data = {}
        self._drag_bounds = None
        self._frame_rate = 0
        self._frame_period = 0

        self._drag_object = None
        self._drag_offset_x = 0.0
        self._drag_offset_y = 0.0

        self.frameRate = 100

        if _core._request_render:
            _core._request_render()

        self._event_map = {
            _core.etKeyDown:
                lambda event:
                    self._on_key(event, KeyboardEvent.KEY_DOWN),

            _core.etKeyUp:
                lambda event:
                    self._on_key(event, KeyboardEvent.KEY_UP),

            _core.etMouseMove:
                lambda event:
                    self._on_mouse(event, MouseEvent.MOUSE_MOVE, True),

            _core.etMouseDown:
                lambda event:
                    self._on_mouse(event, MouseEvent.MOUSE_DOWN, True),

            _core.etMouseUp:
                lambda event:
                    self._on_mouse(event, MouseEvent.MOUSE_UP, True),

            _core.etMouseClick:
                lambda event:
                    self._on_mouse(event, MouseEvent.CLICK, True),

            _core.etResize:
                lambda event:
                    self._on_resize(),

            _core.etPoll:
                lambda event:
                    self._poll_timers(),

            _core.etQuit:
                lambda event:
                    self._on_quit(),

            _core.etFocus:
                self._on_focus,

            _core.etShouldRotate:
                self._should_rotate,

            _core.etDestroyHandler:
                lambda event: None,

            _core.etRedraw:
                lambda event:
                    self._render(True),

            _core.etTouchBegin:
                self._on_touch_begin,

            _core.etTouchMove:
                self._on_touch_move,

            _core.etTouchEnd:
                self._on_touch_end,

            _core.etChange:
                self._on_change,

            _core.etActivate:
                lambda event:
                    self._set_active(True),

            _core.etDeactivate:
                lambda event:
                    self._set_active(False),

            _core.etGotInputFocus:
                lambda event:
                    self._on_got_input_focus(),

            _core.etLostInputFocus:
                lambda event:
                    self._on_lost_input_focus(),

            _core.etJoyAxisMove:
                lambda event:
                    self._on_joystick(event, 0),

            _core.etJoyBallMove:
                lambda event:
                    self._on_joystick(event, 0),

            _core.etJoyHatMove:
                lambda event:
                    self._on_joystick(event, 0),

            _core.etJoyButtonDown:
                lambda event:
                    self._on_joystick(event, 0),

            _core.etJoyButtonUp:
                lambda event:
                    self._on_joystick(event, 0),
        }

    def _process_stage_event(self, event):
        self._event_map[event.type](event)
        self._update_next_wake()

    def _check_render(self):
        if self.frameRate > 0:
            now = time.time()
            if now >= (self._last_render + self._frame_period):
                self._last_render = now

                if _core._request_render:
                    _core._request_render()
                else:
                    self._render(True)

    def _render(self, send_enterframe):
        if not self.active:
            return
        if send_enterframe:
            self._broadcast(Event(Event.ENTER_FRAME))
        if self._invalid:
            self._invalid = False
            self._broadcast(Event(Event.RENDER))
        self._render_stage()

    def _on_quit(self):
        flappy.stop()

    def _on_key(self, event, etype):
        stack = []
        obj = self._find_by_id(event.id)
        if obj is not None:
            obj._get_interactive_object_stack(stack)

        if stack:
            value = event.value
            if ord('a') <= value <= ord('z'):
                value -= (ord('a') - ord('A'))

            obj = stack[0]
            flags = event.flags
            key_location = 1 if (flags & self._EF_LOCATION_RIGHT ) else 0
            ctrl_down = (flags & self._EF_CTRL_DOWN) != 0
            alt_down = (flags & self._EF_ALT_DOWN) != 0
            shift_down = (flags & self._EF_SHIFT_DOWN) != 0

            evt = KeyboardEvent(etype,
                bubbles=True, cancelable=True, charCodeValue=event.code,
                    keyCodeValue=value, keyLocationValue=key_location,
                        ctrlKeyValue=ctrl_down, altKeyValue=alt_down,
                            shiftKeyValue=shift_down)
            obj._fire_event(evt)

    def _on_change(self, event):
        obj = self._find_by_id(event.id)
        if obj is not None:
            obj._fire_event(Event(Event.CHANGE))

    def _on_got_input_focus(self):
        evt = Event(FocusEvent.FOCUS_IN)
        self._dispatch_event(evt)

    def _on_lost_input_focus(self):
        evt = Event(FocusEvent.FOCUS_OUT)
        self._dispatch_event(evt)

    def _on_focus(self, event):
        stack = []
        obj = self._find_by_id(event.id)

        if obj is not None:
            obj._get_interactive_object_stack(stack)

        if stack and (event.value == 1 or event.value == 2):
            obj = stack[0]
            if event.value == 1:
                etype = FocusEvent.MOUSE_FOCUS_CHANGE
            else:
                etype = FocusEvent.KEY_FOCUS_CHANGE
            relobj = None
            if self._focus_over_objects:
                relobj = self._focus_over_objects[0]

            evt = FocusEvent(etype,
                    bubbles=True, cancelable=True, relatedObject=relobj,
                        shiftKey=(event.flags > 0), keyCode=event.code)
            obj._fire_event(evt)
            if evt.isCancelled:
                event.result = 1

        stack.reverse()
        self._checkFocusInOuts(event, stack)

    def _checkFocusInOuts(self, event, stack):
        new_n = len(stack)
        new_obj = stack[-1] if stack else None
        old_n = len(self._focus_over_objects)
        if self._focus_over_objects:
            old_obj = self._focus_over_objects[-1]
        else:
            old_obj = None

        if new_obj != old_obj:
            common = 0
            while (common < new_n) and \
                    (common < old_n) and \
                        (stack[common] == self._focus_over_objects[common]):
                common += 1

            fout = FocusEvent(FocusEvent.FOCUS_OUT,
                        bubbles=False, cancelable=False, relatedObject=new_obj,
                            shiftKey=(event.flags > 0), keyCode=event.code)
            i = old_n - 1
            while i >= common:
                self._focus_over_objects[i]._dispatch_event(fout)
                i -= 1

            fin = FocusEvent(FocusEvent.FOCUS_IN,
                        bubbles=False, cancelable=False, relatedObject=old_obj,
                            shiftKey=(event.flags > 0), keyCode=event.code)
            i = new_n - 1
            while i >= common:
                stack[i]._dispatch_event(fin)
                i -= 1

            self._focus_over_objects = stack


    def _on_mouse(self, event, event_type, from_mouse):
        etype = event_type
        button = event.value
        if not from_mouse:
            button = 0

        wheel = 0
        if event_type == MouseEvent.MOUSE_DOWN:
            if button > 2:
                return
            etype = Stage._S_DOWN_EVENTS[button]

        elif event_type == MouseEvent.MOUSE_UP:
            if button > 2:
                etype = MouseEvent.MOUSE_WHEEL
                wheel = 1 if button == 3 else -1
            else:
                etype = Stage._S_UP_EVENTS[button]

        if self._drag_object != None:
            self._drag(Point(event.x, event.y))

        stack = []
        obj = self._find_by_id(event.id)
        if obj is not None:
            obj._get_interactive_object_stack(stack)

        local = None
        if stack:
            obj = stack[0]
            stack.reverse()
            local = obj.globalToLocal(Point(event.x, event.y))
            evt = MouseEvent._create(etype, event, local, obj)
            evt.delta = wheel
            if from_mouse:
                self._check_in_outs(evt, stack)
            obj._fire_event(evt)
        else:
            local = Point(event.x, event.y)
            evt = MouseEvent._create(etype, event, local, None)
            evt.delta = wheel
            if from_mouse:
                self._check_in_outs(evt, stack)

        click_obj = stack[-1] if len(stack) else self
        if event_type == MouseEvent.MOUSE_DOWN and button < 3:
            self._last_down[button] = click_obj

        elif event_type == MouseEvent.MOUSE_UP and button < 3:
            if click_obj == self._last_down[button]:
                evt = MouseEvent._create(Stage._S_CLICK_EVENTS[button],
                                            event, local, click_obj)
                click_obj._fire_event(evt)
                if button == 0 and click_obj.doubleClickEnabled:
                    now = time.time()
                    diff = now - self._last_click_time
                    if diff <= self.DOUBLE_CLICK_INTERVAL:
                        evt = MouseEvent._create(MouseEvent.DOUBLE_CLICK,
                                                    event, local, click_obj)
                        click_obj._fire_event(evt)
                    self._last_click_time = now

            self._last_down[button] = None


    def _check_in_outs(self, event, stack, touch_info=None):
        if touch_info is not None:
            prev = touch_info.touchOverObjects
            mevents = self._TOUCH_CHANGES
        else:
            prev = self._mouse_over_objects
            mevents = self._MOUSE_CHANGES

        new_n = len(stack)
        new_obj = stack[-1] if new_n else None
        old_n = len(prev)
        old_obj = prev[-1] if old_n else None

        if new_obj != old_obj:
            if old_obj is not None:
                nevent = event._create_similar(mevents[0], new_obj, old_obj)
                old_obj._fire_event(nevent)
            if new_obj != None:
                nevent = event._create_similar(mevents[1], old_obj)
                new_obj._fire_event(nevent)

            common = 0
            while (common < new_n) and \
                    (common < old_n) and \
                        (stack[common] == prev[common]):
                common += 1

            nevent = event._create_similar(mevents[2], new_obj, old_obj)
            i = old_n - 1
            while i >= common:
                prev[i]._dispatch_event(nevent)
                i -= 1

            nevent = event._create_similar(mevents[3], old_obj)
            i = new_n - 1
            while i >= common:
                stack[i]._dispatch_event(nevent)
                i -= 1

            if touch_info:
                touch_info.touchOverObjects = stack
            else:
                self._mouse_over_objects = stack

    def _on_touch_begin(self, event):
        touch_info = _TouchInfo()
        self._touch_info[event.value] = touch_info
        self._on_touch(event, TouchEvent.TOUCH_BEGIN, touch_info)

        if event.flags & TouchEvent.efPrimaryTouch:
            self._on_mouse(event, MouseEvent.MOUSE_DOWN, False)

    def _on_touch_move(self, event):
        touch_info = self._touch_info[event.value]
        self._on_touch(event, TouchEvent.TOUCH_MOVE, touch_info)

    def _on_touch_end(self, event):
        touch_info = self._touch_info[event.value]
        self._on_touch(event, TouchEvent.TOUCH_END, touch_info)
        del self._touch_info[event.value]

        if event.flags & TouchEvent.efPrimaryTouch:
            self._on_mouse(event, MouseEvent.MOUSE_UP, False)

    def _on_touch(self, event, etype, touch_info):
        stack = []

        obj = self._find_by_id(event.id)

        if obj is not None:
            obj._get_interactive_object_stack(stack)

        if stack:
            obj = stack[0]
            stack.reverse()
            local = obj.globalToLocal(Point(event.x, event.y))
            evt = TouchEvent._create(etype, event, local, obj,
                                        event.scaleX, event.scaleY)
            evt.touchPointID = event.value
            evt.isPrimaryTouchPoint = \
                                bool(event.flags & TouchEvent.efPrimaryTouch)
            self._check_in_outs(evt, stack, touch_info)
            obj._fire_event(evt)

            if evt.isPrimaryTouchPoint and etype == TouchEvent.TOUCH_MOVE:
                if self._drag_object:
                    self._drag(Point(event.x, event.y))
                evt = MouseEvent._create(MouseEvent.MOUSE_MOVE, event,
                                            local, obj)
                obj._fire_event(evt)
        else:
            evt = TouchEvent._create(etype, event, Point(event.x, event.y),
                                        None, event.scaleX, event.scaleY)
            evt.touchPointID = event.value
            evt.isPrimaryTouchPoint = \
                                bool(event.flags & TouchEvent.efPrimaryTouch)
            self._check_in_outs(evt, stack, touch_info)

    def _drag(self, mouse):
        parent = self._drag_object.parent
        if parent is not None:
            mouse = parent.globalToLocal(mouse)

        dragobj_x = mouse.x - self._drag_offset_x
        dragobj_y = mouse.y - self._drag_offset_y

        if self._drag_bounds:
            if dragobj_x < self._drag_bounds.x:
                dragobj_x = self._drag_bounds.x
            elif dragobj_x > self._drag_bounds.right:
                dragobj_x = self._drag_bounds.right

            if dragobj_y < self._drag_bounds.y:
                dragobj_y = self._drag_bounds.y
            elif dragobj_y > self._drag_bounds.bottom:
                dragobj_y = self._drag_bounds.bottom

        self._drag_object.x = dragobj_x
        self._drag_object.y = dragobj_y

    def _on_joystick(self, event, event_type):
#TODO: joystick handler
        pass

    def _should_rotate(self, event):
#TODO: 'should rotate' handler 
        pass
    
    def _start_drag(self, obj, lock_center, bounds):
        self._drag_bounds = None
        if bounds:
            self._drag_bounds = bounds.clone()

        self._drag_object = obj

        if lock_center:
            self._drag_offset_x = -obj.width * 0.5
            self._drag_offset_y = -obj.height * 0.5
        else:
            mouse = Point(self.mouseX, self.mouseY)
            parent = self._drag_object.parent
            if parent is not None:
                mouse = parent.globalToLocal(mouse)
            self._drag_offset_x = self._drag_object.x - mouse.x
            self._drag_offset_y = self._drag_object.y - mouse.y


    def _stop_drag(self, obj):
        self._drag_bounds = None
        self._drag_object = None

    def _on_resize(self):
        event = Event(Event.RESIZE)
        self._broadcast(event)

        if _core._request_render is None:
            self._render(False)

    def _poll_timers(self):
        self._check_render()

    def _set_active(self, active):
        if active != self.active:
            self.active = active
            if not active:
                self._last_render = time.time()

            event = Event(Event.ACTIVATE if active else Event.DEACTIVATE)
            self._broadcast(event)
            if active:
                self._poll_timers()

    def _update_next_wake(self):
        next_wake = self._next_frame_due(60.0)
        self._set_next_wake_delay(next_wake)

    def _next_frame_due(self, other_timers):
        if not self.active:
            return other_timers

        if self.frameRate > 0:
            next = self._last_render - time.time()
            next += (self._frame_period - Stage._EARLY_WAKE_UP)
            if next < other_timers:
                return next

        return other_timers


class _TouchInfo(object):
    def __init__(self):
        self.touchOverObjects = []