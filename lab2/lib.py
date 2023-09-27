from math import sin, ceil, log

def z( a: float, b: float ) -> float:
	return sin(a-b)*sin(a+b)

def exponential_athlete( initial_distance: float, growth: float, percent: bool = False ) -> int:
	# if value of growth is provided in percents, make 100% a 1
	if percent:
		growth /= 100
	
	"""
	Distance in N days is:
		initial_distance * growth^(days)

	This means that our goal is to find out which `days` makes this formula output bigger than 50.

	However, if we assert that `days` is a float and we can use gamma is equal to power,
	we can accept that the answer would be the ceiling of `days`.

	So, in the equation
		initial_distance * (1+growth)^days > 50
	can be written as
		(1+growth)^days = 50/initial_distance
		days = log( 50/initial_distance, growth + 1 )
	and the return value is
		ceil(days)

	(accounting for the fact that if it is strictly equal 50 then it must be one more day)
		
	"""

	# adhere to the aforementioned formula
	days = log( 50/initial_distance, growth+1 )

	# apply a workaround around that formula
	if days == 50.:
		days += 1.
	
	# finish off by rounding up
	return ceil(days)
