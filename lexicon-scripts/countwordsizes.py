from argparse import ArgumentParser
from pathlib import Path
from collections import Counter

def parse_arg() -> Path:
    parser = ArgumentParser()
    parser.add_argument("wordsfile", type = Path)
    return parser.parse_args().wordsfile

def main(wordsfile: Path) -> None:
    sizes: Counter[int] = Counter()
    with wordsfile.open() as ifile:
        for line in ifile:
            word = line.strip()
            sizes[len(word)] += 1
    for size, count in sorted(sizes.items()):
        print(f"{size=}: {count=}") 

if __name__ == "__main__":
    main(parse_arg())
