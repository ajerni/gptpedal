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
        fx3.ctrl(title="SDelay")

    fx4 = Waveguide(
        fx3_out,
        freq=selections["waveguide"]["freq"],
        dur=selections["waveguide"]["dur"],
        minfreq=selections["waveguide"]["minfreq"],
        mul=selections["waveguide"]["mul"],
        add=selections["waveguide"]["add"],
    )
    fx4_out = Interp(fx3_out, fx4, interp=selections["waveguide"]["use"])
    if selections["waveguide"]["use"] == 1:
        fx4.ctrl(title="Waveguide")

    fx5 = AllpassWG(
        fx4_out,
        freq=selections["allpass"]["freq"],
        feed=selections["allpass"]["feed"],
        detune=selections["allpass"]["detune"],
        minfreq=selections["allpass"]["minfreq"],
        mul=selections["allpass"]["mul"],
        add=selections["allpass"]["add"],
    )
    fx5_out = Interp(fx4_out, fx5, interp=selections["allpass"]["use"])
    if selections["allpass"]["use"] == 1:
        fx5.ctrl(title="Allpass")

    fx6 = Freeverb(
        fx5_out,
        size=selections["freeverb"]["size"],
        damp=selections["freeverb"]["damp"],
        bal=selections["freeverb"]["bal"],
        mul=selections["freeverb"]["mul"],
        add=selections["freeverb"]["add"],
    )
    fx6_out = Interp(fx5_out, fx6, interp=selections["freeverb"]["use"])
    if selections["freeverb"]["use"] == 1:
        fx6.ctrl(title="Freeverb")

    # and so on...

    return fx6_out


if __name__ == "__main__":
    s = Server(buffersize=128, audio="coreaudio").boot()
    s.start()

    # call GPT/langchain to fill the selections dictonary as per result of the prompt using
    # the description stings in effects.py

    # then trigger fxChain...
    # sel_dict = {} // this is what GPT should generate and is passed to fxChain then...

    # gets the audio signal from the soundcard
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
            "waveguide": {
                "use": 0,
                "freq": 100,
                "dur": 10,
                "minfreq": 20,
                "mul": 1,
                "add": 0,
            },
            "allpass": {
                "use": 0,
                "freq": 100,
                "feed": 0.95,
                "detune": 0.5,
                "minfreq": 20,
                "mul": 1,
                "add": 0,
            },
            "freeverb": {
                "use": 1,
                "size": 0.5,
                "damp": 0.5,
                "bal": 0.5,
                "mul": 1,
                "add": 0,
            },
        },
    )
    stereo = output.mix(2).out()
    s.gui(locals())
