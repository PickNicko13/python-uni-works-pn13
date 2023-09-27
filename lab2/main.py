from lib import z, exponential_athlete
from sys import argv

def main():
	usage = \
f'''
Usage:
	{argv[0]} <job_number>

Where <job_number> can be one of:
	1: some Z math
	2: exponential_athlete
''';

	if len(argv) < 2:
		print(usage)
		exit(1)
	
	# Z
	if int(argv[1]) == 1:
		a = float(input('Input a: '))
		b = float(input('Input b: '))
		print( z(a, b) )

	# athlete
	if int(argv[1]) == 2:
		print('Exponential athlete')

		initial_distance = 0.
		while initial_distance <= 0.:
			initial_distance = float(input('Input the initial (day 0) distance (in percents, must be > 0): '))

		growth = 0.
		while growth <= 0.:
			growth = float(input('Input the distance growth rate (in percents, must be > 0): '))

		day = exponential_athlete(initial_distance, growth, percent=True)
		print(f'The athlete will run more than 50km in {day} days')


main()
