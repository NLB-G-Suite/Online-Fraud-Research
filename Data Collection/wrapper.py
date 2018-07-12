import crawlerFixed
import sys
import json2csv
import linkAnalysis
import descriptionsTagsTitlesExtract
# import ldaonTitlesDescriptionTags
import uniqueChan
import fraudUserGenerator

def main(argv):
	# query = argv[1]
	# nres = argv[2]
	# print nres
	# print "Running crawler.."
	# crawlerFixed.search(query, nres)
	# print "Exiting crawler.. Starting Link Analysis.."
	# linkAnalysis.linkWork(nres)
	# print "Ending Link Analysis.. Converting JSON to CSV.."
	# json2csv.csvConvert()
	# print "Starting LDA Analysis per Channel.."
	# descriptionsTagsTitlesExtract.makeDict()
	# ldaonTitlesDescriptionTags.runLda()
	fraudUserGenerator.potentialFraud()
	print 'Ending LDA.. Identifying unique channels..'
	uniqueChan.findPercentage()
	print "DONE"

if __name__ == "__main__":
  main(sys.argv)
