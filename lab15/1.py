#!/bin/python3

import pandas as pd

def main():
	students_json = 'students.json'
	try:
		students_data = pd.read_json(students_json, orient='index')
	except Exception as e:
		print(f"Error while reading '{students_json}': {e}")
		exit(1)

	print("\nLoaded data:")
	print(students_data)

	# grouping
	grade = students_data['grade']
	print('\nStudent grades:')
	print(grade)
	print(f"Average grade: {grade.mean()}")
	print(f"Minimum grade: {grade.min()}")
	print(f"Maximum grade: {grade.max()}")

	# aggregation
	print("\nGrade and attendance day mode values:\n",
		students_data[['grade','attendance_day']].agg('mode'), sep='')

if __name__ == "__main__":
	main()
