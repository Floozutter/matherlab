from argparse import ArgumentParser
from json import dumps
from pathlib import Path

def parse_args() -> Path:
    parser = ArgumentParser()
    parser.add_argument("csvfile", type = Path)
    return parser.parse_args().csvfile

def main(csvfile: Path) -> None:
    stim = {}
    text = csvfile.read_text(encoding = "utf-8")
    rows = (line.split(",") for line in text.split("\n"))
    header, *data = rows
    for phase, category, setstr, trialstr, center, facing, target, _, _, _, order in data:
        if phase not in stim:
            stim[phase] = {}
        if category not in stim[phase]:
            stim[phase][category] = {}
        try:
            setn = int(setstr)
        except ValueError:
            setn = 0
        if setn not in stim[phase][category]:
            stim[phase][category][setn] = {"order": None, "trials": []}
        try:
            trialn = int(trialstr)
        except ValueError:
            trialn = 0
        stim[phase][category][setn]["order"] = order
        stim[phase][category][setn]["trials"].append({
            "center": center,
            "facing": facing,
            "target": target,
            "n": trialn
        })
    json = dumps(stim, indent = 4)
    csvfile.with_suffix(csvfile.suffix + ".json").write_text(json)

if __name__ == "__main__":
    main(parse_args())
