from pyo import *
from aifunctions import generateEffect
from fxchain import fxChain
import ast
from presets import presets


sel_dict = {}


def getGPTeffect(q):
    sel_dict_string = generateEffect(q)

    sel_dict = ast.literal_eval(sel_dict_string)
    print(sel_dict)


if __name__ == "__main__":
    # q = "A chorus and a reverb"
    # getGPTeffect(q)

    sel_dict = presets.CHORUS

    if sel_dict is not None:
        s = Server(buffersize=128, audio="coreaudio").boot()
        s.start()
        input = Input()
        output = fxChain(
            input,
            sel_dict,
        )
        stereo = output.mix(2).out()
        s.gui(locals())
