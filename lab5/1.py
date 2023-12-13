#!/bin/python

# Get array length
N = int(input("Enter array length (integer): "))

# Get values
arr = []
for i in range(N):
	num = int(input(f"Enter A[{i}]: "))
	arr.append(num)

# Calculate sum of all positive elements which are multiples of 3
sum_positive_multiple_of_three = sum(x for x in arr if x > 0 and x % 3 == 0)

print(f"Sum of all positive elements which are multiples of 3: {sum_positive_multiple_of_three}")
