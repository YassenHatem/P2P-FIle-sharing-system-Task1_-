from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sentence = "This example showing off stop word filtration."
stop_words = set(stopwords.words("english"))
print(stop_words)