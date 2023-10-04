from sys import argv

def calc_x(a: float, b: float):
	if a > b:
		return a*b + 21
	elif a < b:
		return 3 * a/b + 1
	else:
		return -5

def main():
	# check if enough arguments given
	if len(argv) < 3:
		print("Not enough arguments - expected 3.")
		print(f"Usage: {argv[0]} <a> <b>")
		return 1

	# parse numbers
	try:
		a = float(argv[1])
	except Exception as e:
		print(f"Error when parsing <a>: {e}")
		return 2
	try:
		b = float(argv[2])
	except Exception as e:
		print(f"Error when parsing <a>: {e}")
		return 2
	
	# verify the number range
	if a < 0:
		print("<a> is negative. Choose a positive number.")
		return 3
	if b < 0:
		print("<b> is negative. Choose a positive number.")
		return 3


	print(f"X: {calc_x(a, b)}")
	return 0

main()
