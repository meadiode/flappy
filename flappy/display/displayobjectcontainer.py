
from flappy.display import InteractiveObject
from flappy._core import _DisplayObjectContainer

class DisplayObjectContainer(_DisplayObjectContainer, InteractiveObject):

    def __init__(self, name=None):
        InteractiveObject.__init__(self, name)
        self._children = []

    def _native_init(self):
        _DisplayObjectContainer.__init__(self)

    def addChild(self, child):
        self._add_child(child)
        return child

    def addChildAt(self, child, index):
        self._add_child(child)
        self._set_child_index(child, index)
        return child

    def contains(self, child):
        if not child:
            return False

        if self == child:
            return True

        for c in self._children:
            if c == child:
                return True

        return False

    def __contains__(self, item):
        return self.contains(item)

    def getChildAt(self, index):
        if 0 <= index < len(self._children):
            return self._children[index]
        raise IndexError("Index is out of range")

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.getChildAt(key)
        raise IndexError("Index must be of integer type")

    def __len__(self):
        return self.numChildren

    def __bool__(self):
        return True    

    def __nonzero__(self):
        return True

    def __iter__(self):
        return _DOCIterator(self)

    def getChildByName(self, name):
        for c in self._children:
            if name == c.name:
                return c
        return None

    def getChildIndex(self, child):
        return self._get_child_index(child)

    def getObjectsUnderPoint(self, p):
        ret = []
        self._get_objects_under_point(p, ret)
        return ret

    def _add_child(self, child):
        if child == self:
            raise ValueError

        if child.parent == self:
            self._set_child_index(child, len(self._children) - 1)
        else:
            _DisplayObjectContainer.addChild(self, child)
            child._set_parent(self)
            self._children.append(child)

    def _broadcast(self, e):
        if self._children:
            chcopy = self._children[:]
            for c in chcopy:
                c._broadcast(e)
        InteractiveObject._broadcast(self, e)

    def _find_by_id(self, obj_id):
        ret = InteractiveObject._find_by_id(self, obj_id)
        if not ret:
            for c in self._children:
                ret = c._find_by_id(obj_id)
                if ret is not None:
                    break
        return ret

    def _get_child_index(self, child):
        for i, c in enumerate(self._children):
            if c == child:
                return i
        return -1

    def _get_objects_under_point(self, p, result):
        InteractiveObject._get_objects_under_point(self, p, result)
        for c in self._children:
            c._get_objects_under_point(p, result)

    def _on_added(self, obj, isonstage):
        InteractiveObject._on_added(self, obj, isonstage)
        for c in self._children:
            c._on_added(obj, isonstage)

    def _on_removed(self, obj, wasonstage):
        InteractiveObject._on_removed(self, obj, wasonstage)
        for c in self._children:
            c._on_removed(obj, wasonstage)

    def _remove_child_from_array(self, child):
        i = self._get_child_index(child)
        if i >= 0:
            _DisplayObjectContainer.removeChildAt(self, i)
            del self._children[i]

    def _set_child_index(self, child, index):
        if index > len(self._children):
            raise IndexError

        s = None
        orig = self._get_child_index(child)
        if orig < 0:
            raise ValueError

        _DisplayObjectContainer.setChildIndex(self, child, index)
        self._children.insert(index, self._children.pop(orig))

    def _swap_children_at(self, index1, index2):
        if (0 <= index1 < len(self._children)) and \
                (0 <= index2 < len(self._children)):
            if index1 != index2:
                children = self._children
                children[index1], children[index2] = \
                                        children[index2], children[index1]
                _DisplayObjectContainer.swapChildrenAt(self, index1, index2)
        else:
            raise IndexError

    def removeChild(self, child):
        if self._get_child_index(child) >= 0:
            child._set_parent(None)
            return child
        return None

    def removeChildAt(self, index):
        if 0 <= index < len(self._children):
            child = self._children[index]
            child._set_parent(None)
            return child
        raise IndexError

    def removeAllChildren(self):
        while self.numChildren:
            self.removeChildAt(self.numChildren - 1)

    def setChildIndex(self, child, index):
        self._set_child_index(child, index)

    def swapChildren(self, child1, child2):
        idx1 = self._get_child_index(child1)
        idx2 = self._get_child_index(child2)
        if idx1 < 0 or idx2 < 0:
            raise ValueError
        self._swap_children_at(idx1, idx2)

    def swapChildrenAt(self, index1, index2):
        self._swap_children_at(index1, index2)

    def clear(self):
        InteractiveObject.clear(self)
        self.removeAllChildren()        

    @property
    def mouseChildren(self):
        return self.getMouseChildren()

    @mouseChildren.setter
    def mouseChildren(self, value):
        self.setMouseChildren(value)

    @property
    def numChildren(self):
        return len(self._children)

class _DOCIterator(object):
    def __init__(self, obj):
        self.obj = obj
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        ret = None
        if self.index < self.obj.numChildren:
            ret = self.obj.getChildAt(self.index)
            self.index += 1
        else:
            raise StopIteration
        return ret