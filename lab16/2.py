from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,PorterStemmer

def main():
	# try to open and read the text file
	try:
		raw_text = open('data/small_text.txt', 'r').read()
	except Exception as e:
		print(f"An exception occurred opening 'small_text.txt' for reading: {e}")
		exit(2)

	# 1 - tokenize (with basic cleanup)
	tokens = word_tokenize(raw_text.lower())

	# 2 - lemmatize and stemmatize
	lemmatizer = WordNetLemmatizer()
	stemmer = PorterStemmer()
	tokens = [stemmer.stem((lemmatizer.lemmatize(word))) for word in tokens]

	# 3 - remove stopwords
	tokens = [
			t for t in tokens
			if t not in stopwords.words('english')
	]

	# 4 - remove punctuation
	tokens = [
			t for t in tokens
			if t.isalpha()
	]

	try:
		open('out.txt', 'w').write(' '.join(tokens))
	except Exception as e:
		print(f"An exception occurred opening 'out.txt' for writing: {e}")
		exit(2)

	print("'out.txt' generated successfully.")

main()
