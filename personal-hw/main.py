#!/bin/python3

from sys import argv
from time import perf_counter
from enum import Enum

import numpy as np
from scipy import interpolate
from matplotlib import pyplot

from typing import Sequence, Tuple
from numpy._typing import NDArray

class Gruvbox(Enum):
	BG0_H	= '#1D2021'
	BG0_S	= '#32302F'
	BG0		= '#282828'
	BG1		= '#3C3836'
	BG2		= '#504945'
	BG3		= '#665C54'
	BG4		= '#7C6F64'
	BG		= BG0
	FG0		= '#FBF1C7'
	FG1		= '#EBDBB2'
	FG2		= '#D5C4A1'
	FG3		= '#BDAE93'
	FG4		= '#A89984'
	FG		= FG1

	BG_GRAY		= '#928374'
	BG_RED		= '#CC241D'
	BG_ORANGE	= '#D65D0E'
	BG_YELLOW	= '#D79921'
	BG_GREEN	= '#98971A'
	BG_AQUA		= '#689D6A'
	BG_BLUE		= '#458588'
	BG_PURPLE	= '#B16286'

	FG_GRAY		= '#A89984'
	FG_RED		= '#FB4934'
	FG_ORANGE	= '#FE8019'
	FG_YELLOW	= '#FABD2F'
	FG_GREEN	= '#B8BB26'
	FG_AQUA		= '#8EC07C'
	FG_BLUE		= '#83A598'
	FG_PURPLE	= '#D3869B'

def read_csv(file_path: str) -> Tuple[NDArray,NDArray]:
	data = np.genfromtxt(file_path, delimiter=',', names=True, dtype=float)
	print(f"Given data: {data}")
	x = data['x']
	y = data['y']
	return x, y

def lagrange_coefficients(x: Sequence[float], y: Sequence[float]) -> np.poly1d:
	"""
	i'th Lagrange polynomial (li) = product of (x-xj)/(xi-xj) for all points except i=j
	full Lagrange polynomial = sum of y value times the coefficients (yi*li)

	Basically, the resulting function is the sum of subfunctions fi,
	where each fi is equal to yi at xi and 0 at all other x_, so it will not contrubute to them.

	The nice part is that it first normalizes the point to 1 at xi
	{ e.g. for point xi it's (xi-xj)/(xi-xj) at xi }
	"""
	n = len(x)
	if len(y) != n:
		raise ValueError("The number of x and y values must be the same")

	coefficients = np.zeros(n)

	for i in range(n):
		# i'th Lagrange polynomial
		li = np.poly1d([1]) # y = 1
		for j in range(n):
			if i == j:
				continue
			li *= np.poly1d([1, -x[j]]) / (x[i] - x[j])

		# Scale and add to the total
		coefficients += li.coefficients * y[i]

	return np.poly1d(coefficients.round(15))

def lagrange_coefficients_2(x: Sequence[float], y: Sequence[float]):
	"""
	Unlike the first implementation, this one is based on roots instead of coefficients
	"""
	n = len(x)
	if len(y) != n:
		raise ValueError("The number of x and y values must be the same")

	coefficients = np.zeros(n)

	for i in range(n):
		# i'th Lagrange polynomial
		li = np.poly1d([x[j] for j in range(n) if j!=i], True)

		# Scale and add to the total
		coefficients += li.coefficients * y[i]/li(x[i])

	return np.poly1d(coefficients.round(15))

def newtons_polynomial(x: Sequence[float], y: Sequence[float]):
	n = len(x)
	if len(y) != n:
		raise ValueError("The number of x and y values must be the same")

	# ys:
	# [
	#     [ 0 1 2 ... n ]
	#     [ 0 1 2 ... n-1 ]
	#     ...
	#     [ 0 ]
	# ]
	ys = [[*y]]

	for i in range(1,n):
		# Append new subarray
		ys.append([])

		for j in range(n-i):
			divident = ys[i-1][j+1]-ys[i-1][j]
			divisor = x[i+j]-x[j]

			ys[i].append(divident/divisor)

	coefficients = [round(c[0],15) for c in ys]

	f = np.poly1d([coefficients[0]])
	for n,c in enumerate( coefficients[1:] ):
		f += np.poly1d(x[:n+1], True) * c

	return f

def main():
	if len(argv) != 3:
		print(f"Usage: {argv[0]} <csv_file_path> <x>")
		exit(1)

	# Get arguments
	file_path = argv[1]
	user_x = float(argv[2])

	# Get value lists
	x, y = read_csv(file_path)

	y_min = min(y)
	x_min = min(x)
	y_max = max(y)
	x_max = max(x)

	x_diff = x_max-x_min
	y_diff = y_max-y_min

	times = {}
	t0 = perf_counter()

	# Create interpolation polynomial using Lagrange formula, round to 15 decimal places
	# to avoid tiny coefficients introduced by rounding errors
	f_l0 = np.poly1d(interpolate.lagrange(x, y).coefficients.round(15))

	# Print the polynomial in the simplified form
	print(f"SciPy Lagrange:\n{f_l0}")

	t1 = perf_counter()
	times['scipy lagrange'] = t1-t0
	t0 = t1

	# f_n = newtons_polynomial(x,y)
	# print(f"Manual Newton's:\n{f_n}")
	#
	# t1 = perf_counter()
	# times['manual newton'] = t1-t0
	# t0 = t1
	#
	# f_l1 = lagrange_coefficients(x,y)
	# print(f"Manual Lagrange's 1:\n{f_l1}")
	#
	# t1 = perf_counter()
	# times['manual lagrange 1'] = t1-t0
	# t0 = t1
	#
	# f_l2 = lagrange_coefficients_2(x,y)
	# print(f"Manual Lagrange's 2:\n{f_l2}")
	#
	# t1 = perf_counter()
	# times['manual lagrange 2'] = t1-t0
	# t0 = t1
	#
	cubic_spline = interpolate.CubicSpline(x,y)
	# print(f"\nCubic Spline:\n{cubic_spline.c}")

	t1 = perf_counter()
	times['cubic spline'] = t1-t0

	# print(f"\nExecution times:\n{times}\n\n")
	print(f"\nSciPy Lagrange time: {times['scipy lagrange']}")
	for t in times.keys():
		if t != "scipy lagrange":
			print(f"{t}: {times[t]/times['scipy lagrange']*100:.2f}%")

	# Print the interpolated value at x given by the user
	print(f"\nInterpolated value at x={user_x}:",
		f"SciPy Lagrange) {f_l0(user_x)}\n",
		# f"Manual Lagrange 1) {f_l1(user_x)}",
		# f"Manual Lagrange 2) {f_l2(user_x)}",
		# f"Manual Newton) {f_n(user_x)}",
		sep='\n'
	)

	# create the interpolation (actually with a bit of extrapolation) space
	space = np.linspace(x[0]-x_diff/18, x[-1]+x_diff/18, 2000)

	# create basic plot foundations
	fig, ax = pyplot.subplots()
	# set some visuals
	fig.patch.set_facecolor(Gruvbox.BG0_H.value)
	for spine in ax.spines.keys():
		ax.spines[spine].set_color(Gruvbox.FG3.value)
	for axis in (ax.xaxis, ax.yaxis):
		axis.label.set_color(Gruvbox.FG3.value)
	ax.tick_params(colors=Gruvbox.FG2.value, direction='inout')
	ax.set_facecolor(Gruvbox.BG0.value)
	ax.grid(color=Gruvbox.BG3.value, linestyle='dashed')
	ax.set_xlabel('x', color=Gruvbox.FG1.value)
	ax.set_ylabel('y', color=Gruvbox.FG1.value, rotation=0)

	# Plot interpolation functions available in SciPy (except for Lagrange)
	# ax.plot(
	# 		space, interpolate.krogh_interpolate(x,y,space)+y_diff/4,
	# 		linestyle='--', label=f'Krogh + {y_diff/4}', color=Gruvbox.FG_AQUA.value, linewidth=1)
	# ax.plot(
	# 		space, interpolate.pchip_interpolate(x,y,space),
	# 		linestyle='--', label='Piecewise Cubic Hermite Spline', color=Gruvbox.FG_BLUE.value, linewidth=1)
	# ax.plot(
	# 		space, interpolate.Akima1DInterpolator(x,y)(space),
	# 		linestyle='--', label='Akima (Piecewise Cubic Sub-spline?)', color=Gruvbox.FG_GREEN.value, linewidth=1)
	ax.plot(
			space, cubic_spline(space),
			linestyle='-', label=f'Piecewise Cubic Spline', color=Gruvbox.FG_PURPLE.value, linewidth=4)
	# Plot all the polinomes constituting the cubic spline
	print("\nCubic spline polynomials and their ranges:")
	for i in range(len(cubic_spline.c[0])):
		_poly = np.poly1d(cubic_spline.c[:, i])
		segment_y = np.polyval(_poly, space - cubic_spline.x[i])
		ax.plot(space, segment_y, linestyle='-.', linewidth=1.6, label=f'Polynomial {i + 1}\n{_poly}')
		print(f"{_poly} at x [{cubic_spline.x[i]};{cubic_spline.x[i+1]}]")

	# If applicable, plot smoothing spline
	# if len(x) > 5:
	# 	ax.plot(
	# 			space, interpolate.make_smoothing_spline(x,y)(space),
	# 			linestyle='--', label='Smoothnig spline', color=Gruvbox.FG_YELLOW.value, linewidth=1)
	# Plot the Lagrange on top (but below the datapoints)
	ax.plot(
			space, f_l0(space),
			linestyle='-', label='Lagrange polynomial', color=Gruvbox.FG_GRAY.value, linewidth=2)
	# Plot the source datapoints
	ax.scatter(
			x,y,
			marker='.', label='Datapoints', color=Gruvbox.FG0.value, zorder=999)
	# Plot the user_x
	ax.scatter(
			[user_x],[f_l0(user_x)],
			marker='o', label='x*', color=Gruvbox.FG0.value, zorder=9999)
	fig.set_layout_engine('tight')
	ax.legend(facecolor=Gruvbox.BG0_S.value, labelcolor=Gruvbox.FG3.value, edgecolor=Gruvbox.BG2.value)


	ax.set_xlim([x_min-x_diff/20,x_max+x_diff/20])
	ax.set_ylim([y_min-y_diff,y_max+y_diff])

	pyplot.show()

if __name__ == "__main__":
	main()
