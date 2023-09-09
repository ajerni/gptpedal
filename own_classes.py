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

        # Create delay lines for each voice and mix them
        self._delay_lines = [
            Delay(in_fader[i], delay=0.001 + i * 0.001, feedback=feedback[i])
            for i in range(len(in_fader))
        ]
        self._mix = Mix(self._delay_lines, voices=len(in_fader))

        # Apply balance control
        self._phaser_output = self._mix * bal + self._in_fader * (1 - bal)

        self._init_play()

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [
            SLMap(0.0, 5.0, "lin", "depth", self._depth),
            SLMap(0.0, 1.0, "lin", "feedback", self._feedback),
            SLMap(0.0, 1.0, "lin", "bal", self._bal),
            SLMapMul(self._mul),
        ]
        PyoObject.ctrl(self, map_list, title, wxnoserver)
