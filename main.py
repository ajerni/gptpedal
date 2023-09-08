from pyo import *
from aifunctions import generateEffect
from fxchain import fxChain
import ast

if __name__ == "__main__":
    # call GPT/langchain to fill the selections dictonary as per result of the prompt q
    # TODO: get this q string form any input (like mic on rapi)
    q = "A distortion with low drive"  # example "A short delay" works
    sel_dict_string = generateEffect(q)

    # Convert string to dictionary / this is what GPT generated and is passed to fxChain
    sel_dict_dict = ast.literal_eval(sel_dict_string)
    print(sel_dict_dict)

    if sel_dict_dict is not None:
        s = Server(buffersize=128, audio="coreaudio").boot()
        s.start()
        input = Input()
        output = fxChain(input, sel_dict_dict)
        stereo = output.mix(2).out()
        s.gui(locals())
