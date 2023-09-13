def main():
	# predefine n1 and n2
	n1: int = 0
	n2: int = 1

	count = 3
	while count <= 25:
		nth = n1 + n2
		if count >= 5:
			print(nth)
		# update values
		n1 = n2
		n2 = nth
		count += 1
main()
