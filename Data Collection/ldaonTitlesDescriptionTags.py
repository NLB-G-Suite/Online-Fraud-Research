from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import json
import gensim

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
data = json.load(open('tagsDescriptionsTitleChannel.json'))

# print doc_set
# compile sample documents into a list
# doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
tcount=0.0
for channels in data:
	tcount+=1.0

dict = {}
count=0.0
for channels in data:
	dict[channels] = {}
	texts = []
	count+=1.0
	print str(100*(count/tcount))[:4]+'% Complete'
	doc_set = data[channels]
	# loop through document list
	try:
		temp = ""

		for i in doc_set:
		    
		    # clean and tokenize document string
		    if data[channels][i]['title'] != "No Title":
		    	
			    raw = data[channels][i]['title'].lower()
			    tokens = tokenizer.tokenize(raw)

			    # remove stop words from tokens
			    stopped_tokens = [data[channels][i]['title'] for data[channels][i]['title'] in tokens if not data[channels][i]['title'] in en_stop]
			    
			    # stem tokens
			    stemmed_tokens = [p_stemmer.stem(data[channels][i]['title']) for data[channels][i]['title'] in stopped_tokens]
			    
			    # add tokens to list
			    texts.append(stemmed_tokens)

		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)
		    
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		dict[channels]['title'] = ldaAns

		# temp+=str(channels)+': '+str(ldaAns)+'\n'
		# print temp
	except Exception,e:
		print str(e)


	try:
		temp = ""
	
		for i in doc_set:
		    
		    # clean and tokenize document string
		    if data[channels][i]['description'] != "No Description":
		    	
			    raw = data[channels][i]['description'].lower()
			    tokens = tokenizer.tokenize(raw)

			    # remove stop words from tokens
			    stopped_tokens = [data[channels][i]['description'] for data[channels][i]['description'] in tokens if not data[channels][i]['description'] in en_stop]
			    
			    # stem tokens
			    stemmed_tokens = [p_stemmer.stem(data[channels][i]['description']) for data[channels][i]['description'] in stopped_tokens]
			    
			    # add tokens to list
			    texts.append(stemmed_tokens)

		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)
		    
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		dict[channels]['description'] = ldaAns

		# temp+=str(channels)+': '+str(ldaAns)+'\n'
		# print temp
	except Exception,e:
		print str(e)

	try:
		temp = ""
	
		for i in doc_set:
		    
		    # clean and tokenize document string
			if data[channels][i]['tags'] != "No Tags":
				tempTag=''
				for tag in data[channels][i]['tags']:
					tempTag+=tag
				raw = tempTag.lower()
				tokens = tokenizer.tokenize(raw)

				# remove stop words from tokens
				stopped_tokens = [tempTag for tempTag in tokens if not tempTag in en_stop]
				
				# stem tokens
				stemmed_tokens = [p_stemmer.stem(tempTag) for tempTag in stopped_tokens]
				
				# add tokens to list
				texts.append(stemmed_tokens)

		# turn our tokenized documents into a id <-> term dictionary
		dictionary = corpora.Dictionary(texts)
		    
		# convert tokenized documents into a document-term matrix
		corpus = [dictionary.doc2bow(text) for text in texts]

		# generate LDA model
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

		ldaAns = ldamodel.print_topics(num_topics=3, num_words=3)

		dict[channels]['tags'] = ldaAns

		# temp+=str(channels)+': '+str(ldaAns)+'\n'
		# print temp
	except Exception,e:
		print str(e)

with open('ldaonTitleDescriptionTagsResults.json', 'w') as f:
        json.dump(dict, f)
with open('ldaTitleResults.txt','w') as f:
	f.write(temp)
	
print 'Done'