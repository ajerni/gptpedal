default_values = {
    "disto": {"use": 0, "drive": 0.75, "slope": 0.5, "mul": 1, "add": 0},
    "delay": {
        "use": 0,
        "delay": 0.25,
        "feedback": 0,
        "maxdelay": 1,
        "mul": 1,
        "add": 0,
    },
    "sdelay": {"use": 0, "delay": 0.25, "maxdelay": 1, "mul": 1, "add": 0},
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
        "use": 0,
        "size": 0.5,
        "damp": 0.5,
        "bal": 0.5,
        "mul": 1,
        "add": 0,
    },
    "monoreverb": {
        "use": 0,
        "feedback": 0.5,
        "cutoff": 5000,
        "bal": 0.5,
        "mul": 1,
        "add": 0,
    },
    "chorus": {
        "use": 0,
        "depth": 1,
        "feedback": 0.25,
        "bal": 0.5,
        "mul": 1,
        "add": 0,
    },
    "harmonizer": {
        "use": 0,
        "transpo": -7.0,
        "feedback": 0,
        "winsize": 0.1,
        "mul": 1,
        "add": 0,
    },
    "simpledelay": {"use": 0, "mul": 1, "add": 0},
    "stereoreverb": {
        "use": 0,
        "inpos": 0.5,
        "revtime": 1,
        "cutoff": 5000,
        "bal": 0.5,
        "roomSize": 1,
        "firstRefGain": -3,
        "mul": 1,
        "add": 0,
    },
    "smoothdelay": {
        "use": 0,
        "delay": 0.25,
        "feedback": 0,
        "crossfade": 0.05,
        "maxdelay": 1,
        "mul": 1,
        "add": 0,
    },
    "freqshift": {"use": 0, "shift": 100, "mul": 1, "add": 0},
}
