import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
	''' stem tockens '''
	return [stemmer.stem(item) for item in tokens]

def normalize(text):
	''' remove punctuation, lowercase, stem'''
	return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

def cosine_sim(text1, text2):
	''' cosine sim between two texts '''
	vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
	tfidf = vectorizer.fit_transform([text1, text2])
	return ((tfidf * tfidf.T).A)[0,1]
