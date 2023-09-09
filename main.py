from pyo import *
from aifunctions import generateEffect, createNewClass
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
    # q = "A hard distortion fed into long delay"
    # getGPTeffect(q)

    p = presets.DOPPELVERB
    getPresetEffect(p)

    # class_name = "Phaser"
    # createNewClass(
    #     f"You are Python expert using the pyo library to create sound effects. Based on how the extisting classes work, create a new class {class_name}(PyoObject): that creates a {class_name} effect."
    # )
