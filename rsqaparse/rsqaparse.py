"""
parses data from HTML files in RS_qa
"""

#from __future__ import annotations

from csv import DictWriter
from pathlib import Path
from argparse import ArgumentParser
from sys import exit
from typing import NamedTuple

class RestRow(NamedTuple):
    source: str
    subject: str
    session: str
    version: str
    bidsfile: str
    tsnr: str
    fd_mean: str
    gcor: str
    gsr_x: str
    gsr_y: str
    @classmethod
    def from_file(cls, filepath: Path) -> RestRow:
        # parse from path
        source = filepath.as_posix()
        subject, session, *_ = filepath.stem.split("_")
        # parse from html
        version = ...
        # init and return
        return cls(...)

class WholebrainRow(NamedTuple):
    source: str
    subject: str
    session: str
    version: str
    bidsfile: str
    cnr: str
    cjv: str
    efc: str
    wm_median: str
    wm2max: str
    @classmethod
    def from_file(cls, filepath: Path) -> WholebrainRow:
        # parse from path
        source = filepath.as_posix()
        subject, session, *_ = filepath.stem.split("_")
        # parse from html
        version = ...
        # init and return
        return cls(...)

def parse_args() -> tuple[str, str, str]:
    parser = ArgumentParser(description = __doc__)
    parser.add_argument("root", type = str, help = "root RS_qa directory")
    parser.add_argument("out_rest", type = str, help = "output filename for rest csv")
    parser.add_argument("out_wholebrain", type = str, help = "output filename for wholebrain csv")
    args = parser.parse_args()
    return args.root, args.out_rest, args.out_wholebrain

def main(root: str, out_rest: str, out_wholebrain) -> int:
    # read
    files = tuple(sorted(Path(root).rglob("*.html")))
    rest = tuple(RestRow.from_file(f) for f in files if "task-rest" in f.name)
    wholebrain = tuple(WholebrainRow.from_file(f) for f in files if "anat-wholebrain" in f.name)
    # write
    with open(out_rest, "w", newline = "") as ofile:
        writer = DictWriter(ofile, fieldnames = RestRow._fields, dialect = "excel-tab")
        writer.writeheader()
        writer.writerows(row._asdict() for row in rest)
    with open(out_wholebrain, "w", newline = "") as ofile:
        writer = DictWriter(ofile, fieldnames = WholebrainRow._fields, dialect = "excel-tab")
        writer.writeheader()
        writer.writerows(row._asdict() for row in wholebrain)
    return 0

if __name__ == "__main__":
    exit(main(*parse_args()))
