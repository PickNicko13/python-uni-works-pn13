# this code takes a string and outputs a substring from 18 to -3

s = ''

while len(s) < 21:
	# yes, I do realize that 21-symbol strings will end up being 0-length
	s = input("Input a string (at least 21 symbols): ")

print(s[18:-3])
