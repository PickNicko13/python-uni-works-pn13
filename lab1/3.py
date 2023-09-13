from sys import argv

def main():
	# check if enough arguments given
	if len(argv) < 2:
		print("Not enough arguments - expected 2.")
		print(f"Usage: {argv[0]} <N>")
		return 1

	# parse N
	try:
		N = int(argv[1])
	except Exception as e:
		print(f"Error when parsing <N>: {e}")
		return 2
	# verify the number range
	if ( N <= 1 ) or ( N >= 9 ):
		print("<N> is not in range (1;9). Choose a number that is in the specified range.")
		return 3

	for i in range(1, N+1):
		while i > 0:
			print(f" {i}", end='')
			i -= 1
		print()

main()
