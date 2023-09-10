class Presets:
    CHORUS: dict = {
        "chorus": {
            "use": 1,
            "depth": 1,
            "feedback": 0.25,
            "bal": 0.5,
            "mul": 1,
            "add": 0,
        }
    }
    DOPPELVERB: dict = {
        "freeverb": {
            "use": 1,
            "size": 0.708,
            "damp": 0.592,
            "bal": 0.492,
            "mul": 1,
            "add": 0,
        },
        "monoreverb": {
            "use": 1,
            "feedback": 0.6,
            "cutoff": 1623,
            "bal": 0.5,
            "mul": 1.538,
            "add": 0,
        },
    }
    GPTOUTPUT: dict = {
        "chorus": {
            "use": 1,
            "depth": 1,
            "feedback": 0.25,
            "bal": 0.5,
            "mul": 1,
            "add": 0,
        },
        "stereoreverb": {
            "use": 1,
            "inpos": 0.5,
            "revtime": 1,
            "cutoff": 5000,
            "bal": 0.5,
            "roomSize": 1,
            "firstRefGain": -3,
            "mul": 1,
            "add": 0,
        },
    }
    TEST: dict = {
        "disto": {"use": 1, "drive": 0.6, "slope": 0.5, "mul": 1, "add": 0},
        "freeverb": {
            "use": 1,
            "size": 0.708,
            "damp": 0.592,
            "bal": 0.492,
            "mul": 1,
            "add": 0,
        },
        "monoreverb": {
            "use": 1,
            "feedback": 0.6,
            "cutoff": 1623,
            "bal": 0.5,
            "mul": 1.538,
            "add": 0,
        },
    }
    PHASER: dict = {
        "phaser": {
            "use": 1,
            "depth": 1,
            "feedback": 0.25,
            "bal": 0.5,
            "mul": 1,
            "add": 0,
        }
    }
    FLANGER: dict = {
        "flanger": {
            "use": 1,
            "depth": 1,
            "feedback": 0.25,
            "delay": 0.003,
            "rate": 0.2,
            "mul": 1,
            "add": 0,
        }
    }
    DOUBLEDELAY: dict = {
        "delay": {
            "use": 1,
            "delay": 0.25,
            "feedback": 0,
            "maxdelay": 1,
            "mul": 1,
            "add": 0,
        },
        "sdelay": {"use": 1, "delay": 0.25, "maxdelay": 1, "mul": 1, "add": 0},
    }


presets = Presets()
