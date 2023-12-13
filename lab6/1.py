#!/bin/python

# delete an element from list
# Note: if there are duplicate elements only the first one will be deleted
def delete_element_from_list(user_list):
	while True:
		try:
			# get element to delete
			element_to_delete = int(input("Enter the element you want to delete: "))
			
			# test if it exists
			if element_to_delete in user_list:
				user_list.remove(element_to_delete)
				print("Element successfully dismembered.")
				# point of yes return
				return
			else:
				print("Error: element not found.")
		except ValueError:
			print("Invalid value. Element must be an integer that is present in the list.")

# get the values and convert them to integers
while True:
	try:
		user_list = list(map(int, input("Enter the list elements (separated with spaces): ").split()))
		break
	except Exception as e:
		print("Exception caught, retrying.")

print(f"List: {user_list}")

delete_element_from_list(user_list)

# print the modified list
print(f"Result: {user_list}")
