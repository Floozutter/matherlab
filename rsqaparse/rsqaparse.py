"""
parses data from HTML files in RS_qa
"""

from __future__ import annotations

from csv import DictWriter
from pathlib import Path
from argparse import ArgumentParser
from sys import exit
from re import compile, VERBOSE
from typing import NamedTuple

P_VERSION = compile(r"MRIQC version:\s*(.*)\s*\.")
P_SUBJECTID = compile(r"Subject ID:\s*(.*)\s*\.")
P_BIDSFILENAME = compile(r"BIDS filename:\s*(.*)\s*\.")
#P_TSNR = compile(r"<tr>(?:(?!<tr)[\s\S])*tsnr(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
#P_TSNR = compile(r"<tr>(?:(?!<tr)[\s\S])*tsnr(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>\s*<\/tr>")
#P_TSNR = compile(r"<tr>(?:(?!<tr)[\s\S])*tsnr[\s\S]*?<td>\s*(.*)\s*<\/td>\s*<\/tr>")

class RestRow(NamedTuple):
    source: str
    subject: str
    session: str
    acquisition: str
    kind: str
    version: str
    special: str
    tsnr: str
    fd_mean: str
    gcor: str
    gsr_x: str
    gsr_y: str
    @classmethod
    def from_file(cls, filepath: Path) -> RestRow:
        # parse from path
        source = filepath.as_posix()
        subject, session, acquisition, kind, *_ = filepath.stem.split("_")
        # parse from html
        text = filepath.read_text()
        version = P_VERSION.search(text).group(1)
        if version == "0.11.0":
            special = P_SUBJECTID.search(text).group(1)
        elif version == "0.15.1":
            special = P_BIDSFILENAME.search(text).group(1)
        else:
            raise ValueError(f"unexpected vesion `{version}`!")
        tsnr = P_TSNR.search(text).group(1)
        # instantiate and return
        return cls(
            source = source,
            subject = subject,
            session = session,
            acquisition = acquisition,
            kind = kind,
            version = version,
            special = special,
            tsnr = tsnr,
            fd_mean = fd_mean,
            gcor = gcor,
            gsr_x = gsr_x,
            gsr_y = gsr_y
        )

class WholebrainRow(NamedTuple):
    source: str
    subject: str
    session: str
    acquisition: str
    kind: str
    version: str
    special: str
    cnr: str
    cjv: str
    efc: str
    wm_median: str
    wm2max: str
    @classmethod
    def from_file(cls, filepath: Path) -> WholebrainRow:
        # parse from path
        source = filepath.as_posix()
        subject, session, acquisition, kind, *_ = filepath.stem.split("_")
        # parse from html
        version = ...
        # instantiate and return
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
