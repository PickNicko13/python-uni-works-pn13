#!/bin/python

import json
import re
from os import path

# duh
def display_dictionary(d: dict) -> None:
	for key, value in d.items():
		print(f"{key:2}: {value}")

student_keys = [
	'surname',
	'name',
	'address',
	'school_n',
	'grade',
	'attendance_day',
]
# add a new entry to a dictionary
def add_entry(d: dict) -> bool:
	while True:
		key = input("\nEnter a new key: ")
		if key in d.keys():
			print(f"Key {key} already exists - pick a new one.")
		else:
			break

	while True:
		proto_entry: list[str] = [
			*map(
				lambda x: x.strip(),
				input("\nEnter student data ('|' separated)\n(surname, name, address, school #, grade, attendance_day ['sat','sun']): ")
				.split('|')
			)
		]
		if len(proto_entry) != 6:
			print(f"Expected 6 values, {len(proto_entry)} given.")
		else:
			break
	entry: dict = dict(zip(student_keys, proto_entry))
	# validate data
	try:
		entry['grade'] = int(entry['grade'])
	except Exception as e:
		print(f"Error converting {entry['grade']} to integer: {e}")
		return False
	if entry['attendance_day'] not in ('sat','sun'):
		print(f"Invalid attendance day: '{entry['attendance_day']}'. Permitted values: 'sat', 'sun'.")
		return False
	d[key] = entry
	print(f"Entry added successfully.")
	return True

# delete an entry from a dictionary
def remove_entry(d: dict, key: int|str) -> bool:
	try:
		del d[key]
		print(f"Entry {key} deleted.")
		return True
	except KeyError:
		print(f"Entry {key} not found.")
		return False

# duh
def sort_and_display(d: dict) -> None:
	display_dictionary(dict(sorted(d.items())))


def main():
	attendance_days = ('sat','sun')
	students_json = 'students.json'

	def dump_students() -> bool:
		print(f"Writing '{students_json}'.")
		try:
			json.dump(students_data, open(students_json, 'w'), indent='\t', ensure_ascii=False)
			return True
		except Exception as e:
			print(f"Error writing the updated json: {e}")
			return False

	# load existing json if it exists or generate some data and save a json for future use
	if path.exists(students_json):
		print(f"File '{students_json}' exists - attempting to read the student data.")
		try:
			students_data = json.load(open(students_json, 'r'))
		except Exception as e:
			print(f"Error while reading '{students_json}': {e}")
			exit(1)
	else:
		print(f"File '{students_json}' doesn't exists - autogenerating some student data.")
		# init students dict with autogenereted data
		students_data = {
			f"stud{20-i*2}": {
				'surname': f"surname{i}",
				'name': f"name{i}",
				'address': f"address{i}",
				'school_n': f"school_n{i}",
				'grade': 6+i%5,
				'attendance_day': attendance_days[i%2],
			} for i in range(0,10)
		}
		# save it for future use
		dump_students()

	while True:
		print(
			"""
		1. Print all student data.
		2. Add a new student.
		3. Terminate a student.
		4. Print all student data (sorted).
		5. Print names, surnames and addresses of students in grades 7-8 attending the club at Saturdays.
		6. Print filtered student data.
		7. Escape.""")

		choice = input("Choose your fighter: ")

		# do corresponding action
		match choice:
			case '1':
				display_dictionary(students_data)
			case '2':
				if add_entry(students_data):
					dump_students()
			case '3':
				key = input("Enter key to delete: ")
				if remove_entry(students_data, key):
					dump_students()
			case '4':
				sort_and_display(students_data)
			case '5':
				filtered_data = {k:v for (k,v) in students_data.items()
					 if v['grade'] in (7,8) and v['attendance_day'] == 'sat'}
				print("\nStudents matching the criteria:")
				for key, value in filtered_data.items():
					print(f"\t{value['name']} {value['surname']}, {value['address']}")
			case '6':
				print("Available fields:")
				print('    '.join(
					map(
						lambda x: f"{x[0]}: {x[1]}",
						enumerate(student_keys)
					)
				))
				try:
					field_n = int(input("Choose the number of field to filter by: "))
					# if field_n < 0 or field_n > len(student_keys):
					# 	raise ValueError('Invalid field number')
					field = student_keys[field_n]

					pattern = input("Enter the filter (regex-based): ")

					filtered_data = {k:v for (k,v) in students_data.items()
						 if re.match(pattern, str(v[field]), re.IGNORECASE)}
					print("\nStudents matching the criteria:")
					display_dictionary(filtered_data)
				except Exception as e:
					print(e)
			case '7':
				exit(0)
			case _:
				print("Unknown operation. Try again.")

if __name__ == "__main__":
	main()
