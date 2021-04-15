"""
parses data from HTML files in RS_qa
"""

from __future__ import annotations

from csv import DictWriter
from pathlib import Path
from argparse import ArgumentParser
from sys import exit
from re import compile, Match
from typing import NamedTuple, Optional

# patterns
## summary
P_VERSION = compile(r"MRIQC version:\s*(.*)\s*\.")
P_SUBJECTID = compile(r"Subject ID:\s*(.*)\s*\.")
P_BIDSFILENAME = compile(r"BIDS filename:\s*(.*)\s*\.")
## image quality metrics table
### task-rest
P_TSNR = compile(r"<tr>(?:(?!<tr)[\s\S])*tsnr(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
P_FD_MEAN = compile(r"<tr>(?:(?!<tr)[\s\S])*fd(?:(?!<tr)[\s\S])*mean(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>\s*<\/tr>")
P_GCOR = compile(r"<tr>(?:(?!<tr)[\s\S])*gcor(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
P_GSR_X = compile(r"<tr>(?:(?!<tr)[\s\S])*gsr(?:(?!<tr)[\s\S])*x(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>\s*<\/tr>")
P_GSR_Y = compile(r"<tr>(?:(?!<tr)[\s\S])*gsr(?:(?!<tr)[\s\S])*y(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>\s*<\/tr>")
### anat-wholebrain
P_CJV = compile(r"<tr>(?:(?!<tr)[\s\S])*cjv(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
P_CNR = compile(r"<tr>(?:(?!<tr)[\s\S])*cnr(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
P_EFC = compile(r"<tr>(?:(?!<tr)[\s\S])*efc(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")
P_WM_MEDIAN = compile(r"<tr>(?:(?!<tr)[\s\S])*summary(?:(?!<tr)[\s\S])*wm(?:(?!<tr)[\s\S])*median(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>\s*<\/tr>")
P_WM2MAX = compile(r"<tr>(?:(?!<tr)[\s\S])*wm2max(?:(?!<tr)[\s\S])*<td>\s*(.*)\s*<\/td>(?:(?!<tr)[\s\S])*<\/tr>")

def unwrap(maybematch: Optional[Match]) -> Match:
    if maybematch is None:
        raise ValueError("match not found")
    else:
        return maybematch

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
        version = unwrap(P_VERSION.search(text)).group(1)
        if version == "0.11.0":
            special = unwrap(P_SUBJECTID.search(text)).group(1)
        elif version == "0.15.1":
            special = unwrap(P_BIDSFILENAME.search(text)).group(1)
        else:
            raise ValueError(f"unexpected version `{version}`")
        tsnr = unwrap(P_TSNR.search(text)).group(1)
        fd_mean = unwrap(P_FD_MEAN.search(text)).group(1)
        gcor = unwrap(P_GCOR.search(text)).group(1)
        gsr_x = unwrap(P_GSR_X.search(text)).group(1)
        gsr_y = unwrap(P_GSR_Y.search(text)).group(1)
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
    cjv: str
    cnr: str
    efc: str
    wm_median: str
    wm2max: str
    @classmethod
    def from_file(cls, filepath: Path) -> WholebrainRow:
        # parse from path
        source = filepath.as_posix()
        subject, session, acquisition, kind, *_ = filepath.stem.split("_")
        # parse from html
        text = filepath.read_text()
        version = unwrap(P_VERSION.search(text)).group(1)
        if version == "0.11.0":
            special = unwrap(P_SUBJECTID.search(text)).group(1)
        elif version == "0.15.1":
            special = unwrap(P_BIDSFILENAME.search(text)).group(1)
        else:
            raise ValueError(f"unexpected version `{version}`")
        cjv = unwrap(P_CJV.search(text)).group(1)
        cnr = unwrap(P_CNR.search(text)).group(1)
        efc = unwrap(P_EFC.search(text)).group(1)
        wm_median = unwrap(P_WM_MEDIAN.search(text)).group(1)
        wm2max = unwrap(P_WM2MAX.search(text)).group(1)
        # instantiate and return
        return cls(
            source = source,
            subject = subject,
            session = session,
            acquisition = acquisition,
            kind = kind,
            version = version,
            special = special,
            cjv = cjv,
            cnr = cnr,
            efc = efc,
            wm_median = wm_median,
            wm2max = wm2max
        )

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
