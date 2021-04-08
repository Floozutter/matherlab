"""
process NIH data in Excel-tab formatted csv files to add `type` and `day` columns
"""

from csv import DictReader, DictWriter
from argparse import ArgumentParser
from sys import exit
from datetime import datetime, date
from collections import defaultdict
from enum import Enum
from typing import Sequence, Iterable

Fieldnames = Sequence[str]
Row = dict[str, str]

class Kind(Enum):
    INSTRUCTION = "instruction"
    PRACTICE = "practice"
    MAIN = "main"

def get_kind(row: Row) -> Kind:
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

def get_date(row: Row) -> date:
    datestring, _ = row["DateCreated"].split()
    for format in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            dt = datetime.strptime(datestring, format)
        except ValueError:
            pass
        else:
            return dt.date()
    raise ValueError(f"datestring `{datestring}` matched no formats!")

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
    # read csv file
    prefieldnames, data = read(infilename)
    # prepare new fieldnames
    postfieldnames = tuple(prefieldnames) + ("type", "day")
    # add type kind to each row
    for row in data:
        row["type"] = str(get_kind(row).value)
    # find dates per participant
    id_to_dateset: dict[str, set[date]] = defaultdict(set)
    for row in data:
        id_to_dateset[row["subID"]].add(get_date(row))
    # find day per date per participant
    id_to_daydict: dict[str, dict[date, int]] = {
        id: {date: index for index, date in enumerate(sorted(dateset))}
        for id, dateset in id_to_dateset.items()
    }
    # add day to each row
    for row in data:
        row["day"] = str(id_to_daydict[row["subID"]][get_date(row)])
    # write csv file
    write(outfilename, postfieldnames, data)
    return 0

if __name__ == "__main__":
    exit(main(*parse_args()))
