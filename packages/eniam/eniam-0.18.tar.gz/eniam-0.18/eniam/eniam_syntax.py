SUPPORTED_VALUES = {
    "lemma": None,
    "cat": None,
    "pos": [
        "subst", "depr", "ppron12", "ppron3",
        "siebie", "prep", "num", "intnum",
        "realnum", "intnum-interval",
        "realnum-interval", "symbol", "ordnum",
        "date", "date-interval", "hour-minute", "hour",
        "hour-minute-interval", "hour-interval",
        "year", "year-interval", "day", "day-interval",
        "day-month", "day-month-interval",
        "month-interval", "roman", "roman-interval",
        "roman-ordnum", "match-result",
        "url", "email", "obj-id", "adj", "adjc", "adjp",
        "adja", "adv", "ger", "pact", "ppas", "fin",
        "bedzie", "praet", "winien", "impt", "imps",
        "pred", "aglt", "inf", "pcon", "pant", "qub",
        "comp", "conj", "interj", "sinterj", "burk", "interp",
        "unk", "apron"
    ],
    "number": [ "sg", "pl" ],
    "case": [
        "nom", "gen", "dat", "acc", "inst", "loc", "postp", "pred"
    ],
    "gender": [
        "m1", "m2", "m3", "f", "n1", "n2", "p1", "p2", "p3"
    ],
    "person": [
        "pri", "sec", "ter"
    ],
    "grad": [
        "pos", "com", "sup"
    ],
    "praep": [
        "praep", "npraep", "praep-npraep",
    ],
    "acm": [ "congr", "rec" ],
    "ctype": [ "int", "rel", "sub", "coord" ],
    "mode": [ "abl", "adl", "locat", "perl", "dur", "temp", "mod" ],
    "aspect": [ "perf", "imperf" ],
    "negation": [ "neg", "aff" ],
    "mood": [ "indicative", "imperative", "conditional" ],
    "tense": [ "past", "pres", "fut" ],
    "nsyn": [ "proper", "pronoun", "common" ],
    "nsem": [ "count", "time", "mass", "measure" ],
};

def valence_rule(lemma="", pos=""):
    return f"lemma={lemma},pos2={pos},node=concept|sit"

def root_rule():
    return "__root__"

def rule(
    lemma=None,
    pos=None,
    case=None,
    number=None,
    gender=None,
    person=None,
    grad=None,
    praep=None,
    acm=None,
    ctype=None,
    mode=None,
    aspect=None,
    negation=None,
    mood=None,
    tense=None,
    nsyn=None,
    nsem=None
):
    for key in SUPPORTED_VALUES:
        if key in locals():
            val = locals()[key]
            if val is not None:
                if SUPPORTED_VALUES[key] is not None:
                    if val not in SUPPORTED_VALUES[key]:
                        raise Exception(f"Invalid value '{val}' was used for '{key}' parameter. Allowed values are: {', '.join(SUPPORTED_VALUES[key])}")
    output = []
    for key in SUPPORTED_VALUES:
        if key in locals():
            val = locals()[key]
            if val is not None:
                output.append(f"{key}={val}")
    return ",".join(output)
