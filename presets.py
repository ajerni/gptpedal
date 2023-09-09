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
            "size": 0.5,
            "damp": 0.5,
            "bal": 0.5,
            "mul": 1,
            "add": 0,
        },
        "monoreverb": {
            "use": 1,
            "feedback": 0.5,
            "cutoff": 5000,
            "bal": 0.5,
            "mul": 1,
            "add": 0,
        },
    }


presets = Presets()
