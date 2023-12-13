#!/bin/python

# why is it even supposed to be in a separate function??
def superset(a: set, b:set):
	return a.union(b)

# init base sets
cd_set = {'c', 'd'}
vowel_set = {'a', 'e', 'i', 'o', 'u', 'y'}

# do union operation
result_set = superset(cd_set,vowel_set)

# print result
print("Result:", result_set)
