from pyo import *


def fxChain(input, selections):
    # interp=1 means ON, interp=0 means bypass
    fx1 = Disto(
        input,
        drive=selections["disto"]["drive"],
        slope=selections["disto"]["slope"],
        mul=selections["disto"]["mul"],
        add=selections["disto"]["add"],
    )
    fx1_out = Interp(input, fx1, interp=selections["disto"]["use"])
    if selections["disto"]["use"] == 1:
        fx1.ctrl(title="Distortion")

    fx2 = Delay(
        fx1_out,
        delay=selections["delay"]["delay"],
        feedback=selections["delay"]["feedback"],
        maxdelay=selections["delay"]["maxdelay"],
        mul=selections["delay"]["mul"],
        add=selections["delay"]["add"],
    )
    fx2_out = Interp(fx1_out, fx2, interp=selections["delay"]["use"])
    if selections["delay"]["use"] == 1:
        fx2.ctrl(title="Delay")

    fx3 = SDelay(
        fx2_out,
        delay=selections["sdelay"]["delay"],
        maxdelay=selections["sdelay"]["maxdelay"],
        mul=selections["sdelay"]["mul"],
        add=selections["sdelay"]["add"],
    )
    fx3_out = Interp(fx2_out, fx3, interp=selections["sdelay"]["use"])
    if selections["sdelay"]["use"] == 1:
        fx3.ctrl(title="Delay")

    # fx4 = STRev(fx3_out)
    # fx4_out = Interp(fx3_out, fx4, interp=selections["stereo"])
    # fx4.ctrl(title="Stereo Reverb")

    # fx5 = Waveguide(fx4_out)
    # fx5_out = Interp(fx4_out, fx5, interp=selections["wave"])
    # fx5.ctrl(title="Waveguide")

    # and so on...

    return fx3_out


if __name__ == "__main__":
    s = Server(buffersize=128, audio="coreaudio").boot()
    s.start()

    # call GPT/langchain to create an own effect - add it to the list of effects
    # based on the classes in effetcs.txt like Delay(PyoObject): etc. create a new class GPTEffect(PyoObject): which
    # does blalba ...propt engineere with system and human + ev.  AI for mulitshot

    # --> or just enter all availabel onse into the chain and get GPT to set the 0 and 1 right for the asked sound...

    # GptClass = output from langchain

    # when class is ready triiger fxChain...

    input = Input()
    output = fxChain(
        input,
        {
            "disto": {"use": 0, "drive": 0.75, "slope": 0.5, "mul": 1, "add": 0},
            "delay": {
                "use": 1,
                "delay": 0.25,
                "feedback": 0,
                "maxdelay": 1,
                "mul": 1,
                "add": 0,
            },
            "sdelay": {"use": 1, "delay": 0.25, "maxdelay": 1, "mul": 1, "add": 0},
        },
    )
    stereo = output.mix(2).out()
    s.gui(locals())
