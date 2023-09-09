from pyo import *
from aifunctions import generateEffect
from fxchain import fxChain
import ast
from presets import presets


def getGPTeffect(q):
    sel_dict_string = generateEffect(q)
    sel_dict = ast.literal_eval(sel_dict_string)
    print(sel_dict)
    startServer(sel_dict)


def getPresetEffect(p):
    sel_dict = p
    startServer(sel_dict)


def startServer(sel_dict):
    s = Server(buffersize=128, audio="coreaudio").boot()
    s.start()
    input = Input()
    output = fxChain(
        input,
        sel_dict,
    )
    stereo = output.mix(2).out()
    stereo.ctrl(title="Stereo Output")
    s.gui(locals())


if __name__ == "__main__":
    q = "A hard distortion with phaser effect"
    getGPTeffect(q)

    # p = presets.DOPPELVERB
    # getPresetEffect(p)
