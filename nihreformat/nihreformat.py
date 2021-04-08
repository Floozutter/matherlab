"""
reformats NIH data in Excel-tab formatted csv files
"""

from csv import DictReader, DictWriter
from argparse import ArgumentParser
from sys import exit
from enum import Enum
from typing import Sequence, Iterable

Fieldnames = Sequence[str]
Row = dict[str, str]

class Kind(Enum):
    FIELDNAME = "type"
    INSTRUCTION = "instruction"
    PRACTICE = "practice"
    MAIN = "main"

def kind(row: Row) -> Kind:
    inst = row["inst"]
    itemID = row["itemID"]
    if inst == "NIH Toolbox List Sorting Working Memory Test Age 7+ v2.1":
        if "P" in itemID:
            return Kind.PRACTICE
        else:
            return Kind.MAIN
    elif inst == "NIH Toolbox Pattern Comparison Processing Speed Test Age 7+ Practice v2.1":
        if "INSTR" in itemID:
            return Kind.INSTRUCTION
        else:
            return Kind.PRACTICE
    elif inst == "NIH Toolbox Pattern Comparison Processing Speed Test Age 7+ v2.1":
        return Kind.MAIN
    elif inst == "NIH Toolbox Flanker Inhibitory Control and Attention Test Age 12+ v2.1":
        if "PRAC" in itemID:
            return Kind.PRACTICE
        else:
            return Kind.MAIN
    else:
        raise AssertionError(f"invalid inst `{inst}`!")

def read(infilename: str) -> tuple[Fieldnames, list[Row]]:
    with open(infilename, "r", newline = "") as ifile:
        reader = DictReader(ifile, dialect = "excel-tab")
        assert reader.fieldnames is not None
        return tuple(reader.fieldnames), list(reader)

def write(outfilename: str, fieldnames: Fieldnames, data: Iterable[Row]) -> None:
    with open(outfilename, "w", newline = "") as ofile:
        writer = DictWriter(ofile, fieldnames, dialect = "excel-tab")
        writer.writeheader()
        writer.writerows(data)

def parse_args() -> tuple[str, str]:
    parser = ArgumentParser(description = __doc__)
    parser.add_argument("infilename", type = str, help = "input tsv filename")
    parser.add_argument("outfilename", type = str, help = "output tsv filename")
    args = parser.parse_args()
    return args.infilename, args.outfilename

def main(infilename: str, outfilename: str) -> int:
    prefieldnames, data = read(infilename)
    postfieldnames = tuple(prefieldnames) + (Kind.FIELDNAME.value,)
    for row in data:
        row[Kind.FIELDNAME.value] = str(kind(row).value)
    write(outfilename, postfieldnames, data)
    return 0

if __name__ == "__main__":
    exit(main(*parse_args()))
