s = ascii(input("Input a string (all non-ASCII characters will be converted to UTF sequences): "))

print(f"Converted string: {s}")

# [1:-1] is needed to remove the quotes
print(sum(
	ord(symbol) for symbol in s[1:-1]
))
