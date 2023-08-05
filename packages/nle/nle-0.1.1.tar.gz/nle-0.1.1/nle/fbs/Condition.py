# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Condition(object):
    __slots__ = ['_tab']

    # Condition
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Condition
    def STONE(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Condition
    def SLIME(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(1))
    # Condition
    def STRNGL(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(2))
    # Condition
    def FOODPOIS(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(3))
    # Condition
    def TERMILL(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Condition
    def BLIND(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(5))
    # Condition
    def DEAF(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(6))
    # Condition
    def STUN(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(7))
    # Condition
    def CONF(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # Condition
    def HALLU(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(9))
    # Condition
    def LEV(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(10))
    # Condition
    def FLY(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(11))
    # Condition
    def RIDE(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))

def CreateCondition(builder, STONE, SLIME, STRNGL, FOODPOIS, TERMILL, BLIND, DEAF, STUN, CONF, HALLU, LEV, FLY, RIDE):
    builder.Prep(1, 13)
    builder.PrependBool(RIDE)
    builder.PrependBool(FLY)
    builder.PrependBool(LEV)
    builder.PrependBool(HALLU)
    builder.PrependBool(CONF)
    builder.PrependBool(STUN)
    builder.PrependBool(DEAF)
    builder.PrependBool(BLIND)
    builder.PrependBool(TERMILL)
    builder.PrependBool(FOODPOIS)
    builder.PrependBool(STRNGL)
    builder.PrependBool(SLIME)
    builder.PrependBool(STONE)
    return builder.Offset()
