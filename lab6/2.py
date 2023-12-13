#!/bin/python

from typing import Callable


def avg_if(a: list, test: Callable):
	# create a filtered list
	filtered_elements = [x for x in arr if test(x)]

	# protect against 0-division
	if len(filtered_elements) == 0:
		print("Error: There are no filtered values in the list.")
	else:
		# calcualte average by dividing total sum by the quantity
		average_filtered = sum(filtered_elements) / len(filtered_elements)
		print(f"Average filtered value: {average_filtered}")

# get the values and convert them to integers
while True:
	try:
		arr = list(map(int, input("Enter the list elements (separated with spaces): ").split()))
		break
	except Exception as e:
		print("Exception caught, retrying. Note that list elements must be integers.")

print(f"List: {arr}")


avg_if(arr, lambda x: x<0)
