from pyo import *


class Phaser(PyoObject):
    def __init__(self, input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0):
        pyoArgsAssert(self, "oOOOOO", input, depth, feedback, bal, mul, add)
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._depth = depth
        self._feedback = feedback
        self._bal = bal
        self._in_fader = InputFader(input)
        in_fader, depth, feedback, bal, mul, add, lmax = convertArgsToLists(
            self._in_fader, depth, feedback, bal, mul, add
        )
        self._base_objs = [
            Phaser_base(
                wrap(in_fader, i),
                wrap(depth, i),
                wrap(feedback, i),
                wrap(bal, i),
                wrap(mul, i),
                wrap(add, i),
            )
            for i in range(lmax)
        ]
        self._init_play()
