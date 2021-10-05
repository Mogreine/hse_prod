import numpy as np

from typing import Tuple
from scipy.stats import rankdata
from argparse import ArgumentParser


def read_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []

    with open(path, "r") as f:
        for line in f:
            if line == "":
                break

            p = line.strip().split()
            xs.append(int(p[0]))
            ys.append(int(p[1]))

    assert len(xs) >= 9, "Arrays' lengths should be at least 9"

    return np.array(xs), np.array(ys)


def calc_ranks(xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    args_sorted = np.argsort(xs)
    ys = ys[args_sorted]

    return rankdata(-ys)


def calc(ranks: np.ndarray) -> Tuple[int, int, float]:
    n = len(ranks)
    p = round(n / 3)
    r1, r2 = np.sum(ranks[:p]), np.sum(ranks[-p:])

    diff = r1 - r2
    std = (n + 0.5) * np.sqrt(p / 6)
    conj = diff / (p * (n - p))

    return round(diff), round(std), round(conj, 2)


def save_result(path: str, diff: int, std: int, conj: float) -> None:
    with open(path, "w") as f:
        f.write(f"{diff} {std} {conj}\n")


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--input_file", "-i", type=str, required=True, help="Path to the input file with data.")
    args.add_argument("--output_file", "-o", type=str, required=True, help="Path to the output file with results.")

    args = args.parse_args()

    xs, ys = read_data(args.input_file)
    ranks = calc_ranks(xs, ys)
    diff, std, conj = calc(ranks)

    save_result(args.output_file, diff, std, conj)
