import matplotlib.pyplot
import subprocess
import argparse

def parse_arg() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type = int)
    return parser.parse_args().n

def main(n: int) -> None:
    # run simulation
    s = subprocess.run(
        ("node", "simulate.js", str(n)),
        stdout = subprocess.PIPE
    ).stdout.decode("utf-8").strip()
    # transform data
    xs = range(1, len(s)+1)
    ys = []
    for i, c in enumerate(s):
        ys.append((ys[i-1] if i-1 >= 0 else 0) + int(c))
    # plot
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("total generated short IDs")
    ax.set_ylabel("total collisions")
    ax.xaxis.get_major_locator().set_params(integer = True)
    ax.yaxis.get_major_locator().set_params(integer = True)
    ax.plot(xs, ys)
    print(s)
    matplotlib.pyplot.show()

if __name__ == "__main__":
    main(parse_arg())
