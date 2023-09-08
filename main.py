from pyo import *
from aifunctions import generateEffect
import ast


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

    fx7 = WGVerb(
        fx6_out,
        feedback=selections["monoreverb"]["feedback"],
        cutoff=selections["monoreverb"]["cutoff"],
        bal=selections["monoreverb"]["bal"],
        mul=selections["monoreverb"]["mul"],
        add=selections["monoreverb"]["add"],
    )
    fx7_out = Interp(fx6_out, fx7, interp=selections["monoreverb"]["use"])
    if selections["monoreverb"]["use"] == 1:
        fx7.ctrl(title="Mono Reverb")

    fx8 = Chorus(
        fx7_out,
        depth=selections["chorus"]["depth"],
        feedback=selections["chorus"]["feedback"],
        bal=selections["chorus"]["bal"],
        mul=selections["chorus"]["mul"],
        add=selections["chorus"]["add"],
    )
    fx8_out = Interp(fx7_out, fx8, interp=selections["chorus"]["use"])
    if selections["chorus"]["use"] == 1:
        fx8.ctrl(title="Chorus")

    fx9 = Harmonizer(
        fx8_out,
        transpo=selections["harmonizer"]["transpo"],
        feedback=selections["harmonizer"]["feedback"],
        winsize=selections["harmonizer"]["winsize"],
        mul=selections["harmonizer"]["mul"],
        add=selections["harmonizer"]["add"],
    )
    fx9_out = Interp(fx8_out, fx9, interp=selections["harmonizer"]["use"])
    if selections["harmonizer"]["use"] == 1:
        fx9.ctrl(title="Harmonizer")

    fx10 = Delay1(
        fx9_out,
        mul=selections["simpledelay"]["mul"],
        add=selections["simpledelay"]["add"],
    )
    fx10_out = Interp(fx9_out, fx10, interp=selections["simpledelay"]["use"])
    if selections["simpledelay"]["use"] == 1:
        fx10.ctrl(title="Delay 1")

    fx11 = STRev(
        fx10_out,
        inpos=selections["stereoreverb"]["inpos"],
        revtime=selections["stereoreverb"]["revtime"],
        cutoff=selections["stereoreverb"]["cutoff"],
        bal=selections["stereoreverb"]["bal"],
        roomSize=selections["stereoreverb"]["roomSize"],
        firstRefGain=selections["stereoreverb"]["firstRefGain"],
        mul=selections["stereoreverb"]["mul"],
        add=selections["stereoreverb"]["add"],
    )
    fx11_out = Interp(fx10_out, fx11, interp=selections["stereoreverb"]["use"])
    if selections["stereoreverb"]["use"] == 1:
        fx11.ctrl(title="Stereo Reverb")

    fx12 = SmoothDelay(
        fx11_out,
        delay=selections["smoothdelay"]["delay"],
        feedback=selections["smoothdelay"]["feedback"],
        crossfade=selections["smoothdelay"]["crossfade"],
        maxdelay=selections["smoothdelay"]["maxdelay"],
        mul=selections["smoothdelay"]["mul"],
        add=selections["smoothdelay"]["add"],
    )
    fx12_out = Interp(fx11_out, fx12, interp=selections["smoothdelay"]["use"])
    if selections["smoothdelay"]["use"] == 1:
        fx12.ctrl(title="Smooth Delay")

    fx13 = FreqShift(
        fx12_out,
        shift=selections["freqshift"]["shift"],
        mul=selections["freqshift"]["mul"],
        add=selections["freqshift"]["add"],
    )
    fx13_out = Interp(fx12_out, fx13, interp=selections["freqshift"]["use"])
    if selections["freqshift"]["use"] == 1:
        fx13.ctrl(title="Frequency Shifter")

    # and so on...

    return fx13_out


if __name__ == "__main__":
    # call GPT/langchain to fill the selections dictonary as per result of the prompt q
    # TODO: get this q string form any input (like mic on rapi)
    q = "A long delay"  # example "A short delay" works
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
