#!/bin/python

# duh
def display_dictionary(d: dict):
	for key, value in d.items():
		print(f"{key:2}: {value}")

# add a new entry to a dictionary
def add_entry(d: dict):
	while True:
		key = int(input("\nEnter key (integer): "))
		if key in d.keys():
			print(f"Key {key} already exists - pick a new one.")
		else:
			break

	keys = [
		'surname',
		'name',
		'address',
		'school_n',
		'grade',
	]
	while True:
		entry = [
			*map(
				lambda x: x.strip(),
				input("\nEnter student data ('|' separated)\n(surname, name, address, school #, grade): ")
			.split('|')
			)
		]
		if len(entry) != 5:
			print(f"Expected 5 values, {len(entry)} given.")
		else:
			break
	d[key] = dict(zip(keys, entry))
	print(f"Entry added successfully.")

# delete an entry from a dictionary
def remove_entry(d: dict, key: int|str):
	try:
		del d[key]
		print(f"Entry {key} deleted.")
	except KeyError:
		print(f"Entry {key} not found.")

# duh
def sort_and_display(d: dict):
	display_dictionary(dict(sorted(d.items())))


def main():
	# init students dict
	students_data = {
			10-i: {
				'surname': f"surname{i}",
				'name': f"name{i}",
				'address': f"address{i}",
				'school_n': f"school_n{i}",
				'grade': f"grade{i}",
			} for i in range(0,10)
	}

	while True:
		print(
			"""
		1. Print all student data.
		2. Add a new student.
		3. Terminate a student.
		4. Print all student data (sorted).
		5. Escape.""")

		choice = input("Choose your fighter: ")

		# do corresponding action
		match choice:
			case '1':
				display_dictionary(students_data)
			case '2':
				add_entry(students_data)
			case '3':
				key = int(input("Enter key to delete: "))
				remove_entry(students_data, key)
			case '4':
				sort_and_display(students_data)
			case '5':
				break
			case _:
				print("Unknown operation. Try again.")

if __name__ == "__main__":
	main()
