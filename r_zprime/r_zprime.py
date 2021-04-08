"""
Computes the sample Pearson correlation coefficient (r) and its modified
Fisher z-transformation (z') for a pair of newline-separated text files.
"""

from argparse import ArgumentParser
from math import sqrt, atanh
from typing import List, Tuple


def spcc(x: List[float], y: List[float]) -> float:
	"""Returns the sample Pearson correlation coefficient for x and y."""
	# Get means.
	x_mean = sum(x)/len(x)
	y_mean = sum(y)/len(y)
	# Get deviation scores.
	xd = [x_i - x_mean for x_i in x]
	yd = [y_i - y_mean for y_i in y]
	# Get covariability. (Sum of element-wise products of deviation scores.)
	covariance = sum(xd_i * yd_i for xd_i, yd_i in zip(xd, yd))
	# Get separate variabilities. (Sums of squares of deviation scores.)
	x_variability = sum(xd_i * xd_i for xd_i in xd)
	y_variability = sum(yd_i * yd_i for yd_i in yd)
	# Return the ratio of covariability to separate variabilities.
	return covariance / sqrt(x_variability * y_variability)

def modified_fisher_transform(r: float, n: int) -> float:
	"""Returns a Fisher's z modified by dividing it by the standard error."""
	z = atanh(r)
	inverse_standard_error = sqrt(n - 3)
	return z * inverse_standard_error

def read_file(filename: str) -> List[float]:
	with open(filename) as file:
		return [float(line) for line in file.readlines()]

def main(x_filename: str, y_filename: str) -> None:
	x = read_file(x_filename)
	y = read_file(y_filename)
	assert len(x) == len(y), "Variables aren't paired! (Different sizes.)"
	r = spcc(x, y)
	if -1 < r < 1:
		z_prime = modified_fisher_transform(r, len(x))
		print(f"{r} {z_prime}")
	else:
		print(f"{r} None")

def parse_args() -> Tuple[str, str]:
	parser = ArgumentParser(
		description = "Computes the r and z' for a pair of text files.",
		prog = "r_zprime.py"
	)
	parser.add_argument(
		"x_filename",
		type=str,
		help="File containing newline separated values for variable x."
	)
	parser.add_argument(
		"y_filename",
		type=str,
		help="File containing newline separated values for variable y."
	)
	args = parser.parse_args()
	return args.x_filename, args.y_filename


if __name__ == "__main__":
	main(*parse_args())
