from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import json
import gensim

def runLda():
	tokenizer = RegexpTokenizer(r'\w+')

	# create English stop words list
	en_stop = get_stop_words('en')

	# Create p_stemmer of class PorterStemmer
	p_stemmer = PorterStemmer()
	    
	# create sample documents
	# doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
	# doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
	# doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
	# doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
	# doc_e = "Health professionals say that brocolli is good for your health." 

	videosPerUser=[]
	data = json.load(open('crawlerResult.json'))

	# print doc_set
	# compile sample documents into a list
	# doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
	# loop through document list
	
	try:
		temp = ""
		dict = {}
		for i in range(len(data['videoId'])):
		    
		    # clean and tokenize document string
		    if data['description'][i] != "No description":
		    	
			    raw = data['description'][i].lower()
			    tokens = tokenizer.tokenize(raw)

			    # remove stop words from tokens
			    stopped_tokens = [data['description'][i] for data['description'][i] in tokens if not data['description'][i] in en_stop]
			    
			    # stem tokens
			    stemmed_tokens = [p_stemmer.stem(data['description'][i]) for data['description'][i] in stopped_tokens]
			    
			    # add tokens to list
			    texts.append(stemmed_tokens)

		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)
		    
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		dict[data['videoId'][i]] = ldaAns

		# temp+=str(channels)+': '+str(ldaAns)+'\n'
		# print temp
	except Exception,e:
		print str(e)

	try:
		dictionary = corpora.Dictionary(texts)
		    
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		dict[channels]['tags'] = ldaAns

	except Exception,e:
		print str(e)

	with open('ldaonTitleDescriptionTagsResults.json', 'w') as f:
	        json.dump(dict, f)