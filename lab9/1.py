#!/bin/python

import string
import random
import re

# duh
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))



file_1 = 'TF10_1.txt'
file_2 = 'TF10_2.txt'

# Create a txt file with random strings of varying lengths
try:
	with open(file_1, 'w') as file:
		# write 10 new lines of randomized length (10 to 30)
		for _ in range(10):
			file.write(generate_random_string(random.randint(10, 30)) + '\n')
except Exception as e:
	print(f"An error occurred while creating {file_1}: {e}")

# Read content from input file, remove digits, and write to another file
try:
	with open(file_1, 'r') as input_file, open(file_2, 'w') as output_file:
		full_no_digits_string = ''
		for line in input_file:
			# Remove digits from the line
			line_without_digits = ''.join(char for char in line if not char.isdigit())
			full_no_digits_string += line_without_digits.replace('\n', '')

		# split the full_no_digits_string into <=10 char chunks,
		# then join them with newlines in between and write the resulting string
		output_file.write(
			'\n'.join( re.findall('.{1,10}', full_no_digits_string) )
		)
except Exception as e:
	print(f"An error occurred during step B: {e}")

# Read and print content of a file line by line
try:
	with open(file_2, 'r') as file:
		for line in file:
			print(line.strip())
except Exception as e:
	print(f"An error occurred while reading {file_2}: {e}")
