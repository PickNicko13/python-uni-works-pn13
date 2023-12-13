#!/bin/python

# create an array
a = []
for i in range(0,7):
	# for each line append an internal array
	a.append([])
	# for each internal array add 7 values
	for j in range(0,7):
		# basically 7 minus the difference between array indices
		a[i].append(7-abs(j-i))
	print(a[i])
