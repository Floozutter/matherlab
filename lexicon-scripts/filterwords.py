from argparse import ArgumentParser
from pathlib import Path
from collections.abc import Callable

def parse_args() -> tuple[Path, Callable[[str], bool], Path]:
    parser = ArgumentParser()
    parser.add_argument("wordsfile", type = Path)
    parser.add_argument("keepf", type = str)
    parser.add_argument("outfile", type = Path)
    args = parser.parse_args()
    keepf = eval(args.keepf)
    return args.wordsfile, keepf, args.outfile

def main(wordsfile: Path, keepf: Callable[[str], bool], outfile: Path) -> None:
    visited: set[str] = set()
    words = sorted(filter(keepf, set(wordsfile.read_text().strip().split("\n"))))
    outfile.write_text("\n".join(words) + "\n")

if __name__ == "__main__":
    main(*parse_args())
