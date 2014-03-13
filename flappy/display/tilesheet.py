# encoding: utf-8

from flappy import _core
from flappy._core import _Tilesheet

class Tilesheet(_Tilesheet):

    TILE_SCALE          = 0x0001
    TILE_ROTATION       = 0x0002
    TILE_RGB            = 0x0004
    TILE_ALPHA          = 0x0008
    TILE_TRANS_2x2      = 0x0010
    TILE_SMOOTH         = 0x1000
    TILE_BLEND_ADD      = 0x10000
    TILE_BLEND_MASK     = 0xf0000

    def __init__(self, bitmap_data):
        self._bitmap_data = bitmap_data
        _Tilesheet.__init__(self, bitmap_data)

    def addTileRect(self, rect, center_point=None):
        _Tilesheet.addTileRect(self, rect, center_point)

    def drawTiles(self, graphics_obj, tile_data, flags=0):
        graphics_obj.drawTiles(self, tile_data, flags)
