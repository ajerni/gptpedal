from pyo import *


# AI created / does not work yet - experimental...
class Phaser(PyoObject):
    def __init__(self, input, depth=0.5, feedback=0.5, bal=0.5, mul=1, add=0):
        pyoArgsAssert(self, "oOOOOO", input, depth, feedback, bal, mul, add)
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._depth = depth
        self._feedback = feedback
        self._bal = bal
        self._in_fader = InputFader(input)

        # Convert input to a float
        self._in_fader = Sig(self._in_fader)

        # Create a single delay line
        self._delay_line = Delay(self._in_fader, delay=0.001, feedback=self._feedback)

        # Apply depth control
        self._phaser_output = Allpass(
            self._delay_line, delay=0.002 + self._depth * 0.01, feedback=-self._feedback
        )

        # Apply balance control
        self._phaser_output = self._phaser_output * self._bal + self._in_fader * (
            1 - self._bal
        )

        self._init_play()

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [
            SLMap(0.0, 1.0, "lin", "depth", self._depth),
            SLMap(0.0, 1.0, "lin", "feedback", self._feedback),
            SLMap(0.0, 1.0, "lin", "bal", self._bal),
            SLMapMul(self._mul),
        ]
        PyoObject.ctrl(self, map_list, title, wxnoserver)
