#!/bin/python3

import matplotlib.pyplot as plt  
import numpy as np

def main():
	# init a linear space for plot
	space = np.linspace(0, 4, 1001) 
	# init the function in the linear space
	f = 5*np.sin(10*space)*np.sin(3*space)

	# style future plot a little better
	plt.style.use('classic')

	# init a plot
	plt.plot(space, f, label='5*sin(10x)*sin(3x)', linewidth=2)
	# add labels
	plt.xlabel('x', fontsize=12, color='blue')
	plt.ylabel('y', fontsize=12, color='blue')
	# add legend
	plt.legend()
	# enable grid
	plt.grid(True)

	# show the plot
	plt.tight_layout()
	plt.show()

main()
