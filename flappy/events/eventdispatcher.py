# encoding: utf-8

import weakref
import types
from event import Event, EventPhase


class EventDispatcher(object):

    def __init__(self, target=None):
        self.target = weakref.proxy(self) if target == None else target
        self.eventMap = {}
        self.suspended = False

    def addEventListener(self, etype, listener, 
                            use_capture=False, priority=0, 
                                use_weak_reference=False, once=False):
        if not etype in self.eventMap:
            self.eventMap[etype] = []
        
        lref = None
        if use_weak_reference:
            lref = _CallbackProxy(listener)
        else:
            lref = listener
        self.eventMap[etype].append(
                        Listener(lref, use_capture, priority, once))

    def dispatchEvent(self, e):
        if self.suspended:
            return False
        if not self.eventMap or not (e.type in self.eventMap):
            return False

        if e.target == None:
            e.target = self.target

        if e.currentTarget == None:
            e.currentTarget = self.target

        capture = e.eventPhase == EventPhase.CAPTURING_PHASE
        lst = self.eventMap[e.type]
        idx = 0
        if len(lst):
            while idx < len(lst):
                it = lst[idx]
                if it == None:
                    del lst[idx]
                else:
                    if it.usecapture == capture:
                        if it.once:
                            lst[idx] = None
                        it.dispatchEvent(e)
                        if e.isCancelledNow:
                            return True
                    idx += 1
            return True
        return False

    def hasEventListener(self, etype, listener=None, use_capture=False):
        if not etype in self.eventMap:
            return False
        for it in self.eventMap[etype]:
            if listener:
                if it and it.isSimilar(listener, use_capture):
                    return True
            else:
                if it:
                    return True
        return False

    def removeEventListener(self, etype, listener, use_capture=False):
        if not etype in self.eventMap:
            return
        lst = self.eventMap[etype]
        for i, it in enumerate(lst):
            if it and it.isSimilar(listener, use_capture):
                lst[i] = None
                return

    def willTrigger(self, etype):
        return etype in self.eventMap

    def clear(self):
        for tp in self.eventMap:
            if self.eventMap[tp]: 
                del self.eventMap[tp][:]
        self.eventMap.clear()


class Listener(object):
    _IDS = 1

    def __init__(self, listener, usecapture, priority, once=False):
        self.listener = listener
        self.usecapture = usecapture
        self.priority = priority
        self.once = once
        self.id = Listener._IDS
        Listener._IDS += 1


    def dispatchEvent(self, e):
        self.listener(e)

    def isSimilar(self, listener, usecapture):
        return self.listener == listener and self.usecapture == usecapture


class _CallbackProxy(object):

    def __init__(self, cb):
        try:
            self._cb =  cb
            try:
                self.inst = weakref.ref(cb.im_self)
            except TypeError:
                self.inst = None
            self.func = cb.im_func
            self.cls = cb.im_class
        except AttributeError:
            self.inst = None
            self.func = cb.im_func
            self.cls = None


    def __call__(self, *args, **kwargs):
        if self.inst is not None and self.inst() is None:
            raise ReferenceError
        elif self.inst is not None:
            meth = types.MethodType(self.func, self.inst(), self.cls)
        else:
            meth = self.func
        return meth(*args, **kwargs)

    def __eq__(self, other):
        try:
            return self.func == other.func and self.inst() == other.inst()
        except Exception:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)