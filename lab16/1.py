from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import matplotlib.pyplot as plt

def main():
	# try to open and read the text file
	try:
		raw_text = open('data/bryant-stories.txt', 'r').read()
	except Exception as e:
		print(f"An exception occurred opening the text file: {e}")
		exit(2)

	# tokenize the text
	words = word_tokenize(raw_text)

	# print total word count
	print(f"Word count: {len(words)}")

	# create a figure with 2 axes
	fig, (ax1, ax2) = plt.subplots(2)

	# set tighter layout engine
	fig.set_layout_engine('tight')

	# get top-10 words and form 2 lists from a single tuple list
	ax1.bar(*zip(*FreqDist(words).most_common(10)))

	# set title and labels
	ax1.set_title('10 most popular words (unfiltered)')
	ax1.set_xlabel('Word')
	ax1.set_ylabel('Appearences in text')


	# create a cleaner version
	stop_words = set(stopwords.words('english'))
	words_cleaned = [
			word.lower()
			for word in words
			if word.isalpha() and word not in stop_words
	]
	ax2.bar(*zip(*FreqDist(words_cleaned).most_common(10)))
	ax2.set_title('10 most popular words (filtered)')
	ax2.set_xlabel('Word')
	ax2.set_ylabel('Appearences in text')


	# finally, show the plots
	plt.show()

main()
