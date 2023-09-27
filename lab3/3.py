s = ''

while len(s.split()) < 2:
	s = input("Input a string (at least 2 words): ")

print(*[
	word for word in s.split()
		if word.count('e') >= 3
		]
)
