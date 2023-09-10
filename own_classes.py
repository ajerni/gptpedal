from pyo import *


# AI created / experimental...


class Phaser(PyoObject):
    def __init__(self, input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0):
        pyoArgsAssert(self, "oOOOOO", input, depth, feedback, bal, mul, add)
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._depth = depth
        self._feedback = feedback
        self._bal = bal
        in_fader, depth, feedback, bal, mul, add, lmax = convertArgsToLists(
            self._input, depth, feedback, bal, mul, add
        )
        self._base_objs = [
            Phaser_base(
                wrap(self._input, i),
                wrap(depth, i),
                wrap(feedback, i),
                wrap(bal, i),
                wrap(mul, i),
                wrap(add, i),
            )
            for i in range(lmax)
        ]
        self._init_play()

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [
            SLMap(0.0, 1.0, "lin", "depth", self._depth),
            SLMap(0.0, 1.0, "lin", "feedback", self._feedback),
            SLMap(0.0, 1.0, "lin", "bal", self._bal),
            SLMapMul(self._mul),
        ]
        PyoObject.ctrl(self, map_list, title, wxnoserver)
