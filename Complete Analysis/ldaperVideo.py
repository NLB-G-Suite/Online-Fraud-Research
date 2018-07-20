from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import json

def ldaDesc():
	x = json.load(open('linkStatusBuffer(1).json'))
	ldaDescriptionResults=[]

	for index in range(len(x['videoId'])):

		if len(x['description'][index])==0 or x['description'][index]==' ':
			ldaDescriptionResults.append('No description')
			continue

		tokenizer = RegexpTokenizer(r'\w+')
		en_stop = get_stop_words('en')
		p_stemmer = PorterStemmer()
		
		texts = []

		description=x['description'][index].encode('ascii','ignore')
		
		for i in description.split('.'):
			
			raw = i.lower()
			tokens = tokenizer.tokenize(raw)

			# remove stop words from tokens
			stopped_tokens = [i for i in tokens if not i in en_stop]
			
			# stem tokens
			stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
			
			# add tokens to list
			texts.append(stemmed_tokens)

		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)

		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		ldaDescriptionResults.append(ldaAns)
		


	x['ldaDescriptionResults']=ldaDescriptionResults


	with open('linkStatusBuffer(1).json', 'w') as fp:
		json.dump(x,fp)
