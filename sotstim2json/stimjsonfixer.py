from argparse import ArgumentParser
from json import loads, dumps
from pathlib import Path

def parse_args() -> tuple[Path, Path]:
    parser = ArgumentParser()
    parser.add_argument("old", type = Path)
    parser.add_argument("fixed", type = Path)
    args = parser.parse_args()
    return args.old, args.fixed

def main(badpath: Path, fixedpath: Path) -> None:
    bad = loads(badpath.read_text(encoding = "utf-8"))
    no_n = lambda s: {
        **s,
        **{
            "trials": [
                {k: v for k, v in t.items() if k != "n"}
                for t in s["trials"]
            ],
        },
    }
    fixed = {
        "example": no_n(bad["example"]["example"]["0"]),
        "practice": no_n(bad["practice"]["practice"]["0"]),
        "test-sets": {
            **{
                setn: no_n(setv)
                for setn, setv in bad["pre"]["main"].items()
            },
            **{
                str(int(setn) + 6): no_n(setv)  # DANGER!!!
                for setn, setv in bad["post"]["main"].items()
            },
        }
    }
    fixedpath.with_suffix(".json").write_text(dumps(fixed, indent = 4))

if __name__ == "__main__":
    main(*parse_args())
