#!/bin/python

import csv
from sys import argv
from os import path
from typing import Iterable

# ask a yes/no question
def binary_answer(question: str):
	return input(f"{question} [Y/n]").lower() in ('','y','yes','т','так','д','да')

# if file exists, ask if user is ok with overwriting it
def not_exists_or_overwrite(filename: str):
	return not path.exists(filename) \
			or binary_answer(f"File '{filename}' exists. Overwrite?")

# nice table-like printing for table-like data
def print_in_rows(data: Iterable[Iterable]):
	# define target column sizes
	column_sizes = (54, 3, 6, 6)

	# define row separator string
	row_separator = f"{'├':─<{column_sizes[0]+3}}{'┼':─<{column_sizes[1]+3}}{'┼':─<{column_sizes[2]+3}}{'┼':─<{column_sizes[3]+3}}┤"

	# print table heading
	print(f"{'┌':─<{sum(column_sizes, len(column_sizes)*2)+4}}┐")
	print(f"│{'Exports in % of GDP per country':^{sum(column_sizes, len(column_sizes)*2)+3}}│")
	print(f"{'├':─<{column_sizes[0]+3}}{'┬':─<{column_sizes[1]+3}}{'┬':─<{column_sizes[2]+3}}{'┬':─<{column_sizes[3]+3}}┤")
	print(f"│{'Country':^{column_sizes[0]+2}}│{'Code':^{column_sizes[1]+2}}│{2015:^{column_sizes[2]+2}}│{2019:^{column_sizes[3]+2}}│")

	# cycle through rows
	for n,row in enumerate(data):
		# every fifth row add a separator for clarity
		if n%5 == 0:
			print(row_separator)

		# print a row of data
		print('│', end='')
		for n,column in enumerate(row):
			# if no data, write blanks
			if column is None:
				value = '  -----'
			# if float, format it to have 2 decimal digits and align to the right
			elif isinstance(column, float):
				value = f" {column:>6.2f}"
			# in other cases just use appropriate size
			else:
				value = f" {column:{column_sizes[n]}}"
			print(value, end=' │')
		print() # newline
	# print ending line
	print(f"{'└':─<{column_sizes[0]+3}}{'┴':─<{column_sizes[1]+3}}{'┴':─<{column_sizes[2]+3}}{'┴':─<{column_sizes[3]+3}}┘")
	return


def main():
	data = [] # will contain tuples of (country, country_code, export_2015, export_2019)
	# either get argv[1] or set default value
	filename = argv[1] if len(argv)>1 else 'data/main.csv'
	try:
		# 'utf-8-sig' is set manually to avoid the BOM symbol at each newline
		with open(filename, 'r', encoding='utf-8-sig') as data_file:
			# init a csv reader
			reader = csv.DictReader(data_file)
			# parse rows and add useful data to the data list
			for row in reader:
				_2015 = float(row['2015']) if row['2015'] else None
				_2019 = float(row['2019']) if row['2019'] else None
				data.append((
					row['Country Name'],
					row['Country Code'],
					_2015,
					_2019
				))
	except Exception as e:
		print(f"Couldn't open '{filename}' for reading: {e}")
		exit(1)

	print_in_rows(data)
	print()

	# ask to get a filtered version of the data
	if binary_answer("Wanna get a filtered version?"):
		entry_prompt = "Enter a list ('|' separated) of country codes corresponding to countries you want to see:\n"
		# split entered data by '|', then strip it of spaces and uppercase
		# sorted to always have the same result if country codes are the same
		county_codes = sorted([
			*map(
				lambda x: x.strip().upper(),
				input(entry_prompt).split('|')
			)
		])
		# create a new list of data only for rows matching the entered country codes
		filtered_data = [*(d for d in data if d[1] in county_codes)]

		print()
		print_in_rows(filtered_data)
		print()

		# ask to save the filtered data
		if binary_answer("Wanna save it?"):
			# get name automatically from country codes
			filtered_filename = ', '.join(county_codes).__add__('.csv')
			# ask to overwrite if file exists
			if not_exists_or_overwrite(filtered_filename):
				try:
					# write filtered data
					with open(filtered_filename, 'w') as file:
						writer = csv.writer(file)
						writer.writerow(('Country Name','Country Code','2015','2019'))
						writer.writerows(filtered_data)
				except Exception as e:
					print(f"Couldn't open '{filename}' for writing: {e}")
					exit(1)


main()
