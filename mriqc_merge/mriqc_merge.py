"""
merges the JSON files in a MRIQC task directory into a single CSV file
"""

from argparse import ArgumentParser
from csv import DictWriter, unix_dialect
from pathlib import Path
from json import loads

def flatten(d: dict) -> dict:
    flat = {}
    for k, v in d.items():
        if isinstance(v, None | bool | int | float | str):
            flat[k] = v
        elif isinstance(v, dict):
            sub = {f"{k}.{kk}": vv for kk, vv in flatten(v).items()}
            if set(flat) & set(sub):
                raise AssertionError("duplicate keys in flattened")
            else:
                flat.update(sub)
        else:
            raise AssertionError(f"unsupported type: {type(v)}")
    return flat

def parse_which(name: str) -> str:
    if name.count("e3") == 1:
        return "e3"
    elif name.count("e2") == 1:
        return "e2"
    elif name.count("e1") <= 1:
        return "e1"
    else:
        raise Assertion("can't parse which")

def read_row(jsonfile: Path) -> dict[str, str]:
    *_, task, session, subid, name = jsonfile.parts
    meta = {
        "task": task,
        "session": session,
        "subid": subid,
        "name": name,
        "which": parse_which(name),
    }
    data = flatten(loads(jsonfile.read_text()))
    if set(data) & set(meta):
        raise AssertionError("duplicate keys between data and meta")
    else:
        return meta | data

def parse_args() -> tuple[Path, Path]:
    parser = ArgumentParser(description = __doc__)
    parser.add_argument("indir", type = Path, help = "input task directory")
    parser.add_argument("outfile", type = Path, help = "output CSV file")
    args = parser.parse_args()
    return args.indir, args.outfile

def main(indir: Path, outfile: Path) -> None:
    rows = []
    for path in indir.rglob("*.json"):
        rows.append(read_row(path))
    frontnames = ("task", "session", "subid", "name", "which")
    fieldnames = frontnames + tuple(sorted(set(rows[0]) - set(frontnames)))
    with open(str(outfile), "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames, dialect = unix_dialect)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    main(*parse_args())
