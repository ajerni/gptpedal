from pyo import *
from aifunctions import generateEffect

# from aifunctions import createNewClass
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
    # q = "A shimmery stereo reverb with a 300ms tail."
    # getGPTeffect(q)

    p = presets.CHORUS
    getPresetEffect(p)

    # experimental to create whole new pyo classes
    #
    #  - move output to own_classes.py
    #  - add it to the presets.py file
    #  - add it to the sel_defaults_values.txt
    #  - add it to the fxchain.py file
    #
    # class_name = "Phaser"
    # createNewClass(
    #     f"You are Python expert using the pyo library to create sound effects. Based on how the extisting classes work, create a new class {class_name}(PyoObject): that creates a {class_name} effect."
    # )
