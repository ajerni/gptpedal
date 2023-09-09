from pyo import *


def fxChain(input, selections):
    # interp=1 means ON, interp=0 means bypass
    fx1 = Disto(
        input,
        drive=selections["disto"]["drive"] or 0.75,
        slope=selections["disto"]["slope"] or 0.5,
        mul=selections["disto"]["mul"] or 1,
        add=selections["disto"]["add"] or 0,
    )
    fx1_out = Interp(input, fx1, interp=selections["disto"]["use"] or 0)
    if selections["disto"]["use"] == 1:
        fx1.ctrl(title="Distortion")

    fx2 = Delay(
        fx1_out,
        delay=selections["delay"]["delay"] or 0.25,
        feedback=selections["delay"]["feedback"] or 0,
        maxdelay=selections["delay"]["maxdelay"] or 1,
        mul=selections["delay"]["mul"] or 1,
        add=selections["delay"]["add"] or 0,
    )
    fx2_out = Interp(fx1_out, fx2, interp=selections["delay"]["use"])
    if selections["delay"]["use"] == 1:
        fx2.ctrl(title="Delay")

    fx3 = SDelay(
        fx2_out,
        delay=selections["sdelay"]["delay"] or 0.25,
        maxdelay=selections["sdelay"]["maxdelay"] or 1,
        mul=selections["sdelay"]["mul"] or 1,
        add=selections["sdelay"]["add"] or 0,
    )
    fx3_out = Interp(fx2_out, fx3, interp=selections["sdelay"]["use"])
    if selections["sdelay"]["use"] == 1:
        fx3.ctrl(title="SDelay")

    fx4 = Waveguide(
        fx3_out,
        freq=selections["waveguide"]["freq"] or 100,
        dur=selections["waveguide"]["dur"] or 10,
        minfreq=selections["waveguide"]["minfreq"] or 20,
        mul=selections["waveguide"]["mul"] or 1,
        add=selections["waveguide"]["add"] or 0,
    )
    fx4_out = Interp(fx3_out, fx4, interp=selections["waveguide"]["use"])
    if selections["waveguide"]["use"] == 1:
        fx4.ctrl(title="Waveguide")

    fx5 = AllpassWG(
        fx4_out,
        freq=selections["allpass"]["freq"] or 100,
        feed=selections["allpass"]["feed"] or 0.95,
        detune=selections["allpass"]["detune"] or 0.5,
        minfreq=selections["allpass"]["minfreq"] or 20,
        mul=selections["allpass"]["mul"] or 1,
        add=selections["allpass"]["add"] or 0,
    )
    fx5_out = Interp(fx4_out, fx5, interp=selections["allpass"]["use"])
    if selections["allpass"]["use"] == 1:
        fx5.ctrl(title="Allpass")

    fx6 = Freeverb(
        fx5_out,
        size=selections["freeverb"]["size"] or 0.5,
        damp=selections["freeverb"]["damp"] or 0.5,
        bal=selections["freeverb"]["bal"] or 0.5,
        mul=selections["freeverb"]["mul"] or 1,
        add=selections["freeverb"]["add"] or 0,
    )
    fx6_out = Interp(fx5_out, fx6, interp=selections["freeverb"]["use"])
    if selections["freeverb"]["use"] == 1:
        fx6.ctrl(title="Freeverb")

    fx7 = WGVerb(
        fx6_out,
        feedback=selections["monoreverb"]["feedback"] or 0.5,
        cutoff=selections["monoreverb"]["cutoff"] or 5000,
        bal=selections["monoreverb"]["bal"] or 0.5,
        mul=selections["monoreverb"]["mul"] or 1,
        add=selections["monoreverb"]["add"] or 0,
    )
    fx7_out = Interp(fx6_out, fx7, interp=selections["monoreverb"]["use"])
    if selections["monoreverb"]["use"] == 1:
        fx7.ctrl(title="Mono Reverb")

    fx8 = Chorus(
        fx7_out,
        depth=selections["chorus"]["depth"] or 1,
        feedback=selections["chorus"]["feedback"] or 0.25,
        bal=selections["chorus"]["bal"] or 0.5,
        mul=selections["chorus"]["mul"] or 1,
        add=selections["chorus"]["add"] or 0,
    )
    fx8_out = Interp(fx7_out, fx8, interp=selections["chorus"]["use"])
    if selections["chorus"]["use"] == 1:
        fx8.ctrl(title="Chorus")

    fx9 = Harmonizer(
        fx8_out,
        transpo=selections["harmonizer"]["transpo"] or -7.0,
        feedback=selections["harmonizer"]["feedback"] or 0,
        winsize=selections["harmonizer"]["winsize"] or 0.1,
        mul=selections["harmonizer"]["mul"] or 1,
        add=selections["harmonizer"]["add"] or 0,
    )
    fx9_out = Interp(fx8_out, fx9, interp=selections["harmonizer"]["use"])
    if selections["harmonizer"]["use"] == 1:
        fx9.ctrl(title="Harmonizer")

    fx10 = Delay1(
        fx9_out,
        mul=selections["simpledelay"]["mul"] or 1,
        add=selections["simpledelay"]["add"] or 0,
    )
    fx10_out = Interp(fx9_out, fx10, interp=selections["simpledelay"]["use"])
    if selections["simpledelay"]["use"] == 1:
        fx10.ctrl(title="Delay 1")

    fx11 = STRev(
        fx10_out,
        inpos=selections["stereoreverb"]["inpos"] or 0.5,
        revtime=selections["stereoreverb"]["revtime"] or 1,
        cutoff=selections["stereoreverb"]["cutoff"] or 5000,
        bal=selections["stereoreverb"]["bal"] or 0.5,
        roomSize=selections["stereoreverb"]["roomSize"] or 1,
        firstRefGain=selections["stereoreverb"]["firstRefGain"] or -3,
        mul=selections["stereoreverb"]["mul"] or 1,
        add=selections["stereoreverb"]["add"] or 0,
    )
    fx11_out = Interp(fx10_out, fx11, interp=selections["stereoreverb"]["use"])
    if selections["stereoreverb"]["use"] == 1:
        fx11.ctrl(title="Stereo Reverb")

    fx12 = SmoothDelay(
        fx11_out,
        delay=selections["smoothdelay"]["delay"] or 0.25,
        feedback=selections["smoothdelay"]["feedback"] or 0,
        crossfade=selections["smoothdelay"]["crossfade"] or 0.05,
        maxdelay=selections["smoothdelay"]["maxdelay"] or 1,
        mul=selections["smoothdelay"]["mul"] or 1,
        add=selections["smoothdelay"]["add"] or 0,
    )
    fx12_out = Interp(fx11_out, fx12, interp=selections["smoothdelay"]["use"])
    if selections["smoothdelay"]["use"] == 1:
        fx12.ctrl(title="Smooth Delay")

    fx13 = FreqShift(
        fx12_out,
        shift=selections["freqshift"]["shift"] or 100,
        mul=selections["freqshift"]["mul"] or 1,
        add=selections["freqshift"]["add"] or 0,
    )
    fx13_out = Interp(fx12_out, fx13, interp=selections["freqshift"]["use"])
    if selections["freqshift"]["use"] == 1:
        fx13.ctrl(title="Frequency Shifter")

    # and so on...

    return fx13_out
